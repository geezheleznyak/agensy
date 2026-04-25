---
created: 2026-04-25
updated: 2026-04-25
type: template
stability_tier: foundational
canonicity: canonical
canonical_for: [training_vault_phase_learning_methodology]
audience: both
---

# Phase Learning Methodology — Template

A field manual for turning curriculum phases into vault knowledge in a training vault. The vault has no chapters. It has **phases** (Phase-0 through Phase-N) and within each phase there are **concept areas** — numbered topic sections like Phase-0's "1. Linear Algebra" or "1. Levels of War." Every note is an **atomic concept** — one idea, one note.

This template is canonical for any training vault. Each instance vault (`synthesis_bellum`, `synthesis_mathesis`, future training vaults) keeps its own `phase-learning-methodology.md` that fills the `[VAULT-SPECIFIC: …]` placeholders below with domain-specific content. The rules themselves are universal — they were discovered through a vault-local instance (`synthesis_bellum`, 2026-03-08) and amended through a second-instance failure (`synthesis_mathesis` KL-divergence, 2026-04-24). Keep them stable.

---

## Terminology (Use These Exactly)

| Term | Definition |
|------|-----------|
| **Phase** | One of the major training units defined in the vault's curriculum (Phase-0 onward) |
| **Concept area** | A numbered topic section within a phase |
| **Atomic concept** | A single idea, principle, mechanism, or insight — the unit of one note |
| **Systematic map** | A comprehensive analysis of a complete domain or thinker, with required structural sections [VAULT-SPECIFIC: cite local map-reference for section count and types] |
| **Phase inventory** | A list of all atomic concepts across ALL concept areas in a phase — mandatory before writing any notes |
| **Frontier marker** | The vault's `phase-status.md` "you are here" pointer — current phase, last-completed atom, next-reachable set |
| **Atom reachable** | All upstream prerequisites of the atom have published Tier-2 notes in the vault's evergreen folder |

---

## The Three Errors This System Prevents

### Error 1 — Compression
Multiple distinct atomic ideas stuffed into one note. Symptoms: note title names a framework, but body defines three separate sub-concepts. Test: would different downstream notes link to different parts of this note? If yes, it is compressed and must be split.

### Error 2 — Scope Gap
Treating one concept area as the entire phase and writing notes only for it. Symptom: one concept area is "done," so the phase is "done" — while other concept areas remain completely untouched. **Root cause: applying the inventory at the concept-area level instead of the phase level.** Fix: always run the Phase Inventory first.

### Error 3 — Atomicity Drift in Live Teaching (the KL-failure pattern)
During a `/teach` session, mid-explanation, the teacher (Claude) finds itself defining a *second* atomic concept inline ("to understand X, let me also briefly cover Y"). Y deserves its own note and its own session. Inlining Y into X bundles two atoms into one lesson the user cannot absorb in one pass and produces a non-atomic note (Error 1) downstream.

**Hard-stop rule**: when this drift is detected mid-session, **stop**. Announce a graph update: "Y is not yet a graduated atom; it needs its own session." Then either (a) terminate the current session and reschedule X after Y is taught, or (b) pivot the current session to Y if X cannot be reached without it. Never bundle.

---

## The Atomicity Principle — The Only Rule for Note Count

**One idea = one note. Count the ideas, not the notes.**

There is no floor and no ceiling. A phase that contains 30 genuinely atomic concepts needs 30 notes. A concept area that contains 2 atomic concepts needs 2 notes. Any count — whether 2 or 40 — is correct if it reflects the actual atomic structure of the content.

**The atomization tests (apply before writing, not after):**

1. *Downstream link test*: Would different downstream notes in the vault link to different parts of this note? If yes — split.

2. *Stand-alone gate test*: Can this note pass all of the vault's mandatory schema sections [VAULT-SPECIFIC: cite local Five Gates / mandatory section list] independently, without referencing another note to complete the answer? If no — it is a fragment. Merge it up.

