---
type: reference
audience: claude
---

# Architecture Principles

Complete briefing for Claude before analyzing or modifying framework documents. Starts with what the system IS, then layers on the invariants, trade-offs, and evaluation criteria governing it.

**Read this before modifying any framework document.** After reading this document, you need only read the specific file you are modifying — not all framework documents.

**Reading order**: `architecture-principles.md` (WHY — invariants, trade-offs, change protocol) → `system-contracts.md` (HOW — command-to-key contract table, breaking change rules) → `system-architecture.md` (WHAT — Mermaid diagrams + YAML manifest for topology)

For the operational contract table (command → required keys): `system-contracts.md`
For the visual system map and structured YAML manifest: `system-architecture.md`

---

## §1 — The System in Brief

The agensy framework is an **Agent-first system** for building and maintaining Obsidian knowledge vaults. Claude is the primary executor; the framework is the instruction set.

**3-layer loading hierarchy** (context budget is finite — every layer is sized accordingly):
- **Global CLAUDE.md** (~86 lines, always loaded): universal rules — atomicity, two-zone architecture, tier logic, slash command runtime, tool rules, memory management
- **Vault CLAUDE.md** (~95–120 lines, always loaded per vault): vault identity — role, mission, driving questions, engagement axis, open problems list, domain defaults, note schema summary
- **On-demand** (per command): `vault-config.md` (~260 lines, read per invocation) + the relevant universal protocol file from `[AGENSY_PATH]/framework/universal-commands/`

**Content architecture**: three tiers (T1 capture → T2 analysis → T3 output), two schemas per note (reference substrate or synthesis core, governed by `evergreen-candidate`), four intellectual styles (adversarial, dialectical, contemplative, constructive).

**Execution architecture**: 34 universal command protocols + 2 backward-compat aliases live in agensy (17 core knowledge-work + 4 system-model + 8 article-pipeline + 5 companion-mode). Each vault holds thin stubs (~11 lines) in `.claude/commands/` that point to them. A bug fix in one protocol propagates to all vaults instantly.

**State architecture**: three memory files per vault — `MEMORY.md` (persistent decisions, dialogue log, max 150 lines), `session-state.md` (pre-computed session diagnostics, replaces vault-wide globbing at session start), `note-index.md` (bulk metadata cache, replaces hundreds of individual frontmatter reads for audit commands). One cross-vault file in agensy — `system-state.md` (dynamic operational state: note counts, audit dates, cross-vault user positions; updated by `/coverage-audit` and `/dialogue` Bridge mode).

**Seven vaults**: 1 framework (agensy), 4 accumulation (omega, kratos, oikos, clio), 1 training (belli), 1 expression (cogitationis). Cross-vault: 3 connection types — Type 1 knowledge→expression (one-way), Type 2 knowledge→training (one-way), Type 3 peer↔peer (bidirectional).

---

## §2 — Core Invariants

These are structural load-bearing walls. Violating any requires rebuilding the system, not patching it. Each has a concrete test.

1. **Atomicity** — one idea per note, one protocol per command, one config per vault. *Test*: if you can split it and both halves stand alone, it was not atomic.

2. **Parameterized runtime** — universal protocols never contain vault-specific values (paths, slugs, domain names, problem IDs). All vault identity flows through `vault-config.md` at execution time. *Test*: can this protocol run in a vault that does not yet exist?

3. **Tier direction** — promotion only: T1 → T2 → T3, never reversed. Tier 3 notes are never demoted. Demotion breaks traceability and creates ambiguity about what counts as permanent insight. *Test*: does this change create any path from a higher tier to a lower one?

4. **Context budget** — Global CLAUDE.md max 100 lines; vault CLAUDE.md max 120 lines; MEMORY.md max 150 lines. These are hard constraints, not preferences. Every always-loaded line is paid in every session — it must earn its place. *Test*: count the net line change to any always-loaded file.

5. **Single vault-config.md** — all vault identity in one file, never split. Splitting creates sync problems, partial-read failures, and multi-file maintenance overhead. *Test*: does this change require reading more than one config file per command invocation?

