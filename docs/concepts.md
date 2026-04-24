---
type: documentation
audience: human
---

# Core Concepts

A glossary of AGENSY's key terms. Understanding these before your first vault will save significant confusion.

---

## Vault

A vault is a domain-specific knowledge system — one Obsidian folder containing all the notes, maps, templates, and configuration for one intellectual domain. One vault = one domain.

Vaults are not notebooks. They are structured intellectual systems with defined missions, driving questions, and engagement axes. The structure is not arbitrary; it follows from your answers to the 7 founding questions in the genesis protocol.

**You can have multiple vaults.** They are designed to connect via cross-vault bridges and a shared `system-state.md` file.

---

## Three-Tier Note System

Every note in a vault belongs to one of three tiers:

| Tier | Role | Location |
|---|---|---|
| **Tier 1** | Raw input — captures, highlights, source material | `00-Inbox/`, `10-Sources/` |
| **Tier 2** | Analysis — atomic explanations with structural depth | Domain subfolders |
| **Tier 3** | Judgment — permanent, standalone, claim-titled | Output folder (e.g., `20-Judgment/`) |

Progression is always T1 → T2 → T3. Never reversed. Tier 3 notes are never demoted.

A **Tier 3 title must state a claim**, not a concept. "Debt Cycles" is a concept. "Debt Cycles Are Self-Amplifying Until External Shock Breaks the Feedback Loop" is a Tier 3 title.

---

## Two-Zone Architecture

Within Tier 2, notes split into two zones based on the `evergreen-candidate` frontmatter field:

| Zone | Field Value | Purpose |
|---|---|---|
| **Zone 1 — Reference** | `false` | Mechanistic scaffolding — HOW things work, technical procedures, definitions |
| **Zone 2 — Synthesis** | `true` | Project-facing insights — connected to driving questions and engagement axis |

Zone 1 notes explain. Zone 2 notes argue. The ratio matters: a vault heavy on Zone 1 is a reference library, not a synthesis system.

---

## Arc

An arc is the primary unit of vault-building work. One arc = one subject, producing 8–12 Tier 2 notes plus an updated MOC. Arcs are run with `/arc [subject]`.

Think of an arc as a structured reading + synthesis sprint on one topic. After an arc, the topic is covered at depth — not summarized, but analyzed through the vault's driving questions and engagement axis.

---

## Engagement Axis

Every vault has a central intellectual tension — the core debate that structures the domain. This is not the vault's topic; it's the fault line that runs through the topic.

Examples:
- Economics: *structural forces vs. behavioral-ideational dynamics*
- Military theory: *continuity vs. discontinuity in principles under technological change*
- Philosophy: *complexity as ontologically real vs. epistemic imposition*

Every synthesis note must take a position on this axis. The `engagement` field in the note schema records where the note falls. A vault where every note says "both sides have merit" is a vault that hasn't done its job.

---

## MOC (Map of Content)

A MOC is an orientation layer — a structured index that maps a domain's notes by topic, theme, or conceptual cluster. MOCs are not summaries; they are navigation instruments.

Every vault has one MOC per major domain plus a master index MOC. MOCs are updated after every arc with `/update-moc`.

---

## Genesis Protocol

The 4-phase procedure for bootstrapping a new vault from scratch. Phases:
- **Phase 0** — Config elicitation (7 questions)
- **Phase 1** — Document generation (12 structural documents)
- **Phase 2** — Self-audit (coverage audit of the new structure)
- **Phase 3** — First arc (initial content run)

The genesis protocol turns a domain you know nothing about into a structured knowledge system ready for work in one session.

---

## Command Lifecycle

Commands have four trigger types:

| Type | When |
|---|---|
| **A — Automatic** | Triggered by another command without user input (e.g., `/quick-check` after `/arc`) |
| **B — Milestone** | Triggered when a vault reaches a structural milestone (e.g., first T3 note) |
| **C — Session** | Run at the start of every session to orient Claude |
| **D — Analytical** | Run when you need a specific type of analysis |

The lifecycle is self-regulating: `/coverage-audit` and `/what-next` tell you what to do next. You don't have to plan your own vault-building work.

---

## Cross-Vault Bridge

