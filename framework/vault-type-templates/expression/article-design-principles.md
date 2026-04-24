---
title: "Article Design Principles"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [type/meta, theme/craft]
status: seeded-from-template
purpose: Accumulates cross-essay craft principles. Read by /article-outline, /article-revise, and /article-critique to inform structural decisions. Distinct from voice-profile.md (style) and writer-positions.md (substance commitments).
---

# Article Design Principles

These are structural-craft principles, not stylistic rules. Voice-profile governs *how* sentences sound; writer-positions governs *what* the author believes; this document governs *how an argument is shaped into an article*.

Each principle is stated as a rule, with the failure mode that motivated it, and the corrective heuristic. Principles ship here in the template because they generalize across essay pipelines; your own vault will add pilot-specific principles as your essays expose new structural issues.

**Template status**: ten principles (P1–P10) shipped. P1–P3 are the "build" principles (when the essay is argumentative). P4–P6 are the "braid" principles (when the essay is a synthesis across N frameworks). P7–P10 are the "critic" principles (what an external reader catches that the adversarial revision pass cannot). Keep these as-is until your own pilots surface failure modes that the current set doesn't cover — then add Pn entries following the rule / failure mode / corrective / how-to-apply / realized-by format.

---

## P1 — Orthodoxy-counter articles must name the orthodoxy before striking the counter

**Rule**: When the article's argumentative intent is to refute a widely held thesis, the orthodoxy must be named explicitly in the opening — ideally paragraph 1 — before the counter-argument's anchor case is introduced. Case-first openings work for "here's a phenomenon I want to explain" articles; they fail for "here's a thesis I want to overturn" articles because the reader has not been given the target to see the hit.

**Failure mode observed**: An orthodoxy-counter essay opened with a strong anecdotal case but the opposed thesis did not appear until paragraph 3. A cold reader hit the opening and saw a historical anecdote, not an argumentative crowbar. By the time the orthodoxy was named, the case had already landed and the reader had no referent to land it against.

**Corrective structure**:
1. Name the orthodoxy (thesis + lineage — a few figures, including its most contemporary form).
2. Name its hidden premise (the assumption the thesis makes but rarely states, which the essay will attack).
3. Strike with the anchor case (now an evidence hit against the named premise, not a free-standing puzzle).
4. Introduce the framework author / alternative framework.
5. Generalize the mechanism to contemporary catalog.
6. Compress to thesis.

**How to apply**: Run this check at `/article-outline` time. If the essay's thesis is of the form "X is not what you think it is" or "the standard view of X is wrong," enforce P1. If the essay's thesis is of the form "X is an underappreciated phenomenon that deserves this framework," case-first opening is still valid.

**Realized by preset**: `orthodoxy-counter` — opening type `orthodoxy-first`, seven paragraph beats in [[article-presets]]. Preset inference at `/article-seed` Step 2.5 routes theses matching "X is not Y" grammar into this preset, automatically enforcing P1 at outline time.

---

## P2 — Pressure sections should audit for category errors, not only objections

**Rule**: The pressure-section design question is not "what objections can critics raise against my framework?" but "what is the framework's primary referent actually doing in the world, and does my framework's success metric measure the right thing?" The first question produces defense; the second produces extension.

**Failure mode observed**: A pressure section enumerating two standard objections to the central framework showed both objections partially land but the framework survives. What the section missed: if the framework correctly predicts that practitioners rarely achieve the canonical success metric, why do practitioners keep trying and paying the cost? The answer — practitioners were optimizing for several *other* outputs the canonical metric doesn't measure — was visible only once the category error was named. The objections framing had trained the pressure section to defend, not to extend.

**Corrective structure**:
1. Frame the section not as "objections to the framework" but as "accounts of what the framework's phenomenon is actually doing." Each account is a distinct optimization target.
2. The empirical objection becomes Account 1 — the account on which the objection lands.
3. The theoretical objection becomes Account 2 — the account on which the objection partially lands but is absorbed.
4. The hidden account becomes Account 3 — the account the objections' framing obscured. This is the section's load-bearing addition.
5. Section closes with synthesis: same mechanism across all accounts, different optimization targets.