6. **Engagement field mandatory** — every synthesis-schema note must have a specific, non-trivial entry in the engagement field (Threatens / Complicates / Transforms / Constrains). This is what prevents notes from being mere summaries. The escape valve exists only at Tier 2, and blocks promotion to Tier 3. *Test*: could a note pass quality checks after this change with less analytical work than before?

7. **Stub pattern** — vault command files are logic-free pointers to universal protocols. Protocol logic lives once in agensy. Duplicating protocol logic into vault stubs breaks automatic propagation. *Test*: does this require changing command behavior in vault stubs rather than in the protocol file?

8. **Two-zone integrity** — the `evergreen-candidate` field direction is `false → true` only; a note is never downgraded from synthesis schema to reference schema. Domain defaults apply at creation; note-level value overrides. *Test*: does this create any path where a synthesis note reverts to reference schema?

---

## §3 — Design Trade-offs

Decisions made and the alternatives rejected. Understanding these prevents re-litigating settled choices.

**Single vault-config.md vs. split config files**: One file means one read, one source of truth, no sync drift. Split files mean multiple reads per command, partial failures when any file is missing, and maintenance of multiple files per vault. The cost (a longer single file ~260 lines) is paid once per command; the benefit (reliable runtime) is paid every invocation.

**Hard context budget vs. "load what's useful"**: Finite context means every always-loaded line displaces on-demand content. The hard budget forces prioritization — which forces clarity about what every session actually needs vs. what is only sometimes useful. Without the constraint, CLAUDE.md files grow until they're noise.

**Four intellectual styles vs. universal adversarial framing**: The original framework forced all domains into adversarial framing (fault line, positions, threatens). This distorted non-adversarial domains — economics doesn't have a fault line, phenomenology doesn't have opposing camps. Four styles (adversarial, dialectical, contemplative, constructive) represent genuinely different intellectual structures. Cost: more complex vault-config schema. Benefit: accurate framing for every domain type.

**Engagement field mandatory vs. optional**: Without mandatory engagement, notes degrade into well-organized summaries — comprehensive but intellectually inert. The engagement field is the mechanism that prevents this. The Tier 2 escape valve is the compromise for genuinely stable reference concepts; Tier 3 allows no escape.

**Three tiers vs. two or four**: Two tiers (draft/final) lose the working-concept middle where most intellectual development happens. Four tiers add a promotion decision point that rarely carries enough information to justify itself. Three maps to the natural cognitive progression: capture → analyze → distill.

**Cascade-scoped re-reads vs. session-wide caching of vault-config.md**: Context compression in long sessions degrades cached content. Re-reading vault-config.md for each standalone command invocation is safe and necessary. The exception — skipping re-reads within a tight cascade (arc→update-moc→quick-check) — is safe because those reads are fresh and unchained by compression.

---

## §4 — How Changes Propagate

Consult this table first when assessing any proposed change.

| Change to... | Propagates to... | Action required |
|---|---|---|
| Universal protocol in agensy | All vaults automatically | None — stubs point to protocol |
| `vault-config-schema.md` | New vaults only | None — existing vault configs unchanged |
| New **required** key in vault-config | Every active vault-config.md | Add key to all configs; update contract table |
| New **optional** key with fallback | New vault-configs by default | Document fallback in protocol; update contract table |
| Global CLAUDE.md | Every session in every vault | Must stay under 100 lines |
| Vault CLAUDE.md | Every session in that vault | Must stay under 120 lines |
| Note frontmatter schema | All existing notes (retroactive) | Breaking — requires migration plan |
| Stub format | All vaults (regenerate stubs) | Low cost but broad impact; touch every vault |
| `genesis-protocol.md` | New vaults only | Existing vaults unaffected |
| `command-lifecycle.md` | Claude's session behavior globally | Affects every session start and milestone trigger |
| State file schema (session-state, note-index) | All vaults that have these files | Add migration note; old format must remain parseable |

---

## §5 — Evaluation Framework

Score a proposed change against all six axes before implementing. A change that improves one axis but degrades two others is a net negative.

