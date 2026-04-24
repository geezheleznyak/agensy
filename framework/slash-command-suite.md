---
type: reference
audience: claude
---

# Slash Command Suite

Index of all commands across the synthesis vault system. **Source of truth for protocol logic**: universal commands live in `framework/universal-commands/[command-name].md`. Vault stubs in `.claude/commands/` are 3-line pointers — they contain no protocol logic.

**Command lifecycle and trigger types**: See `framework/command-lifecycle.md`.

---

## Stub Format

Every universal command has a thin stub in `[vault root]/.claude/commands/`:

```markdown
---
description: [one-line description]
---

# /[command-name] [args]

$ARGUMENTS

1. Read the protocol: `[AGENSY_PATH]/framework\universal-commands\[command-name].md`
2. Read vault configuration: `vault-config.md` (vault root)
3. Execute the protocol using this vault's parameters.
```

Vault-specific commands (unique to one vault) stay as full protocol files in `.claude/commands/`, but must read `vault-config.md` for parameters — no hardcoded vault values.

---

## Universal Commands (34 protocol files + 2 backward-compat aliases)

*17 core knowledge-work + 4 system-model + 8 article-pipeline + 5 companion-co. Full inventory below; the article-* and co-* rows are also repeated in the §Expression Vault Commands section for pipeline context.*

| Command | Trigger type | Protocol file |
|---|---|---|
| `/arc [subject] [type]` | User | `universal-commands/arc.md` |
| `/coverage-audit` | Milestone (15 notes) | `universal-commands/coverage-audit.md` |
| `/axis-survey` | Milestone (3+ T3 notes) | `universal-commands/axis-survey.md` |
| `/what-next` | Post audit / unclear intent | `universal-commands/what-next.md` |
| `/promote [note-path]` | Post domain-audit | `universal-commands/promote.md` |
| `/compare [s1] and [s2] on [q]` | User | `universal-commands/compare.md` |
| `/engage-problem [N or name]` | User / post-audit gap | `universal-commands/engage-problem.md` |
| `/synthesis [question]` | User (2+ arcs in domain) | `universal-commands/synthesis.md` |
| `/update-moc [moc-name]` | Auto (post-arc) | `universal-commands/update-moc.md` |
| `/evergreen-note [concept]` | User | `universal-commands/evergreen-note.md` |
| `/engage-deep [claim]` | User / post-arc | `universal-commands/engage-deep.md` |
| `/domain-audit [domain-slug]` | Post arc | `universal-commands/domain-audit.md` |
| `/quick-check` | Auto (end of arc) | `universal-commands/quick-check.md` |
| `/dialogue [topic]` | User | `universal-commands/dialogue.md` |
| `/positions` | User (3+ dialogues) | `universal-commands/positions.md` |
| `/revisit [note-path]` | Milestone (30+ days) | `universal-commands/revisit.md` |
| `/question-bank [add\|list\|resolve]` | User | `universal-commands/question-bank.md` |
| `/system-query [query]` | User | `universal-commands/system-query.md` |
| `/system-audit` | Milestone (post coverage-audit) | `universal-commands/system-audit.md` |
| `/system-build [mode] [args]` | User | `universal-commands/system-build.md` |
| `/system-bridge [mode] [peer]` | User | `universal-commands/system-bridge.md` |

**Backward-compat aliases** (adversarial vaults only): `/confront` = `/engage-deep`, `/fault-line-survey` = `/axis-survey`

**System Model Layer commands** (v0.1): `/system-query` is always available where a vault has a `system-model.yaml`; `/system-audit` fires on the same cadence as `/coverage-audit`. `/system-build` is the only write path into `system-model.yaml` — read-only commands never mutate it. `/system-bridge` is a read-only binding reconciliation tool that proposes edits and routes writes through `/system-build`. All four registered 2026-04-20. See `framework/system-model-architecture.md`.

---

## Generated Commands by Vault Type

Added during Phase 1, Document 9 of the Genesis Protocol. These live as full protocol files in `.claude/commands/` — they are vault-type specific and NOT in `universal-commands/`. Commands marked (→ universal) are now universal and stubs point to `universal-commands/` instead.

### Accumulation Vault Commands

**`/engage-deep [thinker/concept/claim]`** → see `universal-commands/engage-deep.md` (now universal)
*Note: adversarial vaults may also invoke as `/confront` (alias).*

**`/derive [step in derivation]`**
Attempt one step in the vault's core derivation (e.g., cosmology → anthropology → ethics). Protocol:
1. State the step: what does the derivation need to establish?
2. List vault notes that bear on this step
3. State the strongest available argument from vault material
4. State what is still missing (the gap the next arc should fill)
Output: structured derivation note in `00-Inbox/`

