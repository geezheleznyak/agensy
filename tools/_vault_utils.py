#!/usr/bin/env python3
"""
_vault_utils.py — Shared parsing layer for the tools/ package.

Private to the tools/ package (underscore prefix). Houses vault-config
parsing, frontmatter extraction, note discovery, and link-index building
that multiple tools (vault-linter, system-audit, ...) need to share.

Cut-and-moved from vault-linter.py — zero behavior change.

Exports:
    setup_utf8_stdout()    — wrap stdout for UTF-8 safety on Windows
    VaultConfig            — vault-config.md parser
    parse_frontmatter      — YAML-ish frontmatter extractor
    has_valid_frontmatter, get_body, get_wikilinks, get_section, section_exists
    is_infrastructure, is_map, should_skip_dir, discover_notes
    build_link_index, resolve_link
    classify_for_coverage  — coverage-audit tier classifier (T1/T2-Ref/T2-Syn/T3/Map)
    get_note_domain        — flat-folder vs per-folder domain assignment
    MAP_SUFFIXES, INFRA_PATTERNS, BASE_FIELDS, STOPWORDS
"""

import io
import os
import re
import sys
from pathlib import Path


# ─────────────────────────────────────────────────────────────
# UTF-8 stdout helper (call from CLI entry-points)
# ─────────────────────────────────────────────────────────────

def setup_utf8_stdout():
    """Force UTF-8 output on Windows terminals."""
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

        # Axis frontmatter field name (varies: 'fault_line' vs 'engagement_axis')
        self.axis_field_name = self._axis_field_name()

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
        """[adversarial-preset vaults use] open_challenges; others use open_problems."""
        if re.search(r'open_challenges', self.text):
            return 'open_challenges'
        return 'open_problems'

    def _tier_value(self, tier: str) -> str:
        """Extract tier{N}.type_value from the note_tiers: block.

        Anchors on the tier header line, scans until the next sibling
        2-space block-key or top-level key, and reads type_value. Tolerant
        of multi-line description / graduation_rule fields with deeper
        indentation (e.g. `description: >` block scalars).
        """
        block_m = re.search(
            rf'^  {tier}:\n([\s\S]*?)(?=^  \w|^\w|\Z)',
            self.text, re.MULTILINE,
        )
        if not block_m:
            return ''
        block = block_m.group(1)
        tv_m = re.search(r'^    type_value:\s*(\S+)', block, re.MULTILINE)
        return tv_m.group(1).strip('"\'') if tv_m else ''

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
        """True if multiple domains share the same folder ([flat-folder pattern])."""
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
            # Check if it mentions "Reads as" ([adversarial vaults])
            if re.search(r'Reads as', self.text):
                return ['Reads as', 'Threatens', 'Fault line']
            # [structural-analytic vaults] use Primary insight
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

    def _axis_field_name(self) -> str:
        """Return 'fault_line' or 'engagement_axis' depending on which key the
        vault-config uses to declare its position vocabulary. Defaults to
        'fault_line' (the more common form)."""
        if re.search(r'^engagement_axis:', self.text, re.MULTILINE):
            return 'engagement_axis'
        return 'fault_line'

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


def is_map(path: Path) -> bool:
    """Return True if path is a map file (by filename suffix)."""
    return any(path.name.endswith(s) for s in MAP_SUFFIXES)


def should_skip_dir(name: str, config: VaultConfig) -> bool:
    if name.startswith('.'):
        return True
    if name in config.excluded_dirs:
        return True
    if name == '_maps':  # map folders (all vaults)
        return True
    return False


def discover_notes(vault_root: Path, config: VaultConfig, recent_n: int = None,
                   include_infrastructure_maps: bool = False,
                   include_t3_output: bool = False) -> list:
    """Walk vault, collect .md files that aren't infrastructure.

    include_infrastructure_maps: if True, map files (by suffix) are kept even
    though they would normally be filtered as infrastructure. Coverage audits
    need maps; the linter does not.

    include_t3_output: if True, the tier3_output directory (e.g. `50-Curriculum/`)
    is walked even if vault-config marks it as a `curriculum`-style folder key
    that would otherwise be excluded. Coverage audits need T3 docs; the linter
    does not.
    """
    # Optionally relax excluded_dirs for the tier3 output dir
    excluded_dirs = set(config.excluded_dirs)
    if include_t3_output and config.tier3_output:
        t3_top = config.tier3_output.strip('/\\').split('/')[0].split('\\')[0]
        excluded_dirs.discard(t3_top)
        excluded_dirs.discard(config.tier3_output.rstrip('/\\'))

    def _skip_dir(name: str) -> bool:
        if name.startswith('.'):
            return True
        if name in excluded_dirs:
            return True
        if name == '_maps':
            return True
        return False

    notes = []
    for root, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in dirs if not _skip_dir(d)]
        root_path = Path(root)

        for fname in files:
            if not fname.endswith('.md'):
                continue
            fpath = root_path / fname
            if include_infrastructure_maps and is_map(fpath):
                notes.append(fpath)
                continue
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


