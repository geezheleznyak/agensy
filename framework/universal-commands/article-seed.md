---
description: Create an essay seed in cogitationis 10-Thoughts from a source-vault map (Type A solo + Type D braid supported)
type: universal-protocol
audience: claude
---

# /article-seed [map-paths] [type] [--preset <id>]

Extract thesis, primary claims, pressure points, and stakes from one or more source-vault maps, and create a seed note in cogitationis `10-Thoughts/`.

**[map-paths]**:
- **Type A**: single absolute or vault-relative path to a source-vault map.
- **Type D**: comma-separated list of 3–5 map paths (no spaces around commas, or quote the whole list). The N maps are the N frameworks the braid will weave. Minimum 3 enforced — a two-map essay is Type B (pair), not Type D (braid).

**[type]**: `A` (solo — shipped) | `B` (pair — V2 deferred) | `C` (MOC position — V2 deferred) | `D` (braid — shipped). Default `A`. Runtime rejects B/C with "V2 — not yet implemented". Type D is live as of V1.7.

**[--preset <id>]**: optional explicit preset override. Valid ids: `framework-build` | `orthodoxy-counter` | `case-anatomy` | `diagnostic-lens` | `synthesis-braid`. When `[type]=D`, `synthesis-braid` is forced regardless of `--preset` (Type D and `synthesis-braid` are bound 1:1 — the flag is ignored with a warning). When `[type]=A` and `--preset synthesis-braid` is passed: refuse (`synthesis-braid` requires Type D). If `--preset` omitted and `[type]=A`, Step 2.5 infers.

**Runtime**: Read `vault-config.md` from the cogitationis vault root. Extract:
- `reference_docs.map_to_article_schema` — path to extraction recipe
- `reference_docs.writer_positions` — path to writer-positions.md
- `reference_docs.article_presets` — path to article-presets.md (V1.5)
- `reference_docs.positions_index` — path to positions-index.md (V1.6)
- `reference_docs.source_map_registry` — for status update
- `folder_structure.thoughts` — destination folder

Also read the source vault's `vault-config.md` to understand map conventions (section names, pressure-point format).

---

## Step 1 — Validate Input

1. Verify [type]. Accept `A` or `D`. Reject `B/C` with "Type [X] is V2 — not yet implemented. Use Type A (solo) or Type D (braid)."
2. Parse [map-paths]:
   - **Type A**: expect exactly one path. If multiple paths passed with `type=A`: refuse with "Type A takes one map. For N≥3 maps use Type D."
   - **Type D**: split on comma. Enforce 3 ≤ N ≤ 5. If N<3: refuse with "Type D requires ≥3 maps (N=2 is Type B, not yet implemented)." If N>5: refuse with "Type D capped at 5 maps — more than 5 produces diffuse weave; split into two essays."
3. For each parsed path: verify the map file exists. If any missing: error with "Map not found: [path]" and list all missing before aborting.
4. Validate preset compatibility:
   - If `type=A` and `--preset synthesis-braid`: refuse ("`synthesis-braid` requires Type D").
   - If `type=D` and any other `--preset` passed: warn ("Type D forces `synthesis-braid` preset; ignoring `--preset <id>`") and proceed.
5. Read source-map-registry.md. For each map in [map-paths]:
   - If status is `seeded` / `outlined` / `drafted` / `revised`: ask the user whether to overwrite (rare — typically means reseeding after a fresh scan). For Type D, ask per-map; cancel entire seed if any map is refused.
   - If status is `published`: refuse (essay already shipped). For Type D this is per-map — one published map blocks the whole braid (the reader will have seen that framework already; the braid loses its novelty for that axis).
   - Otherwise: proceed.

---

## Step 2 — Read the Map(s)

**Type A**: read the single map file.

**Type D**: loop over all N maps. Read each in full. Produce N parsed-section structures, indexed F1 … FN by the order the user passed them. Track each framework's source vault (may differ across frameworks — a braid commonly spans vaults).

