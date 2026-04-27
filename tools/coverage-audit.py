#!/usr/bin/env python3
"""
coverage-audit.py — Mechanical reconciliation of a vault's note corpus
                    against its coverage plan.

Implements the deterministic half of the /coverage-audit protocol
(Steps 1, 2, 3, 4, optionally 7, plus Step 8's numeric inputs). Steps
requiring judgment (5 priority gaps, 6 plan rewrite narrative, 8
open_actions text, 9 system-audit chain) remain with Claude.

Read-only by default. With `--write-note-index`, writes
`memory/note-index.md` from collected data — that file is a regenerable
cache, rebuilt on every coverage audit.

Usage:
    python coverage-audit.py <vault-path>            # human report
    python coverage-audit.py <vault-path> --json     # machine-readable
    python coverage-audit.py <vault-path> --write-note-index
    python coverage-audit.py <vault-path> --baseline save | compare

Exit codes: 0 success, 3 invocation error.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

from _vault_utils import (
    setup_utf8_stdout,
    VaultConfig,
    parse_frontmatter,
    discover_notes,
    classify_for_coverage,
    get_note_domain,
    is_map,
    STOPWORDS,
)

setup_utf8_stdout()


TOOL_VERSION = "0.1.0"

# Tier order for note-index sort: maps first (domain entry points), T1
# sources next, T2-Ref before T2-Syn within domain, T3 last.
TIER_SORT_ORDER = {'Map': 0, 'T1': 1, 'T2-Ref': 2, 'T2-Syn': 3, 'T3': 4}


# ─────────────────────────────────────────────────────────────
# AXIS ABBREVIATION
# ─────────────────────────────────────────────────────────────

def make_axis_abbrev_map(positions):
    """Build a position -> abbreviation map.

    Strategy:
    - Start at 3-char prefix.
    - On collision, extend ALL conflicting entries by 1 char until distinct.
    - Cap at 6 chars; past cap, fall back to the full position string.

    Returns dict[str, str]. Empty input returns empty dict.
    """
    positions = [p for p in positions if p]
    if not positions:
        return {}

    n = 3
    while n <= 6:
        candidate = {p: p[:n] for p in positions}
        if len(set(candidate.values())) == len(positions):
            return candidate
        n += 1
    # Past the cap — fall back to full names
    return {p: p for p in positions}


# ─────────────────────────────────────────────────────────────
# COUNTERS
# ─────────────────────────────────────────────────────────────

def count_op_coverage(all_fm, config):
    """Count notes referencing each open-problem id."""
    key = config.open_problem_key
    counts = defaultdict(int)
    for fm in all_fm.values():
        ops = fm.get(key) or []
        if isinstance(ops, str):
            ops = [ops]
        for o in ops:
            try:
                counts[int(str(o).strip())] += 1
            except (ValueError, TypeError):
                pass
    return dict(counts)


def count_axis_coverage(all_fm, axis_field):
    """Count notes per axis-position value."""
    counts = defaultdict(int)
    for fm in all_fm.values():
        v = fm.get(axis_field)
        if not v:
            continue
        # Some vaults stuff multiple positions in one string with " / "
        for tok in re.split(r'\s*[/|]\s*', str(v).strip('"\'')):
            tok = tok.strip()
            if tok:
                counts[tok] += 1
    return dict(counts)


def count_by_domain(all_classifications, all_paths_to_domains):
    """Build {domain_slug: {tier: count}}."""
    matrix = defaultdict(lambda: defaultdict(int))
    for path, tier in all_classifications.items():
        domain = all_paths_to_domains.get(path, '') or ''
        matrix[domain][tier] += 1
    return {d: dict(t) for d, t in matrix.items()}


# ─────────────────────────────────────────────────────────────
# STEP 3 — PLANNED NOTES (defensive parsers)
# ─────────────────────────────────────────────────────────────

def parse_planned_notes(coverage_plan_path):
    """Extract planned-note bullets from a coverage plan.

    Looks for a `## Planned Notes` (or `## Planned Notes — ...`) section
    and any sub-sections (`### Domain Name`). Returns list of dicts:
        [{'title': str, 'domain': str|None, 'section': str|None, 'source_line': str}]

    Returns empty list if the file is missing, the section is absent, or
    the section is empty. Never crashes.
    """
    if not coverage_plan_path or not coverage_plan_path.exists():
        return []
    try:
        text = coverage_plan_path.read_text(encoding='utf-8')
    except Exception:
        return []

    # Find the planned-notes section
    section_match = re.search(
        r'^##\s+Planned\s+Notes[^\n]*\n(.+?)(?=\n##\s+|\Z)',
        text, re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if not section_match:
        return []
    body = section_match.group(1)

    planned = []
    current_section = None
    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        sub = re.match(r'^###\s+(.+)$', line)
        if sub:
            current_section = sub.group(1).strip()
            continue
        # Bullet line: `- Title` or `- Title - description` or `| Title | T2 |...`
        bullet = re.match(r'^\s*[-*]\s+(.+)$', line)
        if bullet:
            content = bullet.group(1).strip()
            # Strip trailing parenthetical description
            content = re.split(r'\s+[—–-]\s+', content, maxsplit=1)[0]
            content = content.strip()
            if not content or content.startswith('('):
                continue
            planned.append({
                'title': content,
                'domain': None,
                'section': current_section,
                'source_line': raw_line,
            })
            continue
        # Markdown table row: `| Title | Tier | ... |`
        tablerow = re.match(r'^\s*\|\s*([^|]+?)\s*\|', line)
        if tablerow:
            content = tablerow.group(1).strip()
            if not content or content.lower() == 'note' or content.startswith('---'):
                continue
            planned.append({
                'title': content,
                'domain': None,
                'section': current_section,
                'source_line': raw_line,
            })
    return planned


def title_words(title):
    """Tokenize a title to a set of comparable words (≥4 chars, minus stopwords)."""
    return set(re.findall(r'\b\w{4,}\b', title.lower())) - STOPWORDS


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def match_planned_notes(planned, all_paths):
    """Compute match status for each planned note against the corpus.

    Match thresholds:
      ≥0.80 -> complete
      0.55..0.80 -> partial
      <0.55 -> missing
    """
    # Pre-compute note title tokens
    note_titles = {}
    for p in all_paths:
        stem = p.stem
        m = re.match(r'^\d{12} - (.+)$', stem)
        title = m.group(1) if m else stem
        note_titles[p] = title_words(title)

    results = []
    for entry in planned:
        plan_words = title_words(entry['title'])
        if not plan_words:
            results.append({**entry, 'status': 'missing', 'match_path': None,
                            'match_score': 0.0})
            continue
        best = (None, 0.0)
        for p, words in note_titles.items():
            score = jaccard(plan_words, words)
            if score > best[1]:
                best = (p, score)
        path, score = best
        if score >= 0.80:
            status = 'complete'
        elif score >= 0.55:
            status = 'partial'
        else:
            status = 'missing'
        results.append({
            **entry,
            'status': status,
            'match_path': str(path).replace('\\', '/') if (path and status != 'missing') else None,
            'match_score': round(score, 3),
        })
    return results


# ─────────────────────────────────────────────────────────────
# TARGETS TABLE PARSER (defensive)
# ─────────────────────────────────────────────────────────────

def parse_targets_table(coverage_plan_path, counts_by_domain):
    """Extract Domain Summary 'Target T2' column from the coverage plan.

    Returns dict with parse_status and per-domain target/current/gap. If
    the table is missing or malformed, returns parse_status='not-found'
    or 'malformed' and an empty rows dict.
    """
    out = {
        'parsed_from': str(coverage_plan_path) if coverage_plan_path else None,
        'parse_status': 'not-found',
        'rows': {},
    }
    if not coverage_plan_path or not coverage_plan_path.exists():
        return out
    try:
        text = coverage_plan_path.read_text(encoding='utf-8')
    except Exception:
        out['parse_status'] = 'malformed'
        return out

    # Find Domain Summary table
    section = re.search(
        r'^##\s+Domain\s+Summary[^\n]*\n(.+?)(?=\n##\s+|\Z)',
        text, re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if not section:
        return out
    body = section.group(1)

    # Parse header to find Target T2 column index and Slug column index
    lines = [ln for ln in body.splitlines() if ln.strip().startswith('|')]
    if len(lines) < 2:
        out['parse_status'] = 'malformed'
        return out
    header_cells = [c.strip().lower() for c in lines[0].strip('|').split('|')]
    target_col = None
    slug_col = None
    for i, cell in enumerate(header_cells):
        if 'target' in cell and 't2' in cell:
            target_col = i
        if cell == 'slug':
            slug_col = i
    if target_col is None or slug_col is None:
        out['parse_status'] = 'malformed'
        return out

    # Skip the separator row, parse data rows
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) <= max(target_col, slug_col):
            continue
        slug = cells[slug_col].strip().strip('*')
        target_raw = cells[target_col].strip().strip('*')
        if not slug or slug.lower() in ('total', '—', '-'):
            continue
        try:
            target_n = int(target_raw)
        except ValueError:
            continue
        cnts = counts_by_domain.get(slug, {})
        current_t2 = (cnts.get('T2-Syn', 0) or 0) + (cnts.get('T2-Ref', 0) or 0)
        deficit = target_n - current_t2
        out['rows'][slug] = {
            'target_t2': target_n,
            'current_t2_syn': cnts.get('T2-Syn', 0),
            'current_t2_ref': cnts.get('T2-Ref', 0),
            'gap': 'met' if deficit <= 0 else f'-{deficit}',
        }
    if out['rows']:
        out['parse_status'] = 'ok'
    else:
        out['parse_status'] = 'malformed'
    return out


# ─────────────────────────────────────────────────────────────
# STRAGGLERS
# ─────────────────────────────────────────────────────────────

def compute_stragglers(all_classifications, all_fm, all_paths_to_domains, config):
    """Identify drift signals: notes whose frontmatter doesn't match vault-config."""
    domain_slugs = {d['slug'] for d in (config.domains or [])}
    not_in_config = set()
    no_domain = []
    no_ec = []
    no_axis = []
    axis_field = config.axis_field_name

    for path, tier in all_classifications.items():
        if tier == 'Map':
            continue
        fm = all_fm.get(path, {})
        # domain straggler check (compare frontmatter value, not folder-derived value)
        fm_domain = fm.get('domain')
        if fm_domain and domain_slugs and fm_domain not in domain_slugs:
            not_in_config.add(fm_domain)
        # missing fields
        if not fm.get('domain'):
            no_domain.append(str(path).replace('\\', '/'))
        if not config.is_training and tier in ('T2-Syn', 'T2-Ref'):
            ec_raw = fm.get('evergreen-candidate')
            if ec_raw is None:
                no_ec.append(str(path).replace('\\', '/'))
        if tier in ('T2-Syn', 'T2-Ref', 'T3') and not fm.get(axis_field):
            no_axis.append(str(path).replace('\\', '/'))

    return {
        'domain_slugs_not_in_config': sorted(not_in_config),
        'notes_lacking_domain_frontmatter': no_domain[:25],
        'notes_lacking_ec_frontmatter': no_ec[:25],
        'notes_lacking_axis_frontmatter': no_axis[:25],
    }


