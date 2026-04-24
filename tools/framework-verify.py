#!/usr/bin/env python3
"""
framework-verify.py — Architectural integrity checks for the agensy framework.

Complements vault-linter.py (which validates note CONTENT against schema) by
validating the FRAMEWORK STRUCTURE against its own contracts:
  - vault-config.md completeness
  - context budget compliance
  - stub → protocol integrity
  - reference path resolution
  - cross-framework consistency

Run after any structural change to agensy framework documents.

Usage:
    python framework-verify.py [options]

Options:
    --category F1|F2|F3|F4|F5|all   Which checks to run (default: all)
    --json                           Output JSON format
    --verbose                        Show passing checks (default: failures only)
    --check F01                      Run only a specific check code

Check codes:
    F01–F05  Category F1: Configuration Integrity
    F06–F08  Category F2: Budget Compliance
    F09–F11  Category F3: Stub & Protocol Integrity
    F12–F14  Category F4: Path Integrity
    F15–F17  Category F5: Cross-Framework Consistency
    F18–F22  Category F6: Meta-Architecture Integrity
             (frontmatter schema, canonicity uniqueness, synchronized-with
              symmetry + fact-match, protocol path discipline, supersession chain)
"""

import io
import os
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Force UTF-8 output on Windows
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ─────────────────────────────────────────────────────────────────────────────
# CONTRACT TABLE
# Required vault-config.md keys per command.
# Mirrors system-contracts.md §2. Update both when adding commands.
# ─────────────────────────────────────────────────────────────────────────────

COMMAND_REQUIRED_KEYS = {
    'arc': [
        'domains', 'intellectual_style', 'engagement_axis',
        'note_tiers', 'note_template', 'reference_docs', 'folder_structure',
    ],
    'coverage-audit': [
        'domains', 'open_problems', 'note_tiers',
        'folder_structure', 'reference_docs',
    ],
    'axis-survey': [
        'domains', 'intellectual_style', 'engagement_axis', 'open_problems',
    ],
    'what-next': [
        'domains', 'open_problems', 'reference_docs',
    ],
    'promote': [
        'note_tiers', 'note_template', 'intellectual_style',
        'folder_structure',
    ],
    'compare': [
        'domains', 'intellectual_style', 'engagement_axis', 'open_problems',
    ],
    'engage-problem': [
        'domains', 'open_problems', 'intellectual_style', 'engagement_axis',
    ],
    'synthesis': [
        'domains', 'driving_questions', 'intellectual_style',
        'engagement_axis', 'open_problems',
    ],
    'update-moc': [
        'domains', 'folder_structure',
    ],
    'evergreen-note': [
        'note_tiers', 'note_template', 'intellectual_style',
        'engagement_axis', 'open_problems',
    ],
    'engage-deep': [
        'open_problems', 'driving_questions', 'intellectual_style', 'engagement_axis',
    ],
    'domain-audit': [
        'domains', 'note_tiers', 'note_template', 'intellectual_style',
        'folder_structure', 'reference_docs',
    ],
    'quick-check': [
        'domains', 'note_template', 'intellectual_style',
        'engagement_axis', 'open_problems',
    ],
    'dialogue': [
        'open_problems', 'driving_questions', 'intellectual_style',
        'engagement_axis', 'folder_structure', 'note_template',
    ],
    'positions': [],   # cross-vault: reads note-index, not vault-config
    'revisit': [
        'folder_structure', 'open_problems', 'intellectual_style', 'engagement_axis',
    ],
    'question-bank': [],  # operates on agensy directly

    # ── System Model Layer (v0.1+, registered 2026-04-20) ────────────────
    'system-query': [
        'domains', 'engagement_axis',
    ],
    'system-audit': [
        'domains', 'engagement_axis', 'folder_structure',
    ],
    'system-build': [
        'domains', 'engagement_axis',
    ],
    'system-bridge': [
        'domains',
    ],

    # ── Article Pipeline (cogitationis-facing, registered 2026-04-21/22) ─
    # Consume reference_docs.* keys specific to expression vaults
    # (voice_profile, writer_positions, positions_index, article_presets,
    #  map_to_article_schema, source_map_registry).
    'article-scan': [
        'reference_docs',
    ],
    'article-seed': [
        'reference_docs', 'folder_structure',
    ],
    'article-outline': [
        'reference_docs', 'folder_structure', 'note_template',
    ],
    'article-draft': [
        'reference_docs', 'output_layer',
    ],
    'article-revise': [
        'reference_docs', 'note_template',
    ],
    'article-promote': [
        'reference_docs', 'folder_structure', 'output_layer',
    ],
    'article-critique': [
        'reference_docs', 'folder_structure',
    ],
    'article-companion': [
        'reference_docs', 'folder_structure',
    ],

    # ── Companion Collaborative (registered 2026-04-22) ──────────────────
    # co-find / co-combine read registries, not vault-config (cross-vault)
    'co-find': [],          # reads vault-registry + positions-index
    'co-combine': [],       # reads map files + cross-vault-bridges
    'co-suggest': [
        'reference_docs',
    ],
    'co-critique': [
        'reference_docs',
    ],
    'co-capture': [
        'reference_docs', 'folder_structure',
    ],
}

# Alias stubs that point to the same protocol
STUB_ALIASES = {
    'confront': 'engage-deep',
    'fault-line-survey': 'axis-survey',
}

# Blocks that must be present in vault-config.md for a fully compliant vault
REQUIRED_VAULT_CONFIG_BLOCKS = [
    'domains', 'open_problems', 'intellectual_style', 'driving_questions',
    'note_tiers', 'folder_structure', 'note_template', 'reference_docs',
]

# ─────────────────────────────────────────────────────────────────────────────
# VAULT DISCOVERY
# ─────────────────────────────────────────────────────────────────────────────

def find_meta_root() -> Path:
    """Locate agensy root from this script's location."""
    return Path(__file__).parent.parent


def discover_vaults(meta_root: Path) -> list[dict]:
    """
    Parse vault-registry.md to find all active vault paths and types.
    Returns list of {name, path, type, compliance} dicts.
    """
    registry = meta_root / 'vault-registry.md'
    if not registry.exists():
        return []

    text = registry.read_text(encoding='utf-8')
    vaults = []

    # Parse the Active Vaults table: | name | `path` | type | mission |
    for m in re.finditer(
        r'^\|\s*([\w-]+)\s*\|\s*`([^`]+)`\s*\|\s*(\w+)\s*\|',
        text, re.MULTILINE
    ):
        name, raw_path, vtype = m.group(1), m.group(2), m.group(3)
        path = Path(raw_path.rstrip('\\').rstrip('/'))

        # Compliance from the framework table
        comp_m = re.search(
            rf'^\|\s*{re.escape(name)}\s*\|\s*(\S[^|]+?)\s*\|',
            text, re.MULTILINE
        )
        compliance = comp_m.group(1).strip() if comp_m else 'unknown'

        vaults.append({
            'name': name,
            'path': path,
            'type': vtype,
            'compliance': compliance,
        })

    return vaults


# ─────────────────────────────────────────────────────────────────────────────
# VAULT CONFIG PARSER (lightweight — checks key presence, not deep values)
# ─────────────────────────────────────────────────────────────────────────────