3. *Framework decomposition rule*: Every framework with N named components = N component notes + 1 framework orientation note. The orientation note explains the architecture and links to the components. It does not re-explain what the component notes explain.

4. *Principle list rule*: Each principle in a doctrine list (e.g., the 9 Principles of War; the 5 postulates of a research vault) gets its own note when it has distinct operational implications, distinct failure modes, and distinct counters. Group principles only when they are operationally indistinguishable.

**The inverse test (preventing over-atomization):**

Can this proposed sub-note be understood without reading the parent concept? If no — it is a fragment, not an atom. Keep it merged.

---

## The Phase Inventory — Mandatory First Step

**Before writing any notes for a phase, produce a complete Phase Inventory: a list of every atomic concept across every concept area in the entire phase, with explicit prerequisite arrows between atoms.**

This is the structural protection against scope gaps and against the KL-failure pattern. The inventory forces you to look at ALL concept areas before starting any one of them, AND forces you to draw the dependency graph before teaching begins. Missing concept areas become visible at the inventory stage. Missing prerequisites become visible before they can be inlined into a teaching session.

### Phase Inventory Format

For each concept area in the phase, list:
- The concept area name and number
- Every distinct atomic concept it contains (apply the atomization tests to each)
- Each concept's note type [VAULT-SPECIFIC: framework orientation / atomic concept / historical case / systematic map / code artifact / etc — list the local types]
- Each concept's **upstream prerequisites** (other atoms within the phase or in earlier phases)
- Any concepts that overlap ≥70% with existing notes → mark as merge candidates

The inventory MUST also produce the **dependency DAG**: a topological view of which atoms can be taught only after which others. Concept-area boundaries are administrative; dependency arrows are pedagogical, and they cross concept-area boundaries freely.

Only after the full phase inventory and DAG are complete should note-writing begin.

---

## The Prerequisites-as-Absent Override

When the user has explicitly stated in `learner/learner-profile.md` (section L2) that prerequisites should be **treated as absent unless demonstrated**, the cadence's pre-flight check (Step 2 below) is mandatory and non-skippable for any atom whose prereqs are marked "user-attested" rather than "✓ taught in vault."

The override exists because user self-reports of prior knowledge ("I have linear algebra basics") are systematically optimistic relative to the standard required for downstream load-bearing use. Re-deriving a prereq the user already holds costs a few minutes and often produces connections they hadn't drawn. Inheriting a missing prereq compounds across an entire curriculum. Asymmetric cost → asymmetric default.

---

## The `/teach` Cadence — Seven-Step Loop

Every `/teach` session in a training vault follows this loop. Most steps are seconds. Cognitive load is concentrated in Steps 3–4.

### Step 0 — Read context (silent)
1. `learner/learner-profile.md` (full, ~300 lines max)
2. `learner/learning-trajectory.md` (tail-read, last ≤10 entries)
3. `[VAULT-ROOT]/phase-status.md`
4. `[VAULT-ROOT]/[VAULT-SPECIFIC: curriculum folder]/phase-N-inventory.md` for the current phase
5. The relevant `[VAULT-SPECIFIC: maps folder]/primer-<domain>.md` for the target atom's domain

### Step 1 — Frontier selection
Pick the next *reachable* atom (all upstream prerequisites have published Tier-2 notes). Among reachable, prefer the atom with the most downstream dependents — unblocks the graph fastest. Announce explicitly: *"Next reachable atom is X. Its prereqs Y, Z are [✓ taught | ✓ user-attested | not yet]."* If any prereq is "not yet," recurse upward until prereqs are clean.

### Step 2 — Pre-flight check (mandatory if Prerequisites-as-Absent override is active)
For each prereq marked "user-attested" but not formally taught in this vault, ask one one-sentence calibration question. *"Before X, can you tell me in one sentence what Y is?"* If the answer is shaky, demote: teach Y first. Redundancy is the correct error.