# ─────────────────────────────────────────────────────────────
# NOTE-INDEX WRITER (Step 7)
# ─────────────────────────────────────────────────────────────

def write_note_index(vault_root, config, all_classifications, all_fm,
                     all_paths_to_domains, abbrev_map, total_notes, today):
    """Write memory/note-index.md from collected data."""
    memory_dir = vault_root / 'memory'
    memory_dir.mkdir(exist_ok=True)
    out_path = memory_dir / 'note-index.md'

    axis_field = config.axis_field_name
    op_key = config.open_problem_key

    # Build axis legend for the column-key line
    if abbrev_map:
        legend = ', '.join(f'{abbrev}={full}' for full, abbrev in abbrev_map.items())
        legend_str = f'Axis ({legend})'
    else:
        legend_str = 'Axis'

    op_label = 'Open Challenge IDs' if op_key == 'open_challenges' else 'Open Problem IDs'

    lines = [
        f"# Note Index — {config.name}",
        "",
        f"Last updated: {today} | Total: {total_notes} | "
        f"Last full rebuild: {today} (coverage-audit)",
        "",
        f"**Column key**: Tier (T1/T2-Syn/T2-Ref/T3/Map) | Domain (slug) | "
        f"EC (evergreen-candidate) | {legend_str} | OPs ({op_label}) | "
        f"Source (user-dialogue / user-reflection / —)",
        "",
        "| Path | Tier | Domain | EC | Axis | OPs | Source | Created |",
        "|---|---|---|---|---|---|---|---|",
    ]

    # Sort: tier order, then domain, then path
    def sort_key(item):
        path, tier = item
        domain = all_paths_to_domains.get(path, '') or 'zzz'
        return (TIER_SORT_ORDER.get(tier, 9), domain, str(path))

    for path, tier in sorted(all_classifications.items(), key=sort_key):
        fm = all_fm.get(path, {})
        rel = str(path.relative_to(vault_root)).replace('\\', '/')
        domain = all_paths_to_domains.get(path, '') or '—'
        ec = fm.get('evergreen-candidate', '')
        if isinstance(ec, list):
            ec = ','.join(str(e) for e in ec)
        ec_str = str(ec).strip() if ec not in (None, '') else '—'
        axis_raw = fm.get(axis_field, '')
        if isinstance(axis_raw, list):
            axis_raw = axis_raw[0] if axis_raw else ''
        axis_first = re.split(r'\s*[/|]\s*', str(axis_raw).strip('"\''))[0].strip()
        axis_abbrev = abbrev_map.get(axis_first, '—') if axis_first else '—'
        ops = fm.get(op_key) or []
        if isinstance(ops, str):
            ops = [ops]
        ops_str = ','.join(str(o) for o in ops) if ops else '—'
        src_raw = fm.get('source', '')
        if isinstance(src_raw, list):
            src_raw = src_raw[0] if src_raw else ''
        src_lower = str(src_raw).lower()
        if 'dialogue' in src_lower:
            src = 'user-dialogue'
        elif 'reflection' in src_lower:
            src = 'user-reflection'
        else:
            src = '—'
        created = fm.get('created') or ''
        if not created:
            m = re.match(r'^(\d{4})(\d{2})(\d{2})', path.name)
            if m:
                created = f'{m.group(1)}-{m.group(2)}-{m.group(3)}'
        if not created:
            created = '—'

        lines.append(
            f"| {rel} | {tier} | {domain} | {ec_str} | {axis_abbrev} | "
            f"{ops_str} | {src} | {created} |"
        )

    out_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return out_path