class FrameworkVaultConfig:
    """
    Lightweight parser for vault-config.md — checks structural completeness,
    not semantic correctness (vault-linter.py handles that).
    """

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        config_path = vault_path / 'vault-config.md'
        self.exists = config_path.exists()
        if not self.exists:
            self.text = ''
            return
        self.text = config_path.read_text(encoding='utf-8', errors='ignore')

    def has_block(self, block: str) -> bool:
        """Check if a top-level YAML block key is present."""
        return bool(re.search(rf'^{re.escape(block)}:', self.text, re.MULTILINE))

    def get_positions(self) -> list:
        """Extract engagement_axis position names.
        Supports two formats:
          flat:   `    - materialist: >` (id-as-key)
          nested: `      - id: structuralist` (id-as-field)
        """
        # Format A — flat, 4-space indent id-as-key
        m = re.search(r'\n  positions:\n((?:    - [\w][\w-]*:.*\n)+)', self.text)
        if m:
            return re.findall(r'    - ([\w][\w-]*):', m.group(1))
        # Format B — nested, 6-space indent with `id:` field
        m = re.search(r'\n    positions:\n((?:      - id: [\w][\w-]*\n(?:        [^\n]*\n)+)+)', self.text)
        if m:
            return re.findall(r'      - id: ([\w][\w-]*)', m.group(1))
        # Backward compat: fault_line positions (flat)
        m = re.search(r'\nfault_line:\n(?:.*\n)*?  positions:\n((?:    - [\w][\w-]*:.*\n)+)', self.text)
        if m:
            return re.findall(r'    - ([\w][\w-]*):', m.group(1))
        return []

    def get_open_problems(self) -> list:
        """Return list of {id, has_name, has_question} for each open problem."""
        problems = []
        # Find open_problems: block
        op_m = re.search(r'^open_problems:\n((?:  - [\s\S]*?)(?=\n\w|\Z))', self.text, re.MULTILINE)
        if not op_m:
            return problems
        block = op_m.group(1)
        entries = re.split(r'(?=  - id:)', block)
        for entry in entries:
            if not entry.strip():
                continue
            id_m = re.search(r'  - id:\s*(\d+)', entry)
            name_m = re.search(r'    name:', entry)
            q_m = re.search(r'    question:', entry)
            if id_m:
                problems.append({
                    'id': int(id_m.group(1)),
                    'has_name': bool(name_m),
                    'has_question': bool(q_m),
                })
        return problems

    def get_domains(self) -> list:
        """Return list of {slug, has_label, has_folder, has_priority} dicts."""
        domains = []
        dom_m = re.search(r'^domains:\n((?:  - [\s\S]*?)(?=\n\w|\Z))', self.text, re.MULTILINE)
        if not dom_m:
            return domains
        block = dom_m.group(1)
        entries = re.split(r'(?=  - slug:)', block)
        for entry in entries:
            if not entry.strip():
                continue
            slug_m = re.search(r'  - slug:\s*(\S+)', entry)
            if slug_m:
                domains.append({
                    'slug': slug_m.group(1),
                    'has_label': bool(re.search(r'    label:', entry)),
                    'has_folder': bool(re.search(r'    folder:', entry)),
                    'has_priority': bool(re.search(r'    priority:', entry)),
                })
        return domains

    def get_reference_docs(self) -> dict:
        """Return {key: path} for all reference_docs entries."""
        docs = {}
        rd_m = re.search(r'^reference_docs:\n((?:  \w.*\n)+)', self.text, re.MULTILINE)
        if rd_m:
            for line in rd_m.group(1).splitlines():
                m = re.match(r'  (\w+):\s*"([^"]+)"', line)
                if m:
                    docs[m.group(1)] = m.group(2)
        return docs

    def get_folder_structure(self) -> dict:
        """Return {key: path} for all folder_structure entries."""
        folders = {}
        fs_m = re.search(r'^folder_structure:\n((?:  \w.*\n)+)', self.text, re.MULTILINE)
        if fs_m:
            for line in fs_m.group(1).splitlines():
                m = re.match(r'  (\w+):\s*"([^"]+)"', line)
                if m:
                    folders[m.group(1)] = m.group(2)
        return folders


# ─────────────────────────────────────────────────────────────────────────────
# RESULT HELPERS
# ─────────────────────────────────────────────────────────────────────────────

class Result:
    def __init__(self, code: str, status: str, message: str, detail: str = ''):
        self.code = code
        self.status = status   # 'PASS' | 'FAIL' | 'WARN' | 'SKIP'
        self.message = message
        self.detail = detail

    def to_dict(self):
        d = {'code': self.code, 'status': self.status, 'message': self.message}
        if self.detail:
            d['detail'] = self.detail
        return d

    def __str__(self):
        base = f'[{self.code}] {self.status}: {self.message}'
        if self.detail:
            base += f'\n         {self.detail}'
        return base


def ok(code, msg): return Result(code, 'PASS', msg)
def fail(code, msg, detail=''): return Result(code, 'FAIL', msg, detail)
def warn(code, msg, detail=''): return Result(code, 'WARN', msg, detail)
def skip(code, msg): return Result(code, 'SKIP', msg)


# ─────────────────────────────────────────────────────────────────────────────
# CATEGORY F1 — CONFIGURATION INTEGRITY
# ─────────────────────────────────────────────────────────────────────────────

def check_f01_vault_configs_exist(vaults: list) -> list[Result]:
    """F01: Every active vault (except framework vault) has a vault-config.md."""
    results = []
    for v in vaults:
        if v['type'] == 'framework':
            results.append(skip('F01', f'{v["name"]}: skipped (framework vault — no vault-config by design)'))
            continue
        cfg = FrameworkVaultConfig(v['path'])
        if cfg.exists:
            results.append(ok('F01', f'{v["name"]}: vault-config.md exists'))
        else:
            results.append(fail('F01', f'{v["name"]}: vault-config.md missing',
                                f'Expected at: {v["path"] / "vault-config.md"}'))
    return results


def check_f02_required_blocks(vaults: list) -> list[Result]:
    """F02: vault-config.md has all required top-level blocks."""
    results = []
    for v in vaults:
        cfg = FrameworkVaultConfig(v['path'])
        if not cfg.exists:
            results.append(skip('F02', f'{v["name"]}: skipped (no vault-config.md)'))
            continue
        missing = [b for b in REQUIRED_VAULT_CONFIG_BLOCKS if not cfg.has_block(b)]
        if missing:
            results.append(fail('F02', f'{v["name"]}: missing required blocks',
                                f'Missing: {", ".join(missing)}'))
        else:
            results.append(ok('F02', f'{v["name"]}: all required blocks present'))
    return results


def check_f03_positions_nonempty(vaults: list) -> list[Result]:
    """F03: engagement_axis.positions[] is non-empty in every vault-config."""
    results = []
    for v in vaults:
        if v['type'] in ('framework', 'expression'):
            results.append(skip('F03', f'{v["name"]}: skipped ({v["type"]} vault)'))
            continue
        cfg = FrameworkVaultConfig(v['path'])
        if not cfg.exists:
            results.append(skip('F03', f'{v["name"]}: skipped (no vault-config.md)'))
            continue
        positions = cfg.get_positions()
        if positions:
            results.append(ok('F03', f'{v["name"]}: {len(positions)} engagement axis positions'))
        else:
            results.append(fail('F03', f'{v["name"]}: no engagement axis positions found',
                                'Check intellectual_style.engagement_axis.positions or fault_line.positions'))
    return results