**How to apply**: Run this at `/article-revise` time. After the pressure section is drafted, ask: *what would a practitioner of this phenomenon say I've missed?* If the answer is "you're measuring the wrong KPI," that is the Account-3 slot. Add it, don't defend around it.

**Realized by preset**: `orthodoxy-counter` — pressure type `three-accounts` in [[article-presets]], with Account 3 listed as a load-bearing required slot. `/article-outline` Step 3 imposes the three-slot structure; `/article-revise` Pass E preset-fidelity sub-pass flags missing Account 3 as mandatory revision.

---

## P3 — Empirical-falsification objections often test the wrong metric

**Rule**: When a framework is hit by a devastating-looking empirical result — "your framework predicts X, but X happens less than 5% of the time" — the first response should not be to patch the prediction. It should be to check whether the metric being tested is the metric the framework's users are actually optimizing. Framework predictions and practitioner objectives are often different targets, and the falsification may be an apparent falsification only under a misaligned metric.

**Failure mode observed**: A famous falsification result haunted a framework for decades. Most treatments responded by qualifying the framework's prediction. The deeper reading: compliance with the canonical prediction was almost never what practitioners were buying; the measurement was misaligned with the practice. Under the alternative accounting, the framework's record looks very different.

**Corrective procedure**:
1. When the adversarial pass (Pass E, stress) surfaces an empirical falsification, before patching the framework, ask: *what is the metric, and who is optimizing for it?*
2. If the practitioners are not optimizing for the metric the falsification uses, the falsification is under-threat — the framework still works, but under a different success function.
3. If the practitioners are optimizing for the metric, the falsification lands and the framework needs revision.

**How to apply**: Add this check to `/article-revise` Pass E protocol. Before concluding "the framework survives this objection by predicting X instead of Y," audit whether the practitioners are measured on X, Y, or something else entirely.

**Realized by preset**: applicable across all presets, but runs by default in `/article-revise` Pass E for `orthodoxy-counter` and `framework-build`. The category-error audit is the concrete operational form of P3.

---

## P4 — A braid's seam must be load-bearing; test by removal

**Rule**: In a synthesis-braid article (N≥3 frameworks), the seam — the named tension binding the frameworks — must be load-bearing such that the emergent claim cannot be reached from any single framework alone. The practical test: rewrite a version of the essay with any one framework removed; if the argument still produces roughly the same thesis, the essay is solo-with-footnotes, not a braid.

**Failure mode**: Braid essays routinely collapse to one dominant framework with the others serving as decorative citation. The seam remains named but doesn't do any work; the reader learns the author's preferred framework better than they learn how N frameworks compose.

**Corrective structure**:
1. At outline time (Step 6.5 Seam Audit), run the five-test gate — framework load-bearingness, emergent claim non-derivability, seam specificity, equal weight ±20%, braid section hinge specificity.
2. At revise time (Pass E seam-stress audit), re-run the decoupling test paragraph-by-paragraph; flag any framework whose removal doesn't materially change the emergent claim.
3. At promote time (Step 7), expect 2–4 harvest candidates from a true braid; a braid producing zero cross-vault emergent claims is anomalous.

**How to apply**: The `synthesis-braid` preset's audit list (`seam-stress`, `synthesis-validity`, `metric-realism`) encodes this. Step 6.5 in `/article-outline` is the hard gate; revise Pass E is the second check.

**Realized by preset**: `synthesis-braid` — opening `seam-first`, body `braided`, pressure `seam-stress`, closing `emergent-claim`. See [[article-presets]].

---

## P5 — Braid framework sections must be equal-weight; unequal weight = hidden hierarchy

**Rule**: In a braid, the N framework sections must be within ±20% of the mean section length. Systematic asymmetry signals that the author has a dominant framework and N-1 supporting frameworks — which is a Type A essay with footnotes, not a braid.

**Failure mode**: The author knows F1 best (their home domain), so F1 gets an outsized share of words, F2 gets less, F3 less still. The reader absorbs F1's argument and receives F2/F3 as credibility-marking citations. The emergent claim then sounds like F1's claim with interdisciplinary dressing.

