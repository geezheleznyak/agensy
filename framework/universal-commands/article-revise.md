---
description: Adversarial revision pass — tighten thesis, cut vault-voice bleed, stress-test claims
type: universal-protocol
audience: claude
---

# /article-revise [essay-path] [mode]

Revise a draft against voice profile, writer positions, and standalone-ness constraints. Produces a revised version with `status: revision`.

**[essay-path]**: absolute or vault-relative path to an essay at status `draft` or `revision`.
**[mode]**: `adversarial` (default) | `creative` | `light`. Reuses the style-preset pattern from `/engage-deep`.

**Runtime**: Read `vault-config.md` from cogitationis vault root. Extract:
- `reference_docs.voice_profile`
- `reference_docs.writer_positions`
- `reference_docs.article_presets` — path to article-presets.md (V1.5)
- `reference_docs.positions_index` — path to positions-index.md (V1.6)
- `reference_docs.source_map_registry`
- `note_template.synthesis.five_questions` — end-of-revision checklist

---

## Step 1 — Validate Input

1. Verify [essay-path] exists and status is `draft` or `revision`.
2. Verify source map still exists (follow `source_vault` + `source_seed` frontmatter traversal).
3. Read the current draft fully.
4. Read the essay's `preset` frontmatter field (V1.5). Default `framework-build` if missing. Load the matching preset block from `article-presets.md` — Pass E (and any preset-aware fidelity checks) will consult `structure.opening`, `structure.pressure.required_slots`, and `structure.closing`.
5. Read the essay's `matched_positions` and `matched_position_treatments` frontmatter (V1.6). For each entry, fetch the referenced T3 note — Pass C will use the T3's claim to run the soft-constraint check. Empty list = no soft-constraint check.

---

## Step 2 — Run Revision Passes

Run all passes in order. Each pass either flags or edits.

### Pass A — Thesis integrity
- Read the stated thesis (frontmatter and opening sentence).
- Check every body section: does it advance the thesis? If a section is decorative or tangential → flag for cut.
- Check the close: does it land the thesis (not repeat it)? If it restates → flag for revision.

### Pass B — Vault-voice bleed
- Compare each paragraph against `voice-profile.md`.
- Flag paragraphs that drift into neutral-essayistic, Wikipedia-ish, academic-citation-style, or vault-register (unless audience = academic).
- Common tells: passive voice when voice-profile prefers active; excessive hedging ("I think", "it could be argued", "many would say") when voice-profile is direct; footnote-style asides when voice-profile integrates into prose.

### Pass C — Position alignment (two-layer)

**Layer 1 — Bedrock (hard, from `writer-positions.md`):**
- Check every claim against `writer-positions.md`.
- **Founding commitments**: claims should align or deepen.
- **Rejected frames**: no claim should operate within one. If found → flag.
- **Non-negotiables**: if any claim violates → mandatory revision before `status: final` is possible.
- **Preferred analytical moves**: flag sections where one of these moves was available but not deployed.

**Layer 2 — Matched positions (soft, from `matched_positions` frontmatter, V1.6):**
- For each matched position (with its classified `relation` — supports / extends / tensions-with / orthogonal):
  - **`supports`**: verify the essay's claims do not silently contradict the T3 claim. If contradicted without explicit engagement → flag. If the T3 was not cited despite being reserved at outline time → flag for citation addition.
  - **`extends`**: verify the essay actually builds on the T3's claim rather than repeating it. If the extension is not visible in prose → flag.
  - **`tensions-with`**: verify the essay engages the tension in the pressure section (or equivalent). If the tension is not addressed → flag. If the essay contradicts the T3 position without acknowledgment → flag as a candidate for P### `under-review` in positions-index.
  - **`orthogonal`**: no check required.
- Soft-constraint violations are **surfaced, not silently corrected**. User decides per-case whether to edit the draft, revise the T3 (mark `under-review`), or retire the matched position.

### Pass D — Standalone-ness
- Strip all vault wikilinks mentally. Does every section still read?
- Test every technical term: would a cold reader know it? If not → gloss inline.
- Test every reference to "the project" / "the vault" / "the domain" — these must not appear. Translate to reader-facing language.

### Pass E — Stress-test the argument (adversarial mode only)
- For each argument move: what is the strongest counter-example or counter-claim?
- Is that counter addressed in the Pressure section? If not → flag as missing pressure point.
- For the thesis itself: what's the smartest objection from someone who generally agrees with the user's positions but would push back on this specific claim? If not answered → flag.