def check_f04_open_problems_complete(vaults: list) -> list[Result]:
    """F04: All open_problems entries have id, name, and question."""
    results = []
    for v in vaults:
        if v['type'] in ('framework', 'expression'):
            results.append(skip('F04', f'{v["name"]}: skipped ({v["type"]} vault)'))
            continue
        cfg = FrameworkVaultConfig(v['path'])
        if not cfg.exists:
            results.append(skip('F04', f'{v["name"]}: skipped (no vault-config.md)'))
            continue
        problems = cfg.get_open_problems()
        if not problems:
            results.append(warn('F04', f'{v["name"]}: no open_problems found'))
            continue
        incomplete = [p['id'] for p in problems if not p['has_name'] or not p['has_question']]
        if incomplete:
            results.append(fail('F04', f'{v["name"]}: {len(incomplete)} open_problems missing name/question',
                                f'Problem IDs: {incomplete}'))
        else:
            results.append(ok('F04', f'{v["name"]}: {len(problems)} open_problems all complete'))
    return results


def check_f05_domains_complete(vaults: list) -> list[Result]:
    """F05: All domain entries have slug, label, folder, priority."""
    results = []
    for v in vaults:
        if v['type'] == 'framework':
            results.append(skip('F05', f'{v["name"]}: skipped (framework vault)'))
            continue
        cfg = FrameworkVaultConfig(v['path'])
        if not cfg.exists:
            results.append(skip('F05', f'{v["name"]}: skipped (no vault-config.md)'))
            continue
        domains = cfg.get_domains()
        if not domains:
            results.append(warn('F05', f'{v["name"]}: no domains found'))
            continue
        incomplete = [d['slug'] for d in domains
                      if not d['has_label'] or not d['has_folder'] or not d['has_priority']]
        if incomplete:
            results.append(fail('F05', f'{v["name"]}: {len(incomplete)} domains missing label/folder/priority',
                                f'Slugs: {incomplete}'))
        else:
            results.append(ok('F05', f'{v["name"]}: {len(domains)} domains all complete'))
    return results


# ─────────────────────────────────────────────────────────────────────────────
# CATEGORY F2 — BUDGET COMPLIANCE
# ─────────────────────────────────────────────────────────────────────────────

def count_meaningful_lines(path: Path) -> int:
    """Count non-empty lines in a file."""
    if not path.exists():
        return 0
    text = path.read_text(encoding='utf-8', errors='ignore')
    return sum(1 for line in text.splitlines() if line.strip())


def check_f06_global_claude_budget() -> list[Result]:
    """F06: Global CLAUDE.md is under 100 lines."""
    home = Path.home()
    global_claude = home / '.claude' / 'CLAUDE.md'
    if not global_claude.exists():
        return [warn('F06', f'Global CLAUDE.md not found at {global_claude}')]
    lines = count_meaningful_lines(global_claude)
    if lines <= 100:
        return [ok('F06', f'Global CLAUDE.md: {lines} lines (budget: 100)')]
    return [fail('F06', f'Global CLAUDE.md: {lines} lines EXCEEDS budget of 100',
                 f'Path: {global_claude}')]


def check_f07_vault_claude_budget(vaults: list) -> list[Result]:
    """F07: Each vault CLAUDE.md is under 120 lines."""
    results = []
    for v in vaults:
        claude_md = v['path'] / 'CLAUDE.md'
        if not claude_md.exists():
            results.append(warn('F07', f'{v["name"]}: CLAUDE.md not found'))
            continue
        lines = count_meaningful_lines(claude_md)
        if lines <= 120:
            results.append(ok('F07', f'{v["name"]} CLAUDE.md: {lines} lines (budget: 120)'))
        else:
            results.append(fail('F07', f'{v["name"]} CLAUDE.md: {lines} lines EXCEEDS budget of 120'))
    return results


def check_f08_memory_budget(vaults: list) -> list[Result]:
    """F08: Each vault MEMORY.md is under 150 lines."""
    results = []
    for v in vaults:
        memory_md = v['path'] / 'memory' / 'MEMORY.md'
        if not memory_md.exists():
            results.append(skip('F08', f'{v["name"]}: memory/MEMORY.md not found'))
            continue
        lines = count_meaningful_lines(memory_md)
        if lines <= 150:
            results.append(ok('F08', f'{v["name"]} MEMORY.md: {lines} lines (budget: 150)'))
        else:
            results.append(fail('F08', f'{v["name"]} MEMORY.md: {lines} lines EXCEEDS budget of 150'))
    return results


# ─────────────────────────────────────────────────────────────────────────────
# CATEGORY F3 — STUB & PROTOCOL INTEGRITY
# ─────────────────────────────────────────────────────────────────────────────

def get_universal_protocol_names(meta_root: Path) -> set:
    """Return set of command names from universal-commands/ (stems, no extension)."""
    uc_dir = meta_root / 'framework' / 'universal-commands'
    if not uc_dir.exists():
        return set()
    return {p.stem for p in uc_dir.glob('*.md')}


def get_stub_protocol_path(stub_path: Path) -> str | None:
    """Extract the protocol file path referenced in a stub file."""
    text = stub_path.read_text(encoding='utf-8', errors='ignore')
    m = re.search(r'Read the protocol:\s*`([^`]+)`', text)
    if m:
        return m.group(1).strip()
    # Alternate format: bare path line
    m = re.search(r'universal-commands[/\\]([\w-]+)\.md', text)
    if m:
        return m.group(0)
    return None


def check_f09_stubs_reference_existing_protocols(vaults: list, meta_root: Path) -> list[Result]:
    """F09: Every stub in .claude/commands/ references an existing universal protocol."""
    results = []
    uc_dir = meta_root / 'framework' / 'universal-commands'

    for v in vaults:
        commands_dir = v['path'] / '.claude' / 'commands'
        if not commands_dir.exists():
            results.append(warn('F09', f'{v["name"]}: .claude/commands/ not found'))
            continue

        for stub in commands_dir.glob('*.md'):
            proto_path_str = get_stub_protocol_path(stub)
            if not proto_path_str:
                # Might be a vault-specific full protocol, not a stub — check length
                text = stub.read_text(encoding='utf-8', errors='ignore')
                meaningful = sum(1 for l in text.splitlines() if l.strip() and not l.startswith('---') and not l.startswith('#'))
                if meaningful > 15:
                    # Vault-specific command — OK
                    continue
                results.append(warn('F09', f'{v["name"]}/{stub.name}: stub has no protocol reference'))
                continue

            # Resolve the protocol path
            proto_path = Path(proto_path_str)
            if proto_path.is_absolute():
                exists = proto_path.exists()
            else:
                # Try relative to meta root or to universal-commands
                cmd_name = proto_path.stem
                exists = (uc_dir / f'{cmd_name}.md').exists()

            if exists:
                results.append(ok('F09', f'{v["name"]}/{stub.name}: protocol reference valid'))
            else:
                # Check aliases
                cmd_stem = Path(proto_path_str).stem
                if cmd_stem in STUB_ALIASES:
                    alias_target = STUB_ALIASES[cmd_stem]
                    if (uc_dir / f'{alias_target}.md').exists():
                        results.append(ok('F09', f'{v["name"]}/{stub.name}: alias stub → {alias_target}'))
                        continue
                results.append(fail('F09', f'{v["name"]}/{stub.name}: protocol file not found',
                                    f'Referenced: {proto_path_str}'))
    return results


