---
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: style-card
status: unseeded
---

# Voice Profile

**Style layer** — HOW the writer writes. Consumed by `/article-draft` and `/article-revise` on every run. Pairs with `writer-positions.md` (substance layer).

**Status progression**: `unseeded` → `seeded-v0.1` (a default register is chosen + one corpus sample described) → `seeded-v0.5+` (calibration after first pilot essay: cadence notes, stance markers, failure modes observed in practice). `/article-draft` refuses to run when `status: unseeded` — a vault cannot produce prose in your voice if your voice is not on file.

---

## How this file is used

- `/article-draft` reads this before generating prose. Every sentence is drafted against this profile.
- `/article-revise` checks drafts against this profile, flagging passages that drift toward a neutral-essayistic default or toward the vault's own analytical register.
- `/article-critique` and `/co-critique` use the §"LLM-Essay Failure Modes" checklist to surface tells that distinguish AI-generated prose from your voice.
- Edits are made by you directly. In companion mode, `/co-capture --target voice` can append new corpus samples or register notes with your confirmation.

---

## Sample Inventory

*Describe the corpus that calibrates your voice. A good voice-profile starts with at least one sample of 2,000+ words of your prose at the register you want the pipeline to produce. Aphoristic / short-form corpora calibrate tone but not paragraph-level rhythm; long-form is what the pipeline extrapolates to essay register.*

| Sample | Length | Date | Register |
|---|---|---|---|
| *[Path or description of sample 1 — e.g., "personal Telegram channel export"]* | *[Word or character count]* | *[Date range]* | *[Register summary — aphoristic / essayistic / prose-thinking / etc.]* |

**Corpus shape notes**:
- *[Describe the distribution — e.g., "mostly short-form aphorism; ~15% paragraph-length passages"]*
- *[Note any genre mix — bilingual? quoted passages? project-journal vs. outward-facing?]*

**Calibration caveat**: if your corpus is aphoristic but you want the pipeline to produce essay prose, flag the extrapolation gap here (see §"Extrapolation Notes" below).

---

## Default Register

*Choose a register that your essays default to. Common choices (pick one or describe your own):*

- **Cold-blooded analytical** — structural description without moral framing; paragraphs unfold a mechanism rather than deliver a verdict.
- **Engaged critical** — analytical but with stated stakes and moral position; arguments are accompanied by their "so what."
- **Contemplative / philosophical** — patient depth; rhetorical questions and elaboration are acceptable; paragraphs dwell.
- **Sardonic / mordant** — analytical with dry humor; compression with a bite.
- **Plainspoken / journalistic** — narrative drive; prioritizes comprehension over technical precision.

**Your default register**: *[State the register you want as default. Describe what it is and what it is NOT (what register traps essays in this voice tend to fall into).]*

### What it is

