---
type: invariant
stability_tier: foundational
canonicity: canonical
canonical_for: [document_taxonomy, stability_tiers, frontmatter_spec, supersession_protocol, meta_architecture_invariants]
audience: both
---

# Framework Meta-Architecture

**Reading order**: `architecture-principles.md` (WHY — invariants) → `system-contracts.md` (HOW — contract table) → `system-architecture.md` (WHAT — topology) → `framework-meta-architecture.md` (META — framework-as-system-of-documents, read last, only when designing or auditing framework-level changes).

This document sits one level above the three architectural-spine documents. They describe the framework's project-level design (how vaults, protocols, and schemas work). This document describes the framework's sub-architecture — how the framework's own ~54 documents work as a designed system. It is read only during framework-structure work: adding a new framework doc, reassigning canonicity, changing a schema version, auditing for drift.

---

## §1 — What This Document Is (and Isn't)

**Is**: the canonical declaration of the framework's document-level design. Names the 11 document types, the five stability tiers, the canonicity rules, the communication channels, the self-maintenance loop, the supersession protocol, and the frontmatter specification. Provides the vocabulary the `framework-verify.py` Category F6 checks use.

**Isn't**: a rewrite of any sibling. It does not restate invariants (architecture-principles §2 owns those), does not restate command contracts (system-contracts §2 owns those), does not restate topology (system-architecture owns that). It also does not cover Level 1 (vault/project) architecture — that's what the three siblings exist for.

**Triggered by**: proposing a new framework document, retrofitting frontmatter, changing canonicity assignments, resolving drift between synchronized docs, writing a decision record that supersedes an older one, or any structural change where "which doc is authoritative for X?" is a live question.

**Not triggered by**: adding a new universal command (use genesis-protocol + command-lifecycle), editing a vault config (use vault-config-schema), or running a slash command (use the protocol file directly).

---

## §2 — Document Taxonomy

Eleven structural types. Every framework document belongs to exactly one. Type determines change rigor, lifecycle, and which verify checks apply.

| Type | Purpose | Change rigor | Examples |
|---|---|---|---|
| `invariant` | Defines constraints that must not change without rebuilding the system | Highest — 7-step change protocol; contact with any invariant is almost always wrong | `architecture-principles.md`, this file |
| `topology` | The system's own map of itself — structural diagrams, manifests, relationship graphs | High — affects every framework reader's mental model | `system-architecture.md` |
| `protocol` | Executable instructions for Claude; read during command invocation | Medium — backward-compat preferred; renames require alias | `universal-commands/*.md` (×34) |
| `template` | Fill-in-the-blanks scaffolding consumed during genesis | Medium — additive changes safe; structural changes break new-vault genesis | `claude-md-template.md`, `vault-config-schema.md`, `note-tier-template.md`, `map-type-template.md` |
| `vocabulary` | Shared terms used across multiple docs or protocols | Medium — additive-only preferred (v0.2 showed this works); renames break bindings | `primitives.md` |
| `schema` | Machine-validated constraints; the authoritative shape of a data structure | Versioned (semver-lite); additive-minor, breaking-major | `system-model-schema.yaml` |
| `reference` | Lookup tables consumed by protocols at runtime | Low — additive edits safe; restructures propagate to protocol behavior | `map-to-article-extraction.md` |
| `decision_record` | Historical trace of a specific decision and its reasoning | Immutable after creation; supersession by pointer only | e.g., `phase-N-closure.md` files (when a major phase concludes) |
| `experiment_log` | Historical trace of an empirical test and its gate decision | Immutable after creation; supersession by pointer only | e.g., `primitives-experiment.md` |
| `registry` | Dynamic or semi-dynamic state; authoritative for current values | Expected to change; `updated` must bump | `vault-registry.md`, `system-state.md`, `cross-vault-bridges.md`, `slash-command-suite.md` |
| `meta_workflow` | How the framework itself is operated (genesis, lifecycle) | Medium — changes affect future sessions | `genesis-protocol.md`, `command-lifecycle.md`, `inter-vault-protocol.md`, this file |
| `validation_tool` | Enforcement code (Python); not a markdown doc but part of the framework | Medium — new checks safe; removed checks degrade enforcement | `tools/framework-verify.py`, `tools/vault-linter.py` |

**Assignment rule**: if a doc plausibly fits two types, pick the one that governs the stricter change rigor. A doc that is both a template and a vocabulary is treated as `vocabulary` (stricter).

---

## §3 — Stability Tiers

