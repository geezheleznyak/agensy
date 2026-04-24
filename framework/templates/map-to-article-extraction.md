---
type: schema
audience: claude
---

# Map-to-Article Extraction Schema

Reference document for `/article-seed`, `/article-outline`, and `/article-draft`. Defines the deterministic recipe for pulling article-grade content out of vault maps.

**Scope**: V1 covers Type A (solo map → article). Type B (pair), Type C (MOC position), and Type D (braid) are sketched for V2 but not implemented.

---

## Core Insight

Vault maps already encode arguments. A philosopher or theorist map follows this arc:

> founding problem → first principles → core concepts → pressure points → influence lines → project connection

This is already proto-article structure. Extraction is not *generation* — it is *rearrangement + voice shift + vault-jargon purge + stakes translation*.

---

## Map-Section → Article-Role Mapping

For thinker-maps, concept-maps, and framework-maps in the agensy map ecosystem (see `[AGENSY_PATH]/framework/templates/map-type-template.md`).

| Map section | → Article role | Extraction rule |
|---|---|---|
| Founding problem / Context | → **Hook + Problem statement** | Strip historical framing; restate as live problem a contemporary reader feels. If the map names a historical crisis (e.g., "Parmenides-Heraclitus collision"), translate the crisis into a problem the reader recognizes (e.g., "how can something both persist and change"). |
| First principles / Core claims | → **Thesis candidate** | Extract the single most defensible claim. A first-principle list usually implies a thesis; name it explicitly, don't inherit the list. Thesis must be stateable in one sentence. |
| Core concepts (Depends / Enables / Constrains blocks) | → **Argument moves (3–5)** | Each core concept becomes a body section. Order by dependency: concepts that other concepts depend on go earlier. Drop concepts not load-bearing for the thesis. |
| Pressure points | → **Counter-argument / stress-test section** | Mandatory. A draft that skips the pressure points is intellectually dishonest. Pick the 1–2 strongest pressure points; argue them as the map does, then answer them. |
| Influence lines / Reception | → **Context paragraph** | Use sparingly. One or two lineage lines to situate the thinker/framework; no more. Readers want the argument, not the genealogy. |
| Historical evidence / Cases | → **Illustrative cases** | Pick one or two cases that illustrate the thesis concretely. Prefer the case where the thesis *almost fails*, not the paradigmatic case — argument strength compounds under stress. |
| Connection to the Project / Judgment Instrument | → **Stakes (but translated)** | The map says "this gives X to the project"; the essay must say "this lets *you* read the world differently". Translate vault-project stakes into reader-stakes. |
| Atomic Notes Index | → **Citation pool** | When a claim in the draft needs external support, pull from this pool first. Each atomic note is a pre-argued sub-claim with its own structure — reuse aggressively. |

---

## What to Drop

- Mermaid diagrams (unless the essay needs a diagram — rare; re-generate simplified if so)
- YAML frontmatter (all of it; articles have their own frontmatter from the Essay Template)
- Vault-internal references that don't resolve for cold readers (internal wikilinks, open-problem IDs, domain slugs, fault-line frontmatter values as raw tokens)
- Schema meta-commentary ("This map uses the adversarial preset...")
- Section headers from the map (articles use their own narrative structure)

---

## Thesis Candidate Extraction

The hardest step. Philosophy/theorist maps often have 4–6 first principles; only one of them generalizes to a thesis.

**Heuristic** (in order):
1. Read the map's "Pressure Points" section first. Which first principle is *attacked* by the strongest pressure point? That principle is the load-bearing claim — the thesis candidate.
2. If multiple first principles are attacked, pick the one the map's author clearly considers non-negotiable (the one whose failure would collapse the rest).
3. If none are attacked, the map is weak — flag as "Developable" in `/article-scan` output and decline to seed.

**Format**: thesis candidate is one sentence, declarative, defensible. Not a summary. Not a question. A claim someone could reasonably disagree with.

**Examples**:
- From `clausewitz-systematic-map.md` — *Thesis*: "The political purpose of force cannot be separated from force itself, which is why every military operation that pretends to be apolitical carries the politics it denies."
- From `aristotle-systematic-map.md` — *Thesis*: "Form is not imposed on matter from outside; it is immanent, and this is the only way change and persistence can coexist."

---

## Narrative Arc (for `/article-outline`)

Arc imposition is **preset-driven** (V1.5+). `/article-outline` reads the `preset` field from the seed frontmatter, consults `synthesis_logos/article-presets.md`, and imposes the blueprint defined there. Each preset parameterizes four structural dimensions: **opening type**, **body arc**, **pressure type**, **closing type**. All other sections of this schema (map-section mapping, thesis extraction, what-to-drop rules, voice-position integration, standalone-ness test) remain universal across presets.

**Active presets (V1.5)**:

| Preset | Opening | Body arc | Pressure | Closing |
|---|---|---|---|---|
| `framework-build` (default) | phenomenon-first | concept-by-concept | stress-test | diagnostic |
| `orthodoxy-counter` | orthodoxy-first | standard | three-accounts | aphoristic |
| `case-anatomy` | case-first | structural-unfold | counterfactual | lesson |
| `diagnostic-lens` | reading-failure | lens-components | overreach-risks | reader-ready-diagnostic |
| `synthesis-braid` *(V2, deferred)* | seam-first | braided | seam-stress | emergent-claim |

See `article-presets.md` for full definitions (paragraph-level opening recipes, required slots, word budgets, principles realized, pilot validation).

