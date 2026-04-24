---
type: reference
audience: claude
schema_version: 0.2
---

# Primitives — The Vocabulary of the Vault System Model

This is the canonical reference for the three-layer primitive vocabulary used by every `[vault]/system-model.yaml`. The vocabulary was empirically validated in Phase 0 (see `primitives-experiment.md`) by decomposing three mechanism-rich notes from three vaults (oikos, belli, kratos) and confirming ≥80% shared use without loss of meaning.

**The three layers**:

1. **Nodes (roles)** — what *kinds* of thing populate a mechanism.
2. **Edges (relations)** — how those things *act on* each other.
3. **Patterns** — the recurring *shapes* a mechanism instantiates.

Every vault-level system model is built by identifying nodes, connecting them with typed edges, and flagging the dynamical patterns their subgraphs instantiate.

---

## Layer 1 — Nodes (6 categories)

Each node belongs to exactly one category. A node is *never* a claim or a full explanation — it is a *thing in a model*.

### `agents`
Loci of decision/action with interests.
- **oikos**: `lenders`, `fund_managers`, `central_banks`
- **belli**: `friendly_commander`, `adversary_commander`
- **kratos**: `rising_power`, `dominant_power`, `domestic_coalitions`

### `states`
Conditions persisting until changed (stocks). A state has a level that can rise or fall.
- **oikos**: `leverage_ratio`, `asset_prices`, `financing_regime`
- **belli**: `friendly_mental_model`, `environment`
- **kratos**: `relative_power_position`, `credibility_rigidity`, `anxiety_level`

### `flows`
Rates of change of states. A flow is the derivative of a stock.
- **oikos**: `credit_extension_rate`, `leverage_accumulation_rate`
- **belli**: `friendly_cycle_completion_rate`, `adversary_cycle_completion_rate`
- **kratos**: `growth_trajectory`, `commitment_accumulation_rate`

### `signals`
Information carrying content between agents/states. A signal is *about* something else.
- **oikos**: `risk_model_outputs`, `credit_ratings`, `observed_defaults`
- **belli**: `sensor_data`, `orienting_interpretations`
- **kratos**: `stated_intentions`, `forward_deployments`, `red_lines`

### `constraints`
Boundaries that foreclose possibilities. A constraint rules *out*, not *in*.
- **oikos**: `career_risk`, `Basel_II_capital_rules`, `political_economy_of_tightening`
- **belli**: `cognitive_capacity`, `LOAC`, `human_in_the_loop_requirement`
- **kratos**: `anarchy`, `asymmetric_time_preference`, `nuclear_deterrence`

### `structures`
Persistent configurations of roles and relations. A structure is durable enough that it is the *background* against which action happens, not the action itself.
- **oikos**: `money_manager_capitalism`, `three_stage_financing_regime`
- **belli**: `two_coupled_OODA_loops`
- **kratos**: `international_anarchic_system`, `alliance_network`, `credibility_architecture`

---

## Layer 2 — Edges (5 core + 5 reserve)

Edges are typed, directed relations between two nodes. `from` is the source; `to` is the target. An edge without a type is not an edge — direction plus type defines the relation.

### Core set (empirically dominant in Phase 0)

**`produces`** — `from` generates or causes `to`.
- oikos: `higher_leverage` produces `higher_asset_prices`
- belli: `adversary_action` produces `friendly_observation`
- kratos: `rising_power_growth` produces `dominant_power_fear`

**`reinforces`** — `from` amplifies or stabilizes `to`. Differs from `produces` in that `to` already exists; `from` intensifies it.
- oikos: `observed_stability` reinforces `downward_revision_of_risk`
- belli: `obsolete_model` reinforces `adversary_confusion`
- kratos: `each_new_commitment` reinforces `credibility_rigidity`

**`dampens`** — `from` suppresses or reduces `to`.
- oikos: `central_bank_intervention` dampens `bust_phase`
- belli: `deception` dampens `adversary_orientation_quality`
- kratos: `cultural_similarity` dampens `spiral_intensity`