**Preset fidelity sub-pass (V1.5 / V1.7)**:
- **Opening**: does the opening instantiate the preset's paragraph beats in order? For `orthodoxy-counter`: is the orthodoxy + lineage named in paragraph 1 (P1)? Is the hidden premise named before the anchor case strikes? For `seam-first` (V1.7): is the seam named in the first paragraph without naming any framework in depth? Are all N frameworks signaled in one-sentence form before the body begins? If the opening introduces a framework at length before the body, that's a seam-first violation — the opening is doing the body's job. If the opening collapses or reorders beats → flag.
- **Pressure required-slots**: does each required slot from the preset appear in the Pressure section? For `three-accounts`: Account 1 (empirical-objection target), Account 2 (theoretical-objection target), Account 3 (category error the objections obscure) — all three present? For `stress-test`: are boundary conditions named per framework component? For `seam-stress` (V1.7): are all three slots filled — (1) decoupling + competing-composition, (2) per-framework pressure aggregate, (3) unit-of-analysis / temporal audit? If any required slot is missing → flag as mandatory revision.
- **Closing**: does the closing match the preset's closing type? For `aphoristic`: is there a compressed-punch two-beat close inverting the orthodoxy? For `diagnostic`: is the reader-ready tool explicit? For `emergent-claim` (V1.7): is the emergent claim stated *explicitly* (not left implicit)? Is the reader-usable frame present? Does the close avoid recapitulating F1/F2/F3 structurally? If the close just summarizes each framework and ends, that's a Type A framework-walk close, not emergent-claim — flag for rewrite. If not → flag.
- **Body arc** (V1.7, Type D only): is the body genuinely braided, not enumerated? Check: (a) each framework section ends with a return-to-seam sentence; (b) framework section budgets within ~20% of each other; (c) a distinct braid/compression section exists between the N framework sections and the pressure section; (d) the braid section names the composition mechanism explicitly with a concrete hinge. Any failure → flag for revision.

**Category-error audit (P3 check — for `orthodoxy-counter` and `framework-build` presets, and for any essay with empirical falsification claims)**:
- Before concluding "the framework survives objection X by predicting Y instead of Z," audit: *what is the metric the objection uses, and who is optimizing for it?*
- If the phenomenon's practitioners (states imposing sanctions, central banks setting rates, actors in the domain) are not optimizing for the metric the falsification tests, the falsification is under-threat. Flag for an Account-3 / hidden-optimization-target slot if one is not already present.
- If the practitioners are optimizing for the tested metric, the falsification lands — do not paper over.
- Source: article-design-principles.md §P3.
- **Type D extension**: braids often assert composition-based claims about how a domain works. When a braid cites empirical evidence, run the category-error audit on that evidence as if it were a Type A pressure section. Novel for braids: audit whether the *unit of analysis* in the cited evidence matches the braid's unit — a sovereignty-measured claim can't be falsified by GDP-measured evidence, and vice versa.

**Seam-stress audit (V1.7, synthesis-braid preset only)**:
- **Decoupling test**: for each framework F1/F2/F3, mentally rewrite a key paragraph assuming F_i is absent. If the essay still says roughly the same thing, F_i is decorative — flag for either deepening F_i's section or rethinking whether this should be a braid. Note: this is the revise-time version of the outline's Step 6.5 Test 1, now run against actual prose.
- **Composition-uniqueness test**: could a different set of N frameworks produce the emergent claim? Is there a simpler or more natural composition the essay should acknowledge? If yes and the essay doesn't name it — flag for addition in Slot 1 of the seam-stress pressure section.
- **Unit-of-analysis consistency**: does the essay implicitly shift units between frameworks? E.g., F1 operates on state-level, F2 on firm-level, F3 on network-level — does the essay say that explicitly and defend the composition across scales, or silently collapse them? Silent collapse → flag as mandatory revision.
- **Timescale consistency**: are the frameworks' timescales compatible in the places where the essay composes them? A structural-realist claim (decadal) plus a financial-cycle claim (annual) plus a tactical claim (weekly) may not actually compose without temporal disaggregation. Flag any place where incompatible timescales are being treated as simultaneous.

**Synthesis-validity audit (V1.7, synthesis-braid preset only)**:
- **Braid-dependency test**: re-read the emergent claim. Is every word of it actually earned by the composition, or is some of it already true given any single framework? Compressed statements of C that smuggle in single-framework claims are a failure mode — flag the specific clauses and narrow C accordingly.
- **Framework-contribution symmetry**: does each of the N frameworks carry equivalent load in the braid move? If F1 provides a mechanism and F2+F3 provide "context" — this is a Type A with F1 as lead, with F2/F3 as footnotes. Flag for rebalancing.
- **Emergent-claim falsifiability**: state one condition under which the emergent claim would be falsified. If the claim is not falsifiable as stated — narrow it until it is, then test again. A braid that produces a tautology has failed; its emergent claim should cost something to believe.

