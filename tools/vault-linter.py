#!/usr/bin/env python3
"""
vault-linter.py — Mechanical validation for synthesis vault notes.

Tests Claude's compliance with vault-config.md schema. Catches the
structural failures that convention-based enforcement misses.

Usage:
    python vault-linter.py <vault-path> [options]

Options:
    --category note|vault|graph|all  Which checks to run (default: all)
    --json                           Output JSON format
    --recent N                       Only check the N most recently modified notes
    --verbose                        Show passing checks (default: failures only)
    --baseline save|compare          Save or compare against regression baseline
    --check A01                      Run only a specific check code
"""

import io
import os
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Force UTF-8 output on Windows terminals
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# ─────────────────────────────────────────────────────────────
# VAULT CONFIG PARSER
# ─────────────────────────────────────────────────────────────

class VaultConfig:
    """Parses vault-config.md and exposes schema requirements."""

    def __init__(self, vault_root: Path):
        self.vault_root = vault_root
        config_path = vault_root / "vault-config.md"
        if not config_path.exists():
            raise FileNotFoundError(f"vault-config.md not found at {config_path}")
        self.text = config_path.read_text(encoding='utf-8')

        # Vault identity
        self.name = self._scalar(r'^  name:\s+(\S+)', 'unknown')
        self.vault_type = self._scalar(r'^  type:\s+(\S+)', 'accumulation')
        self.is_training = (self.vault_type == 'training')

        # Schema elements
        self.fault_line_positions = self._fault_line_positions()
        self.open_problem_ids = self._open_problem_ids()
        self.open_problem_key = self._open_problem_key()

        # Tier type values
        self.tier1_type = self._tier_value('tier1')
        self.tier2_type = self._tier_value('tier2')
        self.tier3_type = self._tier_value('tier3')
        self.tier3_output = self._output_folder()

        # Domains
        self.domains = self._domains()
        self.domain_by_slug = {d['slug']: d for d in self.domains}
        self.is_flat_folder = self._detect_flat_folder()

        # Folder structure
        self.folders = self._folder_structure()

        # Note templates
        self.synthesis_sections = self._mandatory_sections('synthesis')
        self.synthesis_checkable = self._extract_checkable_headers(self.synthesis_sections)
        self.synthesis_additional_fm = self._additional_frontmatter()
        self.reference_sections = self._mandatory_sections('reference')
        self.reference_excluded = self._excluded_sections()

        # Judgment instrument
        self.ji_section_name = self._ji_section_name()
        self.ji_subfields = self._ji_subfields()

        # Cross-domain requirement
        self.cross_domain_required = bool(
            re.search(r'[≥>=]1 cross.domain|cross.domain.*required', self.text, re.IGNORECASE)
        ) and not self.is_training

        # Excluded paths for discovery
        self.excluded_dirs = self._build_excluded_dirs()
        self.reference_doc_files = self._reference_doc_files()

    # ── Private extraction helpers ──────────────────────────

    def _scalar(self, pattern: str, default: str) -> str:
        m = re.search(pattern, self.text, re.MULTILINE)
        return m.group(1).strip('"\'') if m else default

    def _fault_line_positions(self) -> list:
        """Extract position names from fault_line.positions block."""
        # Find positions: block — items are "    - positionname: >"
        m = re.search(r'\n  positions:\n((?:    - [\w][\w-]*:.*\n(?:        .*\n)*)+)', self.text)
        if m:
            return re.findall(r'    - ([\w][\w-]*):', m.group(1))
        return []

    def _open_problem_ids(self) -> set:
        return set(int(x) for x in re.findall(r'^\s*- id:\s*(\d+)', self.text, re.MULTILINE))

    def _open_problem_key(self) -> str:
        """belli uses open_challenges; others use open_problems."""
        if re.search(r'open_challenges', self.text):
            return 'open_challenges'
        return 'open_problems'

    def _tier_value(self, tier: str) -> str:
        m = re.search(rf'  {tier}:\n(?:(?!  \w).)*?    type_value:\s*(\S+)', self.text, re.DOTALL)
        return m.group(1) if m else ''

    def _output_folder(self) -> str:
        m = re.search(r'output_folder:\s*"([^"]+)"', self.text)
        return m.group(1) if m else ''

    def _domains(self) -> list:
        """Extract domain entries from the domains: block."""
        domains_m = re.search(r'^domains:\n((?:  - [\s\S]*?)(?=\n\w|\Z))', self.text, re.MULTILINE)
        if not domains_m:
            return []
        block = domains_m.group(1)
        entries = re.split(r'(?=  - slug:)', block)
        domains = []
        for entry in entries:
            if not entry.strip():
                continue
            slug_m = re.search(r'  - slug:\s*(\S+)', entry)
            folder_m = re.search(r'    folder:\s*"([^"]+)"', entry)
            ec_m = re.search(r'    evergreen_candidate:\s*(\S+)', entry)
            priority_m = re.search(r'    priority:\s*(\S+)', entry)
            if slug_m and folder_m:
                domains.append({
                    'slug': slug_m.group(1),
                    'folder': folder_m.group(1),
                    'evergreen_candidate': ec_m.group(1) if ec_m else 'true',
                    'priority': priority_m.group(1) if priority_m else 'tier1',
                })
        return domains

    def _detect_flat_folder(self) -> bool:
        """True if multiple domains share the same folder (belli pattern)."""
        folders = [d['folder'] for d in self.domains]
        return len(folders) != len(set(folders))

    def _folder_structure(self) -> dict:
        folders = {}
        fs_m = re.search(r'^folder_structure:\n((?:  \w.*\n)+)', self.text, re.MULTILINE)
        if fs_m:
            for line in fs_m.group(1).splitlines():
                m = re.match(r'  (\w+):\s*"([^"]+)"', line)
                if m:
                    folders[m.group(1)] = m.group(2)
        return folders

    def _get_schema_block(self, schema: str) -> str:
        """Extract the text block for synthesis: or reference: under note_template:."""
        note_template_m = re.search(r'^note_template:\n((?:  [\s\S]*?)(?=\n\w|\Z))', self.text, re.MULTILINE)
        if not note_template_m:
            return ''
        nt_block = note_template_m.group(1)
        # Find synthesis: or reference: within note_template block
        schema_m = re.search(rf'  {schema}:\n((?:    [\s\S]*?)(?=\n  \w|\Z))', nt_block)
        if schema_m:
            return schema_m.group(1)
        return ''

    def _mandatory_sections(self, schema: str) -> list:
        block = self._get_schema_block(schema)
        if not block:
            return []
        ms_m = re.search(r'    mandatory_sections:\n((?:      - .*\n)+)', block)
        if not ms_m:
            return []
        sections = []
        for line in ms_m.group(1).splitlines():
            m = re.match(r'      - "?(.*?)"?\s*$', line)
            if m:
                val = m.group(1).strip().rstrip('"')
                if val:
                    sections.append(val)
        return sections

    def _extract_checkable_headers(self, sections: list) -> list:
        """From mandatory_sections strings, extract those with ## headers."""
        headers = []
        for s in sections:
            if not s.startswith('##'):
                continue
            # Strip the ## prefix
            header_text = re.sub(r'^#+\s*', '', s)
            # Take text up to first (, →, or : (but not inside a word)
            core = re.split(r'\s*[\(→]|\s*—', header_text)[0].strip()
            # Handle "Header: description" — take up to the colon
            # Use r':\s+' not r':\s+\w' — description may start with non-word chars (e.g. ≥)
            core = re.split(r':\s+', core)[0].strip()
            if core:
                headers.append(core)
        return headers

    def _additional_frontmatter(self) -> list:
        """Extract field names from synthesis additional_frontmatter."""
        block = self._get_schema_block('synthesis')
        if not block:
            return []
        fm_m = re.search(r'    additional_frontmatter:\n((?:      - .*\n)+)', block)
        if not fm_m:
            return []
        field_names = []
        for line in fm_m.group(1).splitlines():
            m = re.match(r'      - "?([\w-]+):', line)
            if m:
                field_names.append(m.group(1))
        return field_names

    def _excluded_sections(self) -> list:
        block = self._get_schema_block('reference')
        if not block:
            return []
        ex_m = re.search(r'    excluded_sections:\n((?:      - .*\n)+)', block)
        if not ex_m:
            return []
        sections = []
        for line in ex_m.group(1).splitlines():
            m = re.match(r'      - "?(.*?)"?\s*$', line)
            if m and m.group(1).strip():
                sections.append(m.group(1).strip().rstrip('"'))
        return sections

    def _ji_section_name(self) -> str:
        if re.search(r'Judgment Instrument', self.text):
            return 'Judgment Instrument'
        return 'Connection to the Project'

    def _ji_subfields(self) -> list:
        """Extract bold sub-field names from judgment_instrument_template."""
        ji_m = re.search(r'judgment_instrument_template:\s*[|>]?\n((?:\s{6}.*\n)+)', self.text)
        if ji_m:
            fields = re.findall(r'\*\*([^*]+)\*\*', ji_m.group(1))
            if fields:
                return fields
        # Fallback: detect from synthesis sections text
        if self.ji_section_name == 'Judgment Instrument':
            # Check if it mentions "Reads as" (kratos)
            if re.search(r'Reads as', self.text):
                return ['Reads as', 'Threatens', 'Fault line']
            # oikos has Primary insight
            if re.search(r'Primary insight', self.text):
                return ['Primary insight', 'Gives', 'Threatens', 'Fault line']
        return ['Gives', 'Threatens', 'Fault line']

    def _build_excluded_dirs(self) -> set:
        excluded = {'.obsidian', '.claude', 'node_modules', '.git'}
        # Exclude infrastructure folders: templates, MOCs, memory, inbox, sources
        skip_keys = ['templates', 'mocs', 'memory', 'inbox', 'sources', 'curriculum']
        # Also exclude any key containing "source" (covers sources_doctrine, sources_history, etc.)
        for key, val in self.folders.items():
            if any(k in key for k in skip_keys) or key.startswith('sources'):
                if val:
                    # Only exclude top-level dir name (first path component)
                    top = val.strip('/\\').split('/')[0].split('\\')[0]
                    excluded.add(top)
                    excluded.add(val.rstrip('/\\'))
        return excluded

    def _reference_doc_files(self) -> set:
        """Extract filenames from reference_docs block."""
        files = set()
        rd_m = re.search(r'^reference_docs:\n((?:  \w.*\n)+)', self.text, re.MULTILINE)
        if rd_m:
            for line in rd_m.group(1).splitlines():
                m = re.match(r'  \w+:\s*"([^"]+)"', line)
                if m:
                    # Only filename, not directory paths
                    val = m.group(1).rstrip('/')
                    if '/' not in val:
                        files.add(val)
        return files


