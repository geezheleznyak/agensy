---
description: External-critic pass. Produces a separate critique document; does NOT edit the essay. Catches what /article-revise's adversarial passes structurally cannot see.
type: universal-protocol
audience: claude
---

# /article-critique [essay-path] [--mode=full|frame-only|writing-only]

Run an external-critic pass against a cogitationis essay at any status (`seed`, `outline`, `draft`, `revision`). Produce a structured critique document at `synthesis_logos/critic/[essay-title].md` — a separate file the operator reads and decides what to address.

**Why this exists**: `/article-revise` audits execution within a frame (voice match, position alignment, preset fidelity, seam-stress). It does not audit *the frame itself*. An essay can pass all Five Questions and all Pass E audits while resting on a circular definitional move, a mis-cited theorist, an unaudited cross-scale analogy, or a concession that silently swallows its structural claim. This command runs the pressure-types that only an external reader normally catches. Calibrated against `synthesis_logos/critic/The frame is the argument, which is the problem.md` (the human-written reference critique of "The Pole Is Obsolete").

**[essay-path]**: absolute or vault-relative path to an essay at any status.

**[--mode]**:
- `full` (default) — all 8 passes + writing-tells.
- `frame-only` — C1, C5, C6 only. Cheap pre-outline / pre-draft check; use when the thesis is still moving.
- `writing-only` — writing-tells + C8 only. Surface polish after `/article-revise` has landed.