### Step 3 — Teach
Vault-style explanation [VAULT-SPECIFIC: cite local style preferences from learner-profile, e.g., Feynman + geometric-first + connect-the-dots]. **One atom only.** Apply the Atomicity Drift Hard Stop: if mid-explanation Claude finds itself defining a second atomic concept, **stop and announce a graph-update** instead of continuing. Time budget: typically 25–40 min, but no fixed cap — atomicity matters more than session length.

### Step 4 — Verification gate (both tests required to graduate the atom)
- (a) **Feynman-back**: user explains the atom in 3–5 sentences in their own words.
- (b) **Diagnostic question**: Claude poses one specific application or edge-case question that requires the mechanism, not just the label. Pass = correct + reasoning legible. Fail = atom is **not** marked taught.

If verification fails: session continues with reinforcement (different angle: switch geometric→algebraic, introduce a worked numerical example) OR terminates with status `reinforcement-pending`. Same atom is re-attempted next session.

### Step 5 — Atomic note authoring
Claude creates `[VAULT-SPECIFIC: evergreen folder]/YYYYMMDDHHMM - <Title>.md` using the vault's Tier-2 schema [VAULT-SPECIFIC: cite local note-taxonomy.md and the mandatory section list]. Foundational atoms may ship with `maturity: scaffold` and stub-level optional sections, allowing later revisit when the atom is reused at depth.

### Step 6 — Bookkeeping (Claude proposes, user one-keystroke confirms)
- Update `phase-status.md`: advance frontier, refresh `last_completed_atom`, recompute `next_reachable_set`.
- Append to `learner/learning-trajectory.md`: `{date, atom, verification result, time, what landed, what didn't}`.
- If atom completes a stratum or concept area, update the vault's coverage tracking [VAULT-SPECIFIC: cite local coverage-plan.md].
- If a domain primer's Note Index should be updated, propose the append.

### Session-complete gate
All four conditions must hold to mark a session complete:
- Atom note exists in the evergreen folder with valid frontmatter.
- Verification (Step 4) passed.
- `phase-status.md` advanced.
- Learning-trajectory entry proposed.

If any condition fails, the session is `exposure-only` (atom not graduated) — explicit category, not silent drift.

---

## The Frontier Marker Schema (`phase-status.md`)

Every training vault carries one `phase-status.md` at the vault root. Universal field schema:

```yaml
current_phase: <integer>           # e.g., 0
current_stratum: <slug>            # e.g., 0a, or null if phase has no strata
last_completed_atom: <slug>        # or "none"
last_session_date: YYYY-MM-DD
next_reachable_set:                # atoms whose prereqs are all ✓
  - <slug>
  - <slug>
pending_reinforcements:            # atoms that failed Step 4 last attempt
  - <slug>
phase_N_exit_checklist:            # one block per active phase
  - "[ ] all atoms in inventory have notes"
  - "[ ] culminating exercise committed"
  - "[VAULT-SPECIFIC: any other phase-exit criteria]"
```

The marker is updated atomically at Step 6 of every session. It is the single source of truth for "where am I in the curriculum."

---

## What Gets a Systematic Map vs. Atomic Notes

[VAULT-SPECIFIC: replace this section with the local rule. `synthesis_bellum` rule: complete strategic thinker (10+ concepts, internal dependencies, internal tensions) → systematic map; everything else → atomic notes. `synthesis_mathesis` rule: three map types per `map-reference.md` — concept / domain-primer / framework. Cite the local map-reference document.]

---

## Phase-Specific Strategy

[VAULT-SPECIFIC: per-phase notes on map types, typical atomic-note count, and specific rules. `synthesis_bellum` example: Phase 0 = 25–40 atomic notes, no maps; Phase 1 = essential notes first then theorist maps. `synthesis_mathesis` example: Phase 0 = ~22 atoms across 6 strata, 0 maps; Phase 2 = transformer architecture map after concept atoms.]