# ─────────────────────────────────────────────────────────────
# NOTE DISCOVERY
# ─────────────────────────────────────────────────────────────

MAP_SUFFIXES = ('-map.md', '-systematic-map.md', '-concept-map.md', '-framework-map.md')
INFRA_PATTERNS = [
    r'-coverage-plan\.md$', r'-development-plan\.md$', r'-map-reference\.md$',
    r'-note-taxonomy\.md$', r'-analytical-standard\.md$', r'-primer-reference\.md$',
    r'^MEMORY\.md$', r'^README\.md$', r'^vault-registry\.md$', r'^open-problems.*\.md$',
    r'^open-challenges.*\.md$', r'^primer-', r'-systematic-map\.md$',
]


def is_infrastructure(path: Path, config: VaultConfig) -> bool:
    name = path.name
    if name in ('vault-config.md', 'CLAUDE.md'):
        return True
    if name in config.reference_doc_files:
        return True
    if any(name.endswith(s) for s in MAP_SUFFIXES):
        return True
    if any(re.search(p, name, re.IGNORECASE) for p in INFRA_PATTERNS):
        return True
    return False


def should_skip_dir(name: str, config: VaultConfig) -> bool:
    if name.startswith('.'):
        return True
    if name in config.excluded_dirs:
        return True
    if name == '_maps':  # map folders (all vaults)
        return True
    return False