# ─────────────────────────────────────────────────────────────
# RESULT ASSEMBLY + EMIT
# ─────────────────────────────────────────────────────────────

def assemble_result(config, totals, by_tier, by_domain, by_op, by_axis,
                    notes_rows, stragglers, planned_status, targets_table,
                    abbrev_map, today, write_note_index_flag):
    notes_total_excluding_t1 = (
        totals.get('T2-Ref', 0) + totals.get('T2-Syn', 0) + totals.get('T3', 0)
    )
    notes_total_including_maps = notes_total_excluding_t1 + totals.get('Map', 0)

    domain_count = len(config.domains or [])
    straggler_count = (
        len(stragglers['domain_slugs_not_in_config'])
        + len(stragglers['notes_lacking_domain_frontmatter'])
    )
    planned_complete = sum(1 for p in planned_status if p['status'] == 'complete')
    planned_total = len(planned_status)
    zero_op = sum(1 for v in by_op.values() if v == 0)
    if config.open_problem_ids:
        for opid in config.open_problem_ids:
            if opid not in by_op:
                zero_op += 1
    targets_met = 0
    targets_total = 0
    if targets_table.get('parse_status') == 'ok':
        for row in targets_table['rows'].values():
            targets_total += 1
            if row['gap'] == 'met':
                targets_met += 1

    summary_line = (
        f"COVERAGE_AUDIT_SUMMARY: vault={config.name} "
        f"notes={notes_total_excluding_t1} domains={domain_count} "
        f"stragglers={straggler_count} planned_complete={planned_complete}/{planned_total} "
        f"zero_op={zero_op} targets_met={targets_met}/{targets_total}"
    )

    steps_executed = ['1', '2', '3', '4', '8-numeric']
    if write_note_index_flag:
        steps_executed.append('7')

    return {
        'vault': config.name,
        'tool_version': TOOL_VERSION,
        'audit_date': today,
        'audit_timestamp': datetime.now().isoformat(),
        'scope': {
            'steps_executed': steps_executed,
            'steps_deferred_to_claude': ['5', '6', '8-narrative', '9'],
        },
        'vault_meta': {
            'is_flat_folder': config.is_flat_folder,
            'is_training': config.is_training,
            'tier3_output': config.tier3_output,
            'axis_field_name': config.axis_field_name,
            'axis_positions': config.fault_line_positions,
            'axis_abbrev_map': abbrev_map,
        },
        'totals': {
            'notes_total_excluding_t1': notes_total_excluding_t1,
            'notes_total_including_maps': notes_total_including_maps,
            'by_tier': totals,
        },
        'notes': notes_rows,
        'counts_by_domain': by_domain,
        'counts_by_op': {str(k): v for k, v in by_op.items()},
        'counts_by_axis': by_axis,
        'stragglers': stragglers,
        'planned_notes_status': planned_status,
        'targets_table': targets_table,
        'session_state_inputs': {
            'notes_since_last_audit_reset': 0,
            'last_coverage_audit': today,
            'total_notes_for_registry': notes_total_excluding_t1,
        },
        'summary_line': summary_line,
    }


