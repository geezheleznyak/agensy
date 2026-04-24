---
type: documentation
audience: human
---

# Article Pipeline — Expression Vault Workflow

The **expression-vault pipeline** turns argument-dense source-vault maps into published essays. It is an opinionated workflow built around one premise: *a well-structured map already contains an article's spine.* Extraction is not generation — it is **rearrangement + voice shift + vault-jargon purge + stakes translation**.

This doc is the end-to-end walkthrough. For command-by-command reference see `docs/commands.md §Article Pipeline Commands`. For companion-mode (operator writes, AI augments) see `docs/companion-mode.md`.

---

## When to use this pipeline

**Use it** when you have source-vault maps that are *Ready* (≥20/25 on `/article-scan`'s five readiness axes) and you want the vault to produce a full draft you then revise into a publishable essay.

**Don't use it** when:
- Your source maps score *Structural gap* (<12/25). Work on the map in the source vault first.
- You want to write the prose yourself. Use **companion mode** (`docs/companion-mode.md`) instead — you write, AI augments.
- The essay is a one-off with no vault substrate. The pipeline assumes an expression vault with voice-profile, writer-positions, and positions-index seeded.

---

## Prerequisites — the six substrate files

Before running any article command, your expression vault needs six substrate files. Five of them ship as scaffolds from `framework/vault-type-templates/expression/` when Genesis Protocol Phase 1 Doc 13 creates the vault:

| File | Seed state |
|---|---|
| `voice-profile.md` | Unseeded. Requires at least one corpus sample (2,000+ words of your long-form prose, or a well-described aphoristic corpus with explicit extrapolation notes). `/article-draft` refuses to run until status moves out of `unseeded`. |
| `writer-positions.md` | Section skeleton. Fill at minimum §1 Founding Commitments (3–7) and §2 Rejected Frames (3–7) before drafting. Section 5 Non-Negotiables should be strict — draft refuses to argue against these. |
| `positions-index.md` | Empty table. Grows automatically via the harvest loop at `/article-promote` Step 7. Do not edit by hand. |
| `article-presets.md` | Ships with five presets that transfer across users. Tune only if a preset doesn't fit your genre. |
| `article-design-principles.md` | Ships with P1–P10 craft principles from accumulated pilot experience. Add your own Pn entries as your pilots expose new failure modes. |
| `source-map-registry.md` | Empty per-vault tables. Populated by `/article-scan`. No manual seeding. |

Fill order: **voice-profile first** (without it, draft refuses), **writer-positions second** (without it, revision can't align), then let the pipeline auto-populate the other four during use.

---

## The pipeline (seven commands, one essay)

```
/article-scan <source-vault>           ← one-time per source vault
         ↓
/article-seed <map-path> [--preset X]  ← per essay: extract spine
         ↓
/article-outline <seed-path>           ← impose narrative arc
         ↓
/article-draft <essay-path>            ← generate prose
         ↓
/article-revise <essay-path>           ← multi-pass revision
         ↓
/article-critique <essay-path>         ← external-critic pass (soft gate)
         ↓
/article-promote <essay-path>          ← ship + harvest novel claims
```

### Stage 1 — Scan (once per source vault)

`/article-scan synthesis_<source>` walks every map in the source vault, scores each on five axes (thesis clarity, pressure points, atomic support, standalone-ness, stakes translation) totaling 0–25, and writes the readiness classification into `source-map-registry.md`. You run this once per source vault, then quarterly to pick up new maps.

**What a Ready map looks like** (≥20/25): has a crisp founding problem, 3–5 defensible first principles (one of which is attacked by a pressure point — that's the load-bearing thesis candidate), 2+ substantive pressure points, standalone-ness (a cold reader could follow), and explicit stakes translation from the source vault's project back to a general reader's concerns.

**What a Developable map looks like** (12–19/25): has some of the above but one or two sections are thin. Usually the pressure points are weak or the stakes are vault-internal.

**What a Structural gap map looks like** (<12/25): indexical, primer-only, or still under construction. Don't seed; iterate on the map in its source vault first.

### Stage 2 — Seed (per essay)

`/article-seed <map-path>` extracts the map's thesis candidate, primary claims, pressure points, and stakes into a seed note in `10-Thoughts/`. Two inputs shape the seed:

1. **Preset inference** (Step 2.5). The command reads the extracted thesis and infers which of the five presets fits:
   - `"X is not Y" / "the standard view is wrong"` → `orthodoxy-counter`
   - `"X produces Y via Z" / "X is the mechanism of Y"` → `framework-build` (default)
   - `"What happened at X" / "How X unfolded"` → `case-anatomy`
   - `"How to read X" / "X requires Y lens"` → `diagnostic-lens`
   - 3+ source maps, Type D → `synthesis-braid` (forced)

   Pass `--preset <id>` to override. Low-confidence inference prompts you to confirm.

2. **Matched positions** (Step 2.6). The command greps `positions-index.md` for topic keywords from the source map and surfaces up to 5 matching T3 positions you've earned in prior essays. Each is classified `supports` / `extends` / `tensions-with` / `orthogonal` relative to this essay's thesis. These get reserved slots in the outline.

**Output**: seed note with preset, thesis candidate, 3–5 argument moves, 1–2 pressure points, translated stakes, and a `matched_positions` frontmatter list.

### Stage 3 — Outline (impose the narrative arc)

`/article-outline <seed-path>` converts the seed into a structured outline at `20-Essays/` with `status: outline`. The preset's blueprint determines:
- **Opening type** — phenomenon-first / orthodoxy-first / case-first / reading-failure / seam-first
- **Body arc** — concept-by-concept / standard / structural-unfold / lens-components / braided
- **Pressure type** — stress-test / three-accounts / counterfactual / overreach-risks / seam-stress
- **Closing type** — diagnostic / aphoristic / lesson / reader-ready-diagnostic / emergent-claim

Each section gets word budgets summing to the universal 2,000–4,000w cap. Matched-position slots reserve argument-move space for `supports`/`extends` positions, and pressure-section space for `tensions-with` positions.

**Type D seam audit (Step 6.5)**: synthesis-braid essays run a five-test gate before advancing — framework load-bearingness, emergent claim non-derivability, seam specificity, equal weight ±20%, braid section hinge specificity. Failing any test blocks the draft until the outline is fixed.

### Stage 4 — Draft (generate prose)

`/article-draft <essay-path>` generates the full draft. It reads:
- The outline (argumentative spine)
- `voice-profile.md` (every sentence calibrated against this)
- `writer-positions.md` (non-negotiables are hard constraints; claim conflicts block generation with a surfaced conflict report)
- `positions-index.md` (matched positions as soft constraints)
- The preset's opening paragraphs, pressure required-slots, closing type

**Wikilink handling**: internal vault wikilinks are *never* included in draft output. The wikilinked concept is unpacked into prose (1–3 sentences, enough for a cold reader to follow). Citations are recorded in the essay's `source_refs` frontmatter for audit trail, not inline.

**Output**: full draft at `status: draft`, typically 2,000–4,000 words.

### Stage 5 — Revise (multi-pass adversarial revision)

`/article-revise <essay-path>` runs six passes:
- **Pass A — Thesis integrity**: does every body section advance the thesis? Does the close land it (not repeat it)?
- **Pass B — Voice match**: does every paragraph match `voice-profile.md`? Flag drift into neutral-essayistic register or vault-analytical register.
- **Pass C — Position alignment**: two-layer. Bedrock `writer-positions.md` is hard (violations refuse promotion). Matched positions from `positions-index.md` are soft (surfaced, not silently corrected).
- **Pass D — Standalone-ness**: would a cold reader follow without the source map or the vault?
- **Pass E — Preset fidelity**: does the opening match the preset's type? Are required pressure slots filled? Frame-pressure sub-pass (lightweight version of `/article-critique` C1/C6/C7) runs as tripwire.
- **Pass F — Metric realism** (for essays citing quantitative claims): are numbers verifiable and stated with appropriate uncertainty?
- **Pass G — Length cap**: if over 4,000 words, Pass G cuts until under cap before allowing advance to `status: final`.

Modes: `adversarial` (default, all passes), `creative` (looser), `light` (surface only).

**Output**: revised essay at `status: revision` with a `revision_log` entry capturing what changed and why. Expect 2–3 revise iterations before promotion.

### Stage 6 — Critique (external-critic pass, soft gate)

`/article-critique <essay-path>` catches what `/article-revise` structurally cannot see. The revise passes audit execution *within* a frame (voice match, position alignment, preset fidelity). They do not audit *the frame itself*. An essay can pass every revise pass while resting on a circular definitional move, a mis-cited theorist, an unaudited cross-scale analogy, or a concession that silently swallows its structural claim.

Eight passes:
- **C1** — Frame circularity (the load-bearing definitional move must be defended independently of the conclusion)
- **C2** — Theorist-as-stamp (cited theorists must actually endorse the argument, not just flavor it)
- **C3** — Analogy validity (cross-domain analogies must hold at the specific level the argument uses them)
- **C4** — Stratification independence (claimed-independent layers must be audited for cross-layer feedback)
- **C5** — Scenario silence (essays that predict must name the conditions under which the prediction fails)
- **C6** — Concession load (concessions can silently weaken a structural claim to a phase-dependent one)
- **C7** — Unit of analysis (same unit across the argument; don't shift levels mid-argument)
- **C8** — Title-thesis match (the title must deliver what the thesis promises)

Plus a writing-tells sub-pass for AI-generation signatures.

Modes: `full` (all 8 + writing-tells), `frame-only` (C1, C5, C6 — cheap pre-draft check), `writing-only` (C8 + writing-tells — surface polish).

**Recommended cadence**: `frame-only` at outline stage; `full` after `/article-revise` lands. `/article-revise` Step 4 Q6 checks that at least one critique has run before recommending `/article-promote`.

**Output**: critique file in `critic/` folder with C1–C8 findings. Does NOT edit the essay — you decide what to address.

### Stage 7 — Promote (ship + harvest)

`/article-promote <essay-path>` moves the essay to `40-Published/`, backlinks source maps, and updates the writing dashboard. Step 7 runs the **harvest loop**:

1. Diff essay claims against source-map atomics and matched-position T3s.
2. Classify each novel claim:
   - **Substantive framework claim** → new T3 note in the relevant source vault + new row in `positions-index.md`
   - **Methodological claim** → append to `writer-positions.md` §"Preferred Analytical Moves" or §"Recurring Dispositions"
   - **Essay-specific** → remains in the essay only; no promotion
3. User confirms each classification (accept / reject / reclassify).
4. Execute accepted promotions.

This is how the substrate grows. Each essay surfaces new claims; the harvest loop decides which deserve to become shared substrate (positions-index T3s readable by future seeds) vs. which stay essay-internal.

**Output**: published essay + source-map backlinks + dashboard update + positions-index rows + (optionally) writer-positions appends.

---

## A worked example — how a single essay flows

*Abstracted from a pilot run; specific vault names replaced with generics.*

1. **Scan**: `/article-scan synthesis_<political>` scores 27 maps. One is Ready: a systematic map of an economic-coercion theorist, scoring 29/25 (the rubric rewards exceptional clarity).

2. **Seed**: `/article-seed <political>/theory/economy/<theorist>-systematic-map.md`
   - Step 2.5 infers `preset: orthodoxy-counter` from thesis grammar ("X is not Y, it is Z")
   - Step 2.6 finds 2 matched positions from `positions-index.md`: P001 (classified `supports`) and P003 (classified `tensions-with`)
   - Output: seed note in `10-Thoughts/` with thesis, 4 argument moves, 2 pressure points, matched_positions frontmatter

3. **Outline**: `/article-outline <seed-path>`
   - Imposes orthodoxy-counter blueprint: 7-beat opening (orthodoxy-first), standard body, three-accounts pressure (required Account 3), aphoristic close
   - Reserves pressure-section slot for P003 (tensions-with)
   - Reserves one argument move for P001 (supports)
   - Outline at `status: outline`, ~3,200w budgeted

4. **Draft**: `/article-draft <essay-path>`
   - Voice calibrated against voice-profile (sentence-length distribution, stance markers, cadence rules)
   - Every wikilink unpacked into prose
   - Source references recorded in `source_refs` frontmatter
   - Draft at `status: draft`, 3,450w

5. **Revise (iteration 1)**: `/article-revise adversarial`
   - Pass B flags 6 sentences drifting to neutral-essayistic register
   - Pass C flags 1 soft-constraint violation against P003 (surfaced, not fixed)
   - Pass E flags missing Account 3 in the pressure section (load-bearing — mandatory revision)
   - After edits: `status: revision`, 3,200w

6. **Critique**: `/article-critique full`
   - C2 flags borrowed authority (a cited figure who wouldn't endorse the specific argument)
   - C6 flags a concession that silently weakens the structural claim
   - You decide: drop the name (C2 fix), re-state thesis at weaker register (C6 fix)

7. **Revise (iteration 2)**: address critique flags
   - Re-run `/article-critique frame-only` to verify C6 is resolved

8. **Promote**: `/article-promote <essay-path>`
   - Moves to `40-Published/`
   - Step 7 harvest surfaces 3 novel claims: 1 substantive → new T3 + positions-index row P004; 1 methodological → writer-positions append; 1 essay-specific → no promotion
   - You confirm each. Published.

Typical pipeline time: one session for scan + seed + outline; one session for draft + first revise; one session for critique + second revise + promote. Two to three working sessions per essay.

---

## When the pipeline fights you

**Draft refuses to run**: `voice-profile.md` is `status: unseeded`. Fill at least the default-register section and sample-inventory before retrying.

**Draft won't produce the thesis you wanted**: writer-positions has a non-negotiable that blocks it. Either (a) revise the thesis to sit within your bedrock, or (b) revise your bedrock — the rejection is telling you the thesis isn't actually yours.

**Revise keeps failing Pass E preset-fidelity**: the outline's preset might not fit the essay. Re-run `/article-seed --preset <other>` to try a different blueprint.

**Critique C1 keeps failing**: your thesis is doing definitional work the argument can't independently defend. This is usually a thesis problem, not a prose problem. Re-outline with a different load-bearing term.

**Revise Pass G can't get you under 4,000w**: usually means the essay is actually two essays. Split.

**Harvest loop surfaces nothing novel**: the essay didn't advance beyond the source map. Either the map was too prescriptive or the essay didn't find its own contribution. Both are honest signals — the pipeline surfaced them.

---

## See Also

- `docs/commands.md §Article Pipeline Commands` — one-paragraph reference per command
- `docs/companion-mode.md` — when you want to write the prose yourself
- `framework/templates/map-to-article-extraction.md` — the deterministic map-section → article-role extraction recipe
- `framework/vault-type-templates/expression/README.md` — substrate file roles and fill-in order