For each map, parse into sections (best-effort — map section names vary by vault):
- Founding problem / Context / Biographical Context
- First principles / Core claims
- Core concepts (each with Depends / Enables / Constrains)
- Operational Prescriptions / Applications
- Historical Evidence / Cases
- Pressure Points / Failure Modes
- Influence / Reception / Doctrine Legacy
- Connection to Project / Judgment Instrument
- Atomic Notes (index or links)

If any map is indexical only (no prose sections — MOC-like), reject: "Map [path] is indexical — Type C (MOC position) is V2. Cannot seed from MOCs."

**Type D extraction priority**: when reading N maps, give extra weight to:
- **Core concepts with explicit `Constrains` or `Enables` clauses** — these are candidate hook-points for the braid move (where one framework's output becomes another's input).
- **Pressure Points that name a *different* framework** — these are candidate seams (the tension is already signposted in the map).
- **Connection-to-Project sections that gesture at a shared problem** — these are candidate seam descriptions.

---

## Step 2.5 — Preset Inference (V1.5 / V1.7)

Read `article-presets.md` from cogitationis root. Determine which preset governs this essay.

**Signal 0 — Type D override (V1.7)**: if `[type]=D`, force `preset: synthesis-braid`. Set `preset_source: type-forced`, `preset_inference_confidence: high`. Skip signals 1–3.

**Signal 1 — User flag (`--preset <id>`)**: if provided (and type=A), adopt as preset. Set `preset_source: user-flag`, `preset_inference_confidence: high`. Skip signals 2-3.

**Signal 2 — Thesis-candidate grammar** (Type A only; run after Step 3 so you have a thesis to match; buffer the preset determination and return here):
- "X is not Y" / "not-X but Y" / "the standard view is wrong" → `orthodoxy-counter`
- "X produces Y via Z" / "X is the mechanism of Y" / "X creates Y when Z" → `framework-build`
- "What happened at/in X" / "How X unfolded" / "X, decoded" → `case-anatomy`
- "How to read X" / "X requires Y lens" / "Seeing X clearly" → `diagnostic-lens`

**Signal 3 — Fall-back**: ambiguous grammar → `framework-build` (most neutral).

**Confidence**:
- `high` — grammar pattern matches cleanly AND source-map's problem_type is in preset's `applies_when`.
- `medium` — grammar matches but problem_type unclear or outside `applies_when`.
- `low` — grammar ambiguous OR falls back to default.

**User prompt on low confidence**: emit one line — *"Inferred preset `<id>` (confidence low). Override? [y/n]."* Wait for response. If `y`, ask for explicit preset id.

Record result for Step 8 frontmatter:
- `preset: <id>`
- `preset_source: [user-flag | inference | default]`
- `preset_inference_confidence: [high | medium | low]`

---

## Step 2.6 — Positions Lookup (V1.6 / V1.7)

Read `positions-index.md` from cogitationis root. Find substantive positions this essay should engage.

**Inputs**: the source-map (Type A) or all N source maps (Type D), already read at Step 2.

**Procedure**:

1. **Extract topic keywords**.
   - **Type A**: from the single source map. Union of:
     - Founding-problem nouns (2–5 keywords)
     - First-principle names (2–5 keywords)
     - Core-concept names (3–8 keywords)
     - Any explicit tags on the source map (`theme/...`, domain slugs)
     - Vault name of source (`kratos`, `oikos`, `belli`, `omega`, `clio`)
   - **Type D**: union the above extraction across **all N maps**, then dedupe. Also add each map's source vault to the keyword set (braids commonly cross vaults; matching T3s may sit in any of the N source vaults).
   Normalize: lowercase, singularize, strip punctuation.

2. **Grep the positions-index `Topics` column** against the keyword set. Filter: `Status == active` only. Score each row by count of distinct keyword matches.

3. **Rank and cap**: top 5 by score. Ties broken by `Registered` date (newer first).

4. **Fetch T3s**: for each of the top matches, read the referenced `Source T3` note. Extract: claim sentence, mechanism summary (first paragraph after the title), primary pressure (first entry under `Internal Tensions` if present).