def human_report(result, verbose=False):
    lines = []
    lines.append("=" * 70)
    lines.append(f"Coverage Audit — {result['vault']}")
    lines.append(f"Date: {result['audit_date']} · Tool: {result['tool_version']}")
    lines.append("=" * 70)
    lines.append("")

    lines.append("## Totals")
    by_tier = result['totals']['by_tier']
    for k in ('T1', 'T2-Ref', 'T2-Syn', 'T3', 'Map'):
        lines.append(f"  {k}: {by_tier.get(k, 0)}")
    lines.append(f"  notes excluding T1: {result['totals']['notes_total_excluding_t1']}")
    lines.append("")

    lines.append("## Counts by Domain")
    for slug, cnts in sorted(result['counts_by_domain'].items()):
        if not slug:
            slug_label = '(no domain)'
        else:
            slug_label = slug
        cells = [f'{k}={v}' for k, v in sorted(cnts.items())]
        lines.append(f"  {slug_label}: {', '.join(cells)}")
    lines.append("")

    lines.append("## Open Problem Coverage")
    for op_id in sorted(result['counts_by_op'].keys(), key=lambda x: int(x)):
        n = result['counts_by_op'][op_id]
        marker = '🔴 ' if n == 0 else '🟡 ' if n < 10 else '🟢 '
        lines.append(f"  {marker}OP {op_id}: {n}")
    lines.append("")

    if result['counts_by_axis']:
        lines.append("## Axis Coverage")
        for pos, n in sorted(result['counts_by_axis'].items(), key=lambda kv: -kv[1]):
            lines.append(f"  {pos}: {n}")
        lines.append("")

    targets = result['targets_table']
    lines.append(f"## Targets ({targets['parse_status']})")
    if targets['parse_status'] == 'ok':
        for slug, row in sorted(targets['rows'].items()):
            lines.append(f"  {slug}: target {row['target_t2']} / current {row['current_t2_syn']} T2-Syn → {row['gap']}")
    else:
        lines.append(f"  (could not parse — Claude reads targets directly in Step 5)")
    lines.append("")

    s = result['stragglers']
    lines.append("## Stragglers")
    lines.append(f"  domain slugs not in vault-config: {len(s['domain_slugs_not_in_config'])}")
    if s['domain_slugs_not_in_config']:
        lines.append(f"    -> {s['domain_slugs_not_in_config']}")
    lines.append(f"  notes lacking domain frontmatter: {len(s['notes_lacking_domain_frontmatter'])}")
    lines.append(f"  notes lacking EC frontmatter: {len(s['notes_lacking_ec_frontmatter'])}")
    lines.append(f"  notes lacking axis frontmatter: {len(s['notes_lacking_axis_frontmatter'])}")
    lines.append("")

    if result['planned_notes_status']:
        lines.append("## Planned Notes Status")
        by_status = Counter(p['status'] for p in result['planned_notes_status'])
        for k in ('complete', 'partial', 'missing'):
            lines.append(f"  {k}: {by_status.get(k, 0)}")
        lines.append("")

    lines.append("## Steps Deferred to Claude")
    lines.append("  - Step 5: priority gap list (which gap matters most given vault state)")
    lines.append("  - Step 6: coverage-plan rewrite (script provides updated tables; Claude integrates narrative)")
    lines.append("  - Step 8 narrative: open_actions, recent_arcs (script provides numeric reset values)")
    lines.append("  - Step 9: chain to /system-audit if system-model.yaml exists")
    lines.append("")
    lines.append(result['summary_line'])
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# BASELINE
# ─────────────────────────────────────────────────────────────