def discover_notes(vault_root: Path, config: VaultConfig, recent_n: int = None) -> list:
    notes = []

    for root, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in dirs if not should_skip_dir(d, config)]
        root_path = Path(root)

        for fname in files:
            if not fname.endswith('.md'):
                continue
            fpath = root_path / fname
            if is_infrastructure(fpath, config):
                continue
            notes.append(fpath)

    # Sort by modification time descending, then take the N most recent if requested
    notes_by_mtime = sorted(notes, key=lambda p: p.stat().st_mtime, reverse=True)
    if recent_n:
        notes_by_mtime = notes_by_mtime[:recent_n]

    return sorted(notes_by_mtime)


# ─────────────────────────────────────────────────────────────
# FRONTMATTER + NOTE PARSING
# ─────────────────────────────────────────────────────────────

def parse_frontmatter(content: str) -> dict:
    fm = {}
    if not content.startswith('---'):
        return fm
    end = content.find('\n---', 3)
    if end == -1:
        return fm
    for line in content[3:end].splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        # List value: key: [a, b, c]
        lm = re.match(r'^([\w-]+):\s*\[([^\]]*)\]', line)
        if lm:
            items = [x.strip().strip('"\'') for x in lm.group(2).split(',') if x.strip()]
            fm[lm.group(1)] = items
            continue
        # Scalar value
        sm = re.match(r'^([\w-]+):\s*(.+)', line)
        if sm:
            val = sm.group(2).strip().strip('"\'')
            val = re.sub(r'\s*#.*$', '', val).strip()
            fm[sm.group(1)] = val
            continue
        # Key with no value
        km = re.match(r'^([\w-]+):\s*$', line)
        if km:
            fm[km.group(1)] = None
    return fm


def has_valid_frontmatter(content: str) -> bool:
    return bool(re.match(r'^---\n', content)) and '\n---' in content[3:]


def get_body(content: str) -> str:
    """Return note body (after frontmatter)."""
    end = content.find('\n---', 3)
    return content[end + 4:] if end > 0 else content


def get_wikilinks(text: str) -> list:
    return re.findall(r'\[\[([^\]|#]+)[^\]]*\]\]', text)


def get_section(content: str, header: str) -> str:
    """Extract content of a ## section."""
    pattern = re.compile(r'^## ' + re.escape(header) + r'[^\n]*\n(.*?)(?=\n## |\Z)',
                         re.MULTILINE | re.DOTALL | re.IGNORECASE)
    m = pattern.search(content)
    return m.group(1) if m else ''


def section_exists(content: str, header_core: str) -> bool:
    """Check if a ## section exists (fuzzy match on core header text)."""
    return bool(re.search(r'^##\s+' + re.escape(header_core), content,
                          re.MULTILINE | re.IGNORECASE))


# ─────────────────────────────────────────────────────────────
# NOTE CLASSIFICATION
# ─────────────────────────────────────────────────────────────

def classify_note(path: Path, fm: dict, config: VaultConfig) -> dict:
    note_type = fm.get('type', '').strip('"\'')
    rel = str(path.relative_to(config.vault_root)).replace('\\', '/')

    # Tier
    tier = 'tier2'
    if note_type == config.tier3_type:
        tier = 'tier3'
    elif note_type == config.tier1_type:
        tier = 'tier1'
    elif config.tier3_output and rel.startswith(config.tier3_output.lstrip('/')):
        tier = 'tier3'

    # Schema
    if config.is_training:
        schema = 'synthesis'
    else:
        ec = str(fm.get('evergreen-candidate', '')).lower()
        if ec == 'true':
            schema = 'synthesis'
        elif ec == 'false':
            schema = 'reference'
        else:
            # Use domain default
            domain_slug = fm.get('domain', '')
            domain = config.domain_by_slug.get(domain_slug)
            default = domain.get('evergreen_candidate', 'true').lower() if domain else 'true'
            schema = 'reference' if default == 'false' else 'synthesis'
            # mixed defaults to reference (conservative)
            if default == 'mixed':
                schema = 'reference'

    # Legacy detection (missing 3+ required fields)
    required = ['created', 'updated', 'domain']
    missing = sum(1 for f in required if not fm.get(f))
    is_legacy = missing >= 2

    return {'tier': tier, 'schema': schema, 'is_legacy': is_legacy,
            'domain_slug': fm.get('domain', '')}


# ─────────────────────────────────────────────────────────────
# LINK INDEX
# ─────────────────────────────────────────────────────────────

def build_link_index(notes: list, vault_root: Path) -> dict:
    """Map lowercase title/filename variants to Path objects.
    Includes ALL .md files (maps, MOCs, etc.) so links to them don't show as broken.
    """
    index = {}
    # First index the given notes list
    for p in notes:
        stem = p.stem
        index[stem.lower()] = p
        tm = re.match(r'^\d{12} - (.+)$', stem)
        if tm:
            index[tm.group(1).lower()] = p

    # Also walk vault for any .md files not in notes (maps, MOCs, etc.)
    for root, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules',)]
        for fname in files:
            if not fname.endswith('.md'):
                continue
            p = Path(root) / fname
            stem = p.stem
            key = stem.lower()
            if key not in index:
                index[key] = p
            tm = re.match(r'^\d{12} - (.+)$', stem)
            if tm:
                title_key = tm.group(1).lower()
                if title_key not in index:
                    index[title_key] = p
    return index


