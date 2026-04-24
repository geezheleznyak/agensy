---
title: "Article Presets"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [type/meta, theme/craft]
status: seeded-from-template
purpose: Registry of narrative-arc blueprints consumed by /article-seed (inference), /article-outline (imposition), /article-draft (opening/closing hints), /article-revise (Pass E audit). Every pipeline-mode essay adopts one preset; the preset determines opening type, body arc, pressure type, and closing type. All other extraction-schema sections remain universal. In companion mode, presets are advisory only.
---

# Article Presets

Presets are the operationalization of the craft principles in `article-design-principles.md`. Each preset is a three-axis blueprint: argumentative intent × problem type × reader default. The preset-parameterized dimensions are the four arc structural choices — opening type, body arc, pressure type, closing type. Everything else in `framework/templates/map-to-article-extraction.md` remains universal across presets.

**Template status**: this file ships with five presets (`framework-build`, `orthodoxy-counter`, `case-anatomy`, `diagnostic-lens`, `synthesis-braid`) that transfer across users and topics. Tune budgets, principle references, or add new presets after your vault has run 2–3 pilot essays and you observe what your pipeline actually needs.

**Mode-sensitivity**: presets are enforced in **pipeline mode** (`mode: pipeline` or field absent — default). In **companion mode** (`mode: companion`), presets become advisory hints: `/article-companion start` suggests 1–3 preset candidates at workspace setup, `/co-suggest` may recommend opening/pressure/closing types from a matching preset, but no `/co-*` verb enforces a preset's structure. The operator can write outside any preset. `preset_status: advisory-only` in the essay frontmatter records this.

**Critic-layer gate**: `/article-critique` is a **soft pre-promotion gate** for any preset. It is not a preset-specific pass; it complements the adversarial pass library in `/article-revise`. Recommended cadence: run `frame-only` mode at outline stage (cheap frame audit before prose exists); run `full` mode after `/article-revise` has landed. Essay frontmatter's `critique_runs` list records every invocation; `/article-revise` Step 4 Q6 checks for at least one run before recommending `/article-promote`.

## Axis definitions

**Axis 1 — Argumentative intent** (what the essay is trying to *do*):
- `framework-build` — introduce a novel analytical framework
- `orthodoxy-counter` — refute a widely-held thesis
- `case-anatomy` — explain a specific event or phenomenon in depth
- `diagnostic-lens` — teach readers how to read a class of situations
- `synthesis-braid` — connect N frameworks to produce emergent claim (Type D only)

**Axis 2 — Problem type** (what phenomenon the essay engages):
- `puzzle` — observed outcome doesn't match expected mechanism
- `prediction-failure` — accepted theory makes wrong predictions
- `concept-drift` — a concept means something different now than it used to
- `regime-shift` — underlying conditions changed, outputs recalibrated
- `category-confusion` — two or more phenomena being conflated

**Axis 3 — Reader default** (who the reader is):
- `naive` — no prior exposure
- `half-believes-orthodoxy` — has absorbed the standard view uncritically
- `expert-skeptical` — professional reader who'll test the framing
- `practitioner` — domain insider looking for pragmatic tools

---

## Preset registry