def baseline_path(vault_name, tools_dir):
    base_dir = tools_dir / 'baselines'
    base_dir.mkdir(exist_ok=True)
    return base_dir / f'{vault_name}-coverage-audit-baseline.json'


def save_baseline(result, tools_dir):
    p = baseline_path(result['vault'], tools_dir)
    p.write_text(json.dumps(result, indent=2, default=str), encoding='utf-8')
    return p


def compare_baseline(result, tools_dir):
    p = baseline_path(result['vault'], tools_dir)
    if not p.exists():
        return None
    baseline = json.loads(p.read_text(encoding='utf-8'))

    def _domain_diffs(a, b):
        out = {}
        for slug in set(a.keys()) | set(b.keys()):
            ac = a.get(slug, {})
            bc = b.get(slug, {})
            for tier in set(ac.keys()) | set(bc.keys()):
                delta = bc.get(tier, 0) - ac.get(tier, 0)
                if delta != 0:
                    out.setdefault(slug, {})[tier] = delta
        return out

    domain_deltas = _domain_diffs(
        baseline.get('counts_by_domain', {}),
        result.get('counts_by_domain', {}),
    )
    op_deltas = {}
    for opid in set(baseline.get('counts_by_op', {}).keys()) | set(result.get('counts_by_op', {}).keys()):
        delta = result.get('counts_by_op', {}).get(opid, 0) - baseline.get('counts_by_op', {}).get(opid, 0)
        if delta != 0:
            op_deltas[opid] = delta

    return {
        'compared_at': datetime.now().isoformat(),
        'current_audit_date': result['audit_date'],
        'baseline_audit_date': baseline.get('audit_date'),
        'tool_version_match': baseline.get('tool_version') == result.get('tool_version'),
        'domain_deltas': domain_deltas,
        'op_deltas': op_deltas,
        'total_delta': (result['totals']['notes_total_excluding_t1']
                        - baseline.get('totals', {}).get('notes_total_excluding_t1', 0)),
    }


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def find_coverage_plan(vault_path, config):
    """Try `<vault-name>-coverage-plan.md` at vault root, then any
    `*-coverage-plan.md` referenced in vault-config reference_docs."""
    candidate = vault_path / f'{config.name}-coverage-plan.md'
    if candidate.exists():
        return candidate
    # Fall back: scan reference_docs for coverage_plan-like entry
    for fname in config.reference_doc_files:
        if 'coverage' in fname.lower() and fname.endswith('.md'):
            p = vault_path / fname
            if p.exists():
                return p
    # Search root for any coverage plan
    for p in vault_path.glob('*-coverage-plan.md'):
        return p
    # Some vaults nest it (e.g. AI/ai-coverage-plan.md)
    for p in vault_path.rglob('*-coverage-plan.md'):
        if 'memory' not in str(p) and '.obsidian' not in str(p):
            return p
    return None


