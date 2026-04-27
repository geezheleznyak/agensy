#!/usr/bin/env python3
"""
system-audit.py — Mechanical reconciliation of [vault]/system-model.yaml.

Implements the deterministic half of the /system-audit protocol (Steps 1, 2, 3,
4A, 5, 5b-typematch, 9). Steps 4B (corpus walk for unreferenced notes), 6
(pattern-name collision heuristic), 7 (report formatting), and 8 (next-actions)
remain with Claude — they require corpus-walking heuristics and judgment that
should not be mechanized.

Read-only by design — never writes to system-model.yaml. Remediation belongs
to /system-build.

Usage:
    python system-audit.py <vault-path>            # human report; exit 0/1/2
    python system-audit.py <vault-path> --json     # machine-readable JSON
    python system-audit.py <vault-path> --baseline save | compare

Exit codes:
    0  green    1  yellow    2  red    3  invocation error

Schema reference (default search order, walking up from vault):
    [framework-root]/framework/system-model/system-model-schema.yaml

Override with --schema, --bridges, --peer-root if non-default layout.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Local imports (tools/ package)
from _vault_utils import setup_utf8_stdout, VaultConfig

setup_utf8_stdout()

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(3)


TOOL_VERSION = "0.1.0"
EXPECTED_SCHEMA_VERSION = "0.4"

# Timescale ordering for adjacency check (Step 5b informational)
TIMESCALE_ORDER = [
    'seconds-to-minutes', 'hours-to-days', 'weeks-to-months', 'years', 'decades+',
]


# ─────────────────────────────────────────────────────────────
# LOADERS
# ─────────────────────────────────────────────────────────────

def find_framework_root(vault_path: Path) -> Path:
    """Find directory containing 'framework/system-model/system-model-schema.yaml'.

    Search order:
    1. Sibling directories of vault_path (the typical case — multiple vaults +
       framework dir all under one workspace)
    2. Ancestors of vault_path (vault nested deeper than framework)
    3. Parent of this script's location (when system-audit.py lives in
       <framework-root>/tools/, the framework root is its grandparent)
    """
    sentinel = Path('framework') / 'system-model' / 'system-model-schema.yaml'
    # Siblings
    parent = vault_path.resolve().parent
    if parent.exists():
        for child in parent.iterdir():
            if child.is_dir() and (child / sentinel).exists():
                return child
    # Ancestors
    cur = parent
    for _ in range(6):
        if (cur / sentinel).exists():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    # Script-relative (this script's grandparent)
    script_root = Path(__file__).resolve().parent.parent
    if (script_root / sentinel).exists():
        return script_root
    return None


def resolve_default_path(vault_path, override, framework_root, relative_path):
    if override:
        return Path(override)
    if framework_root:
        return framework_root / relative_path
    return None


def load_yaml_with_header(path: Path):
    """Load YAML, handling files that start with a `---` comment fence (multi-doc)."""
    text = path.read_text(encoding='utf-8')
    docs = list(yaml.safe_load_all(text))
    for d in reversed(docs):
        if d:
            return d
    return {}


def load_model(path: Path):
    if not path.exists():
        return None
    try:
        return load_yaml_with_header(path)
    except yaml.YAMLError as e:
        print(f"ERROR: malformed YAML in {path}: {e}", file=sys.stderr)
        sys.exit(3)


def load_schema(path: Path):
    if not path or not path.exists():
        print(f"ERROR: schema not found at {path}. Use --schema to override.", file=sys.stderr)
        sys.exit(3)
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def load_bridges(path: Path):
    """Parse cross-vault-bridges.md headings into a set of valid bridge numbers.

    Returns a set of integer bridge numbers (not full ids). Bindings choose
    free-form short names after the number prefix (e.g. 'Strategic Interaction
    and Game Theory' becomes `bridge-7-game-theory` in YAMLs), so we validate
    only that the bridge NUMBER is real.
    """
    if not path or not path.exists():
        return set()
    import re
    text = path.read_text(encoding='utf-8')
    numbers = set()
    for m in re.finditer(r'^##\s+Bridge\s+(\d+)\s+[—-]', text, re.MULTILINE):
        numbers.add(int(m.group(1)))
    return numbers


def parse_bridge_number(bridge_id: str):
    """Extract the integer N from `bridge-N-...`. Returns None if malformed."""
    import re
    m = re.match(r'^bridge-(\d+)-', bridge_id)
    return int(m.group(1)) if m else None


# ─────────────────────────────────────────────────────────────
# PEER VAULT DISCOVERY
# ─────────────────────────────────────────────────────────────

def find_peer_vault(peer_name: str, peer_root: Path) -> Path:
    """Locate a peer vault directory by short name (e.g. 'oeconomia').

    Searches peer_root for any directory containing the peer_name as a substring,
    case-insensitive. This handles common-prefix variants without hardcoding.
    Returns the directory containing system-model.yaml, or None.
    """
    if not peer_root or not peer_root.exists():
        return None
    target = peer_name.lower()
    candidates = []
    for child in peer_root.iterdir():
        if not child.is_dir():
            continue
        if target in child.name.lower():
            sm = child / 'system-model.yaml'
            if sm.exists():
                candidates.append(child)
    if not candidates:
        return None
    # Prefer the shortest match (most-specific name)
    candidates.sort(key=lambda p: len(p.name))
    return candidates[0]


# ─────────────────────────────────────────────────────────────
# CHECKS — Step 1: Schema Conformance
# ─────────────────────────────────────────────────────────────

def required_fields(schema, kind):
    """kind: 'node' | 'edge' | 'pattern' — return required-field list or empty."""
    return schema.get(f'{kind}_required_fields', []) or []


def optional_fields(schema, kind):
    return schema.get(f'{kind}_optional_fields', []) or []


def check_schema_conformance(model, schema, issues):
    """Step 1: keys present, enums valid, references resolve at the graph level."""
    node_categories = set(schema.get('node_categories', {}).keys())
    edge_types = set(schema.get('edge_types', {}).keys())
    pattern_types = set(schema.get('pattern_types', {}).keys())
    timescale_bands = set((schema.get('timescale_bands', {}) or {}).keys())

    valid_node_ids = set()
    valid_pattern_ids = set()

    # Nodes
    for n in (model.get('nodes') or []):
        nid = n.get('id', '<no-id>')
        valid_node_ids.add(nid)
        for req in required_fields(schema, 'node'):
            if req not in n:
                issues['schema_violations'].append({
                    'entity': f'node:{nid}', 'field': req, 'actual': '<missing>',
                    'rule': 'required key absent',
                })
            elif req != 'linked_notes' and n.get(req) in (None, ''):
                # Empty linked_notes is unlinked-entity (Step 4A), not a schema violation.
                issues['schema_violations'].append({
                    'entity': f'node:{nid}', 'field': req, 'actual': '<empty>',
                    'rule': 'required value missing',
                })
        cat = n.get('category')
        if cat and cat not in node_categories:
            issues['schema_violations'].append({
                'entity': f'node:{nid}', 'field': 'category', 'actual': cat,
                'expected_one_of': sorted(node_categories),
            })

    # Edges
    for e in (model.get('edges') or []):
        eid = e.get('id', f"{e.get('from','?')}->{e.get('to','?')}")
        for req in required_fields(schema, 'edge'):
            if req not in e:
                issues['schema_violations'].append({
                    'entity': f'edge:{eid}', 'field': req, 'actual': '<missing>',
                    'rule': 'required key absent',
                })
        et = e.get('type')
        if et and et not in edge_types:
            issues['schema_violations'].append({
                'entity': f'edge:{eid}', 'field': 'type', 'actual': et,
                'expected_one_of': sorted(edge_types),
            })
        for endpoint in ('from', 'to'):
            v = e.get(endpoint)
            if v and v not in valid_node_ids:
                issues['schema_violations'].append({
                    'entity': f'edge:{eid}', 'field': endpoint, 'actual': v,
                    'rule': 'unknown node id',
                })

    # Patterns
    for p in (model.get('patterns') or []):
        pid = p.get('id', '<no-id>')
        valid_pattern_ids.add(pid)
        for req in required_fields(schema, 'pattern'):
            if req not in p:
                issues['schema_violations'].append({
                    'entity': f'pattern:{pid}', 'field': req, 'actual': '<missing>',
                    'rule': 'required key absent',
                })
        pt = p.get('type')
        if pt and pt not in pattern_types:
            issues['schema_violations'].append({
                'entity': f'pattern:{pid}', 'field': 'type', 'actual': pt,
                'expected_one_of': sorted(pattern_types),
            })
        # secondary_types (optional, but if present must be valid pattern types)
        for st in (p.get('secondary_types') or []):
            if st not in pattern_types:
                issues['schema_violations'].append({
                    'entity': f'pattern:{pid}', 'field': 'secondary_types', 'actual': st,
                    'expected_one_of': sorted(pattern_types),
                })
        # timescale (optional)
        ts = p.get('timescale')
        if ts and timescale_bands and ts not in timescale_bands and ts != 'mixed':
            issues['schema_violations'].append({
                'entity': f'pattern:{pid}', 'field': 'timescale', 'actual': ts,
                'expected_one_of': sorted(timescale_bands) + ['mixed'],
            })

    return valid_node_ids, valid_pattern_ids


# ─────────────────────────────────────────────────────────────
# CHECKS — Step 2: Vault-Config Integrity
# ─────────────────────────────────────────────────────────────

def check_vault_config_integrity(model, config, issues):
    """Step 2: domain slugs, engagement_positions match vault-config."""
    valid_domains = {d['slug'] for d in (config.domains or [])}
    valid_positions = set(config.fault_line_positions or [])

    for n in (model.get('nodes') or []):
        nid = n.get('id', '<no-id>')
        dom = n.get('domain')
        if dom and valid_domains and dom not in valid_domains:
            issues['config_drift'].append({
                'entity': f'node:{nid}', 'field': 'domain', 'actual': dom,
                'expected_one_of': sorted(valid_domains),
            })
        eps = n.get('engagement_positions') or []
        if isinstance(eps, str):
            eps = [eps]
        for ep in eps:
            if ep and valid_positions and ep not in valid_positions:
                issues['config_drift'].append({
                    'entity': f'node:{nid}', 'field': 'engagement_positions',
                    'actual': ep, 'expected_one_of': sorted(valid_positions),
                })


# ─────────────────────────────────────────────────────────────
# CHECKS — Step 3: Linked-Notes Integrity
# ─────────────────────────────────────────────────────────────

def check_linked_notes(model, vault_root, issues, counts):
    """Step 3: every linked_notes path resolves. Also tally totals."""
    seen_paths = set()
    total = 0

    def check(entity_label, links):
        nonlocal total
        if not links:
            return
        if isinstance(links, str):
            links = [links]
        for ln in links:
            ln_str = str(ln).strip()
            if not ln_str:
                continue
            total += 1
            seen_paths.add(ln_str)
            target = vault_root / ln_str.replace('\\', '/').lstrip('/')
            if not target.exists():
                issues['broken_linked_notes'].append({
                    'entity': entity_label, 'path': ln_str,
                    'checked_against': 'vault_root',
                })

    for n in (model.get('nodes') or []):
        check(f"node:{n.get('id','?')}", n.get('linked_notes'))
    for e in (model.get('edges') or []):
        eid = e.get('id') or f"{e.get('from','?')}->{e.get('to','?')}"
        check(f"edge:{eid}", e.get('linked_notes'))
    for p in (model.get('patterns') or []):
        check(f"pattern:{p.get('id','?')}", p.get('linked_notes'))
    for b in (model.get('cross_vault_bindings') or []):
        check(f"binding:{b.get('bridge_id','?')}", b.get('linked_notes'))

    counts['linked_notes_total'] = total
    counts['linked_notes_unique'] = len(seen_paths)


# ─────────────────────────────────────────────────────────────
# CHECKS — Step 4A: Unlinked Entities
# ─────────────────────────────────────────────────────────────

def check_unlinked_entities(model, issues):
    """Step 4A: entities with empty/missing linked_notes are writing targets."""
    for n in (model.get('nodes') or []):
        if not n.get('linked_notes'):
            issues['unlinked_entities'].append({
                'entity': f"node:{n.get('id','?')}", 'kind': 'node',
                'category': n.get('category'),
            })
    for e in (model.get('edges') or []):
        if not e.get('linked_notes'):
            eid = e.get('id') or f"{e.get('from','?')}->{e.get('to','?')}"
            issues['unlinked_entities'].append({
                'entity': f"edge:{eid}", 'kind': 'edge', 'category': None,
            })
    for p in (model.get('patterns') or []):
        if not p.get('linked_notes'):
            issues['unlinked_entities'].append({
                'entity': f"pattern:{p.get('id','?')}", 'kind': 'pattern',
                'category': p.get('type'),
            })


# ─────────────────────────────────────────────────────────────
# CHECKS — Step 5: Cross-Vault Binding Integrity
# ─────────────────────────────────────────────────────────────

def check_bindings(model, valid_node_ids, valid_pattern_ids, valid_bridge_numbers,
                   peer_root, issues, info, peer_models):
    """Step 5: bridge number known, local refs resolve, peer refs resolve."""
    for b in (model.get('cross_vault_bindings') or []):
        bid = b.get('bridge_id', '<no-bridge-id>')
        n = parse_bridge_number(bid)
        if valid_bridge_numbers and (n is None or n not in valid_bridge_numbers):
            issues['binding_drift'].append({
                'bridge_id': bid, 'side': 'local', 'kind': 'bridge_id',
                'id': bid, 'issue': 'bridge-number-unknown',
            })
        for ln in (b.get('local_nodes') or []):
            if ln not in valid_node_ids:
                issues['binding_drift'].append({
                    'bridge_id': bid, 'side': 'local', 'kind': 'node',
                    'id': ln, 'issue': 'unknown-local-node',
                })
        for lp in (b.get('local_patterns') or []):
            if lp not in valid_pattern_ids:
                issues['binding_drift'].append({
                    'bridge_id': bid, 'side': 'local', 'kind': 'pattern',
                    'id': lp, 'issue': 'unknown-local-pattern',
                })
        paired = b.get('paired_with') or {}
        if not isinstance(paired, dict):
            continue
        for peer_name, peer_data in paired.items():
            peer_dir = find_peer_vault(peer_name, peer_root)
            if not peer_dir:
                if peer_name not in info['peer_not_bootstrapped']:
                    info['peer_not_bootstrapped'].append(peer_name)
                continue
            # Cache peer model
            if peer_name not in peer_models:
                peer_sm = peer_dir / 'system-model.yaml'
                peer_models[peer_name] = load_model(peer_sm) or {}
            peer_model = peer_models[peer_name]
            peer_node_ids = {n.get('id') for n in (peer_model.get('nodes') or [])}
            peer_pattern_ids = {p.get('id') for p in (peer_model.get('patterns') or [])}
            if not isinstance(peer_data, dict):
                continue
            for pn in (peer_data.get('nodes') or []):
                if pn not in peer_node_ids:
                    issues['binding_drift'].append({
                        'bridge_id': bid, 'side': 'peer', 'vault': peer_name,
                        'kind': 'node', 'id': pn, 'issue': 'unknown-peer-node',
                    })
            for pp in (peer_data.get('patterns') or []):
                if pp not in peer_pattern_ids:
                    issues['binding_drift'].append({
                        'bridge_id': bid, 'side': 'peer', 'vault': peer_name,
                        'kind': 'pattern', 'id': pp, 'issue': 'unknown-peer-pattern',
                    })


# ─────────────────────────────────────────────────────────────
# CHECKS — Step 5b: Mechanism-Pairing Type Match
# ─────────────────────────────────────────────────────────────

def timescale_distance(a, b):
    """Index-distance in TIMESCALE_ORDER. 'mixed' is adjacent to all (returns 0)."""
    if 'mixed' in (a, b):
        return 0
    try:
        return abs(TIMESCALE_ORDER.index(a) - TIMESCALE_ORDER.index(b))
    except ValueError:
        return None  # unknown band — treat as not comparable


def check_mechanism_pairings(model, peer_models, issues, info):
    """Step 5b type-match only; subtype/timescale are informational divergences."""
    pattern_by_id = {p.get('id'): p for p in (model.get('patterns') or [])}

    for b in (model.get('cross_vault_bindings') or []):
        bid = b.get('bridge_id', '<no-bridge-id>')
        pairings = b.get('mechanism_pairings') or []
        if not pairings:
            continue
        for entry in pairings:
            local_id = entry.get('local')
            peers = entry.get('peers') or []
            local_p = pattern_by_id.get(local_id)
            if not local_p:
                # Local pattern id doesn't exist — recorded by binding_drift via Step 5
                continue
            for peer_ref in peers:
                if not isinstance(peer_ref, str) or '.' not in peer_ref:
                    issues['mech_broken_refs'].append({
                        'bridge_id': bid, 'local_pattern': local_id,
                        'peer_ref': str(peer_ref), 'reason': 'malformed-peer-ref',
                    })
                    continue
                peer_name, peer_pid = peer_ref.split('.', 1)
                peer_model = peer_models.get(peer_name)
                if peer_model is None:
                    if peer_name not in info['peer_not_bootstrapped']:
                        info['peer_not_bootstrapped'].append(peer_name)
                    continue
                peer_p = next(
                    (p for p in (peer_model.get('patterns') or []) if p.get('id') == peer_pid),
                    None
                )
                if peer_p is None:
                    issues['mech_broken_refs'].append({
                        'bridge_id': bid, 'local_pattern': local_id,
                        'peer_ref': peer_ref, 'reason': 'peer pattern id not found',
                    })
                    continue

                lt = local_p.get('type')
                pt = peer_p.get('type')
                local_secondary = set(local_p.get('secondary_types') or [])
                peer_secondary = set(peer_p.get('secondary_types') or [])

                if lt == pt:
                    pass  # silent pass
                elif pt in local_secondary or lt in peer_secondary:
                    issues['mech_divergences'].append({
                        'bridge_id': bid, 'local_pattern': local_id, 'peer': peer_ref,
                        'kind': 'secondary-type-match',
                        'local_value': lt, 'peer_value': pt,
                    })
                else:
                    issues['mech_failures'].append({
                        'bridge_id': bid, 'local_pattern': local_id, 'peer': peer_ref,
                        'local_type': lt, 'peer_type': pt,
                        'secondary_types_checked': True,
                    })

                # Subtype divergence
                lst = local_p.get('subtype')
                pst = peer_p.get('subtype')
                if lst and pst:
                    if lst != pst:
                        issues['mech_divergences'].append({
                            'bridge_id': bid, 'local_pattern': local_id, 'peer': peer_ref,
                            'kind': 'subtype', 'local_value': lst, 'peer_value': pst,
                        })
                elif (lst and not pst) or (pst and not lst):
                    issues['mech_divergences'].append({
                        'bridge_id': bid, 'local_pattern': local_id, 'peer': peer_ref,
                        'kind': 'subtype-asymmetric',
                        'local_value': lst, 'peer_value': pst,
                    })

                # Timescale gap
                lts = local_p.get('timescale')
                pts = peer_p.get('timescale')
                if lts and pts:
                    d = timescale_distance(lts, pts)
                    if d is not None and d >= 2:
                        issues['mech_divergences'].append({
                            'bridge_id': bid, 'local_pattern': local_id, 'peer': peer_ref,
                            'kind': 'timescale-gap', 'local_value': lts, 'peer_value': pts,
                        })


# ─────────────────────────────────────────────────────────────
# Step 5b informational: substrate pairings count
# ─────────────────────────────────────────────────────────────

def count_substrate_pairings(model):
    """Cross-products of local_patterns × peer.patterns NOT in mechanism_pairings."""
    total = 0
    bindings_without_mp = 0
    for b in (model.get('cross_vault_bindings') or []):
        local_p = b.get('local_patterns') or []
        paired = b.get('paired_with') or {}
        declared_pairs = set()
        for entry in (b.get('mechanism_pairings') or []):
            local_id = entry.get('local')
            for peer_ref in (entry.get('peers') or []):
                if isinstance(peer_ref, str) and '.' in peer_ref:
                    declared_pairs.add((local_id, peer_ref))
        if not (b.get('mechanism_pairings') or []):
            bindings_without_mp += 1
        if not isinstance(paired, dict):
            continue
        for peer_name, peer_data in paired.items():
            if not isinstance(peer_data, dict):
                continue
            peer_patterns = peer_data.get('patterns') or []
            for lp in local_p:
                for pp in peer_patterns:
                    if (lp, f'{peer_name}.{pp}') not in declared_pairs:
                        total += 1
    return total, bindings_without_mp


# ─────────────────────────────────────────────────────────────
# COUNTS + DIRT LEVEL
# ─────────────────────────────────────────────────────────────

def compute_counts(model, counts):
    nodes = model.get('nodes') or []
    edges = model.get('edges') or []
    patterns = model.get('patterns') or []
    bindings = model.get('cross_vault_bindings') or []

    counts['nodes'] = {
        'total': len(nodes),
        'by_category': dict(_count_by(nodes, 'category')),
    }
    counts['edges'] = {
        'total': len(edges),
        'by_type': dict(_count_by(edges, 'type')),
    }
    counts['patterns'] = {
        'total': len(patterns),
        'by_type': dict(_count_by(patterns, 'type')),
    }
    counts['bindings'] = {
        'total': len(bindings),
        'with_mechanism_pairings': sum(1 for b in bindings if b.get('mechanism_pairings')),
    }


def _count_by(items, key):
    c = defaultdict(int)
    for item in items:
        v = item.get(key)
        if v:
            c[v] += 1
    return c


CONTRIBUTING_KEYS = (
    'schema_violations', 'config_drift', 'broken_linked_notes',
    'unlinked_entities', 'binding_drift', 'mech_failures', 'mech_broken_refs',
)


def compute_dirt_level(issues):
    """Step 9 v0.4 thresholds. Returns (level, rationale_lines)."""
    counts = {k: len(issues.get(k, [])) for k in CONTRIBUTING_KEYS}

    hard_red = (
        counts['broken_linked_notes'] >= 1
        or counts['mech_failures'] >= 1
        or counts['mech_broken_refs'] >= 1
        or any(c > 5 for c in counts.values())
    )
    yellow = any(2 <= c <= 5 for c in counts.values())

    rationale = []
    if hard_red:
        level = 'red'
        if counts['broken_linked_notes'] >= 1:
            rationale.append(f"{counts['broken_linked_notes']} broken linked_notes (hard-red trigger)")
        if counts['mech_failures'] >= 1:
            rationale.append(f"{counts['mech_failures']} mechanism-pairing failures (hard-red trigger)")
        if counts['mech_broken_refs'] >= 1:
            rationale.append(f"{counts['mech_broken_refs']} mechanism-pairing broken refs (hard-red trigger)")
        for k, c in counts.items():
            if c > 5:
                rationale.append(f"{c} {k} (>5 trigger)")
    elif yellow:
        level = 'yellow'
        for k, c in counts.items():
            if 2 <= c <= 5:
                rationale.append(f"{c} {k} (yellow band 2-5)")
    else:
        level = 'green'
        rationale.append("all contributing counts <= 1 and no hard-red triggers")

    return level, rationale


# ─────────────────────────────────────────────────────────────
# RESULT ASSEMBLY + EMIT
# ─────────────────────────────────────────────────────────────

def assemble_result(vault_name, schema_version, model, issues, info, counts, dirt_level, dirt_rationale):
    return {
        'vault': vault_name,
        'schema_version': schema_version,
        'tool_version': TOOL_VERSION,
        'audit_date': datetime.now().strftime('%Y-%m-%d'),
        'audit_timestamp': datetime.now().isoformat(),
        'scope': {
            'steps_executed': ['1', '2', '3', '4A', '5', '5b-typematch', '9'],
            'steps_deferred_to_claude': ['4B', '5b-collision', '6', '7', '8'],
        },
        'counts': counts,
        'issues': issues,
        'informational': info,
        'dirt_level': dirt_level,
        'dirt_rationale': dirt_rationale,
        'summary_line': format_summary_line(vault_name, dirt_level, issues, info),
    }


def format_summary_line(vault_name, dirt_level, issues, info):
    return (
        f"SYSTEM_AUDIT_SUMMARY: vault={vault_name} dirt={dirt_level} "
        f"schema={len(issues['schema_violations'])} "
        f"config={len(issues['config_drift'])} "
        f"broken_notes={len(issues['broken_linked_notes'])} "
        f"unlinked={len(issues['unlinked_entities'])} "
        f"unref=0 "
        f"binding_drift={len(issues['binding_drift'])} "
        f"mech_failures={len(issues['mech_failures'])} "
        f"mech_broken_refs={len(issues['mech_broken_refs'])} "
        f"divergences={len(issues['mech_divergences'])} "
        f"substrate_pairings={info['substrate_pairings']}"
    )


def human_report(result, verbose=False):
    issues = result['issues']
    info = result['informational']
    counts = result['counts']

    lines = []
    lines.append("=" * 70)
    lines.append(f"System Model Audit — {result['vault']}")
    lines.append(f"Schema version: {result['schema_version']} · Date: {result['audit_date']}")
    lines.append("=" * 70)
    lines.append("")

    lines.append("## Summary")
    lines.append(f"- Nodes: {counts['nodes']['total']} (by category: " +
                 ", ".join(f"{k}={v}" for k, v in sorted(counts['nodes']['by_category'].items())) + ")")
    lines.append(f"- Edges: {counts['edges']['total']} (by type: " +
                 ", ".join(f"{k}={v}" for k, v in sorted(counts['edges']['by_type'].items())) + ")")
    lines.append(f"- Patterns: {counts['patterns']['total']} (by type: " +
                 ", ".join(f"{k}={v}" for k, v in sorted(counts['patterns']['by_type'].items())) + ")")
    lines.append(f"- Bindings: {counts['bindings']['total']} ({counts['bindings']['with_mechanism_pairings']} with mechanism_pairings)")
    lines.append(f"- Linked notes: {counts.get('linked_notes_total', 0)} total / {counts.get('linked_notes_unique', 0)} unique")
    lines.append("")

    dot = {'green': '🟢', 'yellow': '🟡', 'red': '🔴'}.get(result['dirt_level'], '?')
    lines.append(f"## Dirt Level: {dot} {result['dirt_level'].upper()}")
    for r in result['dirt_rationale']:
        lines.append(f"  · {r}")
    lines.append("")

    lines.append("## Issues")
    for k in CONTRIBUTING_KEYS + ('mech_divergences',):
        n = len(issues.get(k, []))
        marker = '⚠️ ' if (k in CONTRIBUTING_KEYS and n) else 'ℹ️ ' if k == 'mech_divergences' and n else '   '
        lines.append(f"  {marker}{k}: {n}")
    lines.append(f"  ℹ️ substrate_pairings: {info['substrate_pairings']} (informational)")
    lines.append(f"  ℹ️ peer_not_bootstrapped: {info['peer_not_bootstrapped']} (informational)")
    lines.append("")

    # Detail (cap at 10 per category, --verbose shows all)
    cap = None if verbose else 10
    detail_categories = list(CONTRIBUTING_KEYS) + ['mech_divergences']
    for k in detail_categories:
        items = issues.get(k, [])
        if not items:
            continue
        lines.append(f"### {k} ({len(items)})")
        shown = items if cap is None else items[:cap]
        for it in shown:
            lines.append(f"  - {it}")
        if cap is not None and len(items) > cap:
            lines.append(f"  ... ({len(items) - cap} more — use --verbose to see all)")
        lines.append("")

    lines.append("## Steps Deferred to Claude")
    lines.append("  - Step 4B: walk the corpus for unreferenced notes (overwrite `unref=N` in summary line)")
    lines.append("  - Step 6: pattern-name collision heuristic (categorical-distribution)")
    lines.append("  - Step 7: report formatting + prose synthesis")
    lines.append("  - Step 8: prioritize next actions")
    lines.append("  After Step 4B and Step 6, re-evaluate dirt level — script value is the LOWER bound.")
    lines.append("")

    lines.append(result['summary_line'])
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# BASELINE
# ─────────────────────────────────────────────────────────────

def baseline_path(vault_name, tools_dir):
    base_dir = tools_dir / 'baselines'
    base_dir.mkdir(exist_ok=True)
    return base_dir / f'{vault_name}-system-audit-baseline.json'


def save_baseline(result, tools_dir):
    p = baseline_path(result['vault'], tools_dir)
    p.write_text(json.dumps(result, indent=2, default=str), encoding='utf-8')
    return p


def compare_baseline(result, tools_dir):
    p = baseline_path(result['vault'], tools_dir)
    if not p.exists():
        return None
    baseline = json.loads(p.read_text(encoding='utf-8'))
    deltas = {}
    for k in CONTRIBUTING_KEYS + ('mech_divergences',):
        before = {repr(x) for x in baseline.get('issues', {}).get(k, [])}
        after = {repr(x) for x in result.get('issues', {}).get(k, [])}
        new = after - before
        fixed = before - after
        if new or fixed:
            deltas[k] = {'new': sorted(new), 'fixed': sorted(fixed)}
    regressions = sum(len(d['new']) for d in deltas.values())
    improvements = sum(len(d['fixed']) for d in deltas.values())
    return {
        'compared_at': datetime.now().isoformat(),
        'current_audit_date': result['audit_date'],
        'baseline_audit_date': baseline.get('audit_date'),
        'tool_version_match': baseline.get('tool_version') == result.get('tool_version'),
        'deltas': deltas,
        'regression_count': regressions,
        'improvement_count': improvements,
        'dirt_level_change': f"{baseline.get('dirt_level')}->{result['dirt_level']}"
            if baseline.get('dirt_level') != result['dirt_level'] else 'same',
    }


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

DIRT_TO_EXIT = {'green': 0, 'yellow': 1, 'red': 2}


def main():
    parser = argparse.ArgumentParser(
        description='System Model Audit — mechanical YAML validation.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'Exit codes: 0 green, 1 yellow, 2 red, 3 invocation error.\n'
            'Steps deferred to Claude: 4B (corpus walk for unreferenced notes), '
            '6 (pattern collision), 7 (report prose), 8 (next actions).\n'
            'See framework/universal-commands/system-audit.md.'
        ),
    )
    parser.add_argument('vault_path', help='Path to vault root directory')
    parser.add_argument('--json', action='store_true',
                        help='Emit JSON instead of human-readable report')
    parser.add_argument('--verbose', action='store_true',
                        help='Show all detail items (no truncation)')
    parser.add_argument('--baseline', choices=['save', 'compare'],
                        help='Save current audit as baseline, or diff against it')
    parser.add_argument('--schema', metavar='PATH',
                        help='Path to system-model-schema.yaml (default: search up)')
    parser.add_argument('--bridges', metavar='PATH',
                        help='Path to cross-vault-bridges.md (default: search up)')
    parser.add_argument('--peer-root', metavar='PATH', dest='peer_root',
                        help='Directory containing peer vaults (default: parent of vault_path)')
    args = parser.parse_args()

    vault_path = Path(args.vault_path).resolve()
    if not vault_path.exists():
        print(f"ERROR: vault path does not exist: {vault_path}", file=sys.stderr)
        sys.exit(3)

    sm_path = vault_path / 'system-model.yaml'
    if not sm_path.exists():
        print(f"No system model to audit — run /system-build first.", file=sys.stderr)
        sys.exit(3)

    framework_root = find_framework_root(vault_path)
    schema_path = resolve_default_path(vault_path, args.schema, framework_root,
                                       'framework/system-model/system-model-schema.yaml')
    bridges_path = resolve_default_path(vault_path, args.bridges, framework_root,
                                        'cross-vault-bridges.md')
    peer_root = Path(args.peer_root).resolve() if args.peer_root else vault_path.parent

    # Load
    model = load_model(sm_path)
    if model is None:
        print(f"ERROR: failed to load {sm_path}", file=sys.stderr)
        sys.exit(3)

    schema_version = str(model.get('schema_version', '0.1'))
    if schema_version != EXPECTED_SCHEMA_VERSION:
        print(f"WARN: schema version mismatch — tool built for "
              f"{EXPECTED_SCHEMA_VERSION}, found {schema_version}. "
              f"Some checks may be incorrect.", file=sys.stderr)

    schema = load_schema(schema_path)
    valid_bridge_numbers = load_bridges(bridges_path)

    try:
        config = VaultConfig(vault_path)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(3)

    # Collect
    issues = {
        'schema_violations': [],
        'config_drift': [],
        'broken_linked_notes': [],
        'unlinked_entities': [],
        'binding_drift': [],
        'mech_failures': [],
        'mech_broken_refs': [],
        'mech_divergences': [],
    }
    info = {
        'substrate_pairings': 0,
        'peer_not_bootstrapped': [],
        'bindings_without_mechanism_pairings': 0,
    }
    counts = {}
    peer_models = {}

    # Step 1
    valid_node_ids, valid_pattern_ids = check_schema_conformance(model, schema, issues)
    # Step 2
    check_vault_config_integrity(model, config, issues)
    # Step 3
    check_linked_notes(model, vault_path, issues, counts)
    # Step 4A
    check_unlinked_entities(model, issues)
    # Step 5
    check_bindings(model, valid_node_ids, valid_pattern_ids, valid_bridge_numbers,
                   peer_root, issues, info, peer_models)
    # Step 5b type-match
    check_mechanism_pairings(model, peer_models, issues, info)
    # Step 5b informational
    sub_total, no_mp = count_substrate_pairings(model)
    info['substrate_pairings'] = sub_total
    info['bindings_without_mechanism_pairings'] = no_mp
    # Counts
    compute_counts(model, counts)
    # Step 9
    dirt_level, dirt_rationale = compute_dirt_level(issues)

    # Assemble
    result = assemble_result(
        config.name, schema_version, model, issues, info, counts,
        dirt_level, dirt_rationale,
    )

    # Baseline workflow
    tools_dir = Path(__file__).resolve().parent
    if args.baseline == 'save':
        p = save_baseline(result, tools_dir)
        print(f"Baseline saved: {p}")
        # Save still emits the summary line + exits per dirt level
    elif args.baseline == 'compare':
        cmp = compare_baseline(result, tools_dir)
        if cmp is None:
            print(f"No baseline found for {result['vault']} — run --baseline save first.",
                  file=sys.stderr)
            sys.exit(3)
        if args.json:
            print(json.dumps({'audit': result, 'baseline_diff': cmp},
                             indent=2, default=str))
        else:
            print(f"Baseline diff for {result['vault']}:")
            print(f"  regressions: {cmp['regression_count']}")
            print(f"  improvements: {cmp['improvement_count']}")
            print(f"  dirt_level change: {cmp['dirt_level_change']}")
            print(f"  tool_version match: {cmp['tool_version_match']}")
            for cat, d in cmp['deltas'].items():
                if d['new']:
                    print(f"  + {cat}: {len(d['new'])} new")
                if d['fixed']:
                    print(f"  - {cat}: {len(d['fixed'])} fixed")
            print()
            print(result['summary_line'])
        sys.exit(DIRT_TO_EXIT.get(dirt_level, 3))

    # Standard emit
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(human_report(result, verbose=args.verbose))

    sys.exit(DIRT_TO_EXIT.get(dirt_level, 3))


if __name__ == '__main__':
    main()
