# Changelog

All notable changes to AGENSY are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Convention: each entry names the specific files changed (e.g., `framework/architecture-principles.md`) so readers can trace what `git log` would confirm.

---

## [1.1.0] — 2026-04-20

### Added — System Model Layer v0.1

- `framework/system-model-schema.yaml`: canonical schema for per-vault `system-model.yaml` — 6 node categories (agents, states, flows, signals, constraints, structures), 5 core + 5 reserve edge types, 7 pattern types (positive_feedback, negative_feedback, threshold, reflexivity, selection, accumulation, path_dependence), cross-vault binding structure, and validation rules
- `framework/system-model-architecture.md`: design rationale for the System Model Layer — what it solves, what it is NOT (reuse constraints against vault-config, cross-vault-bridges, theorist maps, MOCs), file layout, integration points, rollout phases, and live risks
- `framework/primitives.md`: human-readable three-layer primitive vocabulary reference with worked examples per vault type and a Pattern-Name Warning for cross-vault bindings
- `framework/universal-commands/system-query.md`: read-only query protocol — 6 query shapes (A–F) including cross-vault pattern aggregation
- `framework/universal-commands/system-audit.md`: reconciliation protocol — schema conformance, vault-config integrity, linked-notes integrity, bidirectional coverage, cross-vault binding integrity, pattern-name collision warning
- `framework/universal-commands/system-build.md`: interactive editor — the only write path into `system-model.yaml`; operation modes include `add-node`, `add-edge`, `add-pattern`, `add-binding`, `update`, `rename`, `remove`, `link-notes`, `bootstrap`; every write preceded by preview diff + user confirmation
- `framework/universal-commands/system-bridge.md`: cross-vault binding reconciliation — diffs a vault's `cross_vault_bindings[]` against `cross-vault-bridges.md`; three modes (`diff`, `propose`, `pair <peer>`); read-only by design

### Changed

- `framework/slash-command-suite.md`: command count 17 → 21; added 4 rows for system-* commands; added System Model Layer commands paragraph explaining read/write separation and command lifecycle integration
- `CLAUDE.md`: added `system-model-schema.yaml`, `system-model-architecture.md`, `primitives.md`, and `universal-commands/` to the Vault Structure listing; updated command count in `slash-command-suite.md` description 17 → 21

### Notes

Backward-compatible. Existing vaults without a `system-model.yaml` are unaffected — the layer is opt-in per vault via `/system-build bootstrap`. When a vault has no system model, `/system-query` and `/system-audit` respond with a pointer to `/system-build` and exit cleanly.

---

## [1.0.4] — 2026-04-05

### Fixed

- `README.md`: removed "full maturity" overclaim in two places — replaced with honest viability framing ("works across real domains", "built by the same process it teaches")

---

## [1.0.3] — 2026-04-05

### Fixed

- `framework/architecture-principles.md`, `framework/system-contracts.md`, `framework/system-architecture.md`,
  `framework/genesis-protocol.md`, `framework/command-lifecycle.md`, `framework/inter-vault-protocol.md`,
  `framework/claude-md-template.md`, `framework/universal-commands/arc.md`, `framework/universal-commands/question-bank.md`,
  `framework/universal-commands/what-next.md`: replaced all `synthesis-meta/...` path references with
  `[AGENSY_PATH]/...` and conceptual "lives in synthesis-meta" with "lives in agensy"

### Changed

- `framework/system-contracts.md` §1: trimmed from 3 verbose paragraphs to 3 bullet one-liners
  + pointer to `architecture-principles.md`; added cross-reference to §5 pointing to `architecture-principles.md` §4
- `framework/architecture-principles.md` §4: added cross-reference to `system-contracts.md` §5
- `CHANGELOG.md`: added convention note — entries should name specific files changed

---

## [1.0.2] — 2026-04-04

### Fixed

- Gitignored `.obsidian/app.json` and `.obsidian/appearance.json` — empty files, user-specific Obsidian state with no framework value

---

## [1.0.1] — 2026-04-04

### Fixed

- Command count corrected from 16 to 17 in `docs/global-claude-md.md` and `README.md` (`/quick-check` was missing from both lists)
- Repository structure comment in `README.md` updated: `16 protocol files + 3 legacy` → `17 + 2`
- `CHANGELOG.md` added (versioning infrastructure was present in `COMPATIBILITY.md` but CHANGELOG was missing)

---

## [1.0.0] — 2026-04-04

### Initial release

- 17 universal command protocols (16 user-invoked + 1 automatic sub-protocol: `quick-check`)
- Two-zone architecture (reference substrate + synthesis core)
- Three-tier note system with graduation logic
- Four vault types: accumulation, training, domain, expression
- Four intellectual style presets: adversarial, dialectical, contemplative, constructive
- Genesis Protocol (7-question vault bootstrapping, 4 phases, 12 documents)
- Cross-vault bridge architecture with shared `system-state.md`
- Command lifecycle with 4 trigger types (automatic, milestone, session, analytical)
- Session state system (`memory/session-state.md` + `memory/note-index.md`)
- Six example vault configs: theoria, bellum, logos, politeia, oeconomia, historia
- Python validation tools: `vault-linter.py`, `framework-verify.py`
