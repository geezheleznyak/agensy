---
description: Hand-mode Pass 3 — Honesty. Composes /article-critique C1–C8 (full mode) + writer-positions non-negotiables check + framework §VI honesty audit ("where is the argument thinner than the prose suggests?"). Output is a notes block; never a rewrite.
type: universal-protocol
---

# /hw-pass-3 [essay-path] [--force]

Pass 3 of the three-pass hand-mode revision protocol (framework §VI: "Honesty. Where are you faking it? Where is the argument thinner than the prose suggests? Mark these. Either repair them or admit them in the text. Faked confidence is the surest way to lose a reader who matters."). Composes existing infrastructure: `/article-critique` C1–C8 (full mode), `writer-positions.md` non-negotiables check (the same logic in `/article-revise` Pass C Layer 1), and framework §VI's honesty audit.

Pass 3 is the last audit before `/article-handwrite finalize`. Operates on operator-written prose. Never edits the essay body — output is `## Pass 3 Notes` appended.

**[essay-path]**: optional. Defaults to most recent `mode: handwrite` essay with status `handwrite-pass-2`.

**[--force]**: bypass the 24h time-gate. Logged.

**Runtime**: Read `vault-config.md`. Extract:
- `reference_docs.essay_framework`
- `reference_docs.framework_integration`
- `reference_docs.writer_positions`
- `reference_docs.hand_mode_protocol`
- `folder_structure.critic`

---

## Step 1 — Pre-conditions

Refuse with specific reason if any fails:
1. Essay exists; `mode: handwrite`.
2. Status is `handwrite-pass-2` or `handwrite-pass-3` (re-run allowed).
3. **Time gate (24h)**: `now - updated >= 24h`, unless `--force`. Same rationale as Pass 2.
4. Pass 2 Notes block exists in body.

---

## Step 2 — Skip-diagnostics warning (if applicable)

Read `diagnostics_locked` from frontmatter. If `false` (i.e., `start --skip-diagnostics` was used), the **first content** of Pass 3 Notes must be a flagged warning:

```
> **WARNING — diagnostics not locked.** This essay was started with `--skip-diagnostics`. The three pre-writing diagnostics (question-not-topic, steelmanned objection, hostile-but-fair reader) were never answered. Pass 3 cannot retroactively run those gates. Consider: is the essay's question one whose answer could have surprised you? Have you steelmanned the strongest opposing view in this draft? Is there a specific intelligent skeptic this essay is addressed to? If any answer is no, the essay is structurally weaker than the prose may suggest. Address before promoting.
```

This warning is mandatory when `diagnostics_locked: false`. It is the cost of using `--skip-diagnostics`.

---

## Step 3 — Audit: Critique passes C1–C8 (compose `/article-critique --mode=full`)

Invoke `/article-critique` against the essay, mode `full`. Reuse the existing protocol and its existing `critic/` output convention. The critique runs C1–C8:

