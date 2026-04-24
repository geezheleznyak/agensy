---
description: Convert an outline into a full draft; voice-calibrated prose, vault-jargon purged
type: universal-protocol
audience: claude
---

# /article-draft [essay-path]

Generate the full draft of an essay from an outline. Voice consumed from `voice-profile.md`; substance constrained by `writer-positions.md`; wikilinks resolved to prose citations.

**[essay-path]**: absolute or vault-relative path to an essay at status `outline` (created by `/article-outline`).

**Runtime**: Read `vault-config.md` from cogitationis vault root. Extract:
- `reference_docs.voice_profile` — style layer
- `reference_docs.writer_positions` — substance layer (bedrock)
- `reference_docs.map_to_article_schema` — extraction recipe
- `reference_docs.article_presets` — path to article-presets.md (V1.5)
- `reference_docs.positions_index` — path to positions-index.md (V1.6)
- `reference_docs.source_map_registry` — for status update
- `output_layer.publication_target` — for audience calibration

---

## Step 1 — Validate Input

1. Verify [essay-path] exists and `status: outline`.
2. Read `voice-profile.md`. If status is `unseeded`: refuse with "voice-profile.md is unseeded. Run the voice-capture session first (see plan): provide 3–5 prose samples." Do not proceed without a seeded voice.
3. Read `writer-positions.md`. If status is `awaiting-user-fill`: warn "positions file unfilled; draft will proceed but cannot check alignment. Recommend filling before revise step."
4. **Type D only (V1.7)**: verify `article_type: D` and `preset: synthesis-braid` in the essay frontmatter. Verify `seam_stress_slot_1_passed: true` — if the outline was not run through the Step 6.5 seam audit, refuse with "Outline failed or skipped seam audit. Re-run /article-outline to pass Step 6.5 before drafting."

---

## Step 2 — Load Inputs

Read into working memory:
1. **The outline** (the essay file).
2. **Preset** (V1.5) — from essay frontmatter `preset` field. Default `framework-build` if missing.
3. **`article-presets.md`** — load the matching preset block. Extract opening paragraph beats + word budgets, closing type + word budget, pressure required-slots (for Step 3 use).
4. **The source map(s)**:
   - **Type A**: from `source_vault` + `source_seed` frontmatter → traverse to original map.
   - **Type D**: from `source_maps` list in essay frontmatter → read each of the N maps.
5. **`voice-profile.md`** — cadence, stance markers, openings, closings, diction, negative space.
6. **`writer-positions.md`** — founding commitments, rejected frames, non-negotiables, analytical moves.
7. **Source map's atomic notes** (from the citation pool in the outline) — for citation-ready sub-claims. For Type D, load atomics for all N maps; keep indexed by framework for Step 3.
8. **Matched positions (V1.6)** — from essay frontmatter `matched_positions` + `matched_position_treatments`. For each, read the referenced T3 note's claim sentence and mechanism paragraph. Keep in working memory as soft constraints during Step 3.
9. **Type D only**: also load `seam`, `braid_move`, `framework_order`. Keep the seam sentence and braid move hinge visible throughout drafting — these are the connective tissue.

---

## Step 3 — Per-Section Drafting

For each outlined section in order:
- **Type A**: Hook → Problem + Thesis → Body sections → Pressure → Implication → Close.
- **Type D** (V1.7): Opening (seam-first) → Body F1 → Body F2 → Body F3 (… FN) → Braid section → Pressure (seam-stress) → Implication → Close (emergent-claim).

### 3.1 Generate candidate prose
Draft the section to its budgeted word count. Key constraints:
- **Voice**: match `voice-profile.md` — cadence, sentence-length distribution, stance markers, openings, closings, diction, structural tics.
- **Substance**: every claim is grounded in source-map content OR in `writer-positions.md`. Nothing invented.
- **Cold reader**: assume the reader has no vault context. Every concept is unpacked in prose (no vault wikilinks).
- **Stakes**: reader-facing, not project-facing.
- **Preset opening** (V1.5): the Opening section's paragraphs must instantiate the preset's paragraph beats in order. For `orthodoxy-first`: paragraph 1 names the orthodoxy + lineage, paragraph 2 names the hidden premise, paragraph 3 strikes with the anchor case, etc. — do not collapse beats or reorder. For `phenomenon-first`: lead with the phenomenon needing explanation, not with a thesis. For `case-first`: drop the reader into the specific event with narrative specificity. For `reading-failure`: show the dominant reading missing the mark on a fresh example. **For `seam-first` (V1.7)**: paragraph 1 names the seam with a fresh observation or example; paragraph 2 shows why existing single-framework readings each fall short; paragraph 3 names the N frameworks in one sentence each, without unpacking; paragraph 4 previews the emergent claim compressed. Do not introduce any framework in depth in the opening — that's the body's job. Do not state the emergent claim as a surprise-reveal — it's a preview the body will earn.
- **Preset closing** (V1.5): the Close section's shape must instantiate the preset's closing type.
  - `aphoristic`: compressed punch inverting the orthodoxy — two-beat close authorized.
  - `diagnostic`: reader-ready tool ("next time you see X, ask Y").
  - `lesson`: one transferable insight the case vindicates.
  - `reader-ready-diagnostic`: small numbered/bulleted list of questions for the reader's next case.
  - `emergent-claim` (V1.7): state C explicitly with its full compositional justification behind it (not compressed — the reader has earned it by now); then offer one reader-usable frame (a diagnostic question or move the reader can take to their own case that invokes the braid). Do not repeat any single framework's argument in the close. Do not recapitulate F1/F2/F3 structurally — the close lands on what the composition produces, treating each framework as absorbed into C.