---

## Recommended Readings Protocol

[VAULT-SPECIFIC: how recommended readings translate into source ingestion + atomic notes. Universal pattern: (1) atomic concept notes for the phase's own concept areas first; (2) systematic maps for recommended thinkers/domains second; (3) atomic notes generated by maps third.]

---

## The Phase Production Protocol

Apply this at the start of every phase. Do not skip steps.

### Step 1 — Read the Entire Phase Document
Read the complete phase document (curriculum + culminating exercise + recommended readings) before producing the inventory.

### Step 2 — Run the Phase Inventory + DAG
List every atomic concept across every concept area. Apply:
- Framework decomposition rule to all frameworks
- Principle list rule to all doctrine principle lists
- Stand-alone gate test to each proposed atomic concept
- Draw upstream-prerequisite arrows between atoms

### Step 3 — Identify Merge Candidates
For each concept on the inventory: does a note already exist in the evergreen folder that covers ≥70% of this concept? If yes, mark as merge — append to existing note, don't create new.

### Step 4 — Identify Recommended Readings → Map Work
List the theorists/domains/sources the phase recommends. These become systematic maps in Step 6, after concept notes are complete.

### Step 5 — Initialize the Frontier Marker
Set `current_phase`, `current_stratum`, populate `next_reachable_set` from the DAG roots. The frontier marker drives every subsequent `/teach` session.

### Step 6 — Write Notes via the `/teach` Cadence
Process atoms in DAG-frontier order. Each session: pick a reachable atom; teach it; verify; ship the atomic note; advance the marker.

Sequence of note types within a phase:
1. Framework orientation notes (the architecture before the components)
2. Component notes (the atoms of each framework)
3. Standalone concept notes
4. [VAULT-SPECIFIC: historical cases / code artifacts / case studies]

### Step 7 — Build Maps for Recommended Readings
After all phase concept notes are complete, build the systematic maps for the phase's recommended thinkers/domains. Each map generates 5–8 additional atomic concept notes.

### Step 8 — Phase Completion Check
Before declaring a phase complete, verify all `phase_N_exit_checklist` items are checked, and the culminating exercise is committed.

---

## The Mandatory Schema Sections — "The Five Gates" (or local equivalent)

[VAULT-SPECIFIC: replace this section with the local Tier-2 mandatory section list from `note-taxonomy.md` or `vault-config.md`. `synthesis_bellum`'s Five Gates: Operational / Historical / Adversarial / Friction / Fault Line. `synthesis_mathesis`'s Five Gates: Mechanism / Why It Works (and Why It Might Not) / Code Artifact / Pressure Points / Connection to Project. Each gate has a specific question the note must answer; if any answer is "no," the note is incomplete.]

---

## Quick Reference

[VAULT-SPECIFIC: per-phase quick-reference table. Columns: Phase | Concept Areas | Map Type | Typical Note Range | Key Rule. `synthesis_bellum`'s table is at the bottom of `synthesis_bellum/50-Curriculum/phase-learning-methodology.md`. `synthesis_mathesis`'s table at the bottom of `synthesis_mathesis/50-Curriculum/phase-learning-methodology.md`.]

**Universal rule**: Run the Phase Inventory + DAG before writing a single note. No floor. No ceiling. Count the atoms.

---

## See Also

- `framework/vault-type-templates/training/curriculum-template.md` — phased curriculum structure
- `framework/vault-type-templates/training/principles-and-postulates-template.md` — load-bearing priors
- `framework/principles/learner-layer-architecture.md` — `/teach` first-use gate; learner-profile L2 override
- `framework/templates/note-tier-template.md` — Tier 1/2/3 universal structure
- Vault instances: `synthesis_bellum/50-Curriculum/phase-learning-methodology.md` (proof-of-concept, 2026-03-08); `synthesis_mathesis/50-Curriculum/phase-learning-methodology.md` (first formal template instance, 2026-04-25)