5. **Classify relation to this essay's thesis** (run after Step 3 — buffer the lookup result and return here; the thesis candidate determines the relation):
   - `supports` — T3 claim reinforces the thesis-candidate; argument benefits from citing.
   - `extends` — thesis-candidate builds the T3 claim into a new domain or case.
   - `tensions-with` — T3 claim complicates, pressures, or directly conflicts with the thesis-candidate; must be engaged.
   - `orthogonal` — same topic surface, different question; mention only if naturally fits.

6. **User confirmation on >3 active matches**: if more than 3 rows survive to this step, emit a one-line summary of each and ask "Load which? (comma-sep IDs, or `none`)". Default (no response treated as) = load top 3. **Type D exception**: the cap raises to 5 matches for braids (braids cross more territory; more matched positions are likely legitimate).

7. **Empty match set** is the common case for Type A; less common for Type D (union across N maps usually hits at least one existing position). Type D with zero matches is a signal the seam is truly novel territory — flag in draft_notes.

**Output (buffered for Step 8 frontmatter)**:
```yaml
matched_positions:
  - id: P001
    relation: supports
    t3: "[[synthesis_politeia/20-Judgment/...]]"
  - id: P007
    relation: tensions-with
    t3: "[[synthesis_oeconomia/20-Judgment/...]]"
```

---

## Step 3 — Extract Thesis Candidate

**Type A** — follow the heuristic in `map-to-article-extraction.md` §"Thesis Candidate Extraction":

1. Read Pressure Points. Identify which first principle each pressure point attacks.
2. The load-bearing first principle (the one attacked most or whose failure collapses the rest) is the thesis candidate.
3. Restate as a one-sentence declarative claim. Not a summary — a claim someone could reasonably disagree with.

**Type D** — extract the seam and emergent claim:

1. **Identify the seam** — the single named tension, question, or phenomenon that connects all N frameworks. Sources of candidate seams, in priority order:
   - A core concept in one map that explicitly Constrains or Enables a concept in another.
   - A Pressure Point in one map that names (or implies) another map's framework.
   - A Founding Problem that is restated (in different vocabulary) across multiple maps.
   - A shared phenomenon the frameworks analyze from incompatible angles.
   The seam is stated as a question or a short phrase (≤12 words). Examples: "What makes a pole in the AGI era?" / "Where does structural power land when the substrate is algorithmic?" / "How does identity form under platform mediation?"

2. **Identify the emergent claim** — the one-sentence thesis that requires all N frameworks and that *none produces alone*. Form: "Together, F1 + F2 + F3 imply C, which none alone implies." The claim must survive the hard test: would any single map, deeply read, already give the reader this claim? If yes — this is not a braid, recast as Type A with references. If no — the claim is genuinely braid-dependent.

3. **Stress-test the seam at seed time** (pre-outline sanity check): write one sentence per framework that says what that framework *alone* produces about the seam. If two of those sentences are the same or subset-related, the frameworks are too close — the braid will feel redundant. Flag in seed notes.

4. **Restate the emergent claim as a declarative sentence**. Not a summary, not a meta-statement about the frameworks — a claim in the domain.

---

## Step 4 — Extract Primary Claims (Argument Moves)

**Type A** — from "Core concepts," select 3–5 concepts that support the thesis. For each:
- Sub-claim: what this concept asserts
- Mechanism: why it holds (the "Depends" block)
- Case (one): where it shows up concretely

Skip concepts that don't serve the thesis. Ordering: by dependency (foundational concepts before dependent ones).

**Type D** — per-framework extraction. For each of the N frameworks, extract 2–4 argument moves (fewer per-framework than Type A because the total budget is divided across N + braid + pressure):
- **F1 argument moves**: 2–4 sub-claims from F1's map that the braid relies on.
- **F2 argument moves**: 2–4 sub-claims from F2's map.
- **F3 (…Fn) argument moves**: same pattern.