# ─────────────────────────────────────────────────────────────
# NOTE-LEVEL CONSTANTS
# ─────────────────────────────────────────────────────────────

BASE_FIELDS = ['created', 'updated', 'domain']

# Common short words filtered from title-similarity matchers.
# Used by jaccard-based duplicate detection (linter G04) and planned-note
# matching (coverage-audit Step 3).
STOPWORDS = {
    'that', 'this', 'with', 'from', 'into', 'they', 'their', 'than',
    'have', 'will', 'been', 'more', 'when', 'does', 'only', 'under',
}


# ─────────────────────────────────────────────────────────────
# COVERAGE-AUDIT CLASSIFIER
# ─────────────────────────────────────────────────────────────

def get_note_domain(path: Path, fm: dict, config: VaultConfig) -> str:
    """Return domain slug for a note.

    For flat-folder vaults, reads `domain:` frontmatter directly.
    For per-folder vaults, falls back to path-based assignment using
    the longest-prefix-matching domain folder.
    """
    if config.is_flat_folder:
        return fm.get('domain', '') or ''
    rel = str(path.relative_to(config.vault_root)).replace('\\', '/')
    # Longest-prefix match (handles nested domains)
    matches = []
    for domain in config.domains:
        folder = (domain.get('folder') or '').lstrip('/').rstrip('/')
        if folder and rel.startswith(folder):
            matches.append((len(folder), domain['slug']))
    if matches:
        matches.sort(reverse=True)
        return matches[0][1]
    return fm.get('domain', '') or ''


def classify_for_coverage(path: Path, fm: dict, config: VaultConfig) -> str:
    """Return one of: 'T1' | 'T2-Ref' | 'T2-Syn' | 'T3' | 'Map'.

    Distinct from vault-linter's classify_note (which returns tier+schema
    separately for compliance checks). This classifier emits the five
    coverage-tier buckets the protocol's Domain Summary table requires.

    Logic order:
      1. Map by filename suffix.
      2. T3 if `type:` matches tier3_type, OR path is under tier3_output.
      3. T1 if `type:` matches tier1_type, OR path is under inbox / a
         sources* folder per folder_structure.
      4. T2: split by evergreen-candidate (explicit > domain default).
         Training vaults are always T2-Syn.
    """
    if is_map(path):
        return 'Map'

    note_type = (fm.get('type') or '').strip('"\'')
    rel = str(path.relative_to(config.vault_root)).replace('\\', '/')

    # T3 — require BOTH note_type and tier3_type to be non-empty to match;
    # empty-string equality would falsely T3 every untyped note.
    if note_type and config.tier3_type and note_type == config.tier3_type:
        return 'T3'
    if config.tier3_output and rel.startswith(config.tier3_output.lstrip('/').rstrip('/')):
        return 'T3'

    # T1
    if note_type and config.tier1_type and note_type == config.tier1_type:
        return 'T1'
    folders = config.folders or {}
    inbox = (folders.get('inbox') or '').lstrip('/').rstrip('/')
    if inbox and rel.startswith(inbox):
        return 'T1'
    for key, val in folders.items():
        if not key.startswith('sources') and key != 'sources':
            continue
        prefix = (val or '').lstrip('/').rstrip('/')
        if prefix and rel.startswith(prefix):
            return 'T1'

    # T2 — training vaults: always synthesis
    if config.is_training:
        return 'T2-Syn'

    ec_raw = str(fm.get('evergreen-candidate', '')).lower().strip()
    if ec_raw == 'true':
        return 'T2-Syn'
    if ec_raw == 'false':
        return 'T2-Ref'

    # Domain-default fallback
    domain_slug = get_note_domain(path, fm, config)
    domain = config.domain_by_slug.get(domain_slug) if domain_slug else None
    if domain:
        default = str(domain.get('evergreen_candidate', 'true')).lower()
        if default == 'false':
            return 'T2-Ref'
        if default == 'mixed':
            return 'T2-Ref'  # conservative default for mixed
        return 'T2-Syn'

    # No domain match — default to T2-Syn (most common case for accumulation)
    return 'T2-Syn'