**`gates`** — `from` is a threshold or condition that enables or blocks `to`. Gates are binary or step-function.
- oikos: `competitive_pressure` gates `individual_exit_option`
- belli: `AI_enabled_cycle` gates `human_participation`
- kratos: `commitment_rigidity` gates `ability_to_back_down`

**`couples`** — `from` makes `to` dependent on a third element. Coupling creates shared fate.
- belli: `two_OODA_loops` couples `friendly_cycle_state` to `adversary_cycle_state`
- kratos: `alliance_commitments` couple `great_power_decisions` to `local_ally_triggers`

### Reserve set (plausible; retained for broader corpus)

- **`consumes`** — `from` depletes or transforms `to`. (Rare in Phase 0; likely common in energy/resource vaults.)
- **`reveals`** — `from` makes `to` observable. (belli signaling; oikos risk revelation.)
- **`conceals`** — `from` hides or obfuscates `to`. (belli deception; kratos strategic ambiguity.)
- **`requires`** — `from` depends on `to` for its operation. (kratos credibility requires commitments.)
- **`opposes`** — `from` and `to` are in structural antagonism. (kratos rising power opposes dominant power interests.)

`realizes` and `acts-on` from Shannon's original list are dropped: the first is too abstract, the second subsumed by `produces`.

---

## Layer 3 — Patterns (7 types)

A pattern is a recurring *shape* of mechanism, instantiated by a subgraph of nodes and edges. Patterns are the load-bearing layer for cross-vault composition: the same pattern type in two vaults, with different local nodes, is the coupling unit.

### `positive_feedback`
Self-amplifying loop — output reinforces input.
- **oikos**: stability → downward risk revision → looser credit → higher leverage → higher asset prices → improved creditworthiness → (back to stability signal).
- **belli**: each side's actions become the other side's observations → each cycle feeds the next → tempo differential amplifies.
- **kratos**: growth → fear → commitments → rigidity → trigger-vulnerability → more fear.

### `negative_feedback`
Self-limiting loop — output dampens input.
- Not explicit in the three Phase 0 notes, but standard in control-theoretic mechanisms (e.g., balance-of-power restoration in kratos, price equilibration in oikos, logistic constraint in belli). Retain.

### `threshold`
Sudden qualitative transition at a critical value.
- **oikos**: Minsky Moment — the accumulated Ponzi structure crosses a threshold at which arrest of asset-price appreciation triggers cascade failure.
- **belli**: OODA mismatch threshold — the tempo differential crosses a point at which adversary cohesion collapses, not merely degrades.
- **kratos**: parity as danger zone — power transition crosses the value at which preventive-war logic becomes dominant.

### `reflexivity`
System's model of itself affects the system.
- **oikos**: risk models calibrated on stability rate the stability-induced fragility as safe, which produces more of it.
- **belli**: each commander's model of the other shapes their actions, which shape the other's observations, which shape the other's model.
- **kratos**: signals of resolve partially create the reality they aim to deter (dominant power's deterrent posture reinforces rising power's perception of threat).

### `selection`
Differential persistence of competing units.
- **belli**: faster-cycling OODA side wins; slower-cycling side is selected out.
- Common in evolutionary / market / institutional contexts. Appears in oikos (firms with hedge financing survive shake-outs that kill Ponzi-financed firms) and kratos (regimes with adaptive coalition management persist; rigid coalitions collapse).

### `accumulation`
Stock grows without a balancing release.
- **oikos**: Ponzi structures accumulate during boom; no mechanism releases them until the Minsky Moment.
- **kratos**: commitment network accumulates; each new commitment is path-dependent.
- **belli**: in prolonged campaigns, cognitive load and decision fatigue accumulate without structural release mechanisms.

### `path_dependence`
History constrains present options.
- **oikos**: central bank interventions preserve Ponzi structures that then constrain future intervention options (each bailout sets the floor for the next).
- **kratos**: commitment to small allies constrains great-power strategic flexibility (Alliance Entrapment).
- **belli**: doctrine written for prior wars shapes (and constrains) adaptation to current war.

---

## Layer 3b — Pattern Timescale (v0.2)

