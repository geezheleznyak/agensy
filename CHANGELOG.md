# Changelog

All notable changes to AGENSY are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Convention: each entry names the specific files changed (e.g., `framework/architecture-principles.md`) so readers can trace what `git log` would confirm.

---

## [2.7.0] — 2026-04-28

### Changed — System Model schema v0.4 → v0.6 (centralized cross-vault bindings)

Two schema bumps shipped together. v0.5 deprecated `paired_with` with on-the-fly derivation; v0.6 took the architectural step v0.5 prepared for: relocate cross-vault binding data out of per-vault `system-model.yaml` files into a single central file. Vaults at `schema_version: 0.6` have no `cross_vault_bindings:` section.

- `framework/system-model/system-model-schema.yaml` — bumped `schema.version` `0.4` → `0.6`. Added `v0_5_motivation` and `v0_6_motivation` blocks. The `cross_vault_bindings_*` field lists are kept (pre-v0.6 vaults still parse) but documented as relocated. New v0.5 + v0.6 validation rules. Extensibility note bumped: v0.5 candidates that shipped — `paired_with` deprecation + on-the-fly derivation; v0.6 candidates that shipped — central-file relocation; v0.7 reserved — node quality/confidence, edge weight.

- `framework/system-model/cross-vault-bindings-schema.yaml` — **NEW**. Canonical schema for the central `cross-vault-bindings.yaml` file. Per-bridge structure: `contributions[vault_short]` carries `self_declared` (this vault's own claim) + `peer_views[claimer]` (what other vaults claim this vault contributes). Both perspectives are preserved — no information loss. `mechanism_pairings` live at the bridge level with explicit `claimer:` field. Defines the audit signals produced from this file (`unratified_peer_views`, `binding_drift`, `mech_failures`, `mech_broken_refs`, `mech_divergences`).

- `tools/system-audit.py` — `TOOL_VERSION` `0.1.0` → `0.3.0`. `EXPECTED_SCHEMA_VERSION` `0.4` → `0.6`. New helpers `load_central_bindings()`, `synthesize_local_bindings()` (projects central file into the per-vault binding view), `check_unratified_peer_views()` (single informational class collapsing five v0.5 classes), `populate_peer_models_by_short()` (pre-loads peer models so `<peer>.<pattern_id>` mechanism_pairings refs resolve under v0.6). `count_substrate_pairings()` reads from the central file. Removed v0.5 helpers `compute_paired_with_for_binding`, `classify_binding_strip_safety`, `compute_claims_about_me`, `index_local_by_bridge`. Summary line: `pw_unratified=N claims_about_me=N safe_to_strip=N` collapses to `unratified_peer_views=N`. `find_framework_root()` now prefers script-relative resolution over sibling-walk (was inconsistent for adjacent framework mirrors).

- `framework/universal-commands/system-audit.md` — Step 5 rewritten to describe the v0.6 central-file flow. Step 9 informational-counts list collapses five v0.5 classes (`paired_with_unratified`, `claims_about_me`, `bindings_safe_to_strip`, `bindings_unratified`, `bindings_selectivity_loss`, `bindings_mixed`, `bindings_derived_only`) into one (`unratified_peer_views`). Summary line trailing fields updated.

- `framework/universal-commands/system-bridge.md` — Runtime inputs now include the central bindings file. Step 2 reads from the central file's `contributions[this_vault]` block. Step 4 candidate template emits v0.6 central-file shape.

- `framework/universal-commands/system-build.md` — Bootstrap skeleton updated: `schema_version: 0.6` and no `cross_vault_bindings:` section. `add-binding` mode now writes to the central file (under `bindings[].contributions[this_vault].self_declared`); peer claims are added under `contributions[peer].peer_views[this_vault]`; mechanism_pairings carry an explicit `claimer:` field at the bridge level.

### Backward compatibility

Pre-v0.6 vaults parse cleanly under the v0.6 audit (the per-vault `cross_vault_bindings:` section is preserved when no central file exists; the central file takes precedence whenever a bridge appears there). Schema-version mismatch is INFO not WARN for vaults at 0.1, 0.2, 0.3, 0.4, or 0.5. The five v0.5 informational audit classes are retired — vaults that surfaced them under v0.5 now see a single `unratified_peer_views` count instead.

### Migration guidance

For existing single-vault users (the common case): bump `system-model.yaml` `schema_version` to `0.6`. No further action — no central file is needed until you have multi-vault cross-vault bindings to declare.

For multi-vault users with existing `cross_vault_bindings:` sections across vaults: a one-shot consolidation moves the data into a single `cross-vault-bindings.yaml` at the framework root. Per-vault sections are then removed. The v0.6 central-file shape is documented in `framework/system-model/cross-vault-bindings-schema.yaml`. Validate post-migration with `python tools/system-audit.py [vault]` — node/edge/pattern/binding counts and dirt levels should be unchanged.

The v0.5 `paired_with` deprecation path (with derivation, `paired_with_unratified`, `claims_about_me`, etc.) is superseded — the central-file structure makes both `self_declared` and `peer_views` explicit, so the visibility kludges those signals provided are no longer needed.

### Substrate pairings semantics shift

Under v0.5, `substrate_pairings` counted `(local_patterns × explicit_paired_with[peer].patterns)` OR `(local_patterns × derived[peer].patterns)`. Under v0.6 the equivalent is `(self_declared.local_patterns × effective_peer_patterns)` where `effective_peer_patterns = self_declared.local_patterns ∪ peer_views[*].patterns`. Numerically larger than v0.5 counts; informational only.

---

## [2.6.0] — 2026-04-27

### Added — Two helper scripts for protocol-deterministic halves

Mechanical reconciliation scripts that execute the deterministic halves of `/system-audit` and `/coverage-audit`. Both follow the same pattern: read-only, JSON or human output, scope of executed-vs-deferred steps explicit in the JSON. Steps requiring judgment (corpus heuristics, narrative synthesis, prioritization) remain with the agent.

- `tools/system-audit.py` — implements protocol Steps 1, 2, 3, 4A, 5, 5b-typematch, and 9 of `/system-audit`. CLI: positional vault path + `--json --verbose --baseline {save|compare} --schema --bridges --peer-root`. Exit codes 0/1/2/3 (green/yellow/red/error). Emits the canonical `SYSTEM_AUDIT_SUMMARY:` line that `/coverage-audit` Step 9 parses (`unref=0` is a sentinel; the agent overwrites with the real count after Step 4B). PyYAML required.
- `tools/coverage-audit.py` — implements protocol Steps 1, 2, 3, 4, 7 (with `--write-note-index`), and 8-numeric of `/coverage-audit`. CLI mirrors system-audit's pattern. Exit code 0 (success) or 3 (invocation error). Defensive parsers for the Domain Summary `Target T2` column and the `## Planned Notes` section never crash on format variation; instead they emit a `parse_status` field. PyYAML not required (stdlib-only).
- `tools/_vault_utils.py` — shared parsing layer extracted from `tools/vault-linter.py` to support multiple consumers. Houses `VaultConfig`, `parse_frontmatter`, `discover_notes`, `classify_for_coverage`, `get_note_domain`, `build_link_index`, plus module-level constants `MAP_SUFFIXES`, `INFRA_PATTERNS`, `BASE_FIELDS`, `STOPWORDS`. Underscore prefix marks the module private to the `tools/` package — not a stable API. Two new optional flags on `discover_notes`: `include_infrastructure_maps`, `include_t3_output` (both default `False` to preserve linter behavior).

### Fixed

- `tools/_vault_utils.py::VaultConfig._tier_value()` — the prior lazy-with-lookahead regex (`(?:(?!  \w).)*?`) returned empty strings for `tier1_type` / `tier2_type` / `tier3_type` across all vaults because the lookahead failed on 4-space-indented body lines. Replaced with `[\s\S]*?` bounded by the next 2-space block-key. **Side effect**: `vault-linter`'s `classify_note` now correctly classifies untyped notes located outside `tier3_output` as tier2 (was: tier3, because `'' == ''`). For training vaults that store atomic concepts in a non-T3 folder, this eliminates the false-positive A17 ("Tier 3 not in output folder") error class — observed drop in one test vault was 251 issues (~31% of total). No other check codes are affected.

### Changed — Protocol amendments

- `framework/universal-commands/system-audit.md` — adds Step 0 documenting the optional helper-script fast path. Steps 1–9 unchanged and remain authoritative. Fallback contract: if the script is missing, fails to import PyYAML, or exits with code 3 (invocation error), the protocol's manual path applies.
- `framework/universal-commands/coverage-audit.md` — adds Step 0, same pattern.

### Changed — Refactor

- `tools/vault-linter.py` — extracted `VaultConfig`, frontmatter helpers, `discover_notes`, `build_link_index`, and the shared constants to `tools/_vault_utils.py`. Linter now imports from there. Pure cut-and-move; all check codes (A01–A18, B01–B08, G01–G04) continue to fire identically. File shrunk from 1238 → 820 lines.

### Backward compatibility

Additive minor release. All changes additive at the protocol level; vaults can adopt the helper scripts when convenient. The `_tier_value` regex fix is a bugfix — vaults with linter regression baselines will see fewer A17 false-positive issues; regenerate baselines after this release if needed.

The new `_vault_utils.py` module is private (underscore-prefixed) and is not a stable API. External consumers should not import from it.

### Migration guidance

No mandatory action. Coverage-audit and system-audit protocols still run end-to-end without the scripts. To use the fast path, ensure PyYAML is installed (`pip install pyyaml`) for system-audit; coverage-audit is stdlib-only.

---

## [2.5.0] — 2026-04-26

### Changed — System Model schema v0.3 → v0.4 (binding-kind disambiguation)

- `framework/system-model/system-model-schema.yaml`: bumped `schema.version` to `0.4`. Added `mechanism_pairings` to `cross_vault_bindings_optional_fields`. New `mechanism_pairings_schema` block specifies `required_fields: [local, peers]` + optional `rationale`. Added v0.4 validation rules and a `v0_4_motivation` paragraph documenting the binding-kind disambiguation. Extensibility note bumped: v0.4 candidates that shipped — `mechanism_pairings`; v0.5 reserved — node quality/confidence, edge weight.

- `framework/universal-commands/system-audit.md`: Step 5b rewritten. Step 5b now fires ONLY on pairings explicitly declared in a binding's `mechanism_pairings[]` list. Cross-products of `local_patterns × paired_with[v].patterns` not in `mechanism_pairings` are treated as implicit substrate overlap and skipped silently. Issue counters renamed: `binding type-mismatch` (v0.2-v0.3) becomes `mechanism-pairing failures` + `mechanism-pairing broken refs`; new informational counters `mechanism-pairing divergences` and `implicit substrate pairings`. Step 7 report format updated; Step 9 dirt-level rule updated (mechanism-pairing failures replace `binding type-mismatch` as the cross-vault drift trigger; informational counts excluded from the "issue count > 5" rule). One-line summary fields renamed accordingly. Migration note added for v0.3 → v0.4 readers: pre-v0.4 yamls produce zero mechanism-pairing failures (correct: no claims were made).

- `framework/system-model/primitives.md`: Pattern-Name Warning section rewritten with explicit substrate-vs-mechanism distinction. New "Rule (updated for v0.4)" replaces the v0.2 rule and specifies that bindings are substrate-by-default; mechanism alignment requires explicit `mechanism_pairings[]` declaration. Annotation discipline section added.

- `framework/system-model/system-model-architecture.md`: cross-vault binding paragraph rewritten to describe the two distinct kinds of cross-vault relation (substrate overlap as the default; mechanism alignment as the rare exception via explicit `mechanism_pairings[]`).

- `CLAUDE.md`: vault-structure tree updates `system-model-schema.yaml` version from `v0.3` to `v0.4`.

### Backward compatibility

All v0.1, v0.2, and v0.3 yamls remain valid against the v0.4 schema. The new field is optional. Pre-v0.4 bindings with no `mechanism_pairings[]` produce zero mechanism-pairing failures under v0.4 audit semantics — correct, because no mechanism alignment claims were made by those bindings.

The legacy `binding type-mismatch` warning class from v0.2-v0.3 is retired. Audit reports under v0.4 emit `mechanism-pairing failures` and `mechanism-pairing broken refs` instead. Downstream consumers of audit summary lines (e.g., `/coverage-audit` Step 9 capture) should update their parsers — the summary line field names changed (`type_mismatch` → `mech_failures`, plus new `mech_broken_refs` and `substrate_pairings` fields).

### Migration guidance

Additive minor release — no mandatory action. To gain back mechanism validation on a binding under v0.4, declare the genuine alignments in `mechanism_pairings[]`. Aspirational or weak pairings should not be declared — substrate is the right default.

---

## [2.4.0] — 2026-04-26

### Added — Learner Layer Phase A.1 (First-Use Gate + `/learner-profile` command)

Phase A.1 was authored 2026-04-24 alongside Phase B but did not ride along in the v2.2.0 release. This release ships it.

- `framework/universal-commands/learner-profile.md`: new universal command — `/learner-profile [init | revise | status]`. Bootstraps or revises the cross-vault learner profile via propose-confirm Q&A on the seven L1–L7 bedrock sections. Reads no `vault-config.md`; operates on `agensy/learner/` directly. Same pattern as `/question-bank` and `/positions`. Exists to unblock the First-Use Gate on hard-gate Learner-Layer-aware commands (`/teach`, `/curriculum`, future `/recall`).

- `framework/principles/learner-layer-architecture.md`: adds new **First-Use Gate** section (~60 lines). Defines hard-gate vs. soft-gate command behavior when `learner-profile.md` is missing or empty. Hard-gate commands (`/teach`, `/curriculum`, `/recall`) **refuse** and redirect to `/learner-profile init`. Soft-gate commands (`/dialogue`, `/what-next`, `/positions`, `/article-promote`) **warn, log the gap, and proceed**. Specifies the `## Step 0 — First-use gate` block every Learner-Layer-aware command must contain. Frontmatter `canonical_for` extended with `learner_first_use_gate`.

### Changed

- `framework/slash-command-suite.md`: count line bumps from "34 protocol files + 2 backward-compat aliases" to "35 protocol files + 2 backward-compat aliases"; categories tally adds "+ 1 learner-layer". `/learner-profile [init|revise|status]` row added to the universal-command table. New paragraph below the System Model Layer paragraph registering the Learner Layer command (Phase A.1, 2026-04-24).

- `tools/framework-verify.py`: `COMMAND_REQUIRED_KEYS` dict gains a new Learner Layer section with the `learner-profile` entry (cross-vault, no required keys — operates on `agensy/learner/` directly).

- `CLAUDE.md`: vault-structure tree updates `slash-command-suite.md` and `universal-commands/` count lines to 35; category breakdown adds `+ 1 learner-layer`.

### Migration guidance

Additive minor release. Existing Learner-Layer-aware commands gain soft-gate Step 0 in their protocols when next updated; future hard-gate commands inherit the gate from authoring time. No mandatory action for existing vaults — the new `/learner-profile` command simply becomes available wherever `agensy/learner/` exists. Vaults without the Learner Layer adopted (no `learner/` directory) see zero behavior change.

If you want to use Phase A.1:

1. Adopt v2.1.0+ first (Learner Layer bedrock — `learner-layer-architecture.md` + template + schema v0.3).
2. Run `/learner-profile init` (or `/learner-profile status` if you already authored a profile manually). Init walks L1–L7 in propose-confirm, writes `learner-profile.md` at `status: seeded-v0.1`.
3. Hard-gate commands like `/teach` and `/curriculum` (vault-specific in training vaults; deferred-Phase-C universal versions) now refuse cleanly when the profile is missing rather than producing un-tailored output.

### Notes

The Phase A.1 work is small and additive but load-bearing for the `/teach` and `/curriculum` hard-gate behavior — releasing it now unblocks any downstream vault that wants to author training-vault commands per the v2.3.0 phase-learning-methodology template's atomicity-drift safeguards.

---

## [2.3.0] — 2026-04-25

### Added — Training-vault phase-learning-methodology template

A new universal template at `framework/vault-type-templates/training/phase-learning-methodology-template.md` codifying the methodology doctrine for any training vault — what was previously implicit in `synthesis_bellum`'s vault-local instance is now explicit and reusable. Abstracted from `synthesis_bellum`'s proven instance (2026-03-08) and amended through the `synthesis_mathesis` KL-divergence failure case (2026-04-24): a teaching session that tried to inline six prerequisite concepts into one lesson, demonstrating that the vault-local methodology — sound in its rules — was missing two safeguards that this template now codifies.

- `framework/vault-type-templates/training/phase-learning-methodology-template.md`: new template. Contains:
  - **Atomicity Principle** — one idea = one note; four atomization tests (downstream link, stand-alone gate, framework decomposition, principle list).
  - **Phase Inventory mandatory-first-step rule** — full atomic inventory + dependency DAG before a single note is written. Protection against scope gap.
  - **Atomicity Drift Hard Stop ("the KL-failure pattern")** — new safeguard. Mid-`/teach`, if Claude finds itself defining a second atomic concept inline, stop and announce a graph update. Never bundle.
  - **Prerequisites-as-Absent Override** — new safeguard. When `learner-profile.md` L2 declares "treat prerequisites as absent unless demonstrated," the cadence's pre-flight check is mandatory and non-skippable.
  - **The `/teach` Cadence — 7-step loop** — Step 0 (silent context read) → Step 1 (frontier selection) → Step 2 (pre-flight check) → Step 3 (teach one atom) → Step 4 (verification gate: Feynman-back + diagnostic) → Step 5 (atomic note authoring) → Step 6 (bookkeeping). Session-complete gate has 4 conditions.
  - **Frontier Marker Schema** — universal `phase-status.md` field schema (`current_phase`, `current_stratum`, `last_completed_atom`, `next_reachable_set`, `pending_reinforcements`, per-phase exit checklist). Single source of truth for "where am I."
  - **Phase Production Protocol** — 8-step protocol for opening a new phase (read phase doc → inventory + DAG → identify merges → identify recommended-readings map work → initialize frontier → run `/teach` cadence → build maps → completion check).

- `framework/vault-type-templates/training/README.md`: updated to register the new template (4th row in the Template table) and to add it as step 4 in the Order of Fill (last to instantiate, just before Phase 0 begins).

### Changed

- The `Order of fill` section reorders: `sources-master-list.md` is now step 3 (was "last"); `phase-learning-methodology.md` is the new step 4 ("last (before Phase 0 begins)"). Functional change for any training-vault genesis: instantiate methodology before the first `/teach` session.

### Migration guidance

Additive minor release. No mandatory action for existing training vaults. `synthesis_bellum`'s vault-local `phase-learning-methodology.md` (authored 2026-03-08, predating this template) continues to operate unchanged — the rules in the template are the same rules, plus the two new safeguards. Optional adoption path:

1. Read the new template at `framework/vault-type-templates/training/phase-learning-methodology-template.md`.
2. Compare to your vault-local methodology doc.
3. Copy the **Atomicity Drift Hard Stop** and **Prerequisites-as-Absent Override** sections into your local doc, plus the §`/teach` Cadence and §Frontier Marker Schema sections.
4. (Optional) Author a `phase-status.md` at your vault root using the universal schema.
5. (Optional) Refactor your local doc to follow the template's section order.

The two new safeguards are valuable specifically for training vaults where the user is acquiring a domain from zero (rather than vaults where the user is mature and synthesizing). They are most visible when the user has explicitly tightened `learner-profile.md` L2 to "treat prerequisites as absent."

### Notes

This release is the first time the framework codifies methodology that was previously vault-local. Before this, `synthesis_bellum`'s methodology doc was a one-off; the template extraction makes it canonical and discoverable for new training vaults at genesis. The training-vault template directory now has 4 templates (curriculum, principles-and-postulates, sources-master-list, phase-learning-methodology) covering the full substrate a training vault needs beyond the universal genesis skeleton.

---

## [2.2.0] — 2026-04-24

### Added — Learner Layer Phase B (trajectory + interest capture)

Wires the Learner Layer (declared in v2.1.0) into the four protocols that produce its data. All extensions skip themselves entirely if a `learner/` directory does not exist at the user's vault-collection root — vaults without Learner Layer adoption see zero behavior change. All writes follow the propose-confirm pattern: Claude detects candidate, proposes entry, user accepts or edits before any file is written.

- `framework/universal-commands/dialogue.md` Step 7 — trajectory delta + interest signal capture. Detects confidence shifts, recurring questions, stuck signals; proposes one entry to `learner/learning-trajectory.md` if anything trajectory-significant happened. Detects interest declarations ("I want to understand X better"); proposes entries to `learner/interests-register.md`. Tail-reads trajectory (~10 entries), grep-only on interests-register — token-budget bounded.

- `framework/universal-commands/what-next.md` Step 4.5 — readiness check + learner context. Loads `learner/learner-profile.md` for current obsessions, formal maturity, learning style calibration. Greps `learner/interests-register.md` for matching active interests (boost). Walks `system-model.yaml` `user_engagement` annotations to detect prerequisite gaps; deprioritizes (does NOT eliminate) candidates with `unseen` prereqs and surfaces the gap explicitly so the user can override.

- `framework/universal-commands/positions.md` Step 3 — mastery state annotation per position. 4-state ladder (`mastered | applied | contested | exploratory`) cross-referenced against `learning-trajectory.md` recent shifts and corresponding `system-model.yaml` `user_engagement` annotations. Conservative downgrade rule: when uncertain, choose more conservative state. Step 5 output gains a per-domain mastery distribution row.

- `framework/universal-commands/article-promote.md` Step 7.6a — interests-register harvest. After the existing claim harvest (7.3–7.5), an additional pass for interest declarations in the essay body ("deserves separate treatment", "I should look more deeply into W"). Proposes entries to `learner/interests-register.md` with `Follow-through: [[essay-path]]` linkback. Frontmatter `harvest:` block extended with `interest_harvests:` list.

### Documentation

- `CLAUDE.md`: directory tree updated to reflect v2.0.0 reorg subdirs (catch-up; was missed in 2.0.0) AND adds optional `learner/` subdir entries. Adds **Task 4: Maintain the Learner Layer** with the propose-confirm rules and per-extension references.
- `docs/concepts.md`: new **Learner Layer** section covering the three artifacts, propose-confirm discipline, token-budget rules, opt-in adoption path, and relationship to System Model + logos writer-positions/voice-profile patterns.
- `docs/commands.md`: per-command Learner Layer extension notes added to `/dialogue`, `/what-next`, `/positions`, `/article-promote`. Each note explains what the extension adds when `learner/` is present.
- `README.md`: adds new "What it solves" bullet — *"My agent doesn't know me — every session starts cold"* — pointing at the Learner Layer.

### Migration guidance

This is an additive minor release. No vault-side action required for v2.2.0 adoption. The Learner Layer extensions to all four protocols are gated on the existence of a `learner/` directory at the user's vault-collection root — adoption is opt-in.

If you want to use the Learner Layer:
1. Adopt v2.1.0 first (the layer's bedrock — `learner-layer-architecture.md` + template + schema v0.3).
2. Author your own `learner-profile.md` from `framework/templates/learner-profile-template.md`.
3. Initialize empty stubs at `learner/learning-trajectory.md` and `learner/interests-register.md` (use the format headers from the meta versions as a guide, or copy from any reference setup).
4. Optionally annotate ~10–30% of your `system-model.yaml` nodes with `user_engagement` and `last_engaged`.
5. From v2.2.0 forward, the four extended commands (`/dialogue`, `/what-next`, `/positions`, `/article-promote`) automatically pick up your Learner Layer artifacts.

### Notes

`learner/` user data (profile, trajectory, interests-register, archives) remains private and is excluded from the public mirror by design — same exclusion pattern as `memory/`. The four protocol extensions in this release are the framework-side instructions for *how* Claude maintains the layer; the layer's actual contents are user-specific and live in each maintainer's working directory.

---

## [2.1.1] — 2026-04-24

### Removed

- `framework/protocols/agensy-sync-protocol.md`: removed from agensy. This file is **meta-only by design** — it describes the upstream meta→agensy publish workflow, which is internal maintainer documentation, not framework-user documentation. Public agensy users do not consume agensy from upstream; they ARE downstream. Shipping the publish workflow added irrelevant noise to the public surface.

### Fixed

- v2.1.0 erroneously included this file based on an outdated self-reference inside the file's own mapping table. The mapping table on the meta side has been corrected: `agensy-sync-protocol.md` now lives in the "Never synced" section with explicit rationale, so this mistake will not recur.

### Migration guidance

If you had any local references or scripts pointing at `agensy/framework/protocols/agensy-sync-protocol.md` (you almost certainly did not — the file existed in agensy for less than one release), remove them. There is no replacement to point at; the file was never intended for downstream consumption.

---

## [2.1.0] — 2026-04-24

### Added — Learner Layer

A new horizontal framework layer that captures the user as a learner-in-progress (acquisition trajectory, struggle signals, interest declarations, per-concept mastery). Sits parallel to the System Model layer: System Model describes the structural shape of each vault's domain; Learner Layer describes the user's traversal of those domains over time. Mirrors the logos writer-positions/voice-profile pattern (user-authored bedrock + Claude-curated trajectory + propose-confirm for all writes), applied to learning rather than authoring.

- `framework/principles/learner-layer-architecture.md`: new file declaring the layer. Covers three artifacts (`learner-profile.md`, `learning-trajectory.md`, `interests-register.md`), curation discipline (propose-confirm pattern; Claude proposes, user accepts or edits before any file is written), token-budget rules (none of the new artifacts auto-load at session start; loaded only by commands that explicitly need them), integration with System Model and the logos writer-positions/voice-profile pattern, and what-it-is-NOT boundaries. The user-data side of the layer (`learner/learner-profile.md`, etc.) lives in each user's working directory, not in agensy — mirrors the `memory/` exclusion pattern.
- `framework/templates/learner-profile-template.md`: new fill-in-the-blanks template for the user-authored bedrock. Seven sections: formative thinkers and traditions (L1), formal/mathematical maturity (L2), languages (L3), current obsessions 3–7 active threads (L4), taboo areas (L5), learning style (L6), goals at 6mo / 2yr / 10yr horizons (L7). Hard cap: 300 lines; deeper sections graduate to `learner/learner-topics/`.

### Changed

- `framework/system-model/system-model-schema.yaml`: v0.2 → v0.3. Adds optional `user_engagement` enum (`unseen | surfaced | applied | mastered` — four-state mastery ladder) and `last_engaged` (YYYY-MM-DD) fields to nodes AND patterns. Sparse by default — annotate only nodes/patterns the user has actually engaged with; do NOT pre-fill `unseen` markers. Backward-compatible: existing v0.2 vault system-models remain valid without modification. Schema-level addition consumed: was a v0.3 candidate; now shipped. Schema validation rules added: `user_engagement` value must be in `user_engagement_states`; `last_engaged` required when `user_engagement` is set; `last_engaged` without `user_engagement` is a violation.
- `framework/principles/architecture-principles.md` §1 "The System in Brief": registers the Learner Layer as the second horizontal framework layer (parallel to the System Model layer), with a one-paragraph note describing its scope, its parallel relationship to the logos writer-positions/voice-profile pattern, and its loading discipline (none of its artifacts auto-load at session start).
- `framework/protocols/agensy-sync-protocol.md`: §1 mapping table updated. (a) Added `framework/principles/learner-layer-architecture.md` and `framework/templates/learner-profile-template.md` to the Copy 1:1 list. (b) Added `learner/` to the Never-synced list with explicit reason: user-as-learner data is private and structurally parallel to `memory/`; framework documents declaring the layer DO sync, the user's actual learner data does NOT. (c) Pre-existing oversight fix: added `framework/principles/framework-meta-architecture.md` to the Copy 1:1 list (was already being synced in practice but not listed).

### Migration guidance for downstream consumers

This is an additive minor release. No vault-side action required for v2.1.0 adoption.

If you maintain a vault `system-model.yaml`: the v0.3 schema is fully backward-compatible. You can continue using v0.2 conventions indefinitely. To adopt the new annotation, add `user_engagement: <state>` and `last_engaged: <date>` to nodes or patterns the user has actually engaged with — sparsely, not exhaustively. Default state for unannotated entries is implicitly `unseen`; do not pre-fill the YAML with `unseen` markers.

If you want to use the Learner Layer in your own setup: copy `framework/templates/learner-profile-template.md` to a new `learner/` subdirectory at your vault-collection root, fill in the seven sections (Q&A-style with Claude is the intended workflow), and configure Claude to load it only via commands that explicitly need it (mirrors the logos writer-positions/voice-profile loading pattern). The `learner/` subdirectory should be excluded from any public mirror or share — it's user-specific intellectual self-portrait data, equivalent in privacy to `memory/`.

Phase B of the Learner Layer (trajectory capture extensions to `/dialogue`, `/what-next`, `/positions`, plus pilot `user_engagement` backfill on a single vault) is a separate forthcoming release.

### Notes

Schema-level additions log: v0.2 candidates that shipped — `timescale`, `subtype`, `secondary_types`. v0.3 candidates that shipped — `user_engagement`, `last_engaged`. Reserved for v0.4 — node `quality`/`confidence`, edge `weight`.

---

## [2.0.0] — 2026-04-24

### ⚠ BREAKING — Framework Directory Reorganization

The flat `framework/` directory has been reorganized into five semantic subdirectories. Every reference to a framework document by path must be updated. The files themselves are unchanged in content; only their locations have moved.

**Migration table** (the only thing downstream consumers need):

| Old path | New path |
|---|---|
| `framework/architecture-principles.md` | `framework/principles/architecture-principles.md` |
| `framework/system-contracts.md` | `framework/principles/system-contracts.md` |
| `framework/system-architecture.md` | `framework/principles/system-architecture.md` |
| `framework/framework-meta-architecture.md` | `framework/principles/framework-meta-architecture.md` |
| `framework/genesis-protocol.md` | `framework/protocols/genesis-protocol.md` |
| `framework/inter-vault-protocol.md` | `framework/protocols/inter-vault-protocol.md` |
| `framework/command-lifecycle.md` | `framework/protocols/command-lifecycle.md` |
| `framework/vault-config-schema.md` | `framework/templates/vault-config-schema.md` |
| `framework/claude-md-template.md` | `framework/templates/claude-md-template.md` |
| `framework/note-tier-template.md` | `framework/templates/note-tier-template.md` |
| `framework/map-type-template.md` | `framework/templates/map-type-template.md` |
| `framework/map-to-article-extraction.md` | `framework/templates/map-to-article-extraction.md` |
| `framework/system-model-architecture.md` | `framework/system-model/system-model-architecture.md` |
| `framework/system-model-schema.yaml` | `framework/system-model/system-model-schema.yaml` |
| `framework/primitives.md` | `framework/system-model/primitives.md` |

**Unchanged** (stay at their existing location):
- `framework/slash-command-suite.md` — the index file, stays at `framework/` root
- `framework/universal-commands/*` — already a subdirectory, all 34 protocol files + 2 aliases unchanged
- `framework/vault-type-templates/*` — already a subdirectory, all substrate files unchanged
- `docs/architecture-diagrams.md` — outside framework/, unchanged

### Subdirectory rationale

| Subdir | Holds | Role |
|---|---|---|
| `principles/` | architecture-principles, system-contracts, system-architecture, framework-meta-architecture | The WHY layer — invariants, contracts, topology, doc-system rules |
| `protocols/` | genesis-protocol, inter-vault-protocol, command-lifecycle | Step-by-step procedures |
| `templates/` | vault-config-schema, claude-md-template, note-tier-template, map-type-template, map-to-article-extraction | Fill-in-the-blanks templates and schemas |
| `system-model/` | system-model-architecture, system-model-schema, primitives | The System Model layer — domain ontology vocabulary and schema |

The flat structure had grown to 14 markdown files plus 2 subdirectories at one level, making the layer affiliation of each doc unclear at a glance. The semantic grouping makes the reading-order spine ("read principles/ first, then protocols/, …") visible from the directory tree alone.

### Changed

- All ~80 internal cross-references across `framework/`, `docs/`, `tools/framework-verify.py`, `vault-registry.md`, `cross-vault-bridges.md`, `CLAUDE.md`, `CONTRIBUTING.md`, and `.claude/commands/new-vault.md` updated to use the new subdir paths. Frontmatter fields (`synchronized_with`, `derives_from`, `supersedes`) updated in moved files.
- `tools/framework-verify.py`: 4 hardcoded Path-joined constants (F15, F16, F17, F20 callbacks) updated to traverse the new subdirs. All 6 categories of architectural integrity checks remain functional.

### Migration guidance for downstream consumers

If you have:
- **Scripts that reference framework docs by path**: apply the migration table above
- **Custom CLAUDE.md files referencing framework docs**: same
- **Forks of the agensy framework**: rebase your patches onto the new structure (file content unchanged, only paths moved)
- **Mental model only**: nothing to do — the framework's semantics, contracts, and protocols are unchanged. The reorganization is purely organizational.

### Notes

This is a structural release — no behavioral, schema, or protocol changes. Doc count and content are identical to 1.2.2; only filesystem layout changed. The `git mv`-preserved history means `git log --follow framework/principles/architecture-principles.md` still shows the file's full evolution.

---

## [1.2.2] — 2026-04-24

### Added

- `docs/architecture-diagrams.md`: new file holding the four Mermaid topology diagrams (Complete System Map, Command Dispatch & Lifecycle, State Management & Feedback Loops, Genesis Protocol) — previously embedded inline in `framework/system-architecture.md`. Diagrams updated to reflect v1.2.0 reality: the 4-doc architectural spine (WHY/HOW/WHAT/META), vault-type-templates layer, expression-vault substrate subgraph, `/coverage-audit` → `/system-audit` auto-fire chain, article pipeline + companion mode, Doc 13 conditional substrate copy.

### Changed

- `framework/system-architecture.md`: Mermaid diagrams removed (~230 lines) and replaced with a pointer line to `docs/architecture-diagrams.md`. The YAML System Manifest remains in place as the canonical machine-readable topology. Split motivated by token economy — Claude reads the YAML manifest for structured analysis; the visual diagrams are for human orientation and don't need to be in Claude's reading chain for every framework-change pass.
- `framework/architecture-principles.md` §1 "The System in Brief": corrected stale command count (19 → 34 universal protocols + 2 backward-compat aliases), with the family breakdown (17 core + 4 system-model + 8 article-pipeline + 5 companion-co).
- `framework/system-architecture.md` YAML manifest `genesis_protocol.phase_1` block: added Doc 13 (conditional vault-type substrate copy for expression/training vaults); output description updated from "12 structural documents" to "12 universal + 1 conditional".
- `framework/system-contracts.md` §4 Structural Variants: added **Expression vault** row documenting the six substrate files, `reference_docs.*` runtime dependencies, the `/article-draft` voice-profile precondition, and the relaxed-domains convention.

### Notes

Documentation-only release (no protocol, schema, or tool changes). The Mermaid diagrams in `docs/architecture-diagrams.md` render natively in Obsidian; open the file for visual orientation. For Claude, the YAML manifest in `framework/system-architecture.md` carries the same topology in structured form and remains the canonical reference.

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
- `framework/system-model-architecture.md`: expanded Self-Maintenance Policy with three-layer staleness prevention and escalation rules; Rollout Status updated through Phase 5 (theoria universality test) with the bounded-universality result explicitly noted
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
  `framework/universal-commands/what-next.md`: replaced absolute upstream-meta paths with
  `[AGENSY_PATH]/...` and conceptual upstream-meta references with `agensy`

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