A bridge is a domain that appears in two or more vaults with different treatments. For example, "political economy" appears in both an economics vault (tool lens) and a politics vault (institutional lens). When notes in bridged domains are built, they can inform each other.

Bridges are defined in `cross-vault-bridges.md`. The `/dialogue` command runs in `Bridge` mode to explicitly connect reasoning across vaults.

---

## System State

`system-state.md` is a global cross-vault memory file. It tracks:
- Which vaults exist and their operational state (note counts, last audit date)
- User positions that emerged from cross-vault dialogues
- Active cross-vault tensions worth exploring

It is updated automatically by `/coverage-audit` and `/dialogue` in Bridge mode. You never edit it manually — Claude maintains it.

---

## System Model Layer

Optional per-vault layer (v1.1.0+): a `system-model.yaml` file at the vault root declaring the domain's structural ontology as **nodes**, **edges**, and **patterns** — plus cross-vault bindings to peer vaults.

**Three-layer vocabulary** (locked in v0.1):
- **Nodes (6 categories)** — *agents* (decision loci), *states* (stocks), *flows* (rates of change), *signals* (information carriers), *constraints* (what's ruled out), *structures* (persistent configurations of roles)
- **Edges (5 core + 5 reserve)** — core: *produces*, *reinforces*, *dampens*, *gates*, *couples*; reserve: *consumes*, *reveals*, *conceals*, *requires*, *opposes*
- **Patterns (7 types)** — *positive_feedback*, *negative_feedback*, *threshold*, *reflexivity*, *selection*, *accumulation*, *path_dependence*

A node is *not* a claim about the world — it's a thing that appears in the vault's mechanisms (e.g., `rising_power` is a node; "rising powers produce fear in dominant powers" is an *edge* between two nodes). Patterns are the recurring shapes the edges instantiate, and they are the layer that enables cross-vault composition — the same pattern type in two vaults with different local nodes is the coupling unit.

**v0.2 extensions** (additive, optional, all v0.1 files remain valid):
- **`timescale` bands** (on patterns and flow-nodes) — `seconds-to-minutes` · `hours-to-days` · `weeks-to-months` · `years` · `decades+` · `mixed`. Keeps fast-reflexivities (OODA-loop deception) and slow-reflexivities (institutional entrapment) from colliding in cross-vault queries as if they were the same mechanism.
- **`subtype`** (free-string, emergent) — differentiates mechanistically distinct variants within a pattern type. Example: within `reflexivity`, subtypes observed across vaults include `target-erosion`, `narrative-fact-cycle`, `orientation-constitution`, `structural-entrapment`.
- **`secondary_types`** (array) — for boundary-case patterns where two mechanisms genuinely live in the same subgraph. Example: capital accumulation with lock-in is primarily `accumulation` with `secondary_types: [path_dependence]`.

**What it's for**: answering structural questions without reading every note — *what are the load-bearing actors in this vault?*, *where is the feedback?*, *which patterns recur across domains?*, *where do two vaults share a pattern instance?* The MOC layer answers *what topics exist*; the system model answers *what shape does this domain have*.

**What it isn't**: not an auto-generated summary of notes (v0.2 remains hand-curated), not a replacement for theorist maps (those index one thinker's logic), not a restatement of `vault-config.md` or `cross-vault-bridges.md` (it references them).

**Opt-in**: vaults without a `system-model.yaml` are unaffected. Bootstrap with `/system-build bootstrap`. Four commands operate on it: `/system-query` (read), `/system-audit` (drift, also auto-fires after `/coverage-audit`), `/system-build` (write), `/system-bridge` (cross-vault binding reconciliation). See `framework/primitives.md` for the full vocabulary with worked examples, `framework/system-model-architecture.md` for the design rationale.

---

## Framework Meta-Architecture

The framework documents themselves form a designed system with explicit rules, not just a loose pile of files. `framework/framework-meta-architecture.md` is the fourth architectural-spine document (alongside WHY / HOW / WHAT — see below) that names this sub-architecture.

**Document taxonomy (11 types)** — every framework file carries a `type:` that places it in exactly one category: `invariant` · `topology` · `protocol` · `template` · `vocabulary` · `schema` · `reference` · `decision_record` · `experiment_log` · `registry` · `meta_workflow` · `validation_tool`. The type determines change rigor (invariants get the 7-step review; operational files get lightweight checks).