def resolve_link(link_text: str, link_index: dict) -> bool:
    target = link_text.strip()
    return target.lower() in link_index


def get_note_domain(path: Path, fm: dict, config: VaultConfig) -> str:
    """Get domain slug for a note."""
    if config.is_flat_folder:
        return fm.get('domain', '')
    rel = str(path.relative_to(config.vault_root)).replace('\\', '/')
    for domain in config.domains:
        folder = domain['folder'].lstrip('/')
        if rel.startswith(folder):
            return domain['slug']
    return fm.get('domain', '')


# ─────────────────────────────────────────────────────────────
# CATEGORY A: NOTE-LEVEL CHECKS
# ─────────────────────────────────────────────────────────────

BASE_FIELDS = ['created', 'updated', 'domain']


def run_note_checks(path: Path, content: str, fm: dict, cls: dict,
                    config: VaultConfig, link_index: dict,
                    all_fm: dict) -> list:
    """Run all 18 Category A checks. Returns list of (code, message) tuples."""
    issues = []
    schema = cls['schema']
    tier = cls['tier']
    body = get_body(content)

    # ── A01: Frontmatter well-formed ──────────────────────────────────────
    if not has_valid_frontmatter(content):
        issues.append(('A01', 'Frontmatter: missing or malformed --- delimiters'))
    elif not fm:
        issues.append(('A01', 'Frontmatter: present but empty or unparseable'))

    # ── A02: Required base fields ──────────────────────────────────────────
    for field in BASE_FIELDS:
        if not fm.get(field):
            issues.append(('A02', f'Frontmatter: missing required field "{field}"'))

    # ── A03: Vault-specific synthesis frontmatter ──────────────────────────
    if schema == 'synthesis':
        for field in config.synthesis_additional_fm:
            if field not in fm or fm.get(field) is None:
                issues.append(('A03', f'Frontmatter: missing synthesis field "{field}"'))

    # ── A04: fault_line value valid ────────────────────────────────────────
    if schema == 'synthesis' and config.fault_line_positions:
        fl_raw = str(fm.get('fault_line', '')).strip('"\'')
        # Value might be "materialist / ideational / ..." — take first token
        fl_val = re.split(r'\s*[/|]\s*', fl_raw)[0].strip()
        if fl_val and fl_val not in config.fault_line_positions:
            issues.append(('A04', f'Frontmatter: fault_line "{fl_val}" not in {config.fault_line_positions}'))

    # ── A05: open_problems IDs valid ──────────────────────────────────────
    if schema == 'synthesis' and config.open_problem_ids:
        prob_key = config.open_problem_key
        probs = fm.get(prob_key)
        if probs:
            if isinstance(probs, str):
                probs = [probs]
            for p in probs:
                try:
                    pid = int(str(p).strip())
                    if pid not in config.open_problem_ids:
                        issues.append(('A05', f'Frontmatter: {prob_key} ID {pid} not valid '
                                              f'(valid: {sorted(config.open_problem_ids)})'))
                except (ValueError, TypeError):
                    issues.append(('A05', f'Frontmatter: {prob_key} contains non-integer "{p}"'))

    # ── A06: evergreen-candidate consistency ──────────────────────────────
    if not config.is_training:
        ec = str(fm.get('evergreen-candidate', '')).lower()
        domain_slug = fm.get('domain', '')
        domain = config.domain_by_slug.get(domain_slug)
        if domain:
            domain_default = domain.get('evergreen_candidate', 'true').lower()
            if ec == 'true' and domain_default == 'false':
                issues.append(('A06', f'Frontmatter: evergreen-candidate=true but domain '
                                      f'"{domain_slug}" defaults to false — verify intentional'))

    # ── A07: Required section headers present ──────────────────────────────
    if schema == 'synthesis' and config.synthesis_checkable:
        for header_core in config.synthesis_checkable:
            if not section_exists(content, header_core):
                issues.append(('A07', f'Missing required section: "## {header_core}"'))

    # ── A08: No empty sections ─────────────────────────────────────────────
    if schema == 'synthesis':
        for m in re.finditer(r'^(## [^\n]+)\n(\s*)((?=## |\Z))', content, re.MULTILINE):
            section_name = m.group(1).strip()
            issues.append(('A08', f'Empty section: "{section_name}"'))

    # ── A09: Judgment Instrument sub-fields ───────────────────────────────
    if schema == 'synthesis' and config.ji_subfields:
        ji_name = config.ji_section_name
        ji_content = get_section(content, ji_name)
        if not ji_content:
            # Try subsection (###) search
            ji_m = re.search(rf'### {re.escape(ji_name)}\n(.*?)(?=\n##|\Z)', content,
                             re.DOTALL | re.IGNORECASE)
            ji_content = ji_m.group(1) if ji_m else ''

        if ji_content:
            for subfield in config.ji_subfields:
                if not re.search(re.escape(subfield), ji_content, re.IGNORECASE):
                    issues.append(('A09', f'Judgment Instrument: missing sub-field "{subfield}"'))

    # ── A10: "Threatens" entry present and non-empty ───────────────────────
    if schema == 'synthesis':
        t_m = re.search(r'\*\*Threatens?\*\*\s*[:\-]\s*(.+)', content)
        if not t_m:
            issues.append(('A10', 'Synthesis instrument: "**Threatens**" entry missing'))
        elif not t_m.group(1).strip().strip('[]…'):
            issues.append(('A10', 'Synthesis instrument: "**Threatens**" entry is empty or placeholder'))

    # ── A11: Open Questions references at least 1 open problem ───────────
    if schema == 'synthesis':
        oq = get_section(content, 'Open Questions')
        if oq:
            prob_key_label = 'Open Challenge' if config.open_problem_key == 'open_challenges' else 'Open Problem'
            if not re.search(rf'{prob_key_label}\s*\d+', oq, re.IGNORECASE):
                issues.append(('A11', f'Open Questions: no "{prob_key_label} N" reference found'))
        # Note: missing section flagged by A07

    # ── A12: Reference notes don't have synthesis-only sections ──────────
    if schema == 'reference' and config.reference_excluded:
        for excl in config.reference_excluded:
            if re.search(re.escape(excl), content, re.IGNORECASE):
                issues.append(('A12', f'Reference note contains synthesis-only content: "{excl}"'))

    # ── A13: Wikilink count in See Also = 4–8 ─────────────────────────────
    sa_content = get_section(content, 'See Also')
    if sa_content:
        links_in_sa = get_wikilinks(sa_content)
        count = len(links_in_sa)
        if count < 4:
            issues.append(('A13', f'See Also: {count} wikilinks (minimum is 4)'))
        elif count > 8:
            issues.append(('A13', f'See Also: {count} wikilinks (maximum is 8)'))
    elif schema == 'synthesis':
        issues.append(('A13', 'See Also: section missing entirely'))

    # ── A14: All wikilinks resolve to existing notes ──────────────────────
    broken = []
    for lnk in get_wikilinks(body):
        if not resolve_link(lnk, link_index):
            broken.append(lnk)
    for lnk in broken:
        issues.append(('A14', f'Broken wikilink: [[{lnk}]] — not found in vault'))

    # ── A15: At least 1 cross-domain wikilink in See Also ────────────────
    if schema == 'synthesis' and config.cross_domain_required and sa_content:
        note_domain = get_note_domain(path, fm, config)
        cross_found = False
        for lnk in get_wikilinks(sa_content):
            target = link_index.get(lnk.strip().lower())
            if target:
                target_fm = all_fm.get(target, {})
                target_domain = get_note_domain(target, target_fm, config)
                if target_domain and target_domain != note_domain:
                    cross_found = True
                    break
        if not cross_found and get_wikilinks(sa_content):
            issues.append(('A15', f'See Also: no cross-domain link found '
                                  f'(all links within domain "{note_domain}")'))

    # ── A16: Filename matches YYYYMMDDHHMM - *.md ────────────────────────
    fname = path.name
    if not re.match(r'^\d{12} - .+\.md$', fname):
        issues.append(('A16', f'Filename: "{fname}" does not match YYYYMMDDHHMM - Title.md pattern'))

    # ── A17: Tier 3 notes in correct output folder ───────────────────────
    if tier == 'tier3' and config.tier3_output:
        rel = str(path.relative_to(config.vault_root)).replace('\\', '/')
        if not rel.startswith(config.tier3_output.lstrip('/')):
            issues.append(('A17', f'Tier 3 note not in output folder "{config.tier3_output}"'))

    # ── A18: Schema-structure mismatch ────────────────────────────────────
    if schema == 'synthesis' and config.synthesis_checkable:
        missing_syn = [h for h in config.synthesis_checkable if not section_exists(content, h)]
        if len(missing_syn) >= 2:
            issues.append(('A18', f'Schema mismatch: marked evergreen-candidate=true but missing '
                                  f'{len(missing_syn)} synthesis sections '
                                  f'({", ".join(missing_syn[:2])}{"..." if len(missing_syn) > 2 else ""}) '
                                  f'— written in reference format?'))

    return issues