```yaml
presets:

  framework-build:
    status: active
    description: Introduce a novel analytical framework for a phenomenon that needs a better explanation.
    applies_when:
      intent: [framework-build]
      problem_type: [puzzle, prediction-failure, regime-shift]
      reader_default: [naive, half-believes-orthodoxy, practitioner]
    structure:
      opening:
        type: phenomenon-first
        paragraphs:
          - name the phenomenon needing explanation + concrete marker of its scale
          - gesture at consequence or puzzle it produces
          - introduce the framework's author / origin (or the speaker's own framing)
          - compress to thesis
        budget_words: 400-600
      body:
        arc: concept-by-concept
        notes: each body section introduces one framework component; sections chain by dependency order
      pressure:
        type: stress-test
        audit: boundary-conditions
        required_slots:
          - for each key component, name the conditions under which it breaks
        budget_words: 500-800
      closing:
        type: diagnostic
        budget_words: 150-250
        notes: reader-ready tool ("next time you see X, ask Y")
    principles_realized: [P3]
    notes: Default preset. Most neutral; widest applicability. Use when no stronger inference signal applies.

  orthodoxy-counter:
    status: active
    description: Refute a widely-held thesis by naming the orthodoxy, exposing its hidden premise, and striking with a counter-framework.
    applies_when:
      intent: [orthodoxy-counter]
      problem_type: [puzzle, prediction-failure, concept-drift, category-confusion]
      reader_default: [half-believes-orthodoxy, expert-skeptical]
    structure:
      opening:
        type: orthodoxy-first
        paragraphs:
          - name the orthodoxy + lineage + contemporary form (~3 figures or dates)
          - name the hidden premise the orthodoxy rarely states explicitly
          - strike anchor case as evidence against the hidden premise
          - unpack the anchor case with minimum required detail
          - introduce the counter-framework's author + general principle
          - generalize the mechanism to a contemporary catalog
          - compress to thesis
        budget_words: 700-900
      body:
        arc: standard
        notes: argument moves unpack the counter-framework; each move carries the reader further from the orthodoxy
      pressure:
        type: three-accounts
        audit: category-error
        required_slots:
          - account-1: target of the empirical objection (where the critic's compliance/result metric lands)
          - account-2: target of the theoretical objection (where the framework appears over-stated)
          - account-3: the category error the objections' framing obscures (what the practitioners are actually optimizing)
        budget_words: 700-1100
        notes: Load-bearing — account-3 must be present. Without it, the section defends the framework as-is instead of extending it.
      closing:
        type: aphoristic
        budget_words: 100-200
        notes: compressed punch that inverts the orthodoxy's framing; typically two-beat close
    principles_realized: [P1, P2, P3]

  case-anatomy:
    status: active
    description: Explain a specific event or phenomenon in depth through structural unfolding.
    applies_when:
      intent: [case-anatomy]
      problem_type: [puzzle, regime-shift, category-confusion]
      reader_default: [naive, half-believes-orthodoxy, practitioner]
    structure:
      opening:
        type: case-first
        paragraphs:
          - drop reader into the event with narrative specificity (time, place, actors, pivotal moment)
          - name the outcome that needs explanation
          - indicate which structural layer this essay will unpack
        budget_words: 400-700
      body:
        arc: structural-unfold
        notes: surface causes → structural conditions → underlying mechanism → contingent factors. Each body section peels one layer.
      pressure:
        type: counterfactual
        audit: factor-attribution
        required_slots:
          - what would have had to be different for a different outcome
          - which framework-independent factors (chance, individual choice, exogenous shock) dominated vs. the structural account
        budget_words: 500-800
      closing:
        type: lesson
        budget_words: 150-250
        notes: one transferable insight the case vindicates — neither summary nor moral
    principles_realized: []

  diagnostic-lens:
    status: active
    description: Teach readers to read a class of situations through a specific lens.
    applies_when:
      intent: [diagnostic-lens]
      problem_type: [concept-drift, regime-shift, category-confusion]
      reader_default: [expert-skeptical, practitioner]
    structure:
      opening:
        type: reading-failure
        paragraphs:
          - show how the dominant reading of a class of situations misses the mark, using a fresh example
          - name the missing analytical move
          - preview the lens this essay will hand the reader
        budget_words: 400-600
      body:
        arc: lens-components
        notes: each body section introduces one diagnostic question the lens asks; demonstrate each on a short case
      pressure:
        type: overreach-risks
        audit: misapplication-conditions
        required_slots:
          - cases where the lens would be misapplied (over-reading)
          - phenomena the lens cannot see (what structural features it omits)
        budget_words: 400-700
      closing:
        type: reader-ready-diagnostic
        budget_words: 150-300
        notes: a small numbered or bulleted list of questions the reader can take to their own next case
    principles_realized: []

  synthesis-braid:
    status: active
    description: Connect N frameworks across domains to produce an emergent claim no single framework makes alone. Activates with Type D commands.
    applies_when:
      intent: [synthesis-braid]
      problem_type: [concept-drift, regime-shift, category-confusion]
      reader_default: [expert-skeptical, half-believes-orthodoxy]
      article_type_required: D
      n_frameworks_min: 3
      n_frameworks_max: 5
    structure:
      opening:
        type: seam-first
        paragraphs:
          - name the seam (the named tension binding the N frameworks) with a fresh observation or example
          - show why existing single-framework readings each fall short
          - name the N frameworks in one sentence each (no in-depth unpacking)
          - preview the emergent claim compressed (the body will earn it)
        budget_words: 300-500
        notes: Do not introduce any framework in depth in the opening. Do not state the emergent claim as a surprise-reveal.
      body:
        arc: braided
        notes: N framework sections (equal weight, ±20% of mean) + one braid/compression section. Each framework section leads with a claim-form header (not biographical), states the framework's contribution to the composition, develops 2-4 sub-claims, closes with a return-to-seam sentence setting up the next framework. The braid section opens by naming the composition mechanism explicitly, uses only material already introduced in F1/F2/F3, closes with the emergent claim in full compositional form.
        budget_words_per_framework: 400-800
        budget_words_braid_section: 200-400
      pressure:
        type: seam-stress
        audit: synthesis-validity
        required_slots:
          - decoupling + competing-composition (try removing each F_i, test whether the emergent claim still holds; try alternative composition hinge)
          - per-framework pressure aggregate (one paragraph per F_i; inherit from each framework's native stress-points)
          - unit-of-analysis / temporal audit (consistency of what is being measured and over what horizon across F1/F2/F3)
        budget_words: 400-700
        notes: All three slots mandatory. Cannot skip Slot 1 (decoupling) — it is the synthesis-validity proof. Synthesize across frameworks; do not enumerate per-framework pressure as three separate sub-sections (bloat signature).
      closing:
        type: emergent-claim
        budget_words: 200-400
        notes: State the emergent claim explicitly with full compositional justification behind it (not compressed — reader has earned it). Offer one reader-usable frame (diagnostic question or move that invokes the braid). Do not recapitulate F1/F2/F3 structurally.
    audits:
      - seam-stress (at outline Step 6.5 and revise Pass E)
      - synthesis-validity (revise Pass E)
      - metric-realism (revise Pass F; mandatory when claims reference quantitative metrics)
    principles_realized: [P4, P5, P6]
    notes: Activate for Type D commands only. Skipping to Type D without piloting Type A first is allowed but not recommended; Type A calibrates the pipeline's voice and position infrastructure on simpler essays first.
```