**Stability tiers (5 bands)** — `bedrock` (never changed without a system rebuild) · `foundational` (months between changes; 7-step review) · `operational` (weeks; lightweight review) · `dynamic` (expected to change; automation often updates) · `historical` (immutable after creation).

**Canonicity** — every fact has exactly one canonical home. Other representations must declare `derives_from` (generated from the canonical doc) or `synchronized_with` (independently maintained but declared to match). This is how the framework keeps the contract table, YAML manifest, command index, and verify tool from drifting — the relationships are machine-checkable, not vigilance-dependent.

**Supersession protocol** — decision records are immutable. To revise a prior conclusion, write a new record with `supersedes: [path]` in its frontmatter. Both records stay on disk; readers trace the chain forward. Git log answers *when* something changed; supersession pointers answer *what decision this supersedes and what new evidence drove the change*.

**Four architectural-spine docs**, read in order before any framework change:
- `architecture-principles.md` — **WHY** (invariants, trade-offs, 7-step change protocol)
- `system-contracts.md` — **HOW** (contract table, breaking-change rules)
- `system-architecture.md` — **WHAT** (topology diagrams, YAML manifest)
- `framework-meta-architecture.md` — **META** (document system, canonicity rules, frontmatter spec, supersession)

For Category F6 verify checks (F18–F22) that enforce the meta-architecture mechanically, see `docs/tools.md`.

---

## Vault-Type Substrate

Different vault types need different substrate files beyond the 12 standard genesis documents. `framework/vault-type-templates/` holds scaffolds organized by type:

**Expression vaults** receive six additional files:
- `voice-profile.md` — style layer (HOW the writer writes)
- `writer-positions.md` — substance bedrock (WHAT the writer believes, user-authored)
- `positions-index.md` — harvest-loop index to T3 framework claims earned in essays
- `article-presets.md` — five narrative-arc blueprints (`framework-build`, `orthodoxy-counter`, `case-anatomy`, `diagnostic-lens`, `synthesis-braid`)
- `article-design-principles.md` — craft principles P1–P10 learned across pilots
- `source-map-registry.md` — per-source-vault readiness manifest

**Training vaults** receive three scaffolds: `curriculum-template.md` (phased development arc), `principles-and-postulates-template.md` (load-bearing priors the vault teaches toward), `sources-master-list-template.md` (curated bibliography).

**Accumulation vaults** receive none — the 12 universal genesis documents cover them completely.

Genesis Protocol Phase 1 Doc 13 (conditional, vault-type-gated) copies the appropriate folder into a new vault. The scaffolds are *starting forms*, not finished content — the vault owner fills them during and after genesis. `/article-draft` refuses to run until `voice-profile.md` is seeded; `/article-revise` Pass C is softened when `writer-positions.md` is unfilled. See `framework/vault-type-templates/README.md` for the full pattern and fill-in order.

---

## AGENSY_PATH

Throughout the framework documents, `[AGENSY_PATH]` is a placeholder for the absolute path to your local agensy/ folder. When setting up, replace this with your actual path, or Claude Code will resolve it from the working directory.

Example: if you cloned to `/Users/alice/vaults/agensy/`, then `[AGENSY_PATH]` = `/Users/alice/vaults/agensy/`.

---

## How Claude Loads Framework Files

Framework files are never loaded proactively — they're fetched on-demand. Three layers:

1. **`~/.claude/CLAUDE.md`** — loaded at every session start. Universal rules, always active. This is what makes framework behavior consistent across all your vaults.

2. **Vault `CLAUDE.md`** — loaded when Claude Code opens the vault folder. Contains vault-specific identity, domains, and task list.

3. **On-demand (per command)** — when a slash command fires, Claude reads two files: the stub in `.claude/commands/[cmd].md` (which points to the protocol), then `[AGENSY_PATH]/framework/universal-commands/[cmd].md` (full protocol) plus `vault-config.md` (vault parameters).

This is why CLAUDE.md files stay lean — they don't need to include protocol logic. That lives in the protocol files and is only loaded when a command requests it.

**If a command behaves unexpectedly**: check that `vault-config.md` is complete (it provides all the parameters the protocol needs) and that `[AGENSY_PATH]` in your global CLAUDE.md resolves to the correct path.