# ─────────────────────────────────────────────────────────────
# CATEGORY B: VAULT-LEVEL HEALTH METRICS
# ─────────────────────────────────────────────────────────────

def run_vault_checks(all_notes: list, all_fm: dict, all_cls: dict,
                     config: VaultConfig) -> dict:
    metrics = {}

    # B01: Note count per domain
    domain_counts = defaultdict(int)
    for p in all_notes:
        slug = all_cls.get(p, {}).get('domain_slug') or all_fm.get(p, {}).get('domain', 'unknown')
        domain_counts[slug] += 1

    domain_warnings = []
    for d in config.domains:
        count = domain_counts.get(d['slug'], 0)
        if d['priority'] in ('core', 'tier1') and count < 5:
            domain_warnings.append(f"{d['slug']}: {count} notes (< 5 for {d['priority']} domain)")

    metrics['domain_counts'] = dict(sorted(domain_counts.items(), key=lambda x: -x[1]))
    metrics['domain_warnings'] = domain_warnings

    # B02: Fault-line distribution
    fl_counts = defaultdict(int)
    syn_total = 0
    for p, fm in all_fm.items():
        if all_cls.get(p, {}).get('schema') == 'synthesis':
            fl_raw = str(fm.get('fault_line', '')).strip('"\'')
            fl = re.split(r'\s*[/|]\s*', fl_raw)[0].strip()
            if fl and fl in config.fault_line_positions:
                fl_counts[fl] += 1
                syn_total += 1

    fl_pct = {}
    fl_warnings = []
    for pos in config.fault_line_positions:
        pct = round(fl_counts[pos] / syn_total * 100, 1) if syn_total > 0 else 0.0
        fl_pct[pos] = pct
        if pct < 15 and syn_total >= 20:
            fl_warnings.append(f'{pos}: {pct:.0f}% (< 15% — underrepresented)')

    metrics['fault_line_distribution'] = fl_pct
    metrics['fault_line_warnings'] = fl_warnings

    # B03: Open problem coverage
    prob_counts = defaultdict(int)
    prob_key = config.open_problem_key
    for fm in all_fm.values():
        probs = fm.get(prob_key, [])
        if isinstance(probs, str):
            probs = [probs]
        for p in (probs or []):
            try:
                prob_counts[int(str(p).strip())] += 1
            except (ValueError, TypeError):
                pass

    zero_coverage = sorted(pid for pid in config.open_problem_ids if prob_counts.get(pid, 0) == 0)
    metrics['open_problem_coverage'] = dict(sorted(prob_counts.items()))
    metrics['zero_coverage_problems'] = zero_coverage

    # B04: Tier distribution
    tier_dist = defaultdict(int)
    for p in all_notes:
        cls = all_cls.get(p, {})
        t = cls.get('tier', '')
        s = cls.get('schema', '')
        if t == 'tier3':
            tier_dist['T3'] += 1
        elif t == 'tier1':
            tier_dist['T1'] += 1
        elif s == 'synthesis':
            tier_dist['T2-Syn'] += 1
        else:
            tier_dist['T2-Ref'] += 1

    metrics['tier_distribution'] = dict(tier_dist)

    # B05: Stale domains
    domain_latest = {}
    for p, fm in all_fm.items():
        d = fm.get('domain', '')
        created = fm.get('created', '')
        if d and created:
            try:
                dt = datetime.strptime(str(created)[:10], '%Y-%m-%d')
                if d not in domain_latest or dt > domain_latest[d]:
                    domain_latest[d] = dt
            except ValueError:
                pass

    now = datetime.now()
    stale = sorted(
        [(d, (now - dt).days) for d, dt in domain_latest.items() if (now - dt).days > 30],
        key=lambda x: -x[1]
    )
    metrics['stale_domains'] = stale[:5]

    # B06: Frontmatter compliance rate by domain
    compliance = defaultdict(lambda: {'total': 0, 'ok': 0})
    for p, fm in all_fm.items():
        d = fm.get('domain', 'unknown')
        compliance[d]['total'] += 1
        if all(fm.get(f) for f in ['created', 'updated', 'domain']):
            compliance[d]['ok'] += 1

    low_compliance = [
        (d, round(v['ok'] / v['total'] * 100), v['total'])
        for d, v in compliance.items()
        if v['total'] >= 3 and v['ok'] / v['total'] < 0.8
    ]
    metrics['low_compliance_domains'] = sorted(low_compliance, key=lambda x: x[1])

    # B07: Legacy note count
    metrics['legacy_note_count'] = sum(1 for cls in all_cls.values() if cls.get('is_legacy'))

    # B08: MOC freshness
    moc_warnings = []
    moc_folder = config.folders.get('mocs', '')
    if moc_folder:
        moc_dir = config.vault_root / moc_folder.rstrip('/\\')
        if moc_dir.exists():
            latest_note_dt = None
            for fm in all_fm.values():
                try:
                    dt = datetime.strptime(str(fm.get('created', ''))[:10], '%Y-%m-%d')
                    if latest_note_dt is None or dt > latest_note_dt:
                        latest_note_dt = dt
                except ValueError:
                    pass

            if latest_note_dt:
                for moc_file in moc_dir.glob('*.md'):
                    try:
                        mc = moc_file.read_text(encoding='utf-8', errors='ignore')
                        mfm = parse_frontmatter(mc)
                        moc_dt = datetime.strptime(str(mfm.get('updated', ''))[:10], '%Y-%m-%d')
                        behind = (latest_note_dt - moc_dt).days
                        if behind > 7:
                            moc_warnings.append(
                                f'{moc_file.name}: last updated {mfm.get("updated")} '
                                f'but notes exist from {latest_note_dt.date()} ({behind}d behind)'
                            )
                    except (ValueError, AttributeError, TypeError):
                        pass

    metrics['moc_warnings'] = moc_warnings

    return metrics