def check_f10_all_protocols_have_stubs(vaults: list, meta_root: Path) -> list[Result]:
    """F10: Every universal protocol has a stub in every compliant vault."""
    results = []
    proto_names = get_universal_protocol_names(meta_root)
    # Exclude alias files — they don't need separate stubs
    alias_targets = set(STUB_ALIASES.values())
    core_protos = {p for p in proto_names if p not in STUB_ALIASES}

    compliant_vaults = [v for v in vaults if 'native' in v.get('compliance', '').lower()
                        or 'migrated' in v.get('compliance', '').lower()]

    for v in compliant_vaults:
        commands_dir = v['path'] / '.claude' / 'commands'
        if not commands_dir.exists():
            results.append(warn('F10', f'{v["name"]}: .claude/commands/ not found — skipping'))
            continue

        stub_names = {p.stem for p in commands_dir.glob('*.md')}
        # Stubs can match either the protocol name or an alias
        all_covered = core_protos | set(STUB_ALIASES.keys())
        missing = core_protos - stub_names - set(STUB_ALIASES.keys())
        # Check if covered by aliases
        missing = {m for m in missing
                   if not any(STUB_ALIASES.get(s) == m for s in stub_names)}

        if missing:
            results.append(fail('F10', f'{v["name"]}: {len(missing)} protocols have no stub',
                                f'Missing stubs: {sorted(missing)}'))
        else:
            results.append(ok('F10', f'{v["name"]}: all {len(core_protos)} protocols have stubs'))
    return results


def check_f11_stubs_not_bloated(vaults: list) -> list[Result]:
    """F11: No stub contains protocol logic (>15 meaningful non-header lines = suspect)."""
    results = []
    for v in vaults:
        commands_dir = v['path'] / '.claude' / 'commands'
        if not commands_dir.exists():
            continue
        for stub in commands_dir.glob('*.md'):
            text = stub.read_text(encoding='utf-8', errors='ignore')
            # Count non-frontmatter, non-comment, non-empty lines
            in_frontmatter = False
            meaningful = 0
            for line in text.splitlines():
                if line.strip() == '---':
                    in_frontmatter = not in_frontmatter
                    continue
                if in_frontmatter:
                    continue
                if line.strip() and not line.startswith('#') and not line.startswith('$'):
                    meaningful += 1

            if meaningful <= 15:
                results.append(ok('F11', f'{v["name"]}/{stub.name}: {meaningful} lines (slim stub)'))
            else:
                # Check if it's a vault-specific command (not a universal stub)
                proto_ref = get_stub_protocol_path(stub)
                if proto_ref:
                    # It has a protocol reference — it's a stub, but bloated
                    results.append(warn('F11', f'{v["name"]}/{stub.name}: {meaningful} meaningful lines — possible protocol duplication'))
                # else: vault-specific full protocol — skip
    return results


# ─────────────────────────────────────────────────────────────────────────────
# CATEGORY F4 — PATH INTEGRITY
# ─────────────────────────────────────────────────────────────────────────────

def check_f12_reference_docs_resolve(vaults: list) -> list[Result]:
    """F12: All reference_docs paths in vault-config.md resolve to existing files."""
    results = []
    for v in vaults:
        cfg = FrameworkVaultConfig(v['path'])
        if not cfg.exists:
            results.append(skip('F12', f'{v["name"]}: skipped (no vault-config.md)'))
            continue
        ref_docs = cfg.get_reference_docs()
        if not ref_docs:
            results.append(warn('F12', f'{v["name"]}: no reference_docs entries found'))
            continue
        for key, rel_path in ref_docs.items():
            # note_index is optional cache — warn not fail if missing
            full_path = v['path'] / rel_path
            if full_path.exists():
                results.append(ok('F12', f'{v["name"]} reference_docs.{key}: exists'))
            elif key == 'note_index':
                results.append(warn('F12', f'{v["name"]} reference_docs.note_index: not yet created (run /coverage-audit)'))
            else:
                results.append(fail('F12', f'{v["name"]} reference_docs.{key}: file not found',
                                    f'Expected at: {full_path}'))
    return results


def check_f13_folder_structure_exists(vaults: list) -> list[Result]:
    """F13: All folder_structure paths in vault-config.md exist as directories."""
    results = []
    # Keys that are files/infra, not content dirs — skip for directory check
    non_dir_keys = {'commands'}

    for v in vaults:
        cfg = FrameworkVaultConfig(v['path'])
        if not cfg.exists:
            results.append(skip('F13', f'{v["name"]}: skipped (no vault-config.md)'))
            continue
        folders = cfg.get_folder_structure()
        if not folders:
            results.append(warn('F13', f'{v["name"]}: no folder_structure entries found'))
            continue
        for key, rel_path in folders.items():
            if key in non_dir_keys:
                continue
            full_path = v['path'] / rel_path
            if full_path.exists() and full_path.is_dir():
                results.append(ok('F13', f'{v["name"]} folder_structure.{key}: exists'))
            else:
                results.append(fail('F13', f'{v["name"]} folder_structure.{key}: directory not found',
                                    f'Expected at: {full_path}'))
    return results


def check_f14_maps_folder_exists(vaults: list) -> list[Result]:
    """F14: _maps/ folder exists in every vault that defines folder_structure.maps."""
    results = []
    for v in vaults:
        cfg = FrameworkVaultConfig(v['path'])
        if not cfg.exists:
            results.append(skip('F14', f'{v["name"]}: skipped (no vault-config.md)'))
            continue
        folders = cfg.get_folder_structure()
        if 'maps' not in folders:
            results.append(skip('F14', f'{v["name"]}: no folder_structure.maps defined'))
            continue
        maps_path = v['path'] / folders['maps']
        if maps_path.exists() and maps_path.is_dir():
            results.append(ok('F14', f'{v["name"]}: maps folder exists at {folders["maps"]}'))
        else:
            results.append(fail('F14', f'{v["name"]}: maps folder not found',
                                f'Expected at: {maps_path}'))
    return results


# ─────────────────────────────────────────────────────────────────────────────
# CATEGORY F5 — CROSS-FRAMEWORK CONSISTENCY
# ─────────────────────────────────────────────────────────────────────────────

