---
description: Companion-mode next-move suggestion. Given a selection or a stuck point, propose 3 distinct next-move options with rationale. Does not write prose.
type: universal-protocol
audience: claude
---

# /co-suggest <selection-or-stuck-point> [--type <next-sentence|next-paragraph|counter|pressure|transition>]

Given the operator's current writing position — a paragraph, a stuck point, a question, a gap — propose **three distinct next-move options** with rationale. Each option is a one-sentence direction, not a generated paragraph. The operator picks an option, then writes.

**<selection-or-stuck-point>**:
- A passage from the essay (pasted in the call) — suggest what comes next.
- A question or description of the gap ("I need to bridge from F1 to F2 but don't know how") — suggest options.
- Empty (no arg) — fall back to asking the operator what they're stuck on.

**[--type]** (optional, biases the kind of suggestion):
- `next-sentence` — options for the single sentence that follows.
- `next-paragraph` — options for the move the next paragraph makes (not its prose).
- `counter` — options for counters/objections that could be raised against the current claim.
- `pressure` — options for what should go in the pressure section of this essay.
- `transition` — options for moving from the current move to a named next move.
- Default: `next-paragraph`.

**Runtime**: Read `voice-profile.md` (for stance constraints on suggested moves), `writer-positions.md` (for bedrock — never suggest a move that violates a non-negotiable), `article-design-principles.md` (to invoke relevant principles in rationale). Read the operator's essay file if accessible (to know what has come before). Read `positions-index.md` if any matched positions are in the essay frontmatter.

---

## Step 1 — Parse Input

1. If a selection is provided (passage or stuck-point description), use that as context.
2. If no selection, prompt the operator: "What are you stuck on? Provide the current paragraph, the last sentence written, or a description of the gap."
3. Infer `--type` from selection content if not explicit (e.g., a trailing question → `counter` or `pressure`; a section-end → `transition`).

---

## Step 2 — Constraints Load

- **Voice constraints**: each suggestion must be compatible with `voice-profile.md` default register (cold-blooded analytical unless essay's audience = metaphysical/philosophical).
- **Position constraints**: no suggestion may violate a `writer-positions.md` non-negotiable. No suggestion may operate from a `Rejected Frames` entry. Suggestions may engage `Open Tensions`.
- **Design-principle constraints**: if the essay is `orthodoxy-counter`-shaped, P1 applies (orthodoxy named before counter strikes). If `framework-build`, P2/P3 apply to pressure suggestions. If any Type D structure, P4–P6 apply.

---

## Step 3 — Generate Three Options

Produce three options. The options must be *distinct* — not variants of the same move. Common distinct shapes:

**For `next-sentence`**:
- Option A: continue the current claim (deepen / unfold).
- Option B: pivot to a different angle (turn / qualify).
- Option C: land the current move (compress / close).

**For `next-paragraph`**:
- Option A: advance the argument (extend the claim with mechanism or case).
- Option B: apply pressure (introduce an objection or counter that must be absorbed).
- Option C: shift unit / scale / frame (zoom in or out, move from abstract to case or vice versa).

**For `counter`**:
- Option A: empirical objection (named case that tests the claim).
- Option B: theoretical objection (named alternative framework producing a different conclusion).
- Option C: category-error objection (the metric / unit / timescale the claim assumes doesn't match practice).

**For `pressure`**:
- Option A: C3-style analogy-validity attack (the claim extends a framework to a domain where conditions differ).
- Option B: C4-style cross-layer feedback (the claim stratifies but the layers aren't independent).
- Option C: P3-style category-error (the metric being defended isn't what practitioners optimize).

**For `transition`**:
- Option A: logical bridge (the next move follows from the prior by explicit implication).
- Option B: tension bridge (the next move appears because the prior produced a pressure the argument must now engage).
- Option C: scale bridge (the next move zooms to a different unit / level to test the prior).

Each option must have:
- **Direction**: a one-sentence statement of what the move does (no prose from the writer's voice; this is a direction, not a draft).
- **Rationale**: 1–2 sentences on why this move serves the argument (what it adds, what risk it mitigates, what principle it realizes).
- **Risk**: 1 sentence naming what the operator should watch for when executing this option (e.g., "requires engaging an orthogonal position from kratos — check positions-index P002 before writing").

---

## Step 4 — Report Options

```
## /co-suggest — YYYY-MM-DD
Type: <type>
Context: <one-line summary of the selection or stuck-point>

### Option A — <one-phrase label>
**Direction**: <one sentence>.
**Rationale**: <1–2 sentences>.
**Risk**: <one sentence>.

### Option B — <one-phrase label>
**Direction**: <one sentence>.
**Rationale**: <1–2 sentences>.
**Risk**: <one sentence>.

### Option C — <one-phrase label>
**Direction**: <one sentence>.
**Rationale**: <1–2 sentences>.
**Risk**: <one sentence>.

---

Pick an option and write. If none fit, rerun /co-suggest with a different --type or a sharper context description.
```

---

## Non-goals

- **Does not draft the paragraph / sentence.** The direction is a verb phrase like "introduce a counter-case that shows the claim fails under condition K" — not the actual sentences the operator would write. Drafting is the operator's job.
- **Does not recommend one option as "best".** The three options are genuinely distinct. The operator picks based on what they want the essay to do.
- **Does not enforce a preset.** Suggestions respect the active preset *if one is set* (advisory in companion mode), but the operator can write outside it.
- **Does not touch the essay file.** Output is a report; the essay is untouched.

---

## Error modes

- If the stuck-point description is too vague to generate distinct options: emit a clarifying question ("What do you want this paragraph to do: land a claim, open pressure, or pivot to a new move?") rather than producing generic options.
- If all three viable options for the requested type violate a non-negotiable (rare — usually signals an essay premise that needs revisiting): report the conflict — "I cannot suggest a <type> move that aligns with your writer-positions non-negotiables. The essay may need to engage a tension before this move is available."
- If the operator asks for a 4th or 5th option: rerun with more specific `--type` or with additional context. Three options is the cap by design — more options means less differentiation per option.
