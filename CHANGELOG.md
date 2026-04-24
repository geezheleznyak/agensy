# Changelog

All notable changes to AGENSY are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Convention: each entry names the specific files changed (e.g., `framework/architecture-principles.md`) so readers can trace what `git log` would confirm.

---

## [1.2.1] — 2026-04-24

### Added — User-facing documentation for v1.2.0

- `docs/article-pipeline.md`: end-to-end walkthrough of the expression-vault pipeline — prerequisites (six substrate files), the seven commands (scan → seed → outline → draft → revise → critique → promote) with what each reads / produces / refuses, a worked example across three sessions, and troubleshooting for common pipeline-fights-you situations
- `docs/companion-mode.md`: when-to-use decision guide, the four read-only verbs (`/co-find`, `/co-combine`, `/co-suggest`, `/co-critique`), the capture verb (`/co-capture`) with its user-confirmation gate, a worked session end-to-end, and a pipeline-vs-companion comparison table

### Changed

- `README.md`: command count 20 → 34 (+2 aliases) across three mentions; added §7 Expression Pipeline and §8 Framework Meta-Architecture to Key Features; added v0.2 System Model extensions (timescale, subtype, secondary_types) to §6
- `docs/commands.md`: command count updated and grouped by family (17 core / 4 system-model / 8 article-pipeline / 5 companion); added Article Pipeline Commands section (one paragraph per command, with what-it-does / when-to-use / output); added Companion Mode Commands section; refreshed Command Trigger Reference with the new families
- `docs/concepts.md`: extended §System Model Layer with v0.2 additions (`timescale`, `subtype`, `secondary_types`); added new §Framework Meta-Architecture concept (11 types, 5 stability tiers, canonicity, supersession, the four architectural-spine docs); added new §Vault-Type Substrate concept (expression / training / accumulation scaffold allocation)
- `docs/tools.md`: rewrote §framework-verify.py with accurate category descriptions (F1–F5 were previously summarized incorrectly) and added §Category F6 — Meta-Architecture Integrity covering F18 (frontmatter schema compliance, with retrofit-WARN convention), F19 (canonicity uniqueness), F20 (synchronized-with symmetry + fact-match callbacks), F21 (protocol path discipline with backtick/code-fence exemption rule), F22 (decision-record supersession chain)
- `docs/getting-started.md`: §Step 3 now explains the conditional Doc 13 (vault-type substrate copy) — expression vaults get six scaffolds, training vaults get three, accumulation vaults get none — plus fill-in order guidance and links to `article-pipeline.md` / `companion-mode.md`

### Notes

Documentation-only release. No framework, protocol, tool, or schema changes. All content in v1.2.0 remains exactly as shipped; this patch documents it for users.

---

## [1.2.0] — 2026-04-24

### Added — Framework Meta-Architecture

- `framework/framework-meta-architecture.md`: new fourth architectural-spine document (WHY · HOW · WHAT · **META**). Names the 11 framework document types (invariant · topology · protocol · template · vocabulary · schema · reference · decision_record · experiment_log · registry · meta_workflow · validation_tool), the 5 stability tiers (bedrock · foundational · operational · dynamic · historical), canonicity rules (canonical / derived / synchronized / none), communication channels (reading-order declarations, prose references, structural references), decision-record supersession protocol (pointer-based, immutable), session economy, frontmatter specification
- `framework/map-to-article-extraction.md`: schema consumed by `/article-*` expression pipeline — map section → article role mapping, thesis-candidate heuristic, preset-driven narrative arc, standalone-ness test
- `framework/vault-type-templates/`: new directory holding vault-type-specific substrate scaffolds that genesis copies into a new vault beyond the 12 universal documents. Organized as:
  - `vault-type-templates/expression/` — six scaffolds for the `/article-*` and `/co-*` pipelines: `voice-profile.md` (style), `writer-positions.md` (substance bedrock), `positions-index.md` (harvest-loop index), `article-presets.md` (five narrative-arc blueprints, near-verbatim), `article-design-principles.md` (P1–P10 craft principles, near-verbatim), `source-map-registry.md` (map readiness schema)
  - `vault-type-templates/training/` — three scaffolds for training vaults: `curriculum-template.md` (phased development arc), `principles-and-postulates-template.md` (load-bearing priors), `sources-master-list-template.md` (curated bibliography)
  - `vault-type-templates/accumulation/` — intentionally empty (README documents why); the 12 universal genesis documents cover accumulation vaults completely
  - Each sub-folder has a README explaining role, fill-in order, and how consumer commands reference the files
- `framework/genesis-protocol.md`: new Doc 13 step (conditional, vault-type-gated) that copies the appropriate `vault-type-templates/` sub-folder into a new vault at bootstrap, and extends `vault-config.md` `reference_docs.*` with the relevant substrate keys
- `tools/framework-verify.py`: F17 relaxed from "exactly 12 Doc entries" to "≥12" (Docs 1–12 universal, Doc 13+ conditional); F6 type alias map extended to recognize template-specific types (`style-card`, `positions-card`, `positions-index`) as variants of `template`
- `tools/framework-verify.py`: new Category F6 — Meta-Architecture Integrity — with five checks:
  - **F18** frontmatter schema compliance (type enum, stability_tier, canonicity; WARN on missing new fields during retrofit)
  - **F19** canonicity uniqueness (every `canonical_for` concern claimed by at most one doc)
  - **F20** synchronized_with symmetry + concern-specific fact-match callbacks (initial callback: command-list cross-check between `system-contracts.md §2` and `system-architecture.md` YAML manifest)
  - **F21** protocol path discipline (invariant I2 enforcement: no bare vault-specific references in universal-commands/; backtick/code-fence examples → WARN)
  - **F22** decision-record supersession chain integrity (pointer resolves, same type, older date, no cycles)