- **Preset pressure slots** (V1.5): when drafting the Pressure section, every required slot in the preset must be filled. For `three-accounts`: Account 3 is load-bearing; do not skip. **For `seam-stress` (V1.7): three slots, all mandatory** — (1) decoupling + competing-composition, (2) per-framework pressure aggregate (one paragraph per framework), (3) unit-of-analysis / temporal audit. If any slot would be light on substance, deepen rather than skip.

### 3.1D Braided body drafting (Type D only, V1.7)
For the N framework sections of the body:
- Each section leads with a **claim-form header** that states the framework's contribution to the emergent claim (not a biographical or doctrinal header). E.g., "Multipolarity Is Structurally Unstable," not "Mearsheimer's Offensive Realism."
- In each section's first two sentences: name the framework and its thinker briefly (one sentence), then immediately pivot to the contribution. Avoid biography; the reader doesn't need a primer.
- Develop 2–4 sub-claims (per the outline's moves for this framework). Use one concrete case per sub-claim when possible. Avoid framework-internal jargon — translate every technical term inline.
- Close each framework section with a **return-to-seam sentence** (drafted at outline time — Step 3.1D uses it or refines it). This sentence names what the seam looks like *through* this framework's lens, and sets up the next framework's angle. Function: continuity device; keeps the reader aware that the frameworks are being composed, not just enumerated.

For the braid/compression section:
- Open by naming the composition mechanism explicitly. If the hinge is "F1's X becomes F2's input, and F2's output constrains F3's Z" — say that, then unpack it.
- Each proof beat uses material already introduced in the F1/F2/F3 sections. Do not introduce new framework content here; the braid section's job is to combine, not to extend.
- Close with the emergent claim stated in full form with its compositional justification immediately behind it. This sentence is the essay's center of gravity; every prior section has been setup.

### 3.2 Wikilink resolution
If the outline references a vault wikilink:
- **Do not include the wikilink in the draft**.
- Instead: unpack the wikilinked concept into prose — one to three sentences of the minimum a cold reader needs.
- Record the reference in `source_refs` frontmatter (for traceability) — not inline.

### 3.3 Position-check (two-layer, V1.6)

**Layer 1 — Bedrock** (`writer-positions.md`, hard):
After drafting the section, check each substantive claim against `writer-positions.md`:
- **Aligned**: proceed.
- **Neutral** (claim is not addressed by positions): proceed, flag in draft notes as "unconstrained by positions".
- **Conflict**: pause. Options:
  - (a) Suppress the claim (cut from draft; note in `position_suppressions` frontmatter).
  - (b) Argue against it (invert the claim; note as intentional contrary).
  - (c) Flag to user for position revision.

Default for conflicts when user is not available: (a) suppress + note.

**Layer 2 — Matched positions** (`matched_positions` from essay frontmatter, soft):
When drafting the section that was reserved for a matched position at outline time (per `matched_position_treatments`):
- `supports`: draft the reserved argument move to cite or build on the T3 claim without duplicating its mechanism; defer to the T3 for the full account.
- `extends`: draft the extension into the new domain; reference the T3 claim as the extension's root.
- `tensions-with`: draft the pressure-slot engaging the T3 claim; do not silently contradict or ignore it. If the essay's thesis prevails over the T3, state the basis explicitly.
- If no reserved treatment but the section naturally touches a matched position: cite if `supports`; otherwise proceed without mention.

### 3.4 Vault-voice bleed check
Compare the drafted prose paragraph-by-paragraph against `voice-profile.md`. Flag any paragraph that drifts into:
- Neutral-essayistic default (sounds like Wikipedia).
- Vault-register detachment (sounds like a map section).
- Academic citation style (unless the audience = `academic` in frontmatter).

Flagged paragraphs are redrafted in profile.

---

## Step 4 — Assemble Draft

Concatenate the drafted sections in order. Ensure transitions are natural (add 1–2 bridging sentences between sections if needed; do not introduce new claims in bridges).

Compute word count. If significantly under or over budget (±25% of target):
- **Under**: flag sections that feel thin; add detail from source map's atomic notes or from the citation pool.
- **Over**: flag sections that drift; cut to budget.

---

## Step 5 — Update the Essay File

Update in place (do not create a new file):

**Frontmatter**:
```yaml
status: draft
updated: YYYY-MM-DD
word_count: <actual count>
source_refs: <updated — append any new references traversed during drafting>
position_suppressions: <updated — append any suppressions from Step 3.3>
draft_notes: <any flags surfaced during drafting (unconstrained claims, intentional contraries, audience-specific decisions)>
```

**Body**: replace outline body with drafted prose. Keep `## Core Argument` (one-sentence thesis) at the top as a stable reference. Drop outline-specific sections ("Budget", "Key moves", "Source-map section" annotations). Keep `## Citation pool` at the bottom (now used as source_refs audit trail).

---

## Step 6 — Update Registry

Update source-map-registry.md:
- Essay status → `drafted`

---

## Step 7 — Report

```
## /article-draft [essay-path] — YYYY-MM-DD

Draft complete: [absolute path to essay file]
Status: draft
Preset: <id>
Word count: <actual>
Target: <preset-specified range>
Position suppressions: <count> — see frontmatter if >0
Unconstrained claims: <count> — flagged in draft_notes
Vault-voice bleed flags: <count> — all redrafted
Preset slot fills: <count / required> (e.g., 3/3 for three-accounts)

Next step: /article-revise [essay-path]
```

---

## Error modes

- Voice-profile unseeded: refuse with instructions.
- Outline has no argument moves: refuse, return to `/article-outline`.
- Source map is unreachable or missing: warn and proceed with outline content only; flag as "source-map-missing" in draft_notes.