def check_f15_contract_table_complete(meta_root: Path) -> list[Result]:
    """F15: system-contracts.md contract table lists all universal commands."""
    sc_path = meta_root / 'framework' / 'principles' / 'system-contracts.md'
    if not sc_path.exists():
        return [fail('F15', 'system-contracts.md not found')]

    sc_text = sc_path.read_text(encoding='utf-8', errors='ignore')
    proto_names = get_universal_protocol_names(meta_root)
    # Exclude alias files from check
    core_protos = {p for p in proto_names if p not in STUB_ALIASES}

    results = []
    missing_from_table = []
    for proto in core_protos:
        # Check if the command appears in the contract table section
        if not re.search(rf'`/{proto}`|/`{proto}`|\| `/\*?{re.escape(proto)}\*?`', sc_text):
            missing_from_table.append(proto)

    if missing_from_table:
        results.append(warn('F15', f'{len(missing_from_table)} universal commands may be missing from contract table',
                            f'Commands: {sorted(missing_from_table)}'))
    else:
        results.append(ok('F15', f'system-contracts.md contract table covers all {len(core_protos)} universal commands'))
    return results


def check_f16_schema_mentions_blocks(meta_root: Path) -> list[Result]:
    """F16: vault-config-schema.md mentions all top-level blocks required by commands."""
    schema_path = meta_root / 'framework' / 'templates' / 'vault-config-schema.md'
    if not schema_path.exists():
        return [fail('F16', 'vault-config-schema.md not found')]

    schema_text = schema_path.read_text(encoding='utf-8', errors='ignore')
    results = []
    missing = []
    for block in REQUIRED_VAULT_CONFIG_BLOCKS:
        if not re.search(rf'^{re.escape(block)}:', schema_text, re.MULTILINE):
            missing.append(block)

    if missing:
        results.append(fail('F16', f'vault-config-schema.md missing blocks: {missing}'))
    else:
        results.append(ok('F16', f'vault-config-schema.md defines all {len(REQUIRED_VAULT_CONFIG_BLOCKS)} required blocks'))
    return results


def check_f17_genesis_doc_count(meta_root: Path) -> list[Result]:
    """F17: genesis-protocol.md Phase 1 lists at least 12 Doc entries (Docs 1–12 universal; Doc 13+ conditional per vault type)."""
    genesis_path = meta_root / 'framework' / 'protocols' / 'genesis-protocol.md'
    if not genesis_path.exists():
        return [fail('F17', 'genesis-protocol.md not found')]

    text = genesis_path.read_text(encoding='utf-8', errors='ignore')
    # Find Phase 1 section and count ### Doc N headers
    phase1_m = re.search(r'## Phase 1.*?\n([\s\S]*?)(?=^## Phase|\Z)', text, re.MULTILINE)
    if not phase1_m:
        return [warn('F17', 'Could not locate Phase 1 section in genesis-protocol.md')]

    phase1_text = phase1_m.group(1)
    doc_headers = re.findall(r'### Doc \d+', phase1_text)
    count = len(doc_headers)
    # Docs 1-12 are universal (required for every new vault);
    # Doc 13+ are conditional (e.g., vault-type substrate templates for expression/training).
    if count >= 12:
        suffix = f' ({count - 12} conditional extension{"s" if count - 12 != 1 else ""})' if count > 12 else ''
        return [ok('F17', f'genesis-protocol.md Phase 1 has {count} Doc entries{suffix}')]
    return [fail('F17', f'genesis-protocol.md Phase 1 has {count} Doc entries (expected ≥12)',
                 f'Found: {doc_headers}')]


# ─────────────────────────────────────────────────────────────────────────────
# CATEGORY F6 — META-ARCHITECTURE INTEGRITY
# Frontmatter-driven checks on the framework's own document system.
# Canonical declaration: framework/principles/framework-meta-architecture.md §11–§12
# ─────────────────────────────────────────────────────────────────────────────

# Enumerations from framework-meta-architecture.md §11
F6_TYPE_CANONICAL = {
    'invariant', 'topology', 'protocol', 'template', 'vocabulary', 'schema',
    'reference', 'decision_record', 'experiment_log', 'registry', 'meta_workflow',
    'validation_tool',
}
# Backward-compat aliases: legacy kebab-case + pre-taxonomy values map to canonical names.
# New docs should use the canonical snake_case forms; existing docs are not forced to migrate.
F6_TYPE_ALIASES = {
    'universal-protocol': 'protocol',
    'decision-record': 'decision_record',
    'experiment-log': 'experiment_log',
    'gate-decision': 'experiment_log',   # Phase 0 gate records = experiment logs
    'architecture': 'reference',          # pre-taxonomy "architecture" type = design rationale reference
    # Vault-type-template files carry types describing what they will BE once copied into
    # a vault (voice-profile.md becomes a style-card; writer-positions.md becomes a
    # positions-card; positions-index.md keeps its indexing role). At framework-level
    # they are all `template` variants.
    'style-card': 'template',
    'positions-card': 'template',
    'positions-index': 'template',
}
F6_TYPE_ENUM = F6_TYPE_CANONICAL | set(F6_TYPE_ALIASES.keys())
F6_STABILITY_ENUM = {'bedrock', 'foundational', 'operational', 'dynamic', 'historical'}
F6_CANONICITY_ENUM = {'canonical', 'derived', 'synchronized', 'none'}

# F21 — invariant I2 (parameterized runtime) enforcement for protocol files.
# Rule: protocols must not hardcode vault-specific paths/slugs. `agensy/...`
# references are allowed (the framework is structurally located there); `synthesis_<vault>`
# references are forbidden (vault-specific identity must flow through vault-config.md).
#
# Forbidden pattern — any reference to a vault-specific namespace:
F6_VAULT_SLUG_RE = re.compile(r'\bsynthesis_([a-z][a-z0-9_]*)\b')
# Absolute Windows path detector (only matched to scope where forbidden slugs might appear):
F6_ABSOLUTE_PATH_RE = re.compile(r'[A-Za-z]:[\\/][^\s\)`"\']*')


def parse_frontmatter(file_path: Path) -> dict | None:
    """Minimal YAML-frontmatter parser (regex-based, no yaml lib dependency).

    Returns a dict of {field: value} where value is str, list[str], or None.
    Returns None if no frontmatter is found.
    Handles simple `key: value` and `key: [a, b, c]` forms plus indented list continuations.
    """
    try:
        # Use utf-8-sig to strip BOM if present (agensy files carry one)
        text = file_path.read_text(encoding='utf-8-sig', errors='ignore')
    except (OSError, IOError):
        return None

    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', text, re.DOTALL)
    if not m:
        return None

    fm_text = m.group(1)
    result = {}
    current_key = None

    for line in fm_text.splitlines():
        # Inline list: `key: [a, b, c]`
        m_inline = re.match(r'^([A-Za-z_][\w_]*)\s*:\s*\[(.*)\]\s*$', line)
        if m_inline:
            key = m_inline.group(1)
            items = [s.strip().strip('"\'') for s in m_inline.group(2).split(',') if s.strip()]
            result[key] = items
            current_key = None
            continue
        # Scalar: `key: value`
        m_scalar = re.match(r'^([A-Za-z_][\w_]*)\s*:\s*(.*?)\s*$', line)
        if m_scalar and not line.startswith(' ') and not line.startswith('\t'):
            key, value = m_scalar.group(1), m_scalar.group(2)
            value = value.strip().strip('"\'')
            if value == '':
                # Empty scalar — may be followed by a list block
                result[key] = []
                current_key = key
            else:
                result[key] = value
                current_key = None
            continue
        # List continuation: `  - item`
        m_item = re.match(r'^\s+-\s+(.+?)\s*$', line)
        if m_item and current_key is not None:
            item = m_item.group(1).strip().strip('"\'')
            if not isinstance(result.get(current_key), list):
                result[current_key] = []
            result[current_key].append(item)
            continue

    return result