Five bands. Tier determines change velocity and review rigor. Independent of type — an `invariant`-type doc is always `bedrock`; a `protocol`-type doc is almost always `operational`; a `registry`-type doc is always `dynamic` or `registry` (registries change expectedly).

| Tier | Change velocity | Review rigor | Who can change |
|---|---|---|---|
| `bedrock` | Years between changes | Architecture-principles §7 full 7-step protocol | User + Claude, only after the 7-step analysis |
| `foundational` | Months between changes | 7-step protocol with evaluation-axis scoring | User + Claude |
| `operational` | Weeks between changes | Lightweight — verify no contract violation | User + Claude |
| `dynamic` | Daily to weekly | Bumped by automation (e.g., `/coverage-audit` Step 8) | Claude on automation; user on policy |
| `historical` | Immutable | None — no edits permitted after `created:` date | No one (supersession creates a new doc, never edits an old one) |

**Examples**:
- `architecture-principles.md` → `bedrock` (invariants)
- This doc, `system-contracts.md`, `system-architecture.md` → `foundational`
- Protocols, templates, schemas, vocabularies → `operational`
- `system-state.md`, `vault-registry.md` → `dynamic`
- Phase closure docs, experiment logs → `historical`

---

## §4 — Canonicity and Representation

**The core problem**: a fact (e.g., "the command inventory") may appear in N documents for N different audiences. If no doc is designated authoritative, drift is inevitable.

**Rule**: every fact has exactly one canonical home. Other representations are either derived (generated/copied from canonical) or synchronized (independently maintained but declared to match).

**Three canonicity states** (declared in frontmatter):

1. **`canonical`** — this doc is the source of truth for the concerns listed in `canonical_for: [...]`. Edits to those concerns must happen here first.
2. **`derived`** — this doc's content is generated or copied from an upstream canonical doc. `derives_from: [path]` names the source. Direct edits here are bugs; edit the canonical doc and regenerate.
3. **`synchronized`** — this doc and one or more peers independently maintain the same fact. `synchronized_with: [paths]` lists the peers. Both must be updated together; drift is caught by F20.
4. **`none`** — the doc's content is unique and not duplicated elsewhere.

**Running example — command inventory**. Today, the command list appears in 5 places: (1) the `universal-commands/` filesystem, (2) `slash-command-suite.md` table, (3) `system-contracts.md §2` contract table, (4) `system-architecture.md` YAML manifest, (5) `framework-verify.py` `COMMAND_REQUIRED_KEYS` dict. Four of these drifted simultaneously when 13 commands were added in April 2026 (caught by the F15 warning, fixed manually).

**Current assignment** (transitional — single-source-of-truth via a `command-registry.yaml` is an out-of-scope follow-up): all five are declared `synchronized_with` each other. F20 symmetry enforces the declaration; F20 fact-match (initial callback) checks that the command lists actually match across the declared pairs. Until the SSoT exists, F20 surfaces any future drift the moment it happens.

**Canonicity assignment rules**:
- When two docs plausibly could be canonical for the same concern, pick the one with the **tightest change velocity** (foundational > operational) — drift is costlier at slower tiers.
- A doc can be canonical for multiple concerns simultaneously (most foundational docs are).
- A concern can only have one canonical home. F19 enforces this.

---

## §5 — How Docs Communicate

Three channels. Only channel 3 is machine-auditable; channels 1 and 2 remain as documentation.

**Channel 1 — Reading-order declarations**. Docs in `bedrock` and `foundational` tiers carry a "Reading order" line in the header that names prerequisites and positions them. Example: `system-contracts.md` declares `architecture-principles → system-contracts → system-architecture`. This is a soft contract — no verify check enforces it today.

**Channel 2 — Prose references**. "See `X.md` §N" or "Per `Y.md`" references scattered through prose. Useful for readers; not structural. Verify does not check these.

**Channel 3 — Structural references** (new with this doc). Frontmatter fields `derives_from`, `synchronized_with`, `supersedes` declare machine-readable relationships. F19/F20/F22 enforce them.

Use channel 3 for load-bearing relationships. Use channels 1–2 for soft navigation.

---

## §6 — How Docs Self-Maintain

The maintenance loop:

1. **Change proposed** → consult `architecture-principles §7` (7-step analysis) for bedrock/foundational changes; lighter review for operational.
2. **Canonical doc updated** → the single authoritative location for the affected concern.
3. **Synchronized peers updated in the same commit** → all docs declared `synchronized_with` the canonical doc for that concern are updated to match.
4. **Derived representations regenerated** → for facts with `derived` relationships (future: command-registry SSoT); currently N/A since no derivation pipeline exists.
5. **Verify run** → `python tools/framework-verify.py` catches drift that slipped through (F18–F22 for sub-architecture integrity).

