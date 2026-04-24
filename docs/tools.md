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

Validates the AGENSY framework itself — checks architectural integrity across six categories totaling 22 individual checks (F01–F22).

**What it checks:**

**Category F1 — Configuration Integrity (F01–F05)**: every active vault has a `vault-config.md` with all required blocks; `intellectual_style.engagement_axis.positions[]` non-empty; every `open_problems[]` entry has `id` / `name` / `question`; every `domains[]` entry has `slug` / `label` / `folder` / `priority`.

**Category F2 — Budget Compliance (F06–F08)**: `~/.claude/CLAUDE.md` under 100 lines; each vault's `CLAUDE.md` under 120 lines; each vault's `memory/MEMORY.md` under 150 lines. Enforces the context budget invariant.

**Category F3 — Stub & Protocol Integrity (F09–F11)**: every `.claude/commands/` stub references an existing universal protocol; every universal protocol has at least one stub pointing at it; stubs are not bloated with duplicated protocol logic.

**Category F4 — Path Integrity (F12–F14)**: every `reference_docs.*` path resolves; every `folder_structure.*` folder exists; `folder_structure.maps` resolves where declared.

**Category F5 — Cross-Framework Consistency (F15–F17)**: `system-contracts.md §2` contract table lists every universal command; `vault-config-schema.md` declares every required block; `genesis-protocol.md` Phase 1 has at least 12 Doc entries (Docs 1–12 universal; Doc 13+ conditional vault-type-gated).

**Category F6 — Meta-Architecture Integrity (F18–F22, added v1.2.0)**:
- **F18 — Frontmatter schema compliance**: every framework `.md` has valid frontmatter (`type`, `stability_tier`, `canonicity` — plus `canonical_for` / `derives_from` / `synchronized_with` as required by state). Missing new fields emit `WARN` (retrofit-pending), not `FAIL` — backward-compat during gradual adoption.
- **F19 — Canonicity uniqueness**: every `canonical_for: [concern]` claim is held by at most one doc. Conflicts `FAIL` loudly with the conflicting set named.
- **F20 — Synchronized-with symmetry + fact-match**: declared `synchronized_with: [peer]` relationships must be reciprocal, and concern-specific callbacks verify the synchronized facts actually match (initial callback: command-list between `system-contracts §2` and `system-architecture` YAML manifest).
- **F21 — Protocol path discipline**: `type: protocol` docs must not hardcode vault-specific references. Paths mentioning `[AGENSY_PATH]/...` are allowed; `synthesis_<vault-slug>` references are flagged. Bare-prose references `FAIL`; backtick-wrapped examples `WARN` (documentation examples, parameterize when convenient).
- **F22 — Decision-record supersession chain**: every `supersedes:` pointer in a `decision_record` / `experiment_log` resolves to an existing file of the same type with an older `created` date; no cycles.

**Usage:**
```bash
python [AGENSY_PATH]/tools/framework-verify.py
python [AGENSY_PATH]/tools/framework-verify.py --category F6
python [AGENSY_PATH]/tools/framework-verify.py --verbose
python [AGENSY_PATH]/tools/framework-verify.py --check F19
```

**When to run:**
- After any change to `framework/` files
- Before submitting a pull request (required — see CONTRIBUTING.md)
- When something in the framework feels broken and you can't identify why

**F01 failures are expected before your vaults are set up.** `vault-registry.md` ships with `/path/to/...` placeholder paths. Until you update those with real paths, `framework-verify.py` will report F01 failures for each vault — this is correct behavior. Categories F2–F6 validate the framework's own internal consistency and pass regardless of vault-path resolution.

**F18 retrofit WARNs are expected** after first clone: many framework files ship without the newer `stability_tier` and `canonicity` fields. These emit `WARN F18: missing stability_tier (retrofit pending)` — not failures. The warning count drops as the framework's own files get retrofitted incrementally.

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