### Added — Article Pipeline (expression-vault, 13 new universal commands)

- `framework/universal-commands/article-scan.md`: readiness-score maps in a source vault
- `framework/universal-commands/article-seed.md`: create essay seed from a source-vault map (Types A solo, D braid)
- `framework/universal-commands/article-outline.md`: convert seed to outline with preset-aware narrative arc
- `framework/universal-commands/article-draft.md`: generate draft with voice + position calibration
- `framework/universal-commands/article-revise.md`: multi-pass adversarial revision (thesis integrity, voice match, position alignment, preset fidelity, seam stress)
- `framework/universal-commands/article-promote.md`: publish with harvest-loop (extracts novel claims to positions index)
- `framework/universal-commands/article-critique.md`: external-critic pass (8 C1–C8 passes catching frame circularity, theorist-as-stamp, analogy validity, stratification independence, scenario silence, concession load, unit of analysis, title-thesis match)
- `framework/universal-commands/article-companion.md`: companion-mode workspace (operator writes; AI augments via four verbs)
- `framework/universal-commands/co-find.md` · `co-combine.md` · `co-suggest.md` · `co-critique.md` · `co-capture.md`: companion-mode read-only verbs (cross-vault material discovery, bridge surfacing, next-move options, surgical critique, substrate harvest)

### Added — System Model Layer v0.2

- `framework/primitives.md`: extended with Layer 3b (pattern timescale bands: seconds-to-minutes · hours-to-days · weeks-to-months · years · decades+ · mixed), Layer 3c (pattern subtypes — free-string, emergent; documented observed subtypes for reflexivity, threshold, positive_feedback), Layer 3d (boundary cases — `secondary_types` dual-tag for accumulation/path_dependence, positive_feedback/reflexivity, selection/path_dependence)
- `framework/system-model-schema.yaml`: v0.2 additive schema — `timescale`, `subtype`, `secondary_types` optional fields on patterns; `timescale` on flow-nodes; validation rules extended. All v0.1 system-model.yaml files remain valid
- `framework/universal-commands/system-audit.md`: new Step 5b "Binding Mechanism Check" — type/subtype/timescale comparison on cross-vault bindings with pattern pairings

### Changed

- `framework/system-contracts.md`: §2 contract table extended from 17 to 34 commands — 13 new rows for system-model and article/co pipelines; new paragraphs explaining expression-vault required keys and system-model required keys; frontmatter upgraded to declare `canonical_for: [vault_config_contract, breaking_change_rules, pre_framework_integration]` + `synchronized_with: [framework/system-architecture.md]`
- `framework/system-architecture.md`: YAML manifest `commands:` block extended with full entries for all 13 new commands; `universal_protocols.count` 19 → 34 with grouped listing (17 core · 4 system-model · 8 article-pipeline · 5 companion-co); Diagram 1 Mermaid node updated; frontmatter upgraded to declare `canonical_for: [topology_map, system_yaml_manifest]` + `synchronized_with: [framework/system-contracts.md]`
- `framework/architecture-principles.md`: §7.1 change-analysis protocol now also references `framework-meta-architecture.md` for framework-structure changes
- `framework/slash-command-suite.md`: header count 17 → 34 protocol files + 2 backward-compat aliases; pipeline-family split explained
- `framework/coverage-audit.md`: new Step 9 mandatory-if-system-model auto-fires `/system-audit` and updates System Model Freshness table with dirt-level classification (🟢/🟡/🔴)
- `framework/system-model-architecture.md`: expanded Self-Maintenance Policy with three-layer staleness prevention and escalation rules; Rollout Status updated through Phase 5 (omega universality test) with the bounded-universality result explicitly noted
- `vault-registry.md`: Framework Documents table expanded and grouped (architectural spine / runtime orchestration / templates / System Model Layer / expression pipeline) — ~20 rows vs. prior 11
- `CLAUDE.md`: vault structure listing updated; command count 21 → 34 + 2 aliases; reading-order convention now explicit (architecture-principles → system-contracts → system-architecture → framework-meta-architecture)
- `README.md`: vault structure listing updated with the new META doc and pipeline additions
- `tools/framework-verify.py`: `COMMAND_REQUIRED_KEYS` dict extended to cover all 34 commands; duplicate `promote` key removed; `--category F6` added

### Fixed

- Stale command inventory across 4 representations (`slash-command-suite.md` header count, `system-contracts.md` §2, `system-architecture.md` YAML manifest, `framework-verify.py COMMAND_REQUIRED_KEYS`) — reconciled against 34-command reality; F19/F20 now keep them synchronized going forward

### Notes

Backward-compatible across the board. All v0.1 system-model.yaml files remain valid under the v0.2 schema (new fields optional). Existing framework docs without the new frontmatter fields emit `WARN F18` (retrofit pending) — retrofit is opportunistic, not forced. No breaking changes to any protocol contract; new commands are additive.

The F19 canonicity-uniqueness check will surface the transitional command-inventory synchronization (4 places declared `synchronized_with` one another) until a single-source-of-truth `framework/command-registry.yaml` lands in a future release.

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