**Corrective procedure**:
1. At outline time, Step 6.5 test 4 enforces the budget range. Outline fails if any section is more than ±20% from mean.
2. At draft time, respect the budget. If F1 feels like it needs more, the author is discovering that F1 is actually the spine and F2/F3 are supports — reconsider whether this is a braid at all.
3. At revise time, Pass E's braided-body check verifies equal budgets in the completed draft.

**How to apply**: Encoded in the `synthesis-braid` preset's `budget_words_per_framework` field and enforced by `/article-outline` Step 6.5. Violations are a hard gate on advancing to draft.

---

## P6 — The emergent claim must be stated explicitly, not implied

**Rule**: A braid essay's emergent claim must appear in the closing as an explicit sentence with its compositional justification. It must not be left to the reader to synthesize from the N framework sections. The whole point of the braid is the emergent claim; compressing it and hoping the reader assembles it defeats the essay.

**Failure mode**: The essay cycles through F1 / F2 / F3 cleanly but closes with "and thus the frameworks illuminate each other" or a meta-reflection on interdisciplinarity. The reader exits with three framework summaries and a vague sense that they connect, not with a new claim they can cite.

**Corrective structure**: The `emergent-claim` closing type in [[article-presets]] requires (a) the emergent claim stated explicitly with full compositional justification behind it (not compressed — the reader has earned it by this point), and (b) one reader-usable frame — a diagnostic question or move that invokes the braid. The close does not recapitulate F1/F2/F3 structurally; it lands on what the composition produces.

**How to apply**: `/article-outline` Step 3 imposes the closing type. `/article-revise` Pass E verifies the closing contains a claim-form sentence (not a summary or meta-reflection).

---

## P7 — The frame is the argument

**Rule**: The load-bearing definitional move — the operative definition of the central term(s) in the thesis — must be defended independently of the conclusion it produces. Test: re-state the conclusion using a different defensible definition of the same term. If the conclusion follows only under the essay's preferred definition, and the definition is not itself defended (without appeal to the conclusion), the frame is doing the argument's work and the essay is self-confirming.

**Failure mode observed**: An essay redefined a key term, then argued that under this definition a structural claim held. Every downstream move inherited the primacy premise without interrogating it. A reader willing to grant every empirical point could still deny the conclusion by denying the redefinition was category-different from prior versions of the same concept. The essay never established this. It assumed it. The adversarial revision passes could not catch the assumption because their machinery operated *inside* the frame.

**Corrective procedure**:
1. Before outline, identify the 1–3 load-bearing terms in the thesis.
2. For each, state its operative definition and list 1–2 plausible alternative definitions.
3. Write one sentence defending the preferred definition on grounds that do not appeal to the conclusion the essay will produce.
4. If that sentence cannot be written, either (a) recast the thesis as conditional on the definition, or (b) find a different load-bearing move.

**How to apply**: Run at `/article-outline` Step 3 (pre-draft, cheap). Re-run at `/article-critique` C1 (post-revision, rigorous). Pass E frame-pressure sub-pass in `/article-revise` is a tripwire version.

**Realized by command**: `/article-critique` C1 is the full test; `/article-revise` Pass E frame-pressure sub-pass is the inline version.

---

## P8 — Theorists are tools, not stamps

**Rule**: A cited theorist's name must be accurate authority for the specific argument being made. If the named figure would reject the argument as written, drop the name and keep the framework's logic explicit. Framework-flavored arguments (realist, Hayekian, Schumpeterian, game-theoretic) do not need a specific author's signature; the logic is what does the work.

**Failure mode observed**: An essay invoked a well-known theorist as authority for a specific claim. The theorist's canonical position did not actually endorse the claim — their framework *flavored* the essay's logic but their own strongest outputs predicted something quite different. The name was borrowed authority, not load-bearing theory.

**Corrective procedure**:
1. For each named theorist, ask: would the cited figure accept the specific argument as written? Not "does their framework apply" — "would they, reading this essay, recognize their view in it?"
2. If no, the theorist is a stamp. Either (a) drop the name and keep the framework's logic explicit, or (b) engage the gap between the theorist's canonical position and the essay's use, or (c) substitute a theorist whose work actually endorses the move.
3. Check whether the theorist's *strongest output* aligns with the essay's predictions. If the theorist predicts one class of outcome and the essay predicts another, there is a mismatch worth naming.