Select each framework's moves by the criterion *"does this sub-claim participate in the emergent claim?"* — not *"is this the strongest claim in the map?"* A braid that uses F1's most famous claim but that claim is unrelated to the seam is decoration, not weave.

**Braid move** (in addition to the per-framework moves): one or two sentences describing *how* the N frameworks compose to produce the emergent claim. This is the hinge of the essay; it goes into its own slot in the seed and gets its own section in the outline. Candidate forms:
- "F1's output (X) becomes F2's input, and F2's output (Y) constrains F3's mechanism (Z) — producing C."
- "Under condition K, F1 / F2 / F3 stop being independent axes and compose toward C."
- "F1 tells you what's true *if K*; F2 tells you K is the condition we're entering; F3 tells you K is irreversible — therefore C."

---

## Step 5 — Extract Pressure Points

**Type A** — from "Pressure Points" (or vault-equivalent): pick the 1–2 strongest pressure points that attack the thesis. For each:
- Pressure: the objection or stress condition
- Case: the exploiter / failure mode (vault-specific format)

**Type D** — two flavors of pressure, both required:

1. **Per-framework pressure** — from each of the N source maps' Pressure Points, pick the 1 strongest objection that attacks *that framework's contribution to the emergent claim* (not every objection in every map; only those that would weaken the braid). This yields N items, one per framework.

2. **Seam-stress pressure** — objections that target the *connection* between frameworks, not any framework individually. Candidates:
   - *Decoupling objection*: can one framework's mechanism be switched off without the other N−1 breaking? If yes, the seam is not load-bearing.
   - *Competing composition*: does a different set of N frameworks produce the same emergent claim? If yes, this particular braid is one instance of a family, not the uniquely-supporting construction.
   - *Unit-of-analysis shift*: does the emergent claim depend on a change in the unit of analysis between frameworks that would be rejected if stated explicitly?
   - *Temporal inconsistency*: do the N frameworks operate on incompatible timescales? (A structural claim + a short-cycle claim may not actually compose.)

Seed stores both flavors; outline's pressure section will use all of them (the seam-stress flavor maps to the preset's `seam-stress` audit slot; per-framework pressures feed the `synthesis-validity` audit).

---

## Step 6 — Extract Stakes (Translate)

**Type A** — from "Connection to Project" / "Judgment Instrument" — the map says "this gives X to the project". Translate into reader-stakes: "this lets *you* read the world differently because…"

**Type D** — stakes for a braid are stakes of the *emergent claim*, not any one framework's stakes. Form: "If C is right, you'll be wrong about the domain in the following specific way, unless you read the domain through the braided frame." The stakes paragraph explicitly says *what frame the reader is probably using* (orthodoxy) and *what reading the braid gives them* (corrective). For Type D, run a brief check: does the stakes paragraph privilege any one framework over the others? If yes — rewrite.

Produce one paragraph (3–5 sentences) for the seed.

---

## Step 7 — Check Writer Positions

Read `writer-positions.md`. For each extracted thesis candidate, sub-claim, and stakes paragraph:
- Does it conflict with any non-negotiable in `writer-positions.md`?
- Does it conflict with any "Rejected Frames"?
- Does it align with or deepen "Founding Commitments"?

Record conflicts in the seed's "Conflicts with positions" section (if any). Do not silently paper over — the drafter will resolve at `/article-draft` time.

If `writer-positions.md` is unfilled (status: `awaiting-user-fill`): proceed with a warning — "positions file unfilled; drafting will proceed from neutral but cannot check alignment".

---

## Step 8 — Write the Seed

Create seed at `[vault]/10-Thoughts/YYYYMMDDHHMM - [Title].md`:

**Title generation**: derive from thesis candidate. Short (5–10 words), claim-form, not question-form.
- Good: "Form Must Be Immanent"
- Good: "Political Primacy Is Structurally Fragile"
- Bad: "Aristotle's metaphysics"
- Bad: "What Clausewitz Got Right"

