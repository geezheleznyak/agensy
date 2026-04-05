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
    'promote': [
        'note_tiers', 'note_template', 'intellectual_style', 'folder_structure',
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
        """Extract engagement_axis position names."""
        m = re.search(r'\n  positions:\n((?:    - [\w][\w-]*:.*\n)+)', self.text)
        if m:
            return re.findall(r'    - ([\w][\w-]*):', m.group(1))
        # Backward compat: fault_line positions
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
    sc_path = meta_root / 'framework' / 'system-contracts.md'
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
    schema_path = meta_root / 'framework' / 'vault-config-schema.md'
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
    """F17: genesis-protocol.md Phase 1 lists exactly 12 Doc entries."""
    genesis_path = meta_root / 'framework' / 'genesis-protocol.md'
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
    if count == 12:
        return [ok('F17', f'genesis-protocol.md Phase 1 has exactly 12 Doc entries')]
    return [fail('F17', f'genesis-protocol.md Phase 1 has {count} Doc entries (expected 12)',
                 f'Found: {doc_headers}')]


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
                        choices=['F1', 'F2', 'F3', 'F4', 'F5', 'all'],
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