### Training Vault Commands

**`/wargame [scenario]`**
Generate a CPX/exercise training document. Protocol:
1. Establish scenario context (force, mission, theater, adversary)
2. Generate 5–7 decision points in sequence
3. For each decision point: situation → information available → options → model answer → key lesson
4. Identify which curriculum phase each decision point belongs to
Output: complete training document in `50-Curriculum/` or equivalent

**`/red-team [concept/plan]`**
Adversarial analysis. Protocol:
1. State the concept or plan to be red-teamed
2. Decompose its core assumptions (3–5 assumptions)
3. For each assumption: state the strongest counter-move an intelligent adversary would make
4. Identify which friction condition is most likely to break the concept
5. State what modifications would make the concept more robust
Output: red-team analysis in `00-Inbox/`

**`/stress-test [concept]`**
Systematic friction testing. Protocol:
1. State the concept
2. Test against each of 5 friction stressors: fog, friction, fear, fatigue, adaptive adversary
3. For each stressor: describe how the concept performs; where it breaks; what the failure mode is
4. State the fault-line position of the concept under stress
Output: stress-test analysis in `00-Inbox/`

### Expression Vault Commands

**Map-to-Article Pipeline** (registered 2026-04-21; V1.5 preset-aware update 2026-04-21; V1.6 position index & harvest loop 2026-04-21; V1 = Type A solo-map essays only; Types B/C/D deferred to V2)

The article-* pipeline turns argument-dense source-vault maps into published essays. Protocols live in `universal-commands/article-*.md`; cogitationis is the consumer. Each command reads `vault-config.md` (cross_vault_dependency.source_vaults), `voice-profile.md` (style layer), `writer-positions.md` (substance layer, bedrock), and — as of V1.5 — `article-presets.md` (three-axis preset registry). V1.6 adds `positions-index.md` (pre-loaded cross-vault pointer table to substantive claims earned in prior essays; T3 bodies loaded on-demand). Pipeline: `/article-scan → /article-seed → /article-outline → /article-draft → /article-revise → /article-promote`.

**Preset-aware commands (V1.5)**: `/article-seed`, `/article-outline`, `/article-draft`, `/article-revise` consume the active essay's preset (recorded in seed/essay frontmatter). `/article-scan` and `/article-promote` remain preset-agnostic.

**Position-aware commands (V1.6)**: `/article-seed` Step 2.6 greps `positions-index.md` by source-map keywords, loads matched T3s, records `matched_positions` in seed frontmatter (with `relation`: supports / extends / tensions-with / orthogonal). `/article-outline` Step 3.5 reserves argument-move slots for matched positions (required slot in pressure section for `tensions-with`). `/article-revise` Pass C runs two-layer check — bedrock `writer-positions.md` (hard) + matched positions (soft; surfaced, not silently corrected). `/article-promote` Step 7 runs the harvest loop — diffs essay claims against source-map atomics + matched T3s, classifies novel claims (substantive framework claim → new T3 + positions-index row; methodological claim → append to writer-positions; essay-specific → no promotion), user-confirms each, executes accepted promotions.

| Command | Protocol | Inputs | Outputs | Preset role (V1.5) | Position role (V1.6) |
|---|---|---|---|---|---|
| `/article-scan [vault]` | `universal-commands/article-scan.md` | source vault name | readiness table → `source-map-registry.md` (5-axis score 0–25) | none | none |
| `/article-seed [map-path(s)] [type] [--preset <id>]` | `universal-commands/article-seed.md` | 1 map path + `A` (V1 only) + optional preset flag | seed note in `10-Thoughts/` with thesis, claims, pressure, stakes, preset, matched positions | Step 2.5 infers preset from thesis-candidate grammar (or accepts `--preset`); records in frontmatter | Step 2.6 greps positions-index by source-map keywords; loads matched T3s; records `matched_positions` with relation classification |
| `/article-outline [seed-path]` | `universal-commands/article-outline.md` | seed note | outline in `20-Essays/` at `status: outline`; preset blueprint imposed; position treatments decided | Reads preset; instantiates opening paragraph beats, body arc, pressure required-slots, closing type per `article-presets.md` | Step 3.5 reserves argument-move slots for `supports`/`extends`; adds required pressure slot for `tensions-with`; records `matched_position_treatments` |
| `/article-draft [essay-path]` | `universal-commands/article-draft.md` | outline note | draft at `status: draft`; voice + positions applied; wikilinks resolved | Fills preset opening/pressure/closing shapes during per-section drafting | Treats matched positions as soft constraints during drafting |
| `/article-revise [essay-path]` | `universal-commands/article-revise.md` | draft note | revised at `status: revision`; 6 passes (adversarial) or subset (light/creative) | Pass E extended with preset-fidelity sub-pass + P3 category-error audit (`orthodoxy-counter` + `framework-build`) | Pass C two-layer: bedrock `writer-positions.md` (hard) + matched-position T3s (soft); soft violations surfaced, not silently corrected |
| `/article-promote [essay-path]` | `universal-commands/article-promote.md` | final-status note | moves to `40-Published/`; backlinks source maps; updates registry + Writing Dashboard; runs harvest loop | none | Step 7 harvest loop: extract claims, diff, classify (substantive / methodological / essay-specific), user-confirm, execute accepted promotions to new T3 + positions-index row or to writer-positions |

