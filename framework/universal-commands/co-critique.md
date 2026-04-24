---
description: Companion-mode surgical critique on a selection. Applies the C1-C8 passes from /article-critique, but scoped to a passage rather than a full essay. Never rewrites in-place.
type: universal-protocol
audience: claude
---

# /co-critique <selection> [--mode light|adversarial]

Apply critic-style pressure to a selected passage from a companion-mode essay (or any prose the operator is writing). Shares the 8-pass library with `/article-critique` but scoped to a selection. Returns a bulleted list of issues with location pointers; does not rewrite, does not edit in-place.

**<selection>**: the text to critique. Pasted in the call, or a reference to an essay + line range (e.g., `[[essay-path]]:42-58`).

**[--mode]**:
- `light` (default in companion mode) — clarity, redundancy, voice-match, minor-logic check. Fast surface critique.
- `adversarial` — full C1–C8 pass library from `/article-critique` applied to the selection, plus writing-tells sub-pass. Heavier; use at major decision points.

**Runtime**: Read `voice-profile.md`, `writer-positions.md`, `article-design-principles.md`. Read the full essay file if the selection is a line-range reference (for context — a critique of one paragraph needs to know what came before).

---

## Step 1 — Parse Input

1. Resolve selection:
   - If passage pasted: use directly.
   - If line-range reference: read the essay file, extract those lines.
   - If empty or invalid: abort with "Provide a selection (paste text or give essay path + line range)".
2. Determine mode. Default `light`. Accept `adversarial`.
3. Optionally detect which part of the essay the selection comes from (opening, body, pressure, close) — affects which passes are most relevant.

---

## Step 2 — Run Passes

### Light mode

Runs four quick checks:

- **Clarity**: does the selection make its claim in a way a cold reader follows? Flag unclear referents, undefined jargon, unclear logical connectives.
- **Redundancy**: does the selection say the same thing twice in different words? Flag duplication at sentence or phrase level.
- **Voice-match**: does the selection match `voice-profile.md` (cold-blooded analytical default)? Apply the 11-tic check from voice-profile §LLM-Essay Failure Modes, but only flag instances that appear in THIS selection (don't over-extend to caps across a full essay).
- **Minor-logic**: are there internal contradictions inside the selection? Does a claim on line X contradict a claim on line Y?

### Adversarial mode

Runs the 8 passes from `/article-critique` (see `article-critique.md` Step 3) **scoped to the selection**:

- **C1 — Frame audit**: only fires if the selection contains a load-bearing definitional move. Often does for thesis-bearing passages; rarely for middle-body paragraphs.
- **C2 — Theorist-binding**: fires if a named theorist is cited in the selection.
- **C3 — Analogy validity**: fires if the selection extends a framework cross-domain.
- **C4 — Stratification independence**: fires if the selection layers a domain.
- **C5 — Scenario completeness**: rarely fires for selections — this pass is normally essay-level. Fires if the selection IS the opening or the close and the thesis scope is stated there.
- **C6 — Concession-load**: fires if the selection concedes.
- **C7 — Unit-of-analysis**: fires if the selection makes predicates about a unit; checks consistency with the declared unit in the essay's thesis.
- **C8 — Title-thesis match**: skipped for selection-level critique (essay-level only).

Plus writing-tells sub-pass (always runs in adversarial mode).

Passes that don't apply to the selection are silently skipped. Report lists them as "n/a — target not present in selection".

---

## Step 3 — Report Bulleted Flags

```
## /co-critique — YYYY-MM-DD
Mode: <light | adversarial>
Selection: <essay path + line range, or "(pasted)"; word count>

### Flags

- **<pass | tic> — L<line or paragraph>**: "<excerpt>" — <what's wrong> — <suggested fix, in 1 sentence>.
- ...

(Cluster related flags. If a passage has 3 flags, show them together.)

### Skipped / N/A
- <pass name>: <reason — e.g., "no named theorist in selection" | "selection is not a definitional passage">

---

<For adversarial mode only:>
### What to address first
<one or two sentences naming the most load-bearing issue. If the selection is thesis-bearing and C1 fired, frame audit is typically the first issue. If the selection is a pressure passage and C6 fired, concession-load is typically the first.>

---

Operator decides per-flag whether to address, reword, or dismiss. /co-critique does NOT edit the essay — the operator applies fixes manually.
```

---

## Non-goals

- **Does not rewrite.** `/co-critique` points at issues and suggests fixes in natural language; the operator writes the fix.
- **Does not edit the essay file in any way.** This is a read-only command. All output goes to the report.
- **Does not apply preset-fidelity gates.** Those are pipeline-mode checks in `/article-revise` Pass E. In companion mode, the operator engages preset structure advisorily — `/co-critique` reports on preset-related issues only if the essay has `preset:` set in frontmatter AND the operator invokes `--mode=adversarial` AND the selection is a preset-structural passage (opening, pressure, closing).
- **Does not run the P3 category-error audit unconditionally.** Runs within C7 (unit-of-analysis) if the selection invokes an empirical metric.

---

## Interaction with the shared pass library

`/article-critique` and `/co-critique` share the 8-pass library defined in `article-critique.md` §Step 3. Any refinement to a pass's procedure in that file applies to both commands. Calibration against `synthesis_logos/critic/The frame is the argument, which is the problem.md` is the shared reference.

---

## Error modes

- If selection is too short (< ~50 words) for adversarial mode to fire meaningfully: downgrade to light mode with a notice.
- If the essay file can't be read for line-range references: fall back to treating the selection as pasted-only and note the degraded context.
- If selection is the full essay (>2000 words): suggest the operator run `/article-critique [essay-path]` instead; `/co-critique` is optimized for passages.
- If no flags fire in either mode: report explicitly — "No flags." Do not manufacture flags to fill the report. A clean selection is a possible outcome.