- **C1** — frame circularity (question and answer share a hidden premise)
- **C2** — theorist-as-stamp (citing X without engaging X's argument)
- **C3** — analogy validity (cross-domain analogies that don't hold under load)
- **C4** — stratification independence (claims that depend on a hidden ordering)
- **C5** — scenario silence (cases the essay's frame can't see)
- **C6** — concession-load (concessions that swallow the thesis)
- **C7** — unit-of-analysis drift (the essay quietly changes what it is talking about)
- **C8** — title-thesis match

Pass 3 does NOT re-implement C1–C8. It calls `/article-critique --mode=full [essay-path]` and ingests the output. The standalone critique writes to `critic/`; Pass 3 then summarizes the C1–C8 verdicts inline in Pass 3 Notes (one line per critique pass, with "see critic/[file]" pointer for full detail).

**Calibration anchor**: `critic/The frame is the argument, which is the problem.md` is the canonical calibration sample for C1. Pass 3 inherits the calibration without restating it.

---

## Step 4 — Audit: Writer-positions non-negotiables

Read `writer-positions.md`. Extract the section listing **non-negotiables** (the section name is vault-specific; per the existing `/article-revise` Pass C Layer 1, look for the section explicitly tagged "non-negotiable" or its closest variant).

For each non-negotiable, scan the essay body for sentences that **violate** the commitment. A violation is:
- A sentence whose claim is incompatible with the non-negotiable.
- A sentence whose framing concedes a position the non-negotiable refuses.
- A sentence whose absence (e.g., a missing caveat the non-negotiable requires) would constitute the violation.

Reuse the existing logic in `/article-revise` Pass C Layer 1 verbatim. Do not invent new checks.

Output: violation count + each violation with: paragraph, sentence, the non-negotiable it violates, and one sentence on whether it can be repaired in-text or whether the essay's frame conflicts with the operator's commitments at a deeper level (the latter is an Open Tension worth capturing).

---

## Step 5 — Audit: Framework §VI honesty pass

Framework §VI: "Where are you faking it? Where is the argument thinner than the prose suggests?"

This is the audit that mechanical critique does not capture. Heuristics:

1. **Confidence-asymmetry scan**. For each load-bearing claim in the essay (claims the thesis depends on): compare the prose's confidence (modal verbs, hedges, asserted-vs-conditional) against the underlying support (evidence cited, T3s referenced, source maps grounded). Flag claims whose prose-confidence exceeds support.
2. **Resting-point honesty**. Re-read the Resting Point (§III) — does it acknowledge what is still unknown, or does it overstate the conclusion the body actually earned? Flag forced resolutions explicitly.
3. **Where the argument thins**. Identify the 1–3 sentences in the essay where the operator can most plausibly be "faking it" — sentences that paper over a gap in the argument with stylistic confidence. These are framework §VI's primary targets. Flag them with a direct prompt: "Repair, or admit in the text. Faked confidence is the surest way to lose a reader who matters."

This audit is necessarily judgment-laden, not mechanical. Pass 3 outputs the flags as a prompt to the operator; the operator decides whether to repair, admit, or override.

---

## Step 6 — Append Pass 3 Notes to Essay

```markdown
---

## Pass 3 Notes — YYYY-MM-DD [--force was used: <yes|no>]

[If diagnostics_locked: false — the warning block from Step 2 appears here]

### C1–C8 critique pass (composed from /article-critique --mode=full)
- Output written to: critic/[file].md
- Summary verdicts:
  - C1 frame circularity:    <pass | flagged> — <one-line>
  - C2 theorist-as-stamp:    <pass | flagged> — <one-line>
  - C3 analogy validity:     <pass | flagged> — <one-line>
  - C4 stratification:       <pass | flagged> — <one-line>
  - C5 scenario silence:     <pass | flagged> — <one-line>
  - C6 concession-load:      <pass | flagged> — <one-line>
  - C7 unit-of-analysis:     <pass | flagged> — <one-line>
  - C8 title-thesis match:   <pass | flagged> — <one-line>

### Writer-positions non-negotiables
- Non-negotiables checked: <count>
- Violations: <count>
  - <paragraph "first 8 words…"> — "<sentence>" — violates <commitment> — <repair-in-text | frame-conflict>
  - …

### §VI honesty audit
- Confidence-asymmetry flags: <count>
  - "<sentence>" — prose-confidence: <high|medium>; support: <weak|medium>
- Resting-point verdict: <honest | forced-resolution> — <one-line>
- Fake-confidence candidates: <count>
  - "<sentence>" — repair, or admit in the text.

### Pass 3 verdict
<one sentence — clean / repair flagged honesty issues / frame-level rewrite recommended>
```

Update frontmatter:
- `status: handwrite-pass-3`
- `updated: YYYY-MM-DD`
- Append to `handwrite_session_log`:
  ```yaml
  - date: YYYY-MM-DD
    event: pass-3-run
    diagnostics_warning_surfaced: <true|false>
    c1_c8_flags: <count>
    non_negotiable_violations: <count>
    honesty_flags: <count>
    force_used: <true|false>
  ```

---

## Step 7 — Report

```
## /hw-pass-3 [path] — YYYY-MM-DD

Pass 3 (Honesty) complete.[--force used: yes]
[Diagnostics-not-locked WARNING surfaced in Pass 3 Notes.]

C1–C8 critique:
  C1: <pass|flagged>  C2: <…>  C3: <…>  C4: <…>
  C5: <…>            C6: <…>  C7: <…>  C8: <…>
Full critique at: critic/[file].md

Non-negotiable violations: <count>
§VI honesty flags: <count>

Pass 3 Notes appended to essay body.
Status: handwrite-pass-3.

Recommended next:
- Repair flagged honesty issues OR admit them in the text.
- Set title to claim-form (frontmatter `title:`).
- /article-handwrite finalize, then /article-promote.
```

---

## Error modes

- Time gate trips without `--force`: refuse with unlock time + framework §VI rationale. Same as Pass 2.
- Pass 2 Notes missing from body: refuse. Pass 3 audits a sentence-clean draft; without Pass 2 there is no signal that sentence-level revision occurred.
- `/article-critique` invocation fails: halt and surface the upstream error. Do not append a partial Pass 3 Notes block — partial honesty audit is worse than no audit.
- Writer-positions.md missing or unfilled: warn and proceed with §VI honesty audit only. Surface "non-negotiables check skipped — writer-positions is <missing|unfilled>" in Pass 3 Notes verdict.
- Re-run on `handwrite-pass-3`: replace prior Pass 3 Notes block. Re-run `/article-critique` against current body (existing critic/ files are versioned by the critique protocol; do not overwrite).
- Frame-level rewrite recommended (multiple C-flags + multiple honesty flags): output the verdict as "frame-level rewrite recommended; do not finalize without addressing C[N] and the honesty flags first." `/article-handwrite finalize` does not refuse on this basis (it is advisory), but the verdict is loud.