def iter_framework_docs(meta_root: Path):
    """Yield (rel_path, Path) for every .md file under framework/ plus top-level CLAUDE.md."""
    framework_dir = meta_root / 'framework'
    if framework_dir.exists():
        for p in sorted(framework_dir.rglob('*.md')):
            yield p.relative_to(meta_root).as_posix(), p
    claude_md = meta_root / 'CLAUDE.md'
    if claude_md.exists():
        yield 'CLAUDE.md', claude_md


def check_f18_frontmatter_schema(meta_root: Path) -> list[Result]:
    """F18: framework docs carry valid frontmatter per meta-architecture §11.

    FAIL on invalid enum values or missing required-by-state fields
    (e.g., canonicity=canonical without canonical_for).
    WARN on missing new fields (stability_tier, canonicity) in existing docs —
    backward-compat: retrofit is opportunistic, not forced.
    """
    results = []
    for rel, path in iter_framework_docs(meta_root):
        fm = parse_frontmatter(path)
        if fm is None:
            results.append(warn('F18', f'{rel}: no frontmatter block'))
            continue

        # type (always required per existing convention, now enum-enforced)
        t = fm.get('type')
        if t is None:
            results.append(warn('F18', f'{rel}: missing type field'))
        elif t not in F6_TYPE_ENUM:
            results.append(fail('F18', f'{rel}: type "{t}" not in allowed enum',
                                f'Allowed: {sorted(F6_TYPE_CANONICAL)} (+ legacy aliases: {sorted(F6_TYPE_ALIASES.keys())})'))

        # Resolve legacy alias to canonical for downstream checks
        canonical_type = F6_TYPE_ALIASES.get(t, t)

        # stability_tier (WARN on absent, FAIL on invalid)
        st = fm.get('stability_tier')
        if st is None:
            results.append(warn('F18', f'{rel}: missing stability_tier (retrofit pending)'))
        elif st not in F6_STABILITY_ENUM:
            results.append(fail('F18', f'{rel}: stability_tier "{st}" not in allowed enum',
                                f'Allowed: {sorted(F6_STABILITY_ENUM)}'))

        # canonicity (WARN on absent, FAIL on invalid)
        c = fm.get('canonicity')
        if c is None:
            results.append(warn('F18', f'{rel}: missing canonicity (retrofit pending)'))
        elif c not in F6_CANONICITY_ENUM:
            results.append(fail('F18', f'{rel}: canonicity "{c}" not in allowed enum',
                                f'Allowed: {sorted(F6_CANONICITY_ENUM)}'))

        # canonical_for required when canonicity=canonical
        if c == 'canonical':
            cf = fm.get('canonical_for')
            if not cf or not isinstance(cf, list) or len(cf) == 0:
                results.append(fail('F18', f'{rel}: canonicity=canonical but canonical_for is empty/missing'))

        # derives_from required when canonicity=derived
        if c == 'derived':
            df = fm.get('derives_from')
            if not df or not isinstance(df, list) or len(df) == 0:
                results.append(fail('F18', f'{rel}: canonicity=derived but derives_from is empty/missing'))

        # synchronized_with required when canonicity=synchronized
        if c == 'synchronized':
            sw = fm.get('synchronized_with')
            if not sw or not isinstance(sw, list) or len(sw) == 0:
                results.append(fail('F18', f'{rel}: canonicity=synchronized but synchronized_with is empty/missing'))

        # supersedes only allowed on decision_record or experiment_log (alias-aware)
        if fm.get('supersedes') and canonical_type not in ('decision_record', 'experiment_log'):
            results.append(fail('F18', f'{rel}: supersedes field only permitted on decision_record/experiment_log',
                                f'This doc has type={t} (canonical: {canonical_type})'))

    if not any(r.status == 'FAIL' for r in results):
        # Emit one summary pass if no hard failures
        n_docs = sum(1 for _ in iter_framework_docs(meta_root))
        results.append(ok('F18', f'frontmatter schema: {n_docs} framework docs scanned, 0 enum violations'))

    return results


def check_f19_canonicity_uniqueness(meta_root: Path) -> list[Result]:
    """F19: every canonical_for concern is claimed by at most one doc.

    Builds a {concern → [docs]} map from every `canonical_for` list.
    FAIL on concerns claimed by >1 doc.
    """
    claims: dict[str, list[str]] = {}
    for rel, path in iter_framework_docs(meta_root):
        fm = parse_frontmatter(path)
        if fm is None:
            continue
        cf = fm.get('canonical_for')
        if not isinstance(cf, list):
            continue
        for concern in cf:
            claims.setdefault(concern, []).append(rel)

    results = []
    conflicts = {c: docs for c, docs in claims.items() if len(docs) > 1}
    if conflicts:
        for concern, docs in conflicts.items():
            results.append(fail('F19', f'concern "{concern}" claimed by {len(docs)} docs',
                                f'Docs: {docs}'))
    else:
        results.append(ok('F19', f'canonicity uniqueness: {len(claims)} distinct concerns, no conflicts'))
    return results


def f20_fact_match_command_inventory(meta_root: Path) -> tuple[bool, str]:
    """F20 callback: check that system-contracts §2 command list matches system-architecture YAML manifest command list.

    Returns (ok, detail_message).
    """
    sc_path = meta_root / 'framework' / 'principles' / 'system-contracts.md'
    sa_path = meta_root / 'framework' / 'principles' / 'system-architecture.md'
    if not sc_path.exists() or not sa_path.exists():
        return True, 'skipped — one or both files missing'

    sc_text = sc_path.read_text(encoding='utf-8', errors='ignore')
    sa_text = sa_path.read_text(encoding='utf-8', errors='ignore')

    # Extract commands from system-contracts §2 table (pattern: `| /command` or `| `/command`)
    sc_cmds = set(re.findall(r'\|\s*`/([a-z][\w-]*)`', sc_text))
    # Extract commands from system-architecture YAML manifest — slice the commands: section
    # then collect every 2-space-indented `<name>:` command key.
    sa_cmds: set[str] = set()
    sa_start = sa_text.find('\ncommands:\n')
    if sa_start >= 0:
        # Commands section runs until next top-level (no-indent) key like `state_files:`
        sa_end_m = re.search(r'\n([a-z_][\w_]*):\s*\n', sa_text[sa_start + 11:])
        sa_section = sa_text[sa_start:sa_start + 11 + (sa_end_m.start() if sa_end_m else len(sa_text))]
        sa_cmds = set(re.findall(r'^  ([a-z][\w-]+):\s*$', sa_section, re.MULTILINE))

    only_in_sc = sc_cmds - sa_cmds
    only_in_sa = sa_cmds - sc_cmds
    if only_in_sc or only_in_sa:
        parts = []
        if only_in_sc:
            parts.append(f'in contracts but not architecture manifest: {sorted(only_in_sc)}')
        if only_in_sa:
            parts.append(f'in architecture manifest but not contracts: {sorted(only_in_sa)}')
        return False, '; '.join(parts)
    return True, f'{len(sc_cmds)} commands match between contracts §2 and architecture manifest'