# ─────────────────────────────────────────────────────────────
# CATEGORY C: GRAPH ANALYSIS
# ─────────────────────────────────────────────────────────────

def run_graph_checks(all_notes: list, all_fm: dict, all_cls: dict,
                     config: VaultConfig, link_index: dict) -> dict:
    graph = {}
    note_set = set(all_notes)

    # Build adjacency: outgoing links, incoming counts
    outgoing = {}
    incoming = defaultdict(int)

    for p in all_notes:
        try:
            body = get_body(p.read_text(encoding='utf-8', errors='ignore'))
        except Exception:
            continue
        targets = []
        for lnk in get_wikilinks(body):
            resolved = link_index.get(lnk.strip().lower())
            if resolved and resolved in note_set:
                targets.append(resolved)
                incoming[resolved] += 1
        outgoing[p] = targets

    # G01: Orphan notes (0 incoming links)
    orphans = [
        str(p.relative_to(config.vault_root)).replace('\\', '/')
        for p in all_notes
        if incoming.get(p, 0) == 0
    ]
    graph['orphan_count'] = len(orphans)
    graph['orphan_notes'] = orphans[:10]

    # G02: Cross-domain link ratio per domain
    domain_link_stats = defaultdict(lambda: {'total': 0, 'cross': 0})
    for p in all_notes:
        p_domain = get_note_domain(p, all_fm.get(p, {}), config)
        for t in outgoing.get(p, []):
            t_domain = get_note_domain(t, all_fm.get(t, {}), config)
            domain_link_stats[p_domain]['total'] += 1
            if t_domain and t_domain != p_domain:
                domain_link_stats[p_domain]['cross'] += 1

    silo_warnings = []
    cross_rates = {}
    for d, stats in domain_link_stats.items():
        if stats['total'] >= 5:
            rate = stats['cross'] / stats['total']
            cross_rates[d] = round(rate * 100, 1)
            if rate < 0.15:
                silo_warnings.append(f'{d}: {rate:.0%} cross-domain links (possible silo)')
    graph['domain_cross_rates'] = cross_rates
    graph['silo_warnings'] = silo_warnings

    # G03: Map-note association integrity
    map_warnings = []
    for root, dirs, files in os.walk(config.vault_root):
        dirs[:] = [d for d in dirs if not should_skip_dir(d, config)]
        for fname in files:
            if not any(fname.endswith(s) for s in MAP_SUFFIXES):
                continue
            map_path = Path(root) / fname
            try:
                mc = map_path.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue
            atomic_m = re.search(
                r'(?:Atomic Notes to Generate|Notes to Generate)[^\n]*\n(.*?)(?=\n## |\Z)',
                mc, re.DOTALL | re.IGNORECASE
            )
            if atomic_m:
                candidates = re.findall(r'[-*]\s+.+', atomic_m.group(1))
                if len(candidates) >= 4:
                    map_stem = map_path.stem.lower()
                    back_refs = sum(
                        1 for fm in all_fm.values()
                        if map_stem in str(fm.get('source', '')).lower()
                    )
                    if back_refs < len(candidates) * 0.4:
                        rel = str(map_path.relative_to(config.vault_root)).replace('\\', '/')
                        map_warnings.append(
                            f'{rel}: ~{len(candidates)} candidate notes but only {back_refs} '
                            f'notes reference this map'
                        )
    graph['map_warnings'] = map_warnings[:5]

    # G04: Near-duplicate title detection (Jaccard similarity ≥ 75%)
    STOPWORDS = {'that', 'this', 'with', 'from', 'into', 'they', 'their', 'than',
                 'have', 'will', 'been', 'more', 'when', 'does', 'only', 'under'}
    titles = {}
    for p in all_notes:
        stem = p.stem
        tm = re.match(r'^\d{12} - (.+)$', stem)
        title = tm.group(1) if tm else stem
        words = set(re.findall(r'\b\w{4,}\b', title.lower())) - STOPWORDS
        titles[p] = words

    duplicates = []
    note_list = list(all_notes)
    for i, p1 in enumerate(note_list):
        for p2 in note_list[i + 1:]:
            w1, w2 = titles.get(p1, set()), titles.get(p2, set())
            if not w1 or not w2:
                continue
            jaccard = len(w1 & w2) / len(w1 | w2) if (w1 | w2) else 0
            if jaccard >= 0.75:
                duplicates.append({
                    'note1': str(p1.relative_to(config.vault_root)).replace('\\', '/'),
                    'note2': str(p2.relative_to(config.vault_root)).replace('\\', '/'),
                    'similarity': round(jaccard * 100),
                })
    graph['near_duplicates'] = duplicates[:5]

    return graph