A pattern's mechanism only composes cleanly across vaults if the timescale matches. A seconds-scale reflexivity (OODA-loop deception) and a decades-scale reflexivity (institutional entrapment) share a mechanism *form* but not a mechanism *tempo* — treating them as the same in a query makes the query degenerate.

Six coarse bands, assigned via optional `timescale:` field on patterns (and on flow-nodes where the rate is load-bearing):

- **`seconds-to-minutes`** — combat tempo, conversational signaling, micro-market price formation.
- **`hours-to-days`** — operational tempo, news cycles, short-run market reactions.
- **`weeks-to-months`** — campaign horizons, business cycles, policy-response cycles.
- **`years`** — electoral cycles, regime consolidation, technology adoption S-curves.
- **`decades+`** — institutional lock-in, demographic transition, civilizational shifts.
- **`mixed`** — genuinely spans multiple bands; use sparingly, and only when the mechanism operates across bands rather than having a single dominant scale.

**Assignment rule**: pick the slowest band over which the mechanism's *full loop* closes. A positive-feedback mechanism whose incremental steps are fast but whose closure requires years should be `years`.

Timescale is optional. An unannotated pattern is queryable across all bands; an annotated pattern is filterable by band. Annotate when cross-vault comparison risks category errors.

---

## Layer 3c — Pattern Subtypes (v0.2, emergent)

Some pattern types conflate mechanistically distinct variants. The schema's `subtype:` field (free string, no enum) lets a vault model differentiate without committing to a fixed taxonomy.

