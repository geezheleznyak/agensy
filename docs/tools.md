---
type: documentation
audience: human
---

# Validation Tools

AGENSY includes two Python scripts in `tools/` for validating vault health. Both are optional but recommended for contributors and for anyone running large arcs.

---

## vault-linter.py

Validates note content and schema compliance within a vault.

**What it checks (Categories A, B, G):**
- **A — Atomic structure**: Each note contains exactly one idea; no note exceeds appropriate scope
- **B — Evergreen compliance**: Notes marked `evergreen-candidate: true` meet Tier 2/3 schema requirements (engagement field populated, wikilinks present, correct section structure)
- **G — General schema**: Required frontmatter fields are present and correctly typed

**Usage:**
```bash
python [AGENSY_PATH]/tools/vault-linter.py "<vault-root>" --category note --recent 20
```

Replace `<vault-root>` with the path to the vault containing `vault-config.md`. The `--recent 20` flag checks only the 20 most recently modified notes — useful for post-arc validation without scanning the entire vault.

**When to run:**
- Automatically invoked by `/arc` via `/quick-check` at arc completion
- Manually after any bulk note creation
- Before a `/coverage-audit` if you want clean input data

**Platform note:** Requires Python 3. Tested on Windows; should work cross-platform.

---

## framework-verify.py

Validates the AGENSY framework itself — checks architectural integrity of the framework documents.

**What it checks (Categories F1–F5):**
- **F1 — Protocol completeness**: All 16 command protocol files are present and have required sections
- **F2 — Schema consistency**: vault-config-schema.md and all vault configs follow the same field structure
- **F3 — Cross-reference integrity**: All `[AGENSY_PATH]` placeholders are correctly formatted (no unresolved absolute paths)
- **F4 — Template coherence**: claude-md-template.md, note-tier-template.md, and map-type-template.md are internally consistent with the framework schema
- **F5 — Registry completeness**: vault-registry.md and system-state.md are in sync (no orphaned entries)

**Usage:**
```bash
python [AGENSY_PATH]/tools/framework-verify.py --verbose
```

**When to run:**
- After any change to `framework/` files
- Before submitting a pull request (required — see CONTRIBUTING.md)
- When something in the framework feels broken and you can't identify why

**F01 failures are expected before your vaults are set up.** `vault-registry.md` ships with `/path/to/...` placeholder paths. Until you update those with real paths, `framework-verify.py` will report F01 failures for each vault — this is correct behavior. The checks that validate the framework's own internal consistency (F06, F15, F16, F17) pass regardless.

**What a fully-configured run looks like:**
```
F1: PASS (16/16 command files present, all sections valid)
F2: PASS (schema consistent across vault configs)
F3: PASS (0 unresolved absolute paths)
F4: PASS (templates internally consistent)
F5: PASS (registry and state in sync)

All checks passed.
```

**Platform note:** Requires Python 3. Tested on Windows; should work cross-platform.

---

## Running Both Scripts Together

For a full pre-commit validation:
```bash
# Validate vault notes (run from inside a vault)
python [AGENSY_PATH]/tools/vault-linter.py "." --category note

# Validate framework integrity
python [AGENSY_PATH]/tools/framework-verify.py --verbose
```

If either script fails, fix the reported issues before committing or publishing.