**Frontmatter** (extends Thought Template):

**Type A frontmatter**:
```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [type/thought, type/article-seed, theme/<inferred from source vault>]
status: raw
article_type: A
source_vault: <vault name>
source_map: "[[<vault>/<path>/<map>.md]]"
source_refs: []
thesis_candidate: "<one sentence>"
preset: <id>  # V1.5 — from Step 2.5
preset_source: [user-flag | inference | default]
preset_inference_confidence: [high | medium | low]
matched_positions: []  # V1.6 — from Step 2.6; populated with {id, relation, t3} entries
position_conflicts: []  # list any conflicts surfaced in Step 7 (bedrock writer-positions)
---
```

**Type D frontmatter (V1.7)**:
```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [type/thought, type/article-seed, type/braid, theme/<primary theme union from N maps>]
status: raw
article_type: D
source_vaults: [kratos, oikos, belli]  # list — one per framework; may repeat if two frameworks from one vault
source_maps:
  - "[[synthesis_<vault>/theory/.../f1-map.md]]"  # F1
  - "[[synthesis_<vault>/theory/.../f2-map.md]]"  # F2
  - "[[synthesis_<vault>/theory/.../f3-map.md]]"  # F3
source_refs: []
seam: "<one sentence or question — the tension/problem binding N frameworks>"
thesis_candidate: "<one sentence — the emergent claim; form: 'Together, F1+F2+F3 imply C'>"
preset: synthesis-braid  # forced by type=D
preset_source: type-forced
preset_inference_confidence: high
matched_positions: []  # V1.6 — union across N maps
position_conflicts: []  # bedrock writer-positions conflicts, from Step 7
braid_move: "<one or two sentences — how the N frameworks compose to produce the emergent claim>"
seam_stress_checks: []  # from Step 5 flavor 2 — list of seam-stress objections to carry into outline
---
```

**Body structure**:

**Type A body**:
```markdown
# <Title>

## Thesis
<one sentence — the thesis candidate>

## Hook / Problem
<one paragraph — translated founding problem, reader-facing>

## Argument moves
1. **<move 1 sub-claim>** — mechanism: <one sentence>. Case: <one phrase>.
2. **<move 2 sub-claim>** — mechanism: <one sentence>. Case: <one phrase>.
3. **<move 3 sub-claim>** — mechanism: <one sentence>. Case: <one phrase>.
(4. ...)
(5. ...)

## Pressure points
1. **<pressure 1>** — case: <exploiter/failure>.
2. **<pressure 2>** — case: <exploiter/failure>.

## Stakes (reader-facing)
<one paragraph — what this lets the reader see or do>

## Conflicts with positions
<list any conflicts surfaced in Step 7; empty if none>

## Matched positions (V1.6)
<list matched_positions from Step 2.6 — one per line with ID, relation, and T3 link; empty if none>

## Source map
<wikilink to source map>

## Seed notes
<any additional extraction notes, open questions, decisions the drafter will face>
```

**Type D body (V1.7)**:
```markdown
# <Title>

## Emergent claim
<one sentence — the thesis candidate; form: "Together, F1 + F2 + F3 imply C, which none alone implies.">

## Seam
<one sentence or question — the named tension binding the N frameworks>

## Hook / Problem
<one paragraph — the phenomenon the braid addresses, reader-facing. Must not privilege any one framework.>

## Braid move
<one or two sentences — how the N frameworks compose to produce the emergent claim; the hinge of the essay>

## Frameworks and their moves

### F1 — <framework label, e.g., "Mearsheimer (Offensive Realism)">
- **<move 1 sub-claim>** — mechanism: <one sentence>. Case: <one phrase>.
- **<move 2 sub-claim>** — mechanism: <one sentence>. Case: <one phrase>.
- (3–4 moves total per framework)

### F2 — <framework label>
- (2–4 moves)

### F3 — <framework label>
- (2–4 moves)

(F4, F5 if present)

## Pressure (two flavors)

### Per-framework pressure (one per framework)
1. **F1 pressure**: <objection that attacks F1's contribution to the emergent claim> — case: <exploiter/failure>.
2. **F2 pressure**: ...
3. **F3 pressure**: ...

### Seam-stress pressure (attacks the connection, not any one framework)
1. **<decoupling / competing-composition / unit-shift / temporal / other>** — <objection> — test: <how to check the essay answers it>.
2. (1–3 seam-stress objections total)

## Stakes (reader-facing)
<one paragraph — what the emergent claim lets the reader see or do that they couldn't with any single framework>

## Conflicts with positions
<list any bedrock writer-positions conflicts; empty if none>

## Matched positions (V1.6)
<list matched_positions from Step 2.6 — one per line with ID, relation, and T3 link>

## Source maps
1. [[F1 map]]
2. [[F2 map]]
3. [[F3 map]]

## Seed notes
<extraction flags — e.g., "F1 and F2 produce overlapping claims about X; check outline for redundancy"; "seam candidate shifted from Y to Z at Step 3 because of ...">
```

