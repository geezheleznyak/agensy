---
description: Recommend the highest-value next subject given current coverage gaps
type: universal-protocol
audience: claude
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

**Question bank**: Read `synthesis-meta/question-bank.md`. Check for open questions tagged to this vault. If any open questions exist:
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