**What this loop does not catch**:
- Semantic drift within a single doc (a concept is used two different ways in the same file).
- Drift across docs that have no declared synchronized-with relationship.
- Stale prose references (channel 2) — reader catches these, not the verifier.

These gaps are listed in §13 as open items.

---

## §7 — Decision-Record Supersession Protocol

**Rule**: decision records (`type: decision_record`) and experiment logs (`type: experiment_log`) are immutable after creation. To change the conclusion of a prior record, write a new record that declares `supersedes: [path-to-old-record]` in its frontmatter. Both records stay on disk. Readers trace the chain forward by following `supersedes` pointers.

**Why immutable**:
- Decision records exist to preserve reasoning, not just state. Rewriting them destroys the "why we changed our minds" trail that makes future decisions informed.
- Git log answers "when did this change"; supersession pointers answer "what decision did this supersede and what new evidence drove the change." These are different questions.
- Uniform treatment (one rule for all historical records) is simpler than differentiating by sub-type and preserves invariant integrity. Mixed policy would introduce a hole in the `historical`-tier immutability guarantee.

**Format**:
```yaml
---
created: 2026-05-10
updated: 2026-05-10
type: decision_record
stability_tier: historical
canonicity: canonical
canonical_for: [phase_6_closure_rationale]
supersedes: framework/closures/phase-5-closure.md
audience: both
---
```

**F22 enforces**: the `supersedes` path resolves; the target is same `type`; the target's `created` is older; no cycles.

**What about small corrections?** A typo in a decision record is a typo — fix it. A factual correction whose reasoning hasn't changed is a typo. A factual correction whose reasoning *has* changed is a new record with `supersedes`. The line is "does this change the decision's logic" — if yes, new record; if no, in-place edit with `updated:` bump.

---

## §8 — Session Economy

Context is finite. Every document has a session-cost profile that determines how tightly it should be written.

| Weight class | Cost model | Docs in this class |
|---|---|---|
| **always-loaded** | Pays context in every session, everywhere | `~/.claude/CLAUDE.md` (global), `[vault]/CLAUDE.md` |
| **read-on-demand** | Pays only when invoked | `vault-config.md`, `universal-commands/*.md` (per command) |
| **reference-only** | Read only during framework-level work | This doc, `architecture-principles.md`, `system-contracts.md`, `system-architecture.md`, all other framework docs |

**Optimization rules**:
- **always-loaded** content: compress ruthlessly. Every line is paid by every session everywhere. Budgets enforced (100-line global, 120-line vault, 150-line MEMORY.md).
- **read-on-demand** content: keep verbose. Protocol precision matters more than token count. Don't compress a protocol to save tokens — you pay precision tax every time Claude mis-interprets.
- **reference-only** content: no hard budget; should still be tight because reader-effort is the real cost, not tokens.

Frontmatter does not count against always-loaded budgets — it's structural metadata, not prose guidance. This is an implicit clarification of architecture-principles §2 invariant 4 "content lines" test.

---

## §9 — Creation Principles for New Framework Docs

Decision tree:

1. **Does the fact this doc would carry already have a canonical home?**
   - **Yes** → edit the canonical doc instead. If the new fact legitimately needs a different view (different audience, different format), create the doc but declare `canonicity: derived` or `synchronized`.
   - **No** → proceed.

2. **What type from §2 does it fit?** Pick exactly one. If two plausibly fit, pick the stricter change rigor.

3. **What stability tier from §3?** Default to `operational` unless the doc introduces structural rules (then `foundational`) or invariants (then `bedrock` — requires 7-step review).

4. **Minimal frontmatter** per §11. Declare `canonicity` honestly. If synchronized with peers, list them and update the peers' `synchronized_with` to match (F20 symmetry will fail otherwise).

5. **Reading-order hook**: if the doc is `foundational` or `bedrock`, add a reading-order line to its header and to any sibling docs whose reading order it affects.

6. **Verify**: run `framework-verify.py --category F6` before committing. F18–F22 must pass (or WARN where expected).

**Do not create new framework docs to group related content by topic.** Grouping follows type, not topic. A topic that spans multiple types spans multiple docs; don't merge across types.

---

## §10 — Structural Roles

Each role maps to one specific framework doc. Missing roles are flagged.