**How to apply**: Run at `/article-critique` C2. Runs whenever a theorist is named.

**Realized by command**: `/article-critique` C2.

---

## P9 — Concessions can swallow theses

**Rule**: Every concession to a counter-position must be audited: does it weaken a *structural* claim to a *phase-dependent* / contingent claim? If yes, the thesis must be re-stated at the weaker register throughout, or the concession reconsidered. An essay cannot advertise a structural reformulation while conceding the very structural claim to its strongest opposition.

**Failure mode observed**: An essay conceded, in passing, that a central structural claim was "phase-dependent" — held in some eras, not others. The concession was massive: if the claim is phase-dependent, the thesis reduces to "in this phase, X is true" — a much weaker, more contingent, more empirical claim than the structural reformulation the essay advertised. To keep the stronger claim, the essay silently shifted weight onto a different, weaker component.

**Corrective procedure**:
1. Grep the draft for concession markers: *"phase-dependent", "granted", "to be sure", "admittedly", "in this phase", "under current conditions", "at present"*.
2. For each hit, ask: does conceding this weaken a structural claim to a phase-dependent / contingent one?
3. If yes, check whether the thesis is re-stated at the weaker register downstream of the concession, or whether the original (stronger) formulation continues to stand.
4. If the original stands: either (a) re-state the thesis at the weaker register throughout, (b) reconsider the concession — is it actually necessary? can the essay defend the structural reading against the counter-position directly?, or (c) name the concession as conditional and engage both branches.
5. Check where the structural weight then rests. If the load moves to another component, run C3 (analogy validity) on that component.

**How to apply**: Run at `/article-critique` C6. Also run as `/article-revise` Pass E frame-pressure sub-pass (lightweight version).

**Realized by command**: `/article-critique` C6; `/article-revise` Pass E frame-pressure sub-pass.

---

## P10 — Stratifications must justify independence

**Rule**: When the argument layers a domain into tiers/strata with distinct dynamics, the independence across layers must be justified. For each pair of adjacent layers, audit cross-layer feedback on the essay's stated timescale. If feedback is plausible, the stratification is a snapshot, not a structure — and either the essay must model the feedback (with consequent weakening of the stratification claim) or restrict scope to timescales where feedback is negligible.

**Failure mode observed**: An essay stratified a domain into N distinct layers with claimed-independent dynamics. But outputs from one layer fed back into adjacent layers on the essay's own timescale. The essay flagged this as a *possible* falsifier but did not model the weaker version: that the stratification was presented as structural equilibrium when it was a snapshot vulnerable to cross-tier feedback.

**Corrective procedure**:
1. Identify the stratification: layers named, dynamics claimed per layer.
2. For each pair of adjacent layers, ask: does output from layer A feed back into layer B on the essay's timescale?
3. For each plausible feedback path, state the mechanism explicitly.
4. If feedback exists, either (a) model it and weaken the stratification claim accordingly, (b) restrict the argument to timescales where the feedback is negligible, or (c) argue structurally why the feedback is bounded.
5. An essay that flags feedback as a "possible falsifier" without modeling the weaker version has not done the work.

**How to apply**: Run at `/article-critique` C4 whenever the argument stratifies. Particularly important for synthesis-braid essays that claim their frameworks operate at different layers.

**Realized by command**: `/article-critique` C4.

---

## Meta: how this document grows

Each pilot's `revision_log` surfaces lessons. Lessons that generalize — that could apply to other essays — get promoted here as Pn principles. Lessons specific to one essay's subject matter do not.

A principle stays here until it is either:
- **Validated on a second pilot**: note the second essay in the source field; upgrade confidence.
- **Disconfirmed on a second pilot**: revise the rule or mark it narrow-scope.
- **Contradicted by a third pilot**: retire to an `archived-principles/` folder with a note on why it did not generalize.

Target cadence: 2-4 principles per pilot in early vault life, settling to 0-1 per pilot once the stable set is found.