**Metric-realism audit (V1.7, optional — run for any essay making quantitative or scaling claims, mandatory for `synthesis-braid` essays that invoke compute, power, economic, or capability metrics)**:
- For every claim about scale, concentration, returns, distribution: is the metric named explicitly, or is the claim floating on vague "concentration is high"?
- For compute-specific claims: distinguish training FLOPs, parameter count, inference throughput, deployed instances, and monetary spend — these are different quantities and move differently under different dynamics.
- For power-law / winner-take-most claims: is the parameter (α, tail index, concentration ratio) specified qualitatively, or is the claim invoking "power-law" as aesthetic shorthand?
- Flag any claim that uses a metric as a label without saying which metric. Braids that collapse these distinctions to sound crisp are category-error-prone.

**Frame-pressure sub-pass (V1.9, universal — runs on all essays regardless of preset)**:

Runs cheap versions of C1 (frame audit), C6 (concession-load audit), and C7 (unit-of-analysis audit) from `/article-critique`. These three are the most common structural failures that pass all prior audits but fail external review. Catching them at revise time means the operator doesn't have to run a separate critique just to surface them.

- **Frame check (C1-lite)**: identify the 1–3 load-bearing terms in the thesis. For each, ask: does the essay defend this term's operative definition independently of the conclusion the definition produces? If the conclusion follows only under the essay's definition AND the definition is not defended — flag as circular-frame risk. Recommend running `/article-critique --mode=frame-only` for the full treatment.
- **Concession check (C6-lite)**: grep for concession markers (*"phase-dependent", "granted", "to be sure", "admittedly", "in this phase", "under current conditions"*). For each hit, ask: does conceding this weaken a structural claim to a phase-dependent / contingent one? If yes AND the thesis still advertises the structural reading downstream of the concession — flag as load-swallowing concession.
- **Unit check (C7-lite)**: identify the declared unit (state, firm, individual, etc.). Spot-check predicates in 2–3 body sections: are they about the declared unit or about a different level of aggregation? If the essay hedges (uses "the X" without committing when committing would change the argument) — flag as unit hedge.

Frame-pressure flags are surfaced, not auto-revised. The operator decides whether to address at revise time or defer to a full `/article-critique` pass before promotion. For deep issues, full `/article-critique` is recommended — this sub-pass is a tripwire, not a replacement.

### Pass F — Structural tightness
- Opening hook: does it grip in the first two sentences? If the first 30 words feel like warm-up → revise to lead with the strongest beat.
- Transitions: any abrupt jumps between body sections? Any transitions that over-signpost ("In this section we will...")? Flag both.
- Close: is the landing beat the strongest image/claim/implication available? Often the essay buries its best line; surface it.

### Pass G — Tightness & length audit (v1.8, universal)

- **Target: 2,000–4,000 words for all essay types (A/B/C/D) regardless of preset.** See `article-presets.md` §"Global length constraint".
- Count words (exclude frontmatter). Compare against the 2,000–4,000 target.
- **If >4,000w**: identify the most repetitive or decorative material and flag for cut. Common bloat signatures (observed in the Pole-Is-Obsolete audit):
  - Same claim restated in two or more sections — keep the strongest statement, cut the others.
  - Case examples that function only as illustration (no logical load) — cut unless the case is doing pressure-test work.
  - Pressure section enumerating per-framework objections as separate sub-sections — rewrite as a single synthesized pressure pass.
  - Machine-feeling cadence: repeated sentence patterns ("X is not Y" overused, structural parallelism with no variation, lists of three where one example would do) — vary or cut.
  - Decorative qualifications and hedges that add no load ("it is worth noting that", "in a certain sense", "one might say") — cut.
  - Opening or closing that restates the body's argument instead of framing or landing it — rewrite to frame/land.
- **If <2,000w**: identify thin moves. Argument moves that name a claim without unpacking mechanism, pressure slots that gesture but don't cost anything, cases mentioned but not walked through. Flag for expansion.
- Apply cuts or expansions now; do not defer to the user. Record total cut/added in `revision_log`.
- **Blocker**: essays outside the 2,000–4,000w range cannot progress to `status: final`. Re-run revise until inside.

---

## Step 3 — Apply Revisions

Apply the flagged revisions directly to the draft prose. Do not just annotate — edit in place.

For large revisions (section cut, section added, thesis restatement): note in `revision_log` frontmatter.

For non-negotiable violations (Pass C): mandatory. If user is unavailable: apply the revision (cut or revise claim) and note in `revision_log`. The draft cannot progress to `final` without this.

---

## Step 4 — Five Questions Check (+ 6th, V1.9)

At end of revision, apply the essay-level quality check from cogitationis `vault-config.md` `note_template.synthesis.five_questions`:

1. Is the core argument stateable in one sentence? → check against current thesis statement.
2. Does the opening grip a cold reader with no vault context? → read first paragraph alone.
3. Does every body section advance the core argument (not decorate it)? → check section-by-section.
4. Have all vault wikilinks been resolved to prose citations or dropped? → grep for `[[` in body.
5. Does the draft argue from writer-positions.md, or does it drift into vault-voice? → spot-check 3 random paragraphs.
6. **(V1.9)** Has `/article-critique` been run, and have its flags been addressed or explicitly dismissed? → check essay frontmatter for `critique_runs` entries and for `critique_dismissals` entries covering any unaddressed flags. Fresh dismissals must name the pass (C1–C8) and give a one-sentence reason.

Any "no" → continue revision. All "yes" → ready for promotion.

**Note on Q6**: it is a soft gate, not a hard block. The operator can skip `/article-critique` by marking Q6 as *"deferred — critique not applicable to this draft stage"* in `revision_log.notes`. But the absence of a critique run is itself recorded and visible in the promotion report.

---

## Step 5 — Update the Essay File

Update in place:

**Frontmatter**:
```yaml
status: revision
updated: YYYY-MM-DD
word_count: <updated count>
revision_log:
  - date: YYYY-MM-DD
    mode: <adversarial/creative/light>
    passes_run: [A, B, C, D, E, F, G]
    flags_resolved: <count>
    non_negotiable_violations: <count>
    word_count_before: <count>
    word_count_after: <count>
    length_in_range: <true/false>  # true iff 2000 ≤ after ≤ 4000 (v1.8)
    five_questions: [yes/no/yes/yes/yes]  # one per question
    frame_pressure_flags: <count>  # V1.9 — from Pass E sub-pass
    critique_status: <run | deferred | not-applicable>  # V1.9 — Q6 state
critique_dismissals:  # V1.9 — only present if any critique flags were dismissed rather than addressed
  - pass: <C1|C2|C3|C4|C5|C6|C7|C8|writing-tells>
    reason: "<one sentence on why this flag was dismissed>"
    date: YYYY-MM-DD
```

**Body**: revised prose. Remove any "DRAFT NOTE:" comments (internal flags from Step 2 passes) once resolved.

---

## Step 6 — Update Registry

Update source-map-registry.md:
- Essay status → `revised`

---

## Step 7 — Report

```
## /article-revise [essay-path] [mode] — YYYY-MM-DD

Revision pass complete: [absolute path to essay file]
Status: revision
Preset: <id>
Mode: <mode>
Word count: <before> → <after>

Passes run: A (thesis) / B (voice bleed) / C (position, two-layer) / D (standalone) / E (stress — adversarial only, preset-aware) / F (tightness) / G (length — universal 2,000–4,000w cap, v1.8)
Flags resolved: <count>
Preset fidelity flags: <count> — <resolved / unresolved>
Category-error audit: <applied / skipped (non-applicable preset)> — <result>
Seam-stress audit (V1.7, Type D): <run / n/a> — decoupling <pass/fail per framework>, composition-uniqueness <pass/fail>, unit-consistency <pass/fail>, timescale-consistency <pass/fail>
Synthesis-validity audit (V1.7, Type D): <run / n/a> — braid-dependency <pass/fail>, framework-symmetry <pass/fail>, falsifiability <pass/fail>
Metric-realism audit (V1.7, when applicable): <run / n/a> — flagged metrics: <list or none>
Frame-pressure sub-pass (V1.9, universal): <flags count> — frame-circular: <count>, load-swallowing concession: <count>, unit hedge: <count>. Full `/article-critique` recommended: <yes/no>
Length audit (G, v1.8): word count <before> → <after>; in-range <yes/no>; bloat signatures flagged: <list or none>
Non-negotiable violations: <count> — <state resolved or unresolved>
Matched-position checks: <count checked> — <IDs flagged>; <under-review recommended: Y/N>

Five Questions Check (V1.9 — 6 questions): <results>
Q6 critique status: <run | deferred | not-applicable> — <critique file path if run>

Next step:
- If all six are yes AND length in range AND (Type D: all seam-stress + synthesis-validity slots pass): /article-promote [essay-path]
- If Q6 is no (critique not run): /article-critique [essay-path] — address flags or dismiss with reason
- If frame-pressure sub-pass flagged ≥1: consider /article-critique [essay-path] before promotion
- If length out of range: /article-revise [essay-path] again with Pass G focus
- If any other question is no: /article-revise [essay-path] again, focusing on <failed question>
```

---

## Mode differences

- **adversarial** (default): all six passes, including Pass E stress-test. Use when the essay needs to survive smart objection.
- **creative**: Pass B (voice bleed) emphasized; Pass E skipped; additional attention to imagery, rhythm, openings/closings. Use for essays that are voice-forward (personal, narrative).
- **light**: Passes A, B, D only. Use for quick tidying; not sufficient for `status: final`.