# F20 fact-match callback registry: {(pathA, pathB) → callback(meta_root) → (ok, detail)}
# Callbacks are symmetrical — registered once for any declared synchronized_with pair.
F6_FACT_MATCH_CALLBACKS = {
    frozenset({'framework/principles/system-contracts.md', 'framework/principles/system-architecture.md'}):
        f20_fact_match_command_inventory,
}


def check_f20_synchronized_with(meta_root: Path) -> list[Result]:
    """F20: synchronized_with symmetry + concern-specific fact-match callbacks.

    (a) Symmetry — if A.synchronized_with contains B, then B.synchronized_with must contain A.
        Exception: WARN (not FAIL) when B has no frontmatter yet — retrofit pending.
    (b) Fact-match — registered callbacks verify the synchronized fact actually matches.
    """
    results = []

    # Build sync graph from frontmatter
    sync_graph: dict[str, set[str]] = {}
    frontmatters: dict[str, dict] = {}
    for rel, path in iter_framework_docs(meta_root):
        fm = parse_frontmatter(path)
        if fm is None:
            continue
        frontmatters[rel] = fm
        sw = fm.get('synchronized_with')
        if isinstance(sw, list) and sw:
            sync_graph[rel] = set(sw)

    # (a) Symmetry check
    for a, peers in sync_graph.items():
        for b in peers:
            b_norm = b.lstrip('./')
            if b_norm not in frontmatters:
                # Peer has no frontmatter — retrofit pending
                results.append(warn('F20', f'{a} synchronized_with {b_norm}, but peer has no frontmatter (retrofit pending)'))
                continue
            peer_sw = frontmatters[b_norm].get('synchronized_with')
            if not isinstance(peer_sw, list) or a not in [p.lstrip('./') for p in peer_sw]:
                results.append(fail('F20', f'{a} synchronized_with {b_norm}, but {b_norm} does not reciprocate',
                                    f'{b_norm} synchronized_with = {peer_sw}'))

    # (b) Fact-match callbacks
    for a, peers in sync_graph.items():
        for b in peers:
            b_norm = b.lstrip('./')
            pair = frozenset({a, b_norm})
            callback = F6_FACT_MATCH_CALLBACKS.get(pair)
            if callback is None:
                continue
            ok_flag, detail = callback(meta_root)
            if not ok_flag:
                results.append(fail('F20', f'fact-match {a} ↔ {b_norm}: {detail}'))
            else:
                results.append(ok('F20', f'fact-match {a} ↔ {b_norm}: {detail}'))

    if not results:
        results.append(ok('F20', 'no synchronized_with declarations yet (retrofit pending)'))
    elif not any(r.status in ('FAIL', 'WARN') for r in results):
        # At least one pair passed; silent on symmetry unless fail
        pass  # the fact-match OK lines already report

    return results


def check_f21_protocol_path_discipline(meta_root: Path) -> list[Result]:
    """F21: type: protocol docs contain no vault-specific bare references.

    Enforces invariant I2 (parameterized runtime): protocols must not hardcode
    vault-specific paths or slugs. References to `agensy/...` are allowed
    (framework-level). References to `synthesis_<vault>` patterns are flagged:
      - Bare prose references (outside backticks) → FAIL  (clear hardcoding)
      - Backtick-wrapped references             → WARN  (examples/templates;
        still discouraged but a softer signal because Claude reads backticks
        as formatting, not as hardcoded runtime values)
    """
    results = []
    proto_dir = meta_root / 'framework' / 'universal-commands'
    if not proto_dir.exists():
        return [fail('F21', f'universal-commands/ not found under {meta_root}')]

    hard_violations = []   # bare prose → FAIL
    soft_violations = []   # in backticks, wikilinks, or code fences → WARN
    files_scanned = 0

    def _slug_is_in_code_span(line: str, pos: int) -> bool:
        """True if position `pos` is inside a backtick-span or double-bracket wikilink on this line."""
        prefix = line[:pos]
        # Backtick span: odd count of ` before pos.
        if prefix.count('`') % 2 == 1:
            return True
        # Wikilink: `[[` before pos and `]]` after pos on same line.
        if '[[' in prefix:
            last_open = prefix.rfind('[[')
            last_close = prefix.rfind(']]')
            if last_close < last_open and ']]' in line[pos:]:
                return True
        return False

    for path in sorted(proto_dir.glob('*.md')):
        files_scanned += 1
        try:
            lines = path.read_text(encoding='utf-8', errors='ignore').splitlines()
        except (OSError, IOError):
            continue
        in_code_fence = False
        for i, line in enumerate(lines, start=1):
            # Track triple-backtick code fences
            if line.lstrip().startswith('```'):
                in_code_fence = not in_code_fence
                continue
            for m in F6_VAULT_SLUG_RE.finditer(line):
                slug = m.group(1)
                snippet = f'{path.name}:{i}  synthesis_{slug}  — {line.strip()[:80]}'
                if in_code_fence or _slug_is_in_code_span(line, m.start()):
                    soft_violations.append(snippet)
                else:
                    hard_violations.append(snippet)

    if hard_violations:
        results.append(fail('F21', f'{len(hard_violations)} bare vault-specific reference(s) in protocol files',
                            '\n         '.join(hard_violations[:10]) +
                            (f'\n         ... (+{len(hard_violations)-10} more)' if len(hard_violations) > 10 else '')))
    if soft_violations:
        results.append(warn('F21', f'{len(soft_violations)} backtick-wrapped vault reference(s) — examples/defaults; parameterize where possible',
                            '\n         '.join(soft_violations[:5]) +
                            (f'\n         ... (+{len(soft_violations)-5} more)' if len(soft_violations) > 5 else '')))
    if not hard_violations and not soft_violations:
        results.append(ok('F21', f'protocol path discipline: {files_scanned} files scanned, 0 vault-specific references'))
    elif not hard_violations:
        results.append(ok('F21', f'protocol path discipline: {files_scanned} files scanned, 0 hard violations ({len(soft_violations)} soft — see WARN)'))
    return results