Observed subtypes from Phase 2–4 corpus (not authoritative — use when they fit; coin new ones when they don't):

### `reflexivity` subtypes
- **`target-erosion`** — action aimed at an object erodes the property that motivated the action. Examples: Hirschman boomerang (weaponizing dependence erodes dependence); Goodhart / policy_target_erosion (targeting a measure destroys its indicator value).
- **`narrative-fact-cycle`** — belief alters behavior alters facts alters belief. Soros's original formulation. Examples: narrative_reflexivity_cycle (oikos).
- **`orientation-constitution`** — the orientation that would detect/correct the pattern is itself constituted by the pattern. Examples: deception_reflexivity (adversary's OODA produces the success of the deception); mission_command_reflexivity (commander's intent shapes what staff report as significant).
- **`structural-entrapment`** — awareness of the pattern cannot translate to individual action because structural position converts awareness into collective inaction. Example: institutional_entrapment (oikos late-cycle career risk).

### `threshold` subtypes (candidate — less developed)
- **`cascade-trigger`** — small marginal change crosses a tipping point releasing accumulated stock.
- **`phase-transition`** — qualitative regime shift (legitimacy collapse, market regime change).

### `positive_feedback` subtypes (candidate)
- **`runaway`** — unbounded amplification until external limit hits.
- **`bounded-amplification`** — amplifies within a structural envelope (e.g., negative_feedback-stabilized positive loop).

**Rule**: Add subtypes when a vault has ≥2 patterns of the same type whose mechanisms diverge meaningfully. Do not add subtypes to single-instance patterns — there is no differentiation pressure yet.

---

## Layer 3d — Boundary Cases (v0.2)

Some pattern pairs have genuinely fuzzy borders. The schema's `secondary_types:` array lets one pattern instance carry two pattern_types when both mechanisms are present in the same subgraph.

### `accumulation` vs. `path_dependence` (the prototypical fuzzy pair)

- **`accumulation`** — a *stock* grows monotonically with no balancing release. Primary claim: about a *quantity*.
- **`path_dependence`** — past *choices* narrow the future *option space*. Primary claim: about branching.

**Clean cases**:
- Pure accumulation: behavioral data accumulates under Zuboff surveillance capitalism — the stock grows; the option space doesn't obviously branch.
- Pure path dependence: QWERTY keyboard layout — no stock grows, but the early choice forecloses alternatives.

**Dual cases** (use `type:` + `secondary_types:` together):
- `capital_accumulation` with lock-in — capital stock grows (accumulation) AND foreclosures of competitive branches accrue as scale economies compound (path_dependence). Primary: `accumulation`; secondary: `[path_dependence]`.
- `commitment_network` growth — commitments pile up (accumulation) AND each commitment narrows future diplomatic options (path_dependence). Primary: whichever mechanism the vault's mechanism-of-interest foregrounds.

**Assignment discipline**: a `secondary_types` tag must be justified by the *same subgraph*. If the accumulation mechanism lives in edges A+B and the path-dependence mechanism lives in edges C+D, these are two distinct patterns — split them, don't dual-tag.

### `positive_feedback` vs. `reflexivity`

- Positive feedback: output reinforces input. Observable from outside the loop.
- Reflexivity: the system's *model of itself* alters the system. Requires that the loop pass through a signal carrying content *about* the system.

A positive-feedback loop without a model-passing-through-signals step is not reflexivity. If in doubt: trace whether any edge in the subgraph is a signal whose content is about a state in the subgraph. If yes, it is (also) reflexivity.

### `selection` vs. `path_dependence`

- Selection: *differential* persistence of competing units. There is a population.
- Path dependence: *one* trajectory foreclosing alternatives. No population required.

Selection pressures that lock in one winner convert into path dependence. The instance is `selection` while variants compete, `path_dependence` once the winner is fixed — and can be both if the vault's analysis spans the transition.

---

## How to Use This Reference

When building a vault's `system-model.yaml`:

1. **Start with agents and structures** — these are the anchors. List them first.
2. **Identify states that matter** — what has a level that rises or falls in your mechanism? These are nodes, not claims about nodes.
3. **Add flows for states whose *rate* of change is part of the mechanism** — not every state needs a flow; only those where the tempo matters.
4. **List signals separately from the things they are about** — price is a state; observed price is a signal. The distinction is load-bearing.
5. **Constraints rule *out*, not in** — if your "constraint" produces something, it is a state or a structure, not a constraint.
6. **Connect with the core edges first** — produces, reinforces, dampens, gates, couples. Most mechanisms need nothing else.
7. **Patterns are identified, not invented** — if your subgraph does not clearly instantiate one of the 7 types, you may have a mechanism that is not yet dynamical (still at the claim level) or the pattern set is missing a category (flag for v0.3, do not improvise).
8. **Annotate timescale when cross-vault composition matters** — the `timescale:` band (v0.2) is what keeps fast reflexivities and slow reflexivities from colliding in a shared query.
9. **Subtype reflexivities (and high-duplication pattern types) when ≥2 instances diverge mechanically** — free-string, emergent. See the observed taxonomy in Layer 3c.
10. **Dual-tag accumulation/path_dependence boundary cases** — use `secondary_types:` sparingly, only when both mechanisms genuinely live in the same subgraph (Layer 3d).

---

## Pattern-Name Warning

Patterns sharing a name across vaults (e.g., `reflexivity` in oikos Soros-style and belli OODA-style) may encode mechanically different dynamics. This was flagged in Phase 0, validated through Phase 4 closure (six reflexivities, all passing the observer-effect mechanism test), and partially mitigated in v0.2 by the `subtype` and `timescale` fields.

**Rule (updated for v0.2)**: A `cross_vault_bindings` entry that pairs two pattern instances by *type* alone is a coarse hypothesis. Tightening it:
- Matching `type` + matching `subtype` (where subtypes exist) = strong pairing.
- Matching `type` + different `subtype` = weak pairing, flagged informationally by `/system-audit` Step 5b.
- Different `type` across `paired_with` entries = binding is suspect; `/system-audit` flags as `⚠️ binding type-mismatch`.
- Matching `type` + divergent `timescale` bands = pairing is real at the mechanism level but degenerate at the application level — query results should preserve the timescale distinction.

---

## See Also

- `framework/system-model-schema.yaml` — the canonical YAML schema.
- `framework/system-model-architecture.md` — design rationale and relationship to other framework layers.
- `framework/primitives-experiment.md` — the Phase 0 experiment that produced this vocabulary.
- `framework/universal-commands/system-query.md` — how to query a system model.
- `framework/universal-commands/system-audit.md` — how to audit a system model for drift.