1. **Precision** — does the change make instructions more specific or more vague? *Test*: can Claude execute this protocol without judgment calls that were previously specified?

2. **Context efficiency** — net line change across always-loaded files (global + vault CLAUDE.md). *Test*: count lines added minus lines removed in files that load every session.

3. **Intellectual depth** — does the change preserve or weaken the engagement requirement? *Test*: could a note pass quality checks with less analytical work than before?

4. **Universality** — does the change work for all vault types (accumulation, training, expression) and all four intellectual styles? *Test*: mentally execute the change against all 12 combinations.

5. **Propagation** — does the change propagate automatically to all vaults, or does it require per-vault migration? *Test*: how many files outside agensy need to change?

6. **Reversibility** — can the change be undone without data loss? *Test*: is there a rollback path that leaves existing vault content intact?

---

## §6 — Anti-Patterns

Changes that look like improvements but degrade the system.

**Optional-params-as-escape**: Adding an optional key to vault-config to avoid a hard design decision pushes the decision onto every future session. The schema grows; documentation grows; cognitive load grows. *Instead*: make the hard decision and document why.

**Protocol compression**: Cutting words from universal protocols to save tokens degrades instruction precision. Claude makes more interpretation errors; output becomes inconsistent across sessions. *Instead*: save tokens in CLAUDE.md files (they're always-loaded), not in protocols (they're on-demand).

**Session-wide vault-config caching**: Context compression in long sessions degrades reads from earlier in the conversation. A session-wide "read vault-config once" rule risks operating on degraded config data. *Instead*: cascade-scoped optimization only — chained sub-commands skip re-reads, but standalone invocations always read fresh.

**Vault-type-specific protocol branches**: Adding `if vault_type == 'training'` branches inside universal protocols breaks universality and multiplies maintenance cost by vault type count. *Instead*: use vault-config.md parameters to handle structural differences at runtime (e.g., `open_problem_key: open_challenges` vs `open_problems`).

**Graduation weakening**: Relaxing Tier 2→Tier 3 graduation criteria to increase T3 throughput dilutes Tier 3's selectivity. Every existing T3 note loses credibility. *Instead*: improve Tier 2 quality so more notes naturally meet the criteria.

**Universal-rule duplication**: Copying universal rules from the global CLAUDE.md into vault CLAUDE.md files "for safety" creates sync drift and wastes context budget in every session. *Instead*: trust the global file. If something needs to be in a vault CLAUDE.md, it must be vault-specific.

---

## §7 — Change Analysis Protocol

Seven steps before implementing any framework change.

1. **Read scope**: this document + `system-contracts.md` + the specific target file. Read the YAML manifest in `system-architecture.md` if you need to trace relationships. For changes to the framework's own document system (new framework doc, frontmatter schema edits, canonicity reassignment, supersession records), also read `framework-meta-architecture.md`.

2. **Check propagation**: consult §4. How many files outside agensy change? If >0, document the migration path before proceeding.

3. **Check invariants**: does the change touch any core invariant from §2? If yes, it is almost certainly wrong unless accompanied by a fundamental architecture revision. State explicitly which invariant is contacted and why the contact is safe.

4. **Run evaluation axes**: score against all six axes from §5. Document the scores — even approximate ones. A change that cannot be scored has not been understood.

5. **Check anti-patterns**: does the change match any pattern from §6? If yes, articulate in one sentence why this case is different, or abandon.

6. **Test across types and styles**: mentally execute in accumulation, training, and expression vaults. Mentally execute against adversarial, dialectical, contemplative, and constructive styles. Any combination that breaks is a blocker.

7. **Write the rationale in one sentence**: "This change improves [axis] by [mechanism] without degrading [other axes]." If you cannot write this sentence, the change is not well-enough understood to implement.

8. **Sync config extracts** (if the change involves any vault's `vault-config.md`): update the corresponding snapshot in `[AGENSY_PATH]/vaults/[vault]-config.md`. These extracts serve as reference documentation for the framework; stale extracts mislead during vault genesis and architecture reviews.
