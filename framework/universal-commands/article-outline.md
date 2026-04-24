---
description: Convert an essay seed into a structured outline with status:outline in 20-Essays
type: universal-protocol
audience: claude
---

# /article-outline [seed-path]

Take a seed note from `10-Thoughts/` and produce a structured outline in `20-Essays/`. Imposes the narrative arc defined in `map-to-article-extraction.md` §"Narrative Arc".

**[seed-path]**: absolute or vault-relative path to a seed note created by `/article-seed`.

**Runtime**: Read `vault-config.md` from cogitationis vault root. Extract:
- `reference_docs.map_to_article_schema` — path to extraction recipe
- `reference_docs.article_presets` — path to article-presets.md (V1.5)
- `reference_docs.writer_positions` — path to writer-positions.md
- `reference_docs.positions_index` — path to positions-index.md (V1.6)
- `reference_docs.source_map_registry` — for status update
- `folder_structure.essays` — destination folder
- `note_template.synthesis` — essay frontmatter schema

---

## Step 1 — Validate Input

1. Verify [seed-path] exists and has frontmatter `type/article-seed` (or `type/thought` with `article_type: A` or `D`).
2. Branch by type:
   - **Type A**: if seed lacks a thesis candidate or has fewer than 3 argument moves: refuse, recommend re-running `/article-seed` or manually strengthening the seed.
   - **Type D (V1.7)**: if seed lacks `seam`, `source_maps` (list of ≥3), `braid_move`, or emergent thesis candidate: refuse. If any framework has fewer than 2 argument moves: refuse (braids are thin if any individual strand is thin). Verify `preset: synthesis-braid` is set; if not, refuse ("Type D seeds must carry preset=synthesis-braid").

---

## Step 2 — Read the Seed + Source Map(s) + Preset

1. Read the seed file fully, including frontmatter.
2. Extract `preset` field from seed frontmatter (V1.5). If missing (pre-V1.5 seed), default to `framework-build`.
3. Read `article-presets.md` from cogitationis root. Locate the block for the seed's preset. Extract `structure.opening`, `structure.body`, `structure.pressure`, `structure.closing` blocks and their word budgets.
4. Read the source map(s):
   - **Type A**: single `source_map` frontmatter field.
   - **Type D**: all N entries in `source_maps` frontmatter list. Read each in full — the outline will need per-framework detail beyond what the seed carried.
5. Read `writer-positions.md`.
6. Extract `matched_positions` from seed frontmatter (V1.6). For each entry, read the referenced T3 note's claim sentence, mechanism paragraph, and primary pressure. Buffer for Step 3.5.
7. **Type D only**: extract `seam`, `braid_move`, `seam_stress_checks` from seed frontmatter. These drive Step 3's braid blueprint imposition.

---

## Step 3 — Impose Preset Blueprint (V1.5)

Arc imposition is preset-driven. Build the outline by instantiating the preset's four structural dimensions — opening type, body arc, pressure type, closing type — as documented in `article-presets.md`.

**Opening**: read `structure.opening.type` and `structure.opening.paragraphs` from the preset. Each paragraph listed becomes a beat in the Opening section of the outline, with the stated word budget.
- `phenomenon-first` (framework-build): 4 paragraphs — name phenomenon, gesture at consequence, introduce framework author/origin, compress to thesis.
- `orthodoxy-first` (orthodoxy-counter): 7 paragraphs — name orthodoxy + lineage, name hidden premise, strike anchor case, unpack case, introduce counter-framework, generalize mechanism, compress to thesis.
- `case-first` (case-anatomy): 3 paragraphs — drop reader into event with specificity, name outcome, indicate structural layer.
- `reading-failure` (diagnostic-lens): 3 paragraphs — show dominant reading missing mark, name missing move, preview the lens.
- `seam-first` (synthesis-braid, V1.7): 4–5 paragraphs — name the seam (the phenomenon/question the N frameworks all engage), gesture at why existing single-framework readings each fall short, signal the N frameworks about to be woven, preview the emergent claim without yet unpacking how it is produced. The opening must not privilege any one framework; each is named in passing, none is introduced in depth. Budget: 500–800 words.