---

## Global length constraint

**All essays, regardless of article type (A / B / C / D) or preset, target 2,000–4,000 words.** This is a hard cap learned from audit evidence — essays that drift past 4,000w tend to read as bloated or machine-feeling regardless of content quality.

- Preset sub-budgets above are *allocations within* this range, not licenses to exceed it. If a preset's nominal budgets sum above 4,000w in a given essay instantiation, tighten per-slot before drafting rather than exceed the cap.
- For `synthesis-braid` specifically: N=3 fits the cap comfortably (opening 300–500 + 3×400–800 + braid 200–400 + pressure 400–700 + closing 200–400 ≈ 2,300–4,400w; trim overlaps to land inside 4,000). N=4 requires per-framework 400–600. N=5 requires per-framework 300–500 and is pipeline-discouraged: braid valency above 4 is a smell that the essay should split.
- `/article-revise` Pass G enforces the cap at revision time. Essays above 4,000w cannot progress to `status: final` without Pass G cuts.
- **Bloat signatures to cut**: same claim restated in multiple sections; case examples serving only as illustration (no logical load); pressure section enumerating per-framework objections as three separate sub-sections instead of synthesizing; machine-feeling cadence from repeated sentence patterns (e.g., "X is not Y" overused, structural parallelism with no variation).

---

## Preset inference (used by `/article-seed` Step 2.5)

Signals, ranked by authority:

1. **User flag** (`--preset <id>`) — explicit override, highest authority. No inference runs.
2. **Thesis-candidate grammar** — default inference from the extracted thesis:
   - "X is not Y" / "not-X but Y" / "X is not peace, it is leverage" → `orthodoxy-counter`
   - "X produces Y via Z" / "X is the mechanism of Y" / "X creates Y when Z" → `framework-build`
   - "What happened at/in X" / "How X unfolded" / "X, decoded" → `case-anatomy`
   - "How to read X" / "X requires Y lens" / "Seeing X clearly" → `diagnostic-lens`
3. **Fall-back**: ambiguous grammar → `framework-build` (most neutral).

Confidence:
- **High**: grammar pattern matches cleanly and problem_type from source map is in `applies_when`.
- **Medium**: grammar matches but problem_type unclear from source map.
- **Low**: grammar ambiguous OR source map problem_type outside preset's `applies_when`.

Low confidence triggers a one-line user prompt at seed time: *"Inferred preset `<id>` (confidence low). Override? [y/n]."*

Record in seed frontmatter:
```yaml
preset: <id>
preset_source: [user-flag | inference | default]
preset_inference_confidence: [high | medium | low]
```

---

## Preset evolution

- New craft principles discovered in a pilot may update existing preset definitions in-place (preferred).
- A preset variant is spawned only when the applicability axis values diverge enough from an existing preset to require different structure (e.g., `orthodoxy-counter-expert` for `expert-skeptical` reader diverging from `half-believes-orthodoxy`).
- When a preset changes, every essay currently using that preset should be listed in a migration note; essays at `status: final` remain unchanged, essays in earlier status should be re-outlined under the new preset.

---

## Related

- [[article-design-principles]] — craft principles that the presets operationalize.
- [[voice-profile]] — style layer (HOW); orthogonal to presets.
- [[writer-positions]] — substance layer (WHAT); orthogonal to presets.
- `framework/templates/map-to-article-extraction.md` — extraction schema; presets govern the §Narrative Arc half.
