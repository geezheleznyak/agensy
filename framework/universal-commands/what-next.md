---
description: Recommend the highest-value next subject given current coverage gaps
type: universal-protocol
---

# /what-next

Analyze the vault's current state and recommend the single highest-value next subject to build.

**Runtime**: Read `vault-config.md` from the vault root before executing. Extract:
- `reference_docs.coverage_plan` — path to the vault's coverage plan
- `reference_docs.development_plan` — path to the vault's development plan
- `open_problems[]` — IDs and names for gap analysis
- `domains[]` — slugs and priorities for structural assessment

---

## Step 1 — State Check

**Question bank**: Read `agensy/question-bank.md`. Check for open questions tagged to this vault. If any open questions exist:
- Note which open problems they address
- Flag any question that aligns with a coverage gap (same domain or OP) — these get a connection bonus in the final recommendation

**Coverage snapshot**: Read `reference_docs.coverage_plan`. Record:
- Current note count per domain vs. target
- Which domains have zero coverage (biggest gaps)
- Which open problems have zero notes
- Which planned notes have status: planned (not yet started)

---

## Step 2 — Development Phase Check

Read `reference_docs.development_plan`. Identify:
- Which development phase is currently active?
- What are the priority arcs for this phase?
- Are phase targets being met?

---

## Step 3 — Dependency Analysis

Identify structural dependencies — subjects that many other subjects depend on:
- Foundation concepts that other notes will need to link to
- Thinkers whose frameworks underlie multiple planned notes
- Historical cases that calibrate multiple theoretical claims

A subject that will be linked from 5 future notes is more valuable than one linked from 1. Name the specific dependency chains.

---

## Step 4 — Open Problem Coverage

Check which open problems (vault-config.md `open_problems[]`) have the fewest notes addressing them.
Flag problems with zero coverage that fall within the current phase's priority domains.

---

## Step 4.5 — Learner Layer Readiness Check

Skip this step entirely if `agensy/learner/` does not exist (vault user has not adopted the Learner Layer).

### 4.5.1 — Load learner context (lazy, capped)

- Read `agensy/learner/learner-profile.md` (capped ≤300 lines — comparable to a CLAUDE.md). One full read.
- Grep `agensy/learner/interests-register.md` Active Interests section for entries matching the current vault's domains, current obsessions from L4 of the profile, or any candidate subjects from prior steps. Do NOT read the whole file.

### 4.5.2 — Readiness gate against `system-model.yaml`

If the vault has a `system-model.yaml` (skip if not):

For each candidate subject from Steps 1–4, identify the corresponding system-model node(s) (by domain + concept match). For each candidate node:
- Walk `produces`, `requires`, `gates` edges backward to identify prerequisite nodes
- Check each prerequisite node's `user_engagement` annotation
- If any prerequisite is `unseen` or unannotated AND the prerequisite is structurally load-bearing (referenced by ≥2 other nodes downstream), mark the candidate as **prereq-gapped**

A `prereq-gapped` candidate is **deprioritized** — not eliminated. The user may legitimately tackle a topic before its prereqs (depth-first learning is a valid mode). The recommendation MUST surface the gap explicitly so the user can override:
> "Recommended: X. Note: prerequisite node Y (`unseen`) supports this concept structurally; consider /arc Y first if you want to build the foundation, or proceed with X if jumping in is intentional."

### 4.5.3 — Interest boost

If a candidate matches an active entry in `interests-register.md` (topic overlap), boost its priority. Surface the match in reasoning:
> "This subject matches active interest INTEREST-#### (`<topic>`, surfaced YYYY-MM-DD)."

### 4.5.4 — Profile-level calibration

Use `learner-profile.md` to calibrate the recommendation framing:
- L4 current obsessions: prefer subjects that connect to active obsession threads
- L7 goals: prefer subjects that advance the 1–2 year goal trajectory
- L6 learning style: phrase the recommendation in the user's preferred mode (e.g., for a Feynman-style learner, lead with the intuition the subject unlocks, not the formal scope)
- L5 taboo areas: do NOT recommend subjects in declared taboo areas (will be empty for users who declared "open to everything")

### 4.5.5 — Token-budget discipline

- learner-profile: one read per `/what-next` invocation
- interests-register: grep only, never full read
- system-model.yaml: already loaded by Step 3 dependency analysis if you're using the system-model — no additional cost

---

## Step 5 — Recommendation

State a single recommendation:

**Recommended next subject**: [Name]
**Type**: thinker | concept | framework | historical case
**Domain**: [slug from vault-config.md domains[]]
**Command to use**: `/arc [subject] [type]`

**Reasoning** (3–5 sentences):
- Why this subject over all others at this moment
- Which coverage gaps it closes
- Which open problems it addresses
- Which future notes it enables as a structural dependency

**Second priority**: [subject] — if the recommended subject is unavailable or already in progress.

---

## Step 6 — Update Session State

Update `memory/session-state.md`:
- Update `last_what_next` to today's date
- Write `open_actions`: the recommended subject as `"/arc [subject] [type]"` plus the second priority
- Update `last_updated`