| Role | Filled by | Notes |
|---|---|---|
| **Entry point** | *(unfilled)* | No `framework/README.md` for Claude/newcomers exists. Gap — see §13. |
| **Contract** | `system-contracts.md` | The most load-bearing doc — binds protocols to vault-config. |
| **Topology** | `system-architecture.md` | Diagrams + YAML manifest. |
| **Invariants** | `architecture-principles.md` | 8 invariants + change protocol + anti-patterns. |
| **Meta-architecture** | this file | Doc taxonomy, tiers, canonicity, supersession, frontmatter spec. |
| **Command index** | `slash-command-suite.md` | Registry listing all 34 protocols + 2 aliases. |
| **Lifecycle** | `command-lifecycle.md` | When to fire which command. |
| **Genesis** | `genesis-protocol.md` | 5-phase bootstrap. |
| **Cross-vault** | `inter-vault-protocol.md` + `cross-vault-bridges.md` | Rules + bridge catalog. |
| **Schemas** | `vault-config-schema.md`, `system-model-schema.yaml` | Machine-validated constraints. |
| **Vocabularies** | `primitives.md` | Cross-vault primitives. |
| **Templates** | `claude-md-template.md`, `note-tier-template.md`, `map-type-template.md` | Genesis fill-in-the-blanks. |
| **Enforcement** | `tools/framework-verify.py`, `tools/vault-linter.py` | Python checkers. |
| **History** | e.g., `phase-N-closure.md` files, `primitives-experiment.md` | Decision records, immutable when created. |
| **Registries** | `vault-registry.md`, `system-state.md`, `cross-vault-bridges.md` | Dynamic state. |

---

## §11 — Frontmatter Specification

Backward-compatibility rule: existing frontmatter (`created`, `updated`, `type: reference|schema`) stays valid. `reference` and `schema` are now members of the enumerated 11-type list. Missing new fields emit `WARN` (not `FAIL`) — retrofit is opportunistic, not forced.

| Field | Type | Required? | Enumerated values | Purpose |
|---|---|---|---|---|
| `created` | date (`YYYY-MM-DD`) | yes (existing) | — | Unchanged from prior convention |
| `updated` | date (`YYYY-MM-DD`) | yes (existing) | — | Unchanged |
| `type` | string | yes | `invariant`, `topology`, `protocol`, `template`, `vocabulary`, `schema`, `reference`, `decision_record`, `experiment_log`, `registry`, `meta_workflow`, `validation_tool` | Taxonomy role (§2) |
| `stability_tier` | string | yes (new docs); WARN on absent (existing) | `bedrock`, `foundational`, `operational`, `dynamic`, `historical` | Change-velocity band (§3) |
| `canonicity` | string | yes (new docs); WARN on absent (existing) | `canonical`, `derived`, `synchronized`, `none` | Relationship to the fact carried (§4) |
| `canonical_for` | list[string] | required if `canonicity: canonical` | free-form concern names | What this doc is SSoT for |
| `derives_from` | list[path] | required if `canonicity: derived` | relative paths from `[AGENSY_PATH]/` root | Upstream canonical doc(s) |
| `synchronized_with` | list[path] | required if `canonicity: synchronized` | relative paths | Peer docs that must match (symmetry enforced) |
| `supersedes` | path | optional; only on `decision_record`/`experiment_log` | relative path | Predecessor record (§7) |
| `schema_version` | string | optional; on `schema`/`vocabulary` | semver-lite (`0.2`) | Schema version |
| `audience` | string | optional | `claude`, `user`, `both` | Intended reader |

### Worked examples

**Example A — bedrock invariant** (`architecture-principles.md`):
```yaml
---
created: 2026-03-30
updated: 2026-03-30
type: invariant
stability_tier: bedrock
canonicity: canonical
canonical_for: [core_invariants, change_analysis_protocol, evaluation_axes, anti_patterns]
audience: both
---
```

**Example B — operational protocol** (`universal-commands/arc.md`):
```yaml
---
created: 2026-02-14
updated: 2026-04-22
type: protocol
stability_tier: operational
canonicity: synchronized
synchronized_with: [framework/principles/system-contracts.md, framework/principles/system-architecture.md, framework/slash-command-suite.md]
audience: claude
---
```

**Example C — historical decision record with supersession** (hypothetical future `framework/phase-6-closure.md`):
```yaml
---
created: 2026-07-15
updated: 2026-07-15
type: decision_record
stability_tier: historical
canonicity: canonical
canonical_for: [phase_6_closure_rationale]
supersedes: framework/closures/phase-5-closure.md
audience: both
---
```

---