# ─────────────────────────────────────────────────────────────
# BASELINE MANAGEMENT
# ─────────────────────────────────────────────────────────────

def get_baseline_path(config: VaultConfig, linter_dir: Path) -> Path:
    return linter_dir / 'baselines' / f'{config.name}.json'


def save_baseline(results: dict, config: VaultConfig, linter_dir: Path) -> Path:
    bp = get_baseline_path(config, linter_dir)
    bp.parent.mkdir(exist_ok=True)
    baseline = {
        'saved_at': datetime.now().isoformat(),
        'vault': config.name,
        'issue_codes': {k: [i[0] for i in v] for k, v in results['note_issues'].items()},
    }
    bp.write_text(json.dumps(baseline, indent=2), encoding='utf-8')
    return bp


def compare_baseline(results: dict, config: VaultConfig, linter_dir: Path) -> dict:
    bp = get_baseline_path(config, linter_dir)
    if not bp.exists():
        return {'error': f'No baseline found. Run --baseline save first.'}
    prev = json.loads(bp.read_text(encoding='utf-8'))
    prev_issues = prev.get('issue_codes', {})
    curr_issues = {k: [i[0] for i in v] for k, v in results['note_issues'].items()}

    regressions, improvements = {}, {}
    for path in set(prev_issues) | set(curr_issues):
        new = set(curr_issues.get(path, [])) - set(prev_issues.get(path, []))
        fixed = set(prev_issues.get(path, [])) - set(curr_issues.get(path, []))
        if new:
            regressions[path] = sorted(new)
        if fixed:
            improvements[path] = sorted(fixed)

    return {
        'baseline_from': prev.get('saved_at', '?'),
        'regressions': regressions,
        'improvements': improvements,
        'regression_count': sum(len(v) for v in regressions.values()),
        'improvement_count': sum(len(v) for v in improvements.values()),
    }


# ─────────────────────────────────────────────────────────────
# REPORTING
# ─────────────────────────────────────────────────────────────