### `framework-build` default arc (reference form)

When a seed's preset is `framework-build`, `/article-outline` imposes this seven-part arc (the pre-V1.5 hardcoded arc, preserved as the default):

1. **Hook** — one paragraph. Drops the reader into the phenomenon without preamble. The map's founding problem, translated.
2. **Problem statement** — one to two paragraphs. What the phenomenon is, why it matters, what the usual framing misses.
3. **Thesis** — stated clearly, usually at the end of the problem section.
4. **Argument moves (3–5 body sections)** — each move is a framework component. Each move includes: the sub-claim, the mechanism, and the case.
5. **Pressure** — for each component, name the boundary conditions under which it breaks.
6. **Implication** — what this framework lets the reader see or do. Translated stakes.
7. **Close** — diagnostic. Reader-ready tool ("next time you see X, ask Y").

**Length budget (universal: 2,000–4,000 words across all types and presets, v1.8)** — applies to every essay regardless of type A/B/C/D or preset. See `article-presets.md` §"Global length constraint". `framework-build` default allocation:
- Hook: 100–200 words
- Problem + thesis: 300–500 words
- Argument moves: 1,200–2,200 words (300–500 per move × 3–5 moves)
- Pressure: 300–600 words
- Implication + close: 200–400 words

Other presets supply their own sub-allocations in `article-presets.md`, all summing to ≤4,000w.

### Preset selection at seed time

`/article-seed` Step 2.5 infers the preset from thesis-candidate grammar (or accepts `--preset <id>` override) and records it in seed frontmatter. `/article-outline` is not expected to re-infer; it reads the seed value. If the seed has no preset field (pre-V1.5 essay), treat as `framework-build`.

---

## Voice and Position Integration (for `/article-draft`)

The draft command reads three inputs:
1. **Outline** (from `/article-outline`) — argumentative spine
2. **voice-profile.md** (vault root) — style layer
3. **writer-positions.md** (vault root) — substance layer

**Per-paragraph check** (draft command applies this as it generates):
- Does this paragraph advance a move from the outline? If no → cut.
- Does this paragraph's voice match voice-profile.md? If no → redraft in profile.
- Does this paragraph's claim conflict with writer-positions.md? If yes → flag; do not paper over.

**Wikilink handling**:
- Internal vault wikilinks are *never* included in the draft output.
- Instead: the wikilinked concept is unpacked into prose (one to three sentences, enough for a cold reader to follow).
- The citation is recorded in the essay's `source_refs` frontmatter for traceability, not inline.

---

## Standalone-ness Test

Before a draft can move to revision:
- Does the draft read if every vault wikilink is stripped? If not → reopen for prose unpacking.
- Does the draft read if the source map is not available to the reader? If not → add problem/stakes context.
- Does the draft define every term that a cold reader would not know? If not → gloss inline (not footnote).

---

## Type B / C / D

**Universal length cap (v1.8)**: all types share the 2,000–4,000w target. Pair / MOC / braid do not earn extra length by virtue of source multiplicity — they earn tighter compression.

### Type B: Pair (2 maps, shared problem)

- Total length: **2,000–4,000w** (same as Type A; pair does not automatically extend length).
- `/article-seed` takes 2 map paths.
- Extraction: compare the two founding-problem blocks. The **shared problem** is named as the hook — often broader than either map's stated problem.
- Thesis: usually a *synthesis* claim — both maps are partially right, here's the scale/domain under which each holds.
- Argument moves: structured as "Map 1's answer → Map 2's answer → where they collide → scale-conditioned resolution".
- Pressure: the *strongest remaining objection* after synthesis.

### Type C: MOC Position Piece (1 MOC)

- Total length: **2,000–4,000w** (same as Type A).
- `/article-seed` takes 1 MOC path.
- Extraction: the MOC's *implicit thesis* is the target. MOCs argue by composition — what's included, what's emphasized, what tensions are foregrounded.
- Thesis: stated as the MOC's position on its domain's fault line, which the MOC demonstrates by arrangement but rarely articulates.
- Argument moves: the MOC's main sections become essay sections; each section defends the implicit thesis from that angle.

### Type D: Braid (3–5 maps, thematic)

- Total length: **2,000–4,000w** (same as Type A).
- Per-framework budget: 400–800w × N frameworks (N=3), scaling down to 300–500w × 5 if N=5. Braid/compression: 200–400w. Pressure: 400–700w. Opening+closing: 500–900w combined. Universal ceiling: 4,000w. If nominal sums exceed 4,000w, compress per-slot before drafting.
- `/article-seed` takes a theme and 3–5 map paths.
- Extraction: the theme is named as the through-line. Each map contributes one argument move.
- Thesis: a claim about the theme itself (not about any one map).
- Argument moves: one per map, each a full sub-argument.
- Pressure: where the maps *disagree* — synthesize into one pressure pass, not per-framework enumeration.
- Specific V2 priority (per plan): Kratos × Oikos "Power Asymmetry & Narrative" braid (Zuboff/Strange × Shiller/behavioral).

---

## File Path Conventions

- Maps live in source vault `[vault]/theory/maps/` or `[vault]/philosophy/maps/` or `[vault]/_maps/` depending on vault.
- Seeds land in `synthesis_logos/10-Thoughts/YYYYMMDDHHMM - [Title].md`.
- Outlines and drafts land in `synthesis_logos/20-Essays/YYYYMMDDHHMM - [Title].md` (same file; status progresses via frontmatter).
- Published essays land in `synthesis_logos/40-Published/`.