## §12 — Verify Checks (F18–F22)

Category F6 — Meta-Architecture Integrity. Each check operates on parsed YAML frontmatter across `framework/**/*.md` plus top-level framework docs like `CLAUDE.md`. Implementation in `tools/framework-verify.py`.

- **F18 — Frontmatter Schema Compliance.** Validates frontmatter parses, required fields present, enum values valid, `canonical`-state docs declare non-empty `canonical_for`. `FAIL` on bad enum; `WARN` on missing new fields in existing docs (backward-compat).
- **F19 — Canonicity Uniqueness.** Every concern in `canonical_for` is claimed by at most one doc. `FAIL` on concern conflicts; shows conflicting doc set.
- **F20 — Synchronized-With Match.** (a) Symmetry — if A `synchronized_with` B, then B `synchronized_with` A. (b) Fact-match — concern-specific callbacks (registry-based) check that the synchronized facts actually match. Initial callback: command-list cross-check between `system-contracts §2` and `system-architecture` manifest. `FAIL` on broken symmetry or fact mismatch.
- **F21 — Protocol Path Discipline.** `type: protocol` docs contain no absolute Windows path literals or vault-specific refs outside an allow-list of meta-level resources (`[AGENSY_PATH]/cross-vault-bridges.md`, `[AGENSY_PATH]/vault-registry.md`, `[AGENSY_PATH]/system-state.md`, `[AGENSY_PATH]/question-bank.md`, `[AGENSY_PATH]/tools/vault-linter.py`). `FAIL` with file + line on violations.
- **F22 — Decision-Record Supersession Chain.** `decision_record`/`experiment_log` with `supersedes:` resolves to existing file of same type; target's `created` is older; no cycles.

---

## §13 — Known Tensions and Open Items

Honest list. Each item names its follow-up.

1. **Command-registry single-source-of-truth is not yet implemented.** Command inventory lives in 5 places; all are declared `synchronized_with` each other as a transitional measure. F20 surfaces drift; it does not prevent it. **Follow-up**: separate plan session to build `framework/command-registry.yaml` as canonical, with the other 4 representations marked `derived`.

2. **Frontmatter retrofit is incomplete.** This plan adopts the spec going forward. Existing ~50 docs emit F18 `WARN` until retrofit. **Follow-up**: optional dedicated retrofit sprint (5-wave migration: bedrock/foundational → schemas/vocabulary → templates/meta-workflow → protocols → historical/dynamic). Until then, retrofit is opportunistic (a doc gets frontmatter the next time it's edited).

3. **F20 fact-match callback registry is stubbed.** Symmetry is fully checked; fact-match ships with one callback (command-list cross-check). Additional concerns need callbacks as they get single-sourced. **Follow-up**: add callbacks alongside any future single-source work.

4. **Absolute-path allow-list is hand-curated.** F21's allow-list of meta-level resources is hardcoded in `framework-verify.py`. If new meta-level resources appear (e.g., a new top-level registry), the allow-list must be updated. **Follow-up**: ambient — part of the meta-workflow discipline.

5. **Channel-2 prose references have no verification.** "See X.md" links in prose are useful for readers but not machine-checked. Broken or stale prose references surface only during human reads. **Follow-up**: optional — could be added as an F23 check (regex-scan for `[^(]*\.md` references and resolve paths). Low priority.

6. **No protocol test harness.** Protocol behavior is verified only by running the protocol. No fixture-based regression. **Follow-up**: separate session — likely `tools/protocol-test.py` with fixture vaults.

7. **Context-budget economy has no per-line audit.** The 100/120/150 budgets are asserted but not analyzed per-line. **Follow-up**: separate session — one-off audit identifying which always-loaded lines earn their place.

8. **No explicit entry-point doc.** A newcomer (or Claude reading cold) has no single starting point. `CLAUDE.md` is close but mixed. **Follow-up**: small separate session — write `framework/README.md` as the framework entry point.

9. **Historical records have no promotion path.** A conclusion reached in a decision record may warrant promotion to invariants (e.g., a closure gate's bounded-universality result). Currently no mechanism exists for this; promotion is implicit via edits to the relevant vocabulary or schema doc. **Follow-up**: extend §7 once a real promotion case arises. Pre-mature to formalize.

---

## See Also

- `framework/principles/architecture-principles.md` — invariants, change analysis protocol
- `framework/principles/system-contracts.md` — vault-config contract table
- `framework/principles/system-architecture.md` — topology diagrams + YAML manifest
- `tools/framework-verify.py` — Category F6 implementation