def check_f22_supersession_chain(meta_root: Path) -> list[Result]:
    """F22: every `supersedes:` pointer in a decision_record/experiment_log resolves, same type, older date, no cycles."""
    results = []

    # Build the supersession graph: {child_rel → parent_rel}
    supersedes: dict[str, str] = {}
    frontmatters: dict[str, dict] = {}
    for rel, path in iter_framework_docs(meta_root):
        fm = parse_frontmatter(path)
        if fm is None:
            continue
        frontmatters[rel] = fm
        s = fm.get('supersedes')
        if s:
            s_norm = s.lstrip('./') if isinstance(s, str) else None
            if s_norm:
                supersedes[rel] = s_norm

    if not supersedes:
        return [ok('F22', 'no supersession pointers declared (no chains to validate)')]

    # (1) Pointer resolution + type match + date ordering
    for child, parent in supersedes.items():
        parent_path = meta_root / parent
        if not parent_path.exists():
            results.append(fail('F22', f'{child} supersedes missing file {parent}'))
            continue
        child_fm = frontmatters.get(child, {})
        parent_fm = frontmatters.get(parent, {})
        # Type match (alias-aware — canonical form)
        child_t = F6_TYPE_ALIASES.get(child_fm.get('type'), child_fm.get('type'))
        parent_t = F6_TYPE_ALIASES.get(parent_fm.get('type'), parent_fm.get('type'))
        if child_t != parent_t:
            results.append(fail('F22', f'{child} supersedes {parent} but canonical types differ',
                                f'child={child_t}, parent={parent_t}'))
        # Date ordering
        child_date = child_fm.get('created', '')
        parent_date = parent_fm.get('created', '')
        if child_date and parent_date and child_date <= parent_date:
            results.append(fail('F22', f'{child} supersedes {parent} but child created ({child_date}) not newer than parent ({parent_date})'))

    # (2) Cycle detection via DFS
    def find_cycle() -> list[str] | None:
        visited: set[str] = set()
        for start in supersedes.keys():
            path = []
            node = start
            local_seen = set()
            while node in supersedes:
                if node in local_seen:
                    # Found a cycle
                    idx = path.index(node)
                    return path[idx:] + [node]
                local_seen.add(node)
                path.append(node)
                if node in visited:
                    break  # already traced, no cycle through here
                node = supersedes[node]
            visited.update(local_seen)
        return None

    cycle = find_cycle()
    if cycle:
        results.append(fail('F22', f'supersession cycle detected: {" → ".join(cycle)}'))

    if not any(r.status == 'FAIL' for r in results):
        results.append(ok('F22', f'supersession chains: {len(supersedes)} pointer(s) validated, no cycles'))

    return results


# ─────────────────────────────────────────────────────────────────────────────
# RUNNER & OUTPUT
# ─────────────────────────────────────────────────────────────────────────────

def run_checks(vaults: list, meta_root: Path, category: str, single_check: str | None) -> list[Result]:
    results = []
    check_filter = single_check.upper() if single_check else None

    def maybe(code_prefix: str, fn):
        """Run fn() if category matches and code prefix matches filter."""
        if check_filter and not check_filter.startswith(code_prefix[:3]):
            return
        results.extend(fn())

    if category in ('F1', 'all'):
        maybe('F01', lambda: check_f01_vault_configs_exist(vaults))
        maybe('F02', lambda: check_f02_required_blocks(vaults))
        maybe('F03', lambda: check_f03_positions_nonempty(vaults))
        maybe('F04', lambda: check_f04_open_problems_complete(vaults))
        maybe('F05', lambda: check_f05_domains_complete(vaults))

    if category in ('F2', 'all'):
        maybe('F06', lambda: check_f06_global_claude_budget())
        maybe('F07', lambda: check_f07_vault_claude_budget(vaults))
        maybe('F08', lambda: check_f08_memory_budget(vaults))

    if category in ('F3', 'all'):
        maybe('F09', lambda: check_f09_stubs_reference_existing_protocols(vaults, meta_root))
        maybe('F10', lambda: check_f10_all_protocols_have_stubs(vaults, meta_root))
        maybe('F11', lambda: check_f11_stubs_not_bloated(vaults))

    if category in ('F4', 'all'):
        maybe('F12', lambda: check_f12_reference_docs_resolve(vaults))
        maybe('F13', lambda: check_f13_folder_structure_exists(vaults))
        maybe('F14', lambda: check_f14_maps_folder_exists(vaults))

    if category in ('F5', 'all'):
        maybe('F15', lambda: check_f15_contract_table_complete(meta_root))
        maybe('F16', lambda: check_f16_schema_mentions_blocks(meta_root))
        maybe('F17', lambda: check_f17_genesis_doc_count(meta_root))

    if category in ('F6', 'all'):
        maybe('F18', lambda: check_f18_frontmatter_schema(meta_root))
        maybe('F19', lambda: check_f19_canonicity_uniqueness(meta_root))
        maybe('F20', lambda: check_f20_synchronized_with(meta_root))
        maybe('F21', lambda: check_f21_protocol_path_discipline(meta_root))
        maybe('F22', lambda: check_f22_supersession_chain(meta_root))

    # If single check requested, filter results
    if check_filter:
        results = [r for r in results if r.code == check_filter]

    return results


def human_report(results: list[Result], verbose: bool):
    fails = [r for r in results if r.status == 'FAIL']
    warns = [r for r in results if r.status == 'WARN']
    passes = [r for r in results if r.status == 'PASS']
    skips = [r for r in results if r.status == 'SKIP']

    print(f'\nframework-verify — {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print(f'  Checks: {len(results)} | FAIL: {len(fails)} | WARN: {len(warns)} | PASS: {len(passes)} | SKIP: {len(skips)}')
    print()

    if fails:
        print('── FAILURES ──────────────────────────────────────────')
        for r in fails:
            print(f'  {r}')
        print()

    if warns:
        print('── WARNINGS ──────────────────────────────────────────')
        for r in warns:
            print(f'  {r}')
        print()

    if verbose and passes:
        print('── PASSING ───────────────────────────────────────────')
        for r in passes:
            print(f'  {r}')
        print()

    if verbose and skips:
        print('── SKIPPED ───────────────────────────────────────────')
        for r in skips:
            print(f'  {r}')
        print()

    status = 'OK' if not fails else 'FAILURES FOUND'
    print(f'── {status} {"─" * (50 - len(status))}')


def main():
    parser = argparse.ArgumentParser(
        description='framework-verify.py — architectural integrity checks for agensy'
    )
    parser.add_argument('--category', default='all',
                        choices=['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'all'],
                        help='Which category of checks to run (default: all)')
    parser.add_argument('--json', action='store_true',
                        help='Output JSON format')
    parser.add_argument('--verbose', action='store_true',
                        help='Show passing checks (default: failures and warnings only)')
    parser.add_argument('--check', metavar='F01',
                        help='Run only a specific check code')
    args = parser.parse_args()

    meta_root = find_meta_root()
    vaults = discover_vaults(meta_root)

    if not vaults:
        print('ERROR: No vaults found. Check vault-registry.md in agensy root.')
        sys.exit(1)

    results = run_checks(vaults, meta_root, args.category, args.check)

    if args.json:
        out = {
            'scanned_at': datetime.now().isoformat(),
            'meta_root': str(meta_root),
            'vault_count': len(vaults),
            'results': [r.to_dict() for r in results],
            'summary': {
                'total': len(results),
                'fail': sum(1 for r in results if r.status == 'FAIL'),
                'warn': sum(1 for r in results if r.status == 'WARN'),
                'pass': sum(1 for r in results if r.status == 'PASS'),
                'skip': sum(1 for r in results if r.status == 'SKIP'),
            }
        }
        print(json.dumps(out, indent=2))
    else:
        human_report(results, verbose=args.verbose)

    # Exit 1 if any failures
    if any(r.status == 'FAIL' for r in results):
        sys.exit(1)


if __name__ == '__main__':
    main()