def human_report(results: dict, config: VaultConfig, verbose: bool):
    note_issues = results.get('note_issues', {})
    vm = results.get('vault_metrics', {})
    graph = results.get('graph', {})

    total = results.get('total_notes', 0)
    affected = sum(1 for v in note_issues.values() if v)
    total_issues = sum(len(v) for v in note_issues.values())

    W = 70
    print(f'\n{"="*W}')
    print(f'VAULT LINTER: {config.name}  ({total} notes scanned)')
    print(f'{"="*W}')
    print(f'Issues: {total_issues}  |  Notes affected: {affected}')

    if note_issues and (affected > 0 or verbose):
        print(f'\n{"─"*W}')
        print('CATEGORY A — NOTE-LEVEL CHECKS')
        print(f'{"─"*W}')
        for p, issues in sorted(note_issues.items()):
            rel = p if isinstance(p, str) else str(Path(p).relative_to(config.vault_root)).replace('\\', '/')
            short = ('...' + rel[-57:]) if len(rel) > 60 else rel
            if issues:
                print(f'\n[FAIL] {short}')
                for code, msg in issues:
                    print(f'  {code}: {msg}')
            elif verbose:
                print(f'[PASS] {short}')

    if vm:
        print(f'\n{"─"*W}')
        print('CATEGORY B — VAULT HEALTH METRICS')
        print(f'{"─"*W}')

        if vm.get('domain_counts'):
            print('\nNotes per domain:')
            for d, n in vm['domain_counts'].items():
                print(f'  {d}: {n}')
            for w in vm.get('domain_warnings', []):
                print(f'  WARN: {w}')

        if vm.get('fault_line_distribution'):
            print('\nFault-line distribution:')
            print('  ' + ' | '.join(f'{k}: {v}%' for k, v in vm['fault_line_distribution'].items()))
            for w in vm.get('fault_line_warnings', []):
                print(f'  WARN: {w}')

        zero = vm.get('zero_coverage_problems', [])
        if zero:
            print(f'\nOpen problems with 0 notes: {zero}')
        else:
            print('\nOpen problem coverage: all problems have at least 1 note')

        td = vm.get('tier_distribution', {})
        if td:
            print('\nTier distribution: ' + ' | '.join(f'{k}: {v}' for k, v in sorted(td.items())))

        lc = vm.get('low_compliance_domains', [])
        if lc:
            print('\nLow frontmatter compliance domains:')
            for d, pct, n in lc:
                print(f'  {d}: {pct}% compliant ({n} notes) — likely legacy/pre-framework notes')

        legacy = vm.get('legacy_note_count', 0)
        if legacy:
            print(f'\nPre-framework (legacy) notes: {legacy}')

        if vm.get('stale_domains'):
            print('\nMost stale domains (days since last note):')
            for d, days in vm['stale_domains']:
                print(f'  {d}: {days}d')

        for w in vm.get('moc_warnings', []):
            print(f'\nMOC WARN: {w}')

    if graph:
        print(f'\n{"─"*W}')
        print('CATEGORY C — GRAPH ANALYSIS')
        print(f'{"─"*W}')

        oc = graph.get('orphan_count', 0)
        print(f'\nOrphan notes (0 incoming links): {oc}')
        for o in graph.get('orphan_notes', [])[:5]:
            print(f'  {o}')
        if oc > 5:
            print(f'  ... and {oc - 5} more')

        for w in graph.get('silo_warnings', []):
            print(f'WARN: {w}')

        for w in graph.get('map_warnings', []):
            print(f'MAP WARN: {w}')

        dups = graph.get('near_duplicates', [])
        if dups:
            print('\nNear-duplicate title pairs:')
            for dup in dups:
                print(f'  ({dup["similarity"]}% similar)')
                print(f'    {dup["note1"]}')
                print(f'    {dup["note2"]}')

    print(f'\n{"="*W}')
    print(f'SUMMARY: {total} notes | {total_issues} issues | {affected} notes affected')
    print(f'{"="*W}\n')


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Vault Linter — validate synthesis vault notes against vault-config.md'
    )
    parser.add_argument('vault_path', help='Path to vault root directory')
    parser.add_argument('--category', choices=['note', 'vault', 'graph', 'all'], default='all')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--recent', type=int, metavar='N',
                        help='Only check the N most recently modified notes')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--baseline', choices=['save', 'compare'])
    parser.add_argument('--check', metavar='CODE',
                        help='Run only a specific check (e.g. A14)')
    args = parser.parse_args()

    vault_root = Path(args.vault_path)
    if not vault_root.exists():
        print(f'Error: vault not found: {vault_root}', file=sys.stderr)
        sys.exit(1)

    try:
        config = VaultConfig(vault_root)
    except FileNotFoundError as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)

    # Discover all notes (for link index + vault metrics)
    all_notes = discover_notes(vault_root, config)
    link_index = build_link_index(all_notes, vault_root)

    # Parse frontmatter and classify all notes
    all_fm, all_cls = {}, {}
    for p in all_notes:
        try:
            content = p.read_text(encoding='utf-8', errors='ignore')
            fm = parse_frontmatter(content)
        except Exception:
            fm = {}
        all_fm[p] = fm
        all_cls[p] = classify_note(p, fm, config)

    # Narrow to recent notes for note-level checks if requested
    check_notes = all_notes
    if args.recent:
        check_notes = discover_notes(vault_root, config, recent_n=args.recent)

    # Run checks
    results = {
        'vault': config.name,
        'scanned_at': datetime.now().isoformat(),
        'total_notes': len(check_notes),
        'note_issues': {},
        'vault_metrics': {},
        'graph': {},
    }

    if args.category in ('note', 'all'):
        for p in check_notes:
            try:
                content = p.read_text(encoding='utf-8', errors='ignore')
                issues = run_note_checks(
                    p, content, all_fm.get(p, {}), all_cls.get(p, {}),
                    config, link_index, all_fm
                )
                if args.check:
                    issues = [(c, m) for c, m in issues if c == args.check.upper()]
                results['note_issues'][p] = issues
            except Exception as e:
                results['note_issues'][p] = [('ERR', f'Check failed: {e}')]

    if args.category in ('vault', 'all'):
        results['vault_metrics'] = run_vault_checks(all_notes, all_fm, all_cls, config)

    if args.category in ('graph', 'all'):
        results['graph'] = run_graph_checks(all_notes, all_fm, all_cls, config, link_index)

    # Baseline
    linter_dir = Path(__file__).parent
    if args.baseline == 'save':
        bp = save_baseline(results, config, linter_dir)
        print(f'Baseline saved: {bp}')
        return
    if args.baseline == 'compare':
        cmp = compare_baseline(results, config, linter_dir)
        if args.json:
            print(json.dumps(cmp, indent=2))
        else:
            print(f'\nBaseline comparison (from: {cmp.get("baseline_from", "?")})')
            print(f'  New failures (regressions): {cmp.get("regression_count", 0)}')
            print(f'  Fixed issues (improvements): {cmp.get("improvement_count", 0)}')
            for path, codes in cmp.get('regressions', {}).items():
                print(f'  REGRESS: {path} — {codes}')
            for path, codes in cmp.get('improvements', {}).items():
                print(f'  FIXED:   {path} — {codes}')
        return

    # Output
    if args.json:
        out = {
            'vault': results['vault'],
            'scanned_at': results['scanned_at'],
            'total_notes': results['total_notes'],
            'note_issues': {
                str(p.relative_to(vault_root)).replace('\\', '/'): issues
                for p, issues in results['note_issues'].items()
            },
            'vault_metrics': results['vault_metrics'],
            'graph': results['graph'],
        }
        print(json.dumps(out, indent=2, default=str))
    else:
        human_report(results, config, verbose=args.verbose)


if __name__ == '__main__':
    main()