**Runtime**: Read `vault-config.md` from cogitationis vault root. Extract:
- `reference_docs.voice_profile` — for writing-tells sub-pass
- `reference_docs.writer_positions` — for position-check inside C2 (is the cited theorist compatible with user's bedrock?)
- `reference_docs.article_design_principles` — for principle references (P7–P10)
- `folder_structure.critic` — destination folder; if missing, default to `synthesis_logos/critic/`

This command never edits the essay. It is Read-only against the essay and Write-only against the `critic/` folder.

---

## Step 1 — Validate Input

1. Verify [essay-path] exists. Read the file fully.
2. Detect status from frontmatter (`status:` field). Accept any of `seed`, `outline`, `draft`, `revision`, `final`, `companion-draft`, `companion-final`.
3. Parse [--mode]. Default `full`. Reject unknown modes.
4. Detect article type from frontmatter (`article_type:` field if present). Used only to decide whether C3 (cross-domain analogy) and C4 (stratification independence) fire — they apply to any essay that extends frameworks or stratifies, regardless of Type A/D.
5. If `synthesis_logos/critic/` does not exist, create it.

---

## Step 2 — Extract Critique Targets

Before running passes, identify what the essay is making load-bearing:

- **Thesis**: from frontmatter `thesis_candidate` / `emergent_claim` or the opening sentence/paragraph.
- **Load-bearing terms**: the central nouns in the thesis (e.g., "pole", "polarity", "structural power"). Identify the 1–3 terms whose definition the argument depends on.
- **Cited theorists**: named figures whose frameworks the essay invokes (from `source_refs`, inline references, section names).
- **Frameworks being extended**: any framework applied outside its canonical domain (e.g., Arthur's increasing-returns applied to frontier AI).
- **Stratifications**: any claim that the argument's domain stratifies into layers/tiers with distinct dynamics.
- **Concessions**: passages where the essay explicitly concedes a point to a counter-position (grep for "concede", "granted", "to be sure", "admittedly", "phase-dependent", or similar hedges against the thesis).
- **Unit of analysis**: the implicit subject of the predicates (state, firm, individual, network, platform, etc.).
- **Title**: the essay's current title.

Buffer these targets; the 8 passes consult them.

---

## Step 3 — Run Critique Passes

Each pass either fires (produces a critique section) or skips (records no applicable target). Skipped passes are reported but produce no section in the output.

### C1 — Frame audit (always fires)

**Question**: Is the load-bearing definitional move doing the argument's work?

**Procedure**:
1. For each load-bearing term, extract its operative definition from the essay (explicit definition, or the first substantive use).
2. State the thesis using that definition. State the thesis again using a *different defensible definition* of the same term (the definition a critic might prefer).
3. If the conclusion follows only under the essay's definition, the frame is the argument. Flag.
4. Check whether the essay defends the definitional move *independently* of the conclusion — i.e., does the essay give reasons to prefer this definition over plausible alternatives, without appeal to the conclusion it produces? If no, flag as circular.
5. Check whether the essay treats its load-bearing term as category-different from prior analogs (e.g., "compute frontier" vs. oil, nuclear, semiconductors). If yes, does it argue for the category-difference or assume it? Assumed category-difference is the deepest frame problem.

**Flag form**: "The essay's definition of [TERM] is [definition]. Under this definition, the conclusion [CONCLUSION] follows. Under [alternative definition], the conclusion does not follow. The essay assumes the definition rather than defending it. [optional: analog case — e.g., nuclear produced a nonproliferation regime, not a redefined polarity; why would [TERM] do what [analog] didn't?]"

**Corrective recommendation**: either (a) add a defense of the definitional move that does not appeal to the conclusion, or (b) recast the thesis as conditional on the definition ("under [this] reading of [TERM]").

**Principle**: P7.

---

### C2 — Theorist-binding audit (fires when named theorists cited)

**Question**: Is each cited theorist actually endorsing the specific argument made, or being used as a stamp?

**Procedure**:
1. For each named theorist, retrieve their canonical claim from the source map (if cited as source) or from general knowledge.
2. Ask: would the cited figure accept the specific argument as written? Not "does their framework apply" — "would they, reading this essay, recognize their view in it?"
3. If no (or not clearly yes), the theorist is being used as stamp. Flag.
4. Check whether the argument requires the theorist's name. If the argument stands as "framework-flavored" (realist, Hayekian, Schumpeterian) without the specific figure's signature, the name is borrowed authority.
5. Check whether the theorist's *strongest output* aligns with the essay's predictions. If the theorist's predictions are about war and the essay predicts coalition labels, there is a mismatch.

**Flag form**: "The essay invokes [THEORIST] in [SECTION] for [SPECIFIC CLAIM]. [THEORIST]'s canonical position is [CANONICAL CLAIM]. [THEORIST] would [reject / not endorse / be indifferent to] the specific argument. The argument is [framework-flavored without needing the signature / requires a different theorist / stands alone]."

**Corrective recommendation**: either (a) drop the name and keep the framework's logic explicit, or (b) engage the gap between the theorist's canonical position and the essay's use, or (c) substitute a theorist whose work actually endorses the move.

**Principle**: P8.

---

### C3 — Analogy validity audit (fires when a framework is extended cross-domain)

**Question**: When a framework is extended from its canonical domain to a new one, are the conditions that made it work in the original domain present in the new one?

**Procedure**:
1. For each extended framework, list its canonical cases (e.g., Arthur: QWERTY, VHS, Windows).
2. List the structural features of those cases that produced the framework's result (e.g., near-zero marginal reproduction cost, dominant consumer-side network effects, weak substitutes).
3. Check whether the target domain of extension shares those features. If two or more features are absent or weaker, the extension is contested.
4. Check whether the essay addresses the absence of those features or waves it off.
5. If the extension operates across scales (firm-level framework applied to state-level outcomes, individual-level applied to collective, platform-level applied to structural), check the cross-scale step: does firm-lock-in actually become state-position, or does a past case show it doesn't?

**Flag form**: "The essay extends [FRAMEWORK] from [CANONICAL DOMAIN] to [TARGET DOMAIN]. Canonical cases have [FEATURE 1, FEATURE 2, FEATURE 3]. [TARGET DOMAIN] has [missing or weakened features]. The extension requires either (a) a defense of why the missing features don't matter, or (b) a weaker claim. Cross-scale propagation: [named past case that disconfirms, if applicable]."

**Corrective recommendation**: engage the disanalogies directly, narrow the claim to the conditions that hold, or drop the extension and make a more local claim.

**Principle**: adjacent to P7 (frame defense); no dedicated principle yet — generalization candidate after second pilot.

---

### C4 — Stratification independence audit (fires when the argument stratifies)

**Question**: When the argument layers or tiers its domain, does it assume independence across layers that is actually false?

**Procedure**:
1. Identify the stratification: layers named, dynamics claimed per layer.
2. For each pair of adjacent layers, ask: does output from layer A feed back into layer B on the relevant timescale?
3. Canonical failure: knowledge outputs (layer 1) feeding into production (layer 2) via AI-for-X, or ideational outputs feeding into material outputs via legitimation. Check for each plausible feedback path.
4. If feedback is plausible on the essay's stated timescale, the stratification is a snapshot rather than a structure. Flag.
5. Check whether the essay names the feedback as a possible falsifier but fails to model the weaker version — that the feedback partially undermines the layer's independence.

**Flag form**: "The essay stratifies [DOMAIN] into [LAYER 1 / LAYER 2 / LAYER 3]. It treats the layers as having independent dynamics. But [LAYER A output] feeds back into [LAYER B] on the essay's [TIMESCALE] via [MECHANISM]. The stratification is therefore a snapshot, not a structural equilibrium. The essay [does / does not] address this."

**Corrective recommendation**: either (a) model the cross-tier feedback explicitly and weaken the stratification claim accordingly, or (b) restrict the argument to timescales on which the feedback is negligible, or (c) argue for why the feedback is structurally bounded.

**Principle**: P10.

---

### C5 — Scenario completeness audit (always fires)

**Question**: When the title, frame, or thesis implies major counter-scenarios, does the essay name them?

**Procedure**:
1. Parse the title and thesis for scope terms ("AGI era", "under X regime", "in the 5–25 year window", etc.).
2. Enumerate the major scenarios the scope term implies:
   - Does the central phenomenon reach its asymptote inside the window? If yes, argument collapses in direction A.
   - Does the central phenomenon commoditize / diffuse inside the window? If yes, argument collapses in direction B.
   - Does the central phenomenon persist at the current rate? (This is usually the scenario the essay implicitly argues.)
   - Are there regime-change scenarios (political, technological, geological) that would invalidate the frame?
3. Check whether the essay names these scenarios and either commits to one or distinguishes the conditions under which each obtains.
4. An essay framed by a scope term that doesn't engage scope-scenarios is incomplete.

**Flag form**: "The essay is framed as [SCOPE]. This implies counter-scenarios [A, B, C]. The essay implicitly argues [C] without naming [A, B]. The reader cannot tell whether the argument holds in [A] or [B]. Name them. Commit to one, or distinguish the conditions."

**Corrective recommendation**: add a scenario-inventory passage, typically before the close, that names the N live scenarios and either commits or conditions. Alternatively, narrow the scope so the unnamed scenarios fall outside.

**Principle**: adjacent to C1 (frame defense); no dedicated principle — candidate after second pilot.

---

### C6 — Concession-load audit (fires when the essay concedes)

**Question**: Does any concession to a counter-position silently weaken a structural claim to a phase-dependent / contingent claim?

**Procedure**:
1. For each concession (grep targets from Step 2), extract the claim conceded.
2. Ask: does conceding this point weaken the essay's thesis from structural to phase-dependent / contextual / contingent?
3. If yes, check whether the essay re-states the thesis at the weaker register or lets the original (stronger) formulation stand.
4. Check where the structural weight then rests. If the load moves to another component of the argument (e.g., Arthur when Strange is conceded), check whether that component can carry the weight (C3 test).
5. A thesis that becomes "in this phase, X is Y" while the essay still advertises structural reformulation has been silently swallowed by its own concession.

**Flag form**: "The essay concedes [POINT] to [COUNTER]. This concession weakens the thesis from [STRUCTURAL CLAIM] to [PHASE-DEPENDENT CLAIM]. The essay does not re-state the thesis at the weaker register; it continues to advertise [ORIGINAL]. The load now rests on [COMPONENT X], which [passes/fails] the C3 / cross-domain test."

**Corrective recommendation**: either (a) re-state the thesis at the weaker register throughout, or (b) reconsider the concession — is it actually necessary?, or (c) defend the structural reading against the concession directly.

**Principle**: P9.

---

### C7 — Unit-of-analysis audit (always fires)

**Question**: Is the unit of analysis consistent with the predicates being made? Does the argument silently shift unit?

**Procedure**:
1. Identify the declared unit (state, firm, individual, platform, network, civilization, etc.).
2. Read the predicates the argument makes about that unit.
3. Check whether those predicates are actually about the declared unit or about a different level of aggregation:
   - State-level arguments about firm-level dynamics
   - Firm-level units making claims about state outcomes
   - Individual-level arguments about collective patterns (or vice versa)
   - Platform-level claims dressed as market-level claims
4. Check whether the essay hedges on unit (uses "the X" without specifying state/firm/etc.) — hedging obscures the question.
5. If the argument's predictions can be retargeted by naming a different unit as primary, the unit matters and the argument has not committed.

**Flag form**: "The essay's declared unit is [DECLARED]. But the predicates in [SECTION(S)] are about [ACTUAL UNIT]. Or: the essay hedges between [UNIT A] and [UNIT B] without committing. A [ALTERNATIVE UNIT]-centric reading of the same material produces [DIFFERENT CLAIM]. The hedge obscures which argument is being made."

**Corrective recommendation**: commit to a unit, make the predicates fit, and engage the alternative unit's reading explicitly as a counter-position.

**Principle**: adjacent to P3 (metric-realism); generalization candidate.

---

### C8 — Title-thesis match audit (always fires)

**Question**: Does the title describe the actual argument, or does it overclaim / mis-describe / frame the argument hostilely against itself?

**Procedure**:
1. Compare the title against the essay's actual thesis (frontmatter `thesis_candidate` / `emergent_claim` or the opening).
2. Identify mismatches:
   - Title overclaims (essay says "stratified", title says "obsolete")
   - Title describes a different argument than the body makes
   - Title frames the argument in a way a reader will use against it
   - Title uses a term the essay later concedes is the wrong term
3. On Substack / public venues: titles set the frame readers read against. A hostile-to-thesis title undermines the argument before the opening paragraph.

**Flag form**: "The essay's title is [TITLE]. The essay's actual argument is [ARGUMENT]. The title [overclaims / mis-describes / frames hostilely]. Alternative titles: [ALT 1, ALT 2]."

**Corrective recommendation**: revise the title to match the actual argument. Test with the cold-reader frame: would a reader, knowing only the title, correctly predict the body?

**Principle**: no dedicated principle; a mechanics rule. Candidate for `article-design-principles.md` as P11 after second pilot.

---

### Writing-tells sub-pass (extension of /article-revise Pass B)

**Question**: Does the prose exhibit LLM-assistance signatures that undercut authority?

**Targets** (expands the seven tics in `voice-profile.md` §LLM-Essay Failure Modes):

1. **Self-marketing phrases**: "the essay's sharpest move lives here", "the place a sharp reader should press first", "the real move is…", "this is where the argument actually happens" — any meta-commentary telling the reader how to read.
2. **Preemptive objection-management before the argument has landed**: "Two scoping notes…", "Before I continue, one caveat…", "I should flag that…" — defensive hygiene ahead of the move. (Flagging weaknesses AFTER the argument lands is fine; BEFORE undermines.)
3. **Repetitive parallel constructions**: "Each X that Y. Each A that B. Each P that Q." — structural parallelism without variation. Once per essay is rhetoric; three times is a tic.
4. **Academic warm-up openings**: "The question sounds like housekeeping for…", "This is a problem that has long vexed…", "Scholars have debated…" — any opening that describes the question instead of striking at it.
5. **All seven tics from `voice-profile.md`** — re-verify per existing pass-B protocol, because `/article-revise` may have under-detected.

**Flag form**: "Writing-tell [TYPE] found at [LOCATION(S)]: [EXCERPT]. Suggested revision: [specific rewrite or cut]."

---

## Step 4 — Compose the Critique Document

Write to `synthesis_logos/critic/[essay-title].md` (derive `[essay-title]` from the essay's title frontmatter; if title has invalid filename characters, sanitize). If a file already exists, append `- rev-YYYY-MM-DD` to the filename.

**Structure** (mirrors the hand-written reference critique):

```markdown
---
critique_of: "[[<essay-path>]]"
created: YYYY-MM-DD
mode: <full | frame-only | writing-only>
passes_fired: [<list of C1-C8 that produced flags, plus writing-tells if any>]
passes_skipped: [<list with reasons>]
essay_status_at_critique: <status read from essay frontmatter>
---

# <Critique title — e.g., "The frame is the argument, which is the problem">

<one-paragraph opener: state the angle of attack — which pass found the deepest issue, what's the thread connecting the others. Mirror the tone of the reference critique: analytical, surgical, direct. Not exhaustive; point at the load-bearing issue first.>

## <Section per fired pass — use descriptive section titles, not "C1 Frame audit">

<For each fired pass, write a section in the tone of an external reader. Name the specific issue found in this essay (not a generic description). Include:
- what the essay does
- what the critic sees wrong with it
- why this matters structurally (not just stylistically)
- a concrete suggestion or test
Length: 100–400 words per section depending on depth. Do not pad.>

## Writing-tells (if the sub-pass fired)

<one section, bulleted, with location pointers>

## What I'd rewrite around

<closing synthesis — 1–2 paragraphs naming the *one* tension worth rebuilding around, or the *one* claim worth load-bearing. This is the constructive close. Do not list every flag; name the rebuild.>
```

**Tone requirements for the critique document**:
- Cold-blooded analytical (same default as voice-profile) — the critic is an adversarial reader, not a cheerleader and not a hater.
- Surgical, not comprehensive. Lead with the deepest issue.
- Concrete, not abstract. Every flag cites a specific passage / claim / term.
- Constructive close. The critic leaves the operator with something to build on.
- Do not include C-codes (C1 / C2) in section titles — the operator reads this as external feedback, not as protocol output.

**Skipped-pass handling**: if a pass doesn't fire (no targets), note it in `passes_skipped` frontmatter with a brief reason. Do not write empty sections for skipped passes.

---

## Step 5 — Update the Essay's Frontmatter (light touch)

Append to the essay's frontmatter (not the body):

```yaml
critique_runs:
  - date: YYYY-MM-DD
    mode: <mode>
    critique_file: "[[critic/<filename>.md]]"
    passes_fired: [<list>]
    flag_count: <total>
```

This is the only edit `/article-critique` makes to the essay. It adds a pointer to the critique file; it does not alter body prose or thesis fields.

---

## Step 6 — Report

```
## /article-critique [essay-path] [--mode=<mode>] — YYYY-MM-DD

Critique written: [absolute path to critique file]
Essay status at critique: <status>
Mode: <mode>

Passes fired: <count> of 8
  - <pass name>: <flag count> — <one-line summary>
  - ...
Passes skipped: <count>
  - <pass name>: <reason>
Writing-tells: <count> — <locations or none>

Deepest flag: <which pass, one-sentence summary>
Rebuild-around recommendation: <one-sentence synthesis from §"What I'd rewrite around">

Essay frontmatter updated: critique_runs entry appended.

Next steps (operator's choice):
- Read [critique path] and decide which flags to address
- Address frame-level flags (C1/C5/C6) at outline level if essay is pre-draft
- Address execution-level flags (C2/C3/C4/C7/C8/writing-tells) at revision level
- /article-revise [essay-path] to apply revisions the operator agrees with
- /article-revise Step 4 6th question ("has critique been run and addressed?") is now checkable
- /article-promote [essay-path] if all critique flags are addressed or explicitly dismissed in essay frontmatter
```

---

## Mode differences

- **full**: all 8 passes + writing-tells. Default. Typical use: once after `/article-revise`, before considering promotion.
- **frame-only**: C1 + C5 + C6. Cheap pre-outline / pre-draft check — catches circular frames, silent scenarios, load-swallowing concessions before prose exists.
- **writing-only**: writing-tells + C8. Post-revision polish. Does not catch structural issues.

---

## Error modes

- If essay file is missing or unreadable: abort with "Essay not found: [path]".
- If essay has no thesis (not yet at seed stage): refuse with "Essay has no thesis_candidate or emergent_claim frontmatter and no identifiable opening thesis. Run /article-seed first, or write an opening claim."
- If `critic/` folder cannot be created (permissions): abort with "Cannot write critique — check folder permissions for [path]".
- If the essay's frontmatter cannot be appended (parse error): write the critique file, skip the frontmatter update, and note the skip in the report.
- If `--mode=full` and all 8 passes skip (no targets for any — unusual for a non-trivial essay): write a minimal critique file noting the essay is thin in load-bearing moves, and suggest the operator check whether the essay has actually made claims yet.

---

## Calibration reference

The 8 passes and writing-tells are calibrated against `synthesis_logos/critic/The frame is the argument, which is the problem.md` — the human-written reference critique of "The Pole Is Obsolete" (V1.7 synthesis-braid pilot, 2026-04-21). When running this command on that essay:
- C1 should catch the compute-frontier-as-pole circularity.
- C2 should catch Mearsheimer-as-stamp.
- C3 should catch the Arthur QWERTY/VHS conditions absent in frontier AI.
- C4 should catch stratification-treats-tiers-as-independent.
- C5 should catch the post-AGI silence (three unnamed scenarios).
- C6 should catch Strange's phase-dependent concession swallowing the structural claim.
- C7 should catch the state/firm hedge.
- C8 should catch "Obsolete" overclaim vs "Stratified" actual argument.
- Writing-tells should catch self-marketing phrases, preemptive objection-management, "Each X that Y" repetition, academic-warm-up opening.

If any pass misses what the human critic caught, that pass is under-calibrated. Update the pass procedure in this file with what the reference critique saw; re-run until convergence.

---

## Shared pass library

`/co-critique` (companion-mode surgical critique) uses the same 8 passes against a *selection* rather than a full essay. See `co-critique.md`. Any refinement to a pass procedure in this file applies to both commands.