**Critic-layer command (V1.9 — 2026-04-22)**: `/article-critique` is a standalone pass that catches what `/article-revise` structurally cannot see — frame circularity, theorist-as-stamp, analogy validity, stratification independence, scenario silence, concession-load, unit-of-analysis, title-thesis match. Eight passes (C1–C8) plus writing-tells. Produces a critique document in `synthesis_logos/critic/`; does NOT edit the essay. Calibrated against the human-written reference critique of "The Pole Is Obsolete". `/article-revise` Pass E now runs a cheap frame-pressure sub-pass (C1/C6/C7) as tripwire; Step 4 Five Questions gains a 6th question asking whether `/article-critique` has been run and its flags addressed-or-dismissed.

| Command | Protocol | Inputs | Outputs |
|---|---|---|---|
| `/article-critique [essay-path] [--mode=full\|frame-only\|writing-only]` | `universal-commands/article-critique.md` | essay at any status | critique file in `critic/`; `critique_runs` frontmatter entry on essay |

**Companion-mode commands (V1.9 — 2026-04-22)**: a parallel mode where the operator writes the essay and AI augments via four read-only verbs. Distinct from the delegation pipeline: no thesis locking, no preset enforcement, no auto-drafting, no in-place revision. Presets are advisory. Same `/article-promote` harvest loop works for both modes.

| Command | Protocol | Inputs | Outputs |
|---|---|---|---|
| `/article-companion start <topic-or-source-map> [--from-map <map-path>]` | `universal-commands/article-companion.md` | topic string or source-map path | essay file at `20-Essays/` with `mode: companion`, `status: companion-draft`; workspace dossier report |
| `/co-find <query> [--vault <name>] [--type <atomic\|t3\|map\|bridge\|all>]` | `universal-commands/co-find.md` | query string | structured dossier: atomic notes, T3 positions, maps, bridges |
| `/co-combine <map1> <map2> [<map3> ...]` | `universal-commands/co-combine.md` | 2–5 source-map paths | shared concepts, opposing claims, complementary mechanisms, synthesis-angle options |
| `/co-suggest <selection-or-stuck-point> [--type ...]` | `universal-commands/co-suggest.md` | passage or stuck-point description | 3 distinct next-move options (direction + rationale + risk per option) |
| `/co-critique <selection> [--mode light\|adversarial]` | `universal-commands/co-critique.md` | selected passage | bulleted flags with fix suggestions; shares C1–C8 library with `/article-critique` in adversarial mode |
| `/co-capture [flag\|sweep\|close] [--target voice\|positions\|methodological\|framework\|all]` | `universal-commands/co-capture.md` | active companion-mode dialogue | voice-profile source files, positions-index rows (status `under-review`), writer-positions.md appends; all substrate writes user-confirmed per-item |

**Legacy expression commands** (cogitationis, retained for non-map-derived essays):

**`/draft [title or thought-note path]`**
Expand a Thought into an Essay. See `synthesis_logos/.claude/commands/draft.md` for the inline protocol. Prefer `/article-seed → /article-outline → /article-draft` for maps-to-articles work.

**`/argument-map [claim]`**
Build a structured argument tree. See `synthesis_logos/.claude/commands/argument-map.md` for the inline protocol. Used mid-essay when the drafter needs to verify the claim's support structure.

### Domain Commands (generated from Q6 priority domains)

**`/domain-audit [domain-slug]`** → see `universal-commands/domain-audit.md` (now universal)

**`/promote [note-path]`** → see `universal-commands/promote.md` (now universal)

---

## Adding Commands to `.claude/commands/`

Each universal command stub is a `.md` file. Example for a vault-specific command (full protocol inline):

```
---
description: Read a political situation structurally
---

# /situation-read [situation]

$ARGUMENTS

Read vault-config.md for domain slugs and open problem IDs.
[Full protocol text here for vault-specific commands only]
```

For universal commands, the stub is always the 3-line pointer format shown at the top of this file.