*[3–5 bullet points describing the register's positive characteristics.]*

### What it is NOT

*[3–5 bullet points describing registers your voice is explicitly not — often this catches drift modes.]*

### Operational tests (for `/article-revise`)

*[3–5 concrete tests that let `/article-revise` Pass B flag voice drift. Each test should be checkable from the prose alone.]*

---

## Cadence and Rhythm

*Describe your sentence-length distribution and paragraph structure. This is what distinguishes your voice from a generic essay voice.*

- **Sentence-length distribution**: *[e.g., "mostly 15–25 word sentences; ~20% shorter punches; rare sentences over 40 words"]*
- **Paragraph structure**: *[e.g., "3–7 sentences doing different argumentative work — setup, turn, qualify, land"]*
- **Cadence rules**: *[e.g., "no more than 2 consecutive short sentences; every paragraph ends on the sentence that did the paragraph's final work, not necessarily a punch line"]*

---

## Stance Markers

*Phrases, moves, or rhythms that signal your stance without stating it. Often these are the tells that make prose feel like yours.*

*[List 5–10 stance markers. Each is a phrasing or structural move that is distinctive to your voice. Examples: "never hedges the conclusion after structurally laying it out", "reaches for the mechanism before the verdict", etc.]*

---

## Openings

*How you tend to open essays or sections. Patterns you reach for.*

*[3–5 opening patterns. Each with an example or a description of when you use it.]*

---

## Closings

*How you tend to close. The landing of the argument.*

*[3–5 closing patterns. Each with a description.]*

---

## Metaphor and Imagery

*What kinds of metaphors you use. What kinds you avoid.*

*[3–5 notes on metaphor discipline. What registers of metaphor (mechanical / biological / military / geometric / etc.) are native to your voice.]*

---

## Diction

*Word-level preferences. Technical vocabulary, Latin or vernacular, abstract vs. concrete.*

*[5–10 diction notes. Capture the texture of your word choice — which registers you mix, which you avoid.]*

---

## Structural Tics

*Specific structural moves that recur in your prose. These are features, not bugs.*

*[3–7 structural tics. Each with a description.]*

---

## Negative Space

*Things your prose avoids. What you will not write. Often harder to specify than what you will write — but critical for `/article-revise` to catch drift.*

*[5–10 negative-space rules. Each is a concrete thing that, if it appears, is a drift flag.]*

---

## Audience Modulation

*How your voice changes for different audiences. Most essays will default to your primary audience; specify when you shift.*

*[Table or bullet list covering 2–4 audience types you write for, with voice modulations for each.]*

---

## LLM-Essay Failure Modes

*The specific AI-generation tells that your voice must avoid. Calibrated over time as drafts fail. Start with the seven common ones; extend as you learn your pipeline's failure modes.*

### The seven baseline tics

1. **Uniform sentence rhythm** — AI prose tends to produce sentences of similar length and cadence, marching instead of varying. Your voice breaks this by deliberately mixing lengths.
2. **Throat-clearing openings** — "In today's complex landscape", "It is important to note that", etc. Your voice opens into the thing directly.
3. **Safety hedges** — "could be argued", "some might say", "it is worth considering". Your voice makes the claim, then pressure-tests it.
4. **Transition bloat** — "Furthermore", "Moreover", "Additionally", "In conclusion". Your voice moves by substance, not by connectives.
5. **Definition-first pedagogy** — stopping to define a term before using it. Your voice lets the term arrive doing work; the reader learns by use.
6. **Thesis repetition** — stating the thesis in the intro, restating at paragraph openings, re-announcing in the close. Your voice lands the thesis and moves on.
7. **Balance-for-balance's-sake** — "On the one hand... on the other hand..." when the essay's actual position is asymmetric. Your voice states the asymmetry.

*(Add your own observed failure modes as you draft. The seven above are the most common starting set.)*

### Revision protocol

When `/article-revise` Pass B detects a voice drift:
1. Flag the specific passage and which tic it matches.
2. Propose a rewrite in your voice.
3. If the rewrite produces a factual or logical drift, flag — do not silently lose content.

---

## Extrapolation Notes

*If your calibration corpus is smaller, more compressed, or in a different genre than your target essays, note the extrapolation rules here.*

### Calibration history

*[List of essays that have refined this file, with one-line notes on what each taught.]*

- *[v0.1 — initial seed from corpus sample]*
- *[v0.2 — after first pilot essay: what drifted, what held]*
- *...*

### Pending calibration

*[Things you know your voice needs but haven't yet calibrated. Ship-of-Theseus items.]*

---

## Seed Samples

*If you have short canonical passages — 2–5 paragraphs — that exemplify your voice at its best, paste them here. `/article-draft` will read them as anchor calibration beyond the statistical profile.*

*[Optional: 2–5 passages of your prose, each with a brief note on what it exemplifies.]*

---

## See Also

- `writer-positions.md` — substance layer (WHAT you believe). Separate from voice (HOW you write).
- `article-design-principles.md` — craft principles (structural rules for essays). Apply across all voices.
- `article-presets.md` — narrative-arc blueprints. Preset-level decisions are upstream of voice-level decisions.