---

## Step 9 — Update Registry

Update source-map-registry.md:
- **Type A**: for the one source map, essay status → `seeded`; essay path → the new seed file path.
- **Type D**: for each of the N source maps, essay status → `seeded (braid)`; essay path → the new seed file path (same path for all N rows, since one braid seed references all N maps). In the Notes column, annotate `braid-1-of-N` so later scans of the registry see this map is not the sole source for its seeded essay.

---

## Step 10 — Report

**Type A report**:
```
## /article-seed [map-path] A — YYYY-MM-DD

Seed created: [absolute path to new seed file]

Thesis candidate:
> <thesis>

Preset: <id> (source: <user-flag | inference | default>, confidence: <high | medium | low>)
Argument moves: <N>
Pressure points: <N>
Position conflicts: <N> (see seed body if >0)
Matched positions: <N> (IDs: <P001, P007>; relations: <supports, tensions-with>)

Registry updated.

Next step: /article-outline [seed-path]
```

**Type D report (V1.7)**:
```
## /article-seed [map-paths] D — YYYY-MM-DD

Braid seed created: [absolute path to new seed file]
Frameworks (N=<count>): F1 <label> / F2 <label> / F3 <label>

Seam:
> <seam sentence/question>

Emergent claim:
> <thesis candidate>

Braid move:
> <one/two-sentence hinge>

Preset: synthesis-braid (forced by type=D)
Per-framework argument moves: F1=<count>, F2=<count>, F3=<count>
Per-framework pressures: <N items, one per framework>
Seam-stress objections: <count>
Position conflicts: <N> (see seed body if >0)
Matched positions: <N> (union across N maps; IDs: <...>; relations: <...>)

Registry updated (N rows marked seeded-braid).

Seed sanity check:
- Braid dependency: thesis requires all N frameworks? [assertion from Step 3 stress test]
- Framework overlap: any two frameworks produce redundant claims about the seam? [flagged if Y]

Next step: /article-outline [seed-path]
```

---

## Error modes

- If source map is too thin (no pressure points, no core concepts): warn "Map has structural gaps — readiness tier was Developable. Seed will be weak; consider deepening map first."
- If source vault's map doesn't match expected section conventions: fall back to best-effort extraction and note the deviation in the seed's "Seed notes" section.
- **Type D: if seam cannot be named** (no shared phenomenon, no cross-framework Constrains/Enables, no shared founding problem): refuse. "These N frameworks do not share a seam the protocol can find — either (a) the user names the seam explicitly, (b) the framework selection is revisited, or (c) this is not a braid."
- **Type D: if the Step 3 stress test returns "any single framework already produces C"**: refuse. "The proposed emergent claim is producible by [framework N] alone — this is a Type A essay, not a braid. Re-run as /article-seed [that map] A."
- **Type D: if two frameworks produce the same claim about the seam** (Step 3.3 check): warn, do not refuse. User may proceed with awareness that F_i and F_j will need differentiation in outline.