**Body arc**: read `structure.body.arc`. Maps seed's argument moves onto the preset's body shape.
- `standard` (orthodoxy-counter): each move unpacks one aspect of the counter-framework.
- `concept-by-concept` (framework-build): each section introduces one framework component; chain by dependency.
- `structural-unfold` (case-anatomy): surface causes → structural conditions → mechanism → contingent factors.
- `lens-components` (diagnostic-lens): each section is one diagnostic question the lens asks.
- `braided` (synthesis-braid, V1.7): N equal-weight framework sections (one per source map) followed by a **braid/compression section** that produces the emergent claim. Ordering of the N sections is by *dependency* (if a braid move requires F1's output as F2's input, F1 comes first), not by prominence of the framework. Each framework section: roughly total-body-budget ÷ (N+1), leaving 1 slot-worth of words for the braid section. No framework section exceeds another by more than ~20% — gross inequality signals "solo with footnotes," not braid. Each section ends with a **return-to-seam sentence** that the next framework section picks up (continuity device).

**Pressure**: read `structure.pressure.type`, `.audit`, and `.required_slots`. Impose the pressure-section shape.
- `stress-test` (framework-build): for each component, boundary conditions.
- `three-accounts` (orthodoxy-counter): Account 1 (empirical target), Account 2 (theoretical target), Account 3 (category error the objections obscure). **Account 3 is load-bearing — flag as mandatory slot.**
- `counterfactual` (case-anatomy): what would have had to differ for different outcome.
- `overreach-risks` (diagnostic-lens): misapplication conditions + what the lens can't see.
- `seam-stress` (synthesis-braid, V1.7): three required slots.
  - **Slot 1 — Seam-stress (decoupling/composition)**: does the emergent claim actually require all N frameworks composed this way? Test decoupling (remove each; does C survive?). Test competing compositions (could a different set produce C?).
  - **Slot 2 — Per-framework pressure aggregate**: the strongest per-framework objection for each F_i (from the seed's per-framework pressure list), bundled into one pressure paragraph per framework. Each framework's strongest objection gets airtime.
  - **Slot 3 — Unit-of-analysis / temporal-consistency audit**: does the emergent claim depend on a unit-of-analysis shift between frameworks that would be rejected if stated explicitly? Do the N frameworks operate on compatible timescales? If either is a real problem, the audit section names it and answers it.
  Audit kind: `synthesis-validity`. All three slots are mandatory; an outline with one missing fails Step 7.

**Closing**: read `structure.closing.type` and `.budget_words`. Impose the closing shape.
- `diagnostic` (framework-build): reader-ready tool.
- `aphoristic` (orthodoxy-counter): compressed punch inverting the orthodoxy.
- `lesson` (case-anatomy): one transferable insight.
- `reader-ready-diagnostic` (diagnostic-lens): numbered/bulleted questions for reader's next case.
- `emergent-claim` (synthesis-braid, V1.7): state the emergent claim *explicitly* (not implied, not left to the reader to synthesize). Then offer one reader-usable frame — a question or diagnostic the reader can take to their own case that invokes the braid. The close does not repeat any single framework's argument; it lands on what the composition produces. Budget: 400–700 words.

**Total target**: sum of preset-specified budgets + body-section budgets.
- Default Type A range 2,500–4,000 words; `orthodoxy-counter` pilot (Hirschman) landed at 4,150 — upper end is acceptable when the pressure section's Account 3 is load-bearing.
- **Type D range (V1.7): 5,000–8,000 words** (braids need room to weave N frameworks and a braid section). If the seed's braid has an explicit length override in `draft_notes` or the user requests a target, honor it; otherwise default to 6,500 for a 3-framework braid, 7,500 for 4 frameworks, 8,000 for 5.

Record the applied preset in essay frontmatter (Step 5).

---

## Step 3.5 — Integrate Matched Positions (V1.6)

If the seed had non-empty `matched_positions`, each entry modifies the outline as follows. Matched positions are **soft constraints** — they shape the outline but do not override the essay's thesis.

**`supports`** — the matched T3's claim reinforces the thesis.
- Reserve one argument move (body section) to cite or build on the T3 claim. Mark in outline as `**Cites P###** — <relation line>`.
- In `source_refs` frontmatter: add the T3 as an explicit source.
- Do not duplicate the T3's argument; compress to one sub-claim and lean on the T3 for full mechanism.

**`extends`** — the thesis builds the T3 claim into a new domain or case.
- One argument move establishes the T3's original claim briefly (paragraph, not section).
- Subsequent moves carry the extension into the new domain.
- Outline note: `**Extends P###** — <domain of extension>`.

**`tensions-with`** — the T3 claim pressures the thesis; must be engaged.
- Add a required slot to the pressure section labeled `<P### claim, compressed>`. If preset is `orthodoxy-counter` and three-accounts is active, the tension-with position is typically Account 1 or Account 2 target; confirm the fit. If preset is `synthesis-braid` (V1.7), route tensions-with slots into the seam-stress Slot 2 (per-framework pressure aggregate) for the framework the T3 most closely sits in, or Slot 3 (unit-of-analysis audit) if the tension is about how different frameworks construe the object.
- If the tension is irreconcilable (thesis directly contradicts the T3), flag for user review: *"P### directly contradicts thesis. Options: (a) essay revises P### — mark P### `under-review` in positions-index; (b) thesis narrows to preserve P###; (c) proceed with explicit disagreement section."*

**`orthogonal`** — same topic surface, different question.
- No required slot. Mention at most once, in passing, if naturally fits. If not, drop without note.

Record the applied treatments in essay frontmatter: `matched_position_treatments: [{id: P001, treatment: cited-in-section-2}, ...]`.

---

## Step 4 — Resolve Conflicts with Positions

If the seed had `position_conflicts` entries, resolve each one now (before drafting):
- **Option A**: suppress the conflicting claim (drop from outline; note in essay frontmatter's `position_suppressions`).
- **Option B**: argue against the map's claim from the user's position (keep in outline; note in pressure section).
- **Option C**: revise `writer-positions.md` (surface to user before committing; outline proceeds on provisional assumption).

Ask the user which option for each conflict. Default Option A if user is not available (noted in essay for later review).

---

## Step 5 — Write the Outline

Create essay at `[vault]/20-Essays/YYYYMMDDHHMM - [Title].md`:

**Title**: inherit from seed (may be refined by user later).

**Type A frontmatter**:
```yaml
---
title: "<Title>"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [type/essay, theme/<from seed>]
status: outline
audience: general
venue: ""
word_count: 0
source_refs:
  - "[[<source map wikilink>]]"
  # additional atomic-note refs added here
series: ""
article_type: A
source_vault: <vault name>
source_seed: "[[<seed wikilink>]]"
preset: <id>  # V1.5 — carried from seed
position_suppressions: []
matched_positions: []  # V1.6 — carried from seed
matched_position_treatments: []  # V1.6 — how each matched position was integrated at outline time
thesis: "<one sentence>"
---
```

**Type D frontmatter (V1.7)**:
```yaml
---
title: "<Title>"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [type/essay, type/braid, theme/<primary from seed>]
status: outline
audience: general
venue: ""
word_count: 0
source_refs:
  - "[[<F1 map wikilink>]]"
  - "[[<F2 map wikilink>]]"
  - "[[<F3 map wikilink>]]"
  # atomic-note refs added as drafted
series: ""
article_type: D
source_vaults: [<vault1>, <vault2>, <vault3>]  # carried from seed
source_maps: [...]  # carried from seed
source_seed: "[[<seed wikilink>]]"
preset: synthesis-braid
position_suppressions: []
matched_positions: []  # carried from seed
matched_position_treatments: []
seam: "<from seed>"
braid_move: "<from seed>"
thesis: "<emergent claim, one sentence>"
framework_order: [F1, F2, F3]  # dependency-ordered for body
seam_stress_slot_1_passed: null  # null until Step 7 runs
---
```

**Body** (outline format — not yet prose). Section headers are preset-determined; the templates below show `orthodoxy-counter` (Type A default) and `synthesis-braid` (Type D). For other presets, substitute section names per Step 3's preset blueprint.

**Type A body (orthodoxy-counter shown; other presets analogous)**:
```markdown
# <Title>

## Core Argument
<thesis — one sentence>

## Preset
<preset id> — opening: <type>, body: <arc>, pressure: <type>, closing: <type>

## Matched positions (V1.6)
<for each matched_position entry, one line: ID — relation — T3 link — treatment decided at Step 3.5>

## Opening
**Preset opening type**: <type>
**Total budget**: <sum from preset>
**Paragraph beats** (one per preset paragraph slot):
1. **<beat 1>** — <one-sentence description>
2. **<beat 2>** — <one-sentence description>
(continue per preset)

## Body

### <Section 1 header — claim-form>
**Budget**: 300–500 words.
**Sub-claim**: <one sentence>
**Mechanism**: <bullet outline>
**Case**: <bullet outline>
**Source-map section**: <which map section this draws from>

### <Section 2 header>
[...]

### <Section 3 header>
[...]

(Sections 4, 5 if present)

## Pressure
**Preset pressure type**: <type>
**Audit**: <audit-kind from preset>
**Budget**: <from preset>
**Required slots**: (instantiate all preset-listed slots)
- **<slot-1 name>**: <objection + answer outline>
- **<slot-2 name>**: <objection + answer outline>
- **<slot-3 name>** *(if preset requires it; e.g., three-accounts Account 3)*: <category-error target + framing>

## Implication
**Budget**: 200–300 words.
**Content**: <what the reader carries away>
**Key moves**: <bullet outline>

## Close
**Preset closing type**: <type>
**Budget**: <from preset>
**Landing shape**: <one sentence describing the close's form>

---

## Citation pool (from source map's atomic notes)
- [[atomic note 1]]
- [[atomic note 2]]
- ...

## Draft notes
<any decisions the drafter should know — tone adjustments, which case to foreground, etc.>
```

**Type D body (synthesis-braid, V1.7)**:
```markdown
# <Title>

## Core Argument (Emergent Claim)
<thesis — one sentence; form: "Together, F1 + F2 + F3 imply C">

## Seam
<one sentence or question — carried from seed>

## Braid Move
<one or two sentences — carried from seed; the hinge>

## Preset
synthesis-braid — opening: seam-first, body: braided, pressure: seam-stress, closing: emergent-claim

## Matched positions (V1.6)
<for each matched_position entry, one line: ID — relation — T3 link — treatment decided at Step 3.5>

## Opening
**Preset opening type**: seam-first
**Total budget**: 500–800 words
**Paragraph beats**:
1. **Name the seam** — introduce the phenomenon/question (e.g., "what makes a pole in the AGI era") with a fresh example or observation. Do not yet name any framework.
2. **Existing single-framework readings fall short** — gesture at how the standard treatments (F1 alone / F2 alone / F3 alone) each answer only part of the question.
3. **Signal the N frameworks** — name F1, F2, F3 in one sentence each, without unpacking.
4. **Preview the emergent claim** — state C in compressed form, without yet showing how the composition produces it.
(5. optional: stake for the reader — why this seam matters to them.)

## Body

### F1 — <framework label, claim-form header>
**Budget**: ~1,500 words (total body / (N+1)).
**Sub-claims** (2–4):
- **<move 1>** — mechanism: <bullet>. Case: <bullet>. Source-map section: <...>
- **<move 2>** — ...
- ...
**Role in braid**: one sentence — what F1's contribution is to the emergent claim.
**Return-to-seam sentence**: <draft the sentence that picks up the next framework>

### F2 — <framework label>
**Budget**: ~1,500 words.
**Sub-claims** (2–4):
- ...
**Role in braid**: <one sentence>
**Return-to-seam sentence**: <draft>

### F3 — <framework label>
**Budget**: ~1,500 words.
**Sub-claims** (2–4):
- ...
**Role in braid**: <one sentence>
**Return-to-seam sentence**: <draft — leads into the braid section>

(F4, F5 if present — same shape)

### Braid / Compression — <claim-form header for the compression>
**Budget**: ~1,500 words.
**Hinge**: <expanded form of the braid move — how F1's output becomes F2's input becomes F3's constraint, or whatever the composition mechanism is>
**Proof beats** (3–5):
- ...
**Emergent-claim landing**: <one sentence — C stated in its full form, with the compositional justification just completed>

## Pressure (seam-stress)
**Preset pressure type**: seam-stress
**Audit**: synthesis-validity
**Budget**: 800–1,200 words
**Required slots** (all three mandatory):
- **Slot 1 — Decoupling + Competing composition**: for each framework F_i, state the strongest decoupling objection ("C survives without F_i because…") and answer it by showing F_i is load-bearing. Then: acknowledge competing compositions (alternative N-tuples that might produce C) and argue why this particular composition is the economical one.
- **Slot 2 — Per-framework pressure aggregate**: one short paragraph per framework. Each names the strongest objection to that framework's contribution and answers it. These paragraphs double as citation-anchors for any `tensions-with` matched positions routed here at Step 3.5.
- **Slot 3 — Unit-of-analysis / temporal consistency**: name any unit-of-analysis shift the braid implicitly performs and defend it (or narrow C to avoid it). Name timescale differences across frameworks and show the composition holds on the decisive timescale.

## Implication
**Budget**: 300–500 words
**Content**: what the emergent claim lets the reader see or do that single-framework readings don't
**Key moves**: <bullet outline — should NOT recapitulate F1/F2/F3; should land what the composition produces>

## Close
**Preset closing type**: emergent-claim
**Budget**: 400–700 words
**Landing shape**: state C explicitly, then offer one reader-usable frame — a question/diagnostic the reader takes to their own case that invokes the braid.

---

## Citation pool (from N source maps' atomic notes)
- **F1 atomics**: [[...]], [[...]]
- **F2 atomics**: [[...]], [[...]]
- **F3 atomics**: [[...]], [[...]]
- **Matched T3s (from V1.6 lookup)**: [[...]], [[...]]

## Draft notes
<any decisions the drafter should know — e.g., "F2 and F3 overlap on claim X; draft must differentiate"; "framework_order set to F1→F2→F3 because F2's output is F3's input">
```

---

## Step 6 — Update Registry

Update source-map-registry.md:
- **Type A**: essay status → `outlined`; essay path → the new essay file path (not the seed).
- **Type D**: for each of the N source maps, essay status → `outlined (braid)`; essay path → the new essay file path. Preserve `braid-1-of-N` annotation from seeding.

The seed in `10-Thoughts/` stays as-is (not moved or deleted).

---

## Step 6.5 — Seam Audit (Type D only, V1.7)

Before reporting, the outline must pass the seam audit. This is the hard pre-draft gate that keeps braids from collapsing into solos-with-footnotes.

**Test 1 — Framework load-bearingness**: for each of the N frameworks, write one sentence stating what the outline would lose if F_i were removed (its role from the Body section). If any F_i's removal-loss is "decorative" or "illustrative only" — the outline is solo-with-decoration, not braid. Reject and return to Step 3.

**Test 2 — Emergent claim non-derivability**: deeply consider whether any single map, read carefully, already produces C. If the outline's emergent claim is reachable from F1 alone (or F2 alone, or F3 alone) — the outline is not a braid. Reject and advise recasting as Type A with references.

**Test 3 — Seam specificity**: is the seam (carried from seed) load-bearing in the body outline? Do the per-framework sections each end with a return-to-seam sentence that actually engages the seam, rather than generic closings? If seam is absent from body transitions — reject and add the transitions before proceeding.

**Test 4 — Equal weight**: are the framework section budgets within 20% of each other? If one framework is ≥1.5× any other's budget — reject and rebalance. (Braids that privilege one framework silently are not braids.)

**Test 5 — Braid section specificity**: does the braid/compression section have a concrete hinge mechanism, not a gesture? (Bad: "These three frameworks together show…" Good: "F1's output X becomes the condition under which F2's Y operates, which makes F3's Z inevitable — therefore C.") If braid section is vague — reject and pull a concrete hinge before proceeding.

If all five tests pass: set `seam_stress_slot_1_passed: true` in essay frontmatter and proceed to Step 7. If any fails: return to Step 3 (or Step 2 for seed-level issues), revise, re-run this audit. Do not allow the draft step to run without seam-audit pass.

---

## Step 7 — Report

**Type A report**:
```
## /article-outline [seed-path] — YYYY-MM-DD

Essay created: [absolute path to essay file]
Status: outline
Preset: <id> (opening: <type>, body: <arc>, pressure: <type>, closing: <type>)
Target length: <sum per preset>

Structure:
- Opening (<preset type>, <budget>w, <N> paragraph beats)
- Body: <N> sections (<body arc>)
- Pressure: <pressure type>, <N> required slots
- Implication + Close (<closing type>, <budget>w)

Position conflicts resolved: <count> — <A/B/C breakdown>
Matched positions integrated: <count> — <IDs + treatments: "P001 cited in §2, P007 engaged in pressure slot 3">

Next step: /article-draft [essay-path]
```

**Type D report (V1.7)**:
```
## /article-outline [seed-path] D — YYYY-MM-DD

Braid outline created: [absolute path to essay file]
Status: outline
Preset: synthesis-braid (seam-first / braided / seam-stress / emergent-claim)
Target length: <total budget, typically 5,000–8,000 for Type D>

Structure:
- Opening (seam-first, 500–800w, 4–5 beats)
- Body: N=<count> framework sections + 1 braid section (~<per-framework budget>w each)
- Pressure (seam-stress, 3 required slots, <budget>w)
- Implication + Close (emergent-claim, 400–700w)

Framework order: F1 <label> → F2 <label> → F3 <label>
Dependency rationale: <one sentence — why this order>

Seam Audit (Step 6.5):
- Test 1 (framework load-bearingness): PASS / details per framework
- Test 2 (emergent claim non-derivability): PASS
- Test 3 (seam specificity): PASS
- Test 4 (equal weight — ±20%): PASS / largest variance
- Test 5 (braid section hinge specificity): PASS

Position conflicts resolved: <count> — <A/B/C breakdown>
Matched positions integrated: <count> — <IDs + treatments>

Next step: /article-draft [essay-path]
```