def main():
    parser = argparse.ArgumentParser(
        description='Coverage Audit — mechanical reconciliation of vault corpus vs coverage plan.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'Exit codes: 0 success, 3 invocation error.\n'
            'Steps deferred to Claude: 5 (priority gaps), 6 (plan rewrite), '
            '8-narrative (open_actions), 9 (system-audit chain).\n'
            'See framework/universal-commands/coverage-audit.md.'
        ),
    )
    parser.add_argument('vault_path', help='Path to vault root directory')
    parser.add_argument('--json', action='store_true',
                        help='Emit JSON instead of human report')
    parser.add_argument('--verbose', action='store_true',
                        help='Show all detail items (no truncation)')
    parser.add_argument('--write-note-index', action='store_true',
                        help='Rewrite memory/note-index.md from collected data (Step 7)')
    parser.add_argument('--include-planned-status', dest='include_planned_status',
                        action='store_true', default=True,
                        help='Run Step 3 planned-note status (default: on)')
    parser.add_argument('--no-include-planned-status', dest='include_planned_status',
                        action='store_false',
                        help='Skip Step 3 planned-note status')
    parser.add_argument('--targets', choices=['parse', 'skip'], default='parse',
                        help='parse: extract Target T2 column; skip: emit nulls')
    parser.add_argument('--baseline', choices=['save', 'compare'],
                        help='Save current audit as baseline, or diff against it')
    args = parser.parse_args()

    vault_path = Path(args.vault_path).resolve()
    if not vault_path.exists():
        print(f"ERROR: vault path does not exist: {vault_path}", file=sys.stderr)
        sys.exit(3)

    try:
        config = VaultConfig(vault_path)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(3)

    today = datetime.now().strftime('%Y-%m-%d')

    # Step 1: Domain walk + classification
    notes = discover_notes(vault_path, config,
                           include_infrastructure_maps=True,
                           include_t3_output=True)
    all_fm = {}
    all_classifications = {}
    all_paths_to_domains = {}
    for p in notes:
        try:
            content = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            content = ''
        fm = parse_frontmatter(content)
        all_fm[p] = fm
        all_classifications[p] = classify_for_coverage(p, fm, config)
        all_paths_to_domains[p] = get_note_domain(p, fm, config)

    # Aggregations
    totals = dict(Counter(all_classifications.values()))
    by_domain = count_by_domain(all_classifications, all_paths_to_domains)
    by_op = count_op_coverage(all_fm, config)
    by_axis = count_axis_coverage(all_fm, config.axis_field_name)

    # Stragglers
    stragglers = compute_stragglers(all_classifications, all_fm, all_paths_to_domains, config)

    # Step 3: Planned notes
    coverage_plan = find_coverage_plan(vault_path, config)
    planned_status = []
    if args.include_planned_status:
        planned = parse_planned_notes(coverage_plan)
        if planned:
            planned_status = match_planned_notes(planned, list(all_fm.keys()))

    # Targets table
    if args.targets == 'parse':
        targets_table = parse_targets_table(coverage_plan, by_domain)
    else:
        targets_table = {'parsed_from': None, 'parse_status': 'skipped', 'rows': {}}

    # Axis abbreviations
    abbrev_map = make_axis_abbrev_map(config.fault_line_positions or [])

    # Build per-note rows
    notes_rows = []
    op_key = config.open_problem_key
    axis_field = config.axis_field_name
    for p in sorted(all_fm.keys()):
        fm = all_fm[p]
        tier = all_classifications[p]
        rel = str(p.relative_to(vault_path)).replace('\\', '/')
        ec_raw = fm.get('evergreen-candidate', '')
        ec_source = 'frontmatter' if ec_raw not in (None, '') else 'domain-default'
        if isinstance(ec_raw, list):
            ec_raw = ','.join(str(x) for x in ec_raw)
        axis_raw = fm.get(axis_field, '')
        if isinstance(axis_raw, list):
            axis_raw = axis_raw[0] if axis_raw else ''
        axis_first = re.split(r'\s*[/|]\s*', str(axis_raw).strip('"\''))[0].strip()
        ops_raw = fm.get(op_key) or []
        if isinstance(ops_raw, str):
            ops_raw = [ops_raw]
        ops_int = []
        for o in ops_raw:
            try:
                ops_int.append(int(str(o).strip()))
            except (ValueError, TypeError):
                pass
        src_raw = str(fm.get('source', '')).lower()
        if 'dialogue' in src_raw:
            src = 'user-dialogue'
        elif 'reflection' in src_raw:
            src = 'user-reflection'
        else:
            src = None
        created = fm.get('created') or ''
        if not created:
            m = re.match(r'^(\d{4})(\d{2})(\d{2})', p.name)
            if m:
                created = f'{m.group(1)}-{m.group(2)}-{m.group(3)}'
        notes_rows.append({
            'path': rel,
            'tier': tier,
            'domain': all_paths_to_domains[p] or '',
            'ec': str(ec_raw).strip() if ec_raw else '',
            'ec_source': ec_source if ec_raw not in (None, '') else 'n/a',
            'axis': axis_first,
            'axis_abbrev': abbrev_map.get(axis_first, ''),
            'ops': ops_int,
            'source': src,
            'created': created,
        })

    # Step 7: Note index (optional)
    note_index_path = None
    if args.write_note_index:
        note_index_path = write_note_index(
            vault_path, config, all_classifications, all_fm,
            all_paths_to_domains, abbrev_map, len(all_fm), today,
        )

    # Assemble result
    result = assemble_result(
        config, totals, dict(totals), by_domain, by_op, by_axis,
        notes_rows, stragglers, planned_status, targets_table,
        abbrev_map, today, args.write_note_index,
    )
    if note_index_path:
        result['note_index_path'] = str(note_index_path).replace('\\', '/')

    # Baseline workflow
    tools_dir = Path(__file__).resolve().parent
    if args.baseline == 'save':
        p = save_baseline(result, tools_dir)
        print(f"Baseline saved: {p}")
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
            print(f"  total notes change: {cmp['total_delta']:+d}")
            print(f"  domain deltas: {len(cmp['domain_deltas'])} domain(s) changed")
            for slug, deltas in cmp['domain_deltas'].items():
                print(f"    {slug}: {deltas}")
            print(f"  op deltas: {len(cmp['op_deltas'])} OP(s) changed")
            print(f"  tool_version match: {cmp['tool_version_match']}")
            print()
            print(result['summary_line'])
        sys.exit(0)

    # Standard emit
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(human_report(result, verbose=args.verbose))

    sys.exit(0)


if __name__ == '__main__':
    main()
