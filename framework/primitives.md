---
type: reference
schema_version: 0.1
audience: claude
---

# Primitives — The Vocabulary of the Vault System Model

This is the canonical reference for the three-layer primitive vocabulary used by every `[vault]/system-model.yaml`. The vocabulary was empirically validated in a Phase 0 experiment by decomposing three mechanism-rich notes from three vaults (oeconomia, bellum, politeia) and confirming ≥80% shared use without loss of meaning.

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
- **oeconomia**: `lenders`, `fund_managers`, `central_banks`
- **bellum**: `friendly_commander`, `adversary_commander`
- **politeia**: `rising_power`, `dominant_power`, `domestic_coalitions`

### `states`
Conditions persisting until changed (stocks). A state has a level that can rise or fall.
- **oeconomia**: `leverage_ratio`, `asset_prices`, `financing_regime`
- **bellum**: `friendly_mental_model`, `environment`
- **politeia**: `relative_power_position`, `credibility_rigidity`, `anxiety_level`

### `flows`
Rates of change of states. A flow is the derivative of a stock.
- **oeconomia**: `credit_extension_rate`, `leverage_accumulation_rate`
- **bellum**: `friendly_cycle_completion_rate`, `adversary_cycle_completion_rate`
- **politeia**: `growth_trajectory`, `commitment_accumulation_rate`

### `signals`
Information carrying content between agents/states. A signal is *about* something else.
- **oeconomia**: `risk_model_outputs`, `credit_ratings`, `observed_defaults`
- **bellum**: `sensor_data`, `orienting_interpretations`
- **politeia**: `stated_intentions`, `forward_deployments`, `red_lines`

### `constraints`
Boundaries that foreclose possibilities. A constraint rules *out*, not *in*.
- **oeconomia**: `career_risk`, `Basel_II_capital_rules`, `political_economy_of_tightening`
- **bellum**: `cognitive_capacity`, `LOAC`, `human_in_the_loop_requirement`
- **politeia**: `anarchy`, `asymmetric_time_preference`, `nuclear_deterrence`

### `structures`
Persistent configurations of roles and relations. A structure is durable enough that it is the *background* against which action happens, not the action itself.
- **oeconomia**: `money_manager_capitalism`, `three_stage_financing_regime`
- **bellum**: `two_coupled_OODA_loops`
- **politeia**: `international_anarchic_system`, `alliance_network`, `credibility_architecture`

---

## Layer 2 — Edges (5 core + 5 reserve)

Edges are typed, directed relations between two nodes. `from` is the source; `to` is the target. An edge without a type is not an edge — direction plus type defines the relation.

### Core set (empirically dominant in Phase 0)

**`produces`** — `from` generates or causes `to`.
- oeconomia: `higher_leverage` produces `higher_asset_prices`
- bellum: `adversary_action` produces `friendly_observation`
- politeia: `rising_power_growth` produces `dominant_power_fear`

**`reinforces`** — `from` amplifies or stabilizes `to`. Differs from `produces` in that `to` already exists; `from` intensifies it.
- oeconomia: `observed_stability` reinforces `downward_revision_of_risk`
- bellum: `obsolete_model` reinforces `adversary_confusion`
- politeia: `each_new_commitment` reinforces `credibility_rigidity`

**`dampens`** — `from` suppresses or reduces `to`.
- oeconomia: `central_bank_intervention` dampens `bust_phase`
- bellum: `deception` dampens `adversary_orientation_quality`
- politeia: `cultural_similarity` dampens `spiral_intensity`

**`gates`** — `from` is a threshold or condition that enables or blocks `to`. Gates are binary or step-function.
- oeconomia: `competitive_pressure` gates `individual_exit_option`
- bellum: `AI_enabled_cycle` gates `human_participation`
- politeia: `commitment_rigidity` gates `ability_to_back_down`

**`couples`** — `from` makes `to` dependent on a third element. Coupling creates shared fate.
- bellum: `two_OODA_loops` couples `friendly_cycle_state` to `adversary_cycle_state`
- politeia: `alliance_commitments` couple `great_power_decisions` to `local_ally_triggers`

### Reserve set (plausible; retained for broader corpus)

- **`consumes`** — `from` depletes or transforms `to`. (Rare in Phase 0; likely common in energy/resource vaults.)
- **`reveals`** — `from` makes `to` observable. (bellum signaling; oeconomia risk revelation.)
- **`conceals`** — `from` hides or obfuscates `to`. (bellum deception; politeia strategic ambiguity.)
- **`requires`** — `from` depends on `to` for its operation. (politeia credibility requires commitments.)
- **`opposes`** — `from` and `to` are in structural antagonism. (politeia rising power opposes dominant power interests.)

`realizes` and `acts-on` from Shannon's original list are dropped: the first is too abstract, the second subsumed by `produces`.

---

## Layer 3 — Patterns (7 types)

A pattern is a recurring *shape* of mechanism, instantiated by a subgraph of nodes and edges. Patterns are the load-bearing layer for cross-vault composition: the same pattern type in two vaults, with different local nodes, is the coupling unit.

### `positive_feedback`
Self-amplifying loop — output reinforces input.
- **oeconomia**: stability → downward risk revision → looser credit → higher leverage → higher asset prices → improved creditworthiness → (back to stability signal).
- **bellum**: each side's actions become the other side's observations → each cycle feeds the next → tempo differential amplifies.
- **politeia**: growth → fear → commitments → rigidity → trigger-vulnerability → more fear.

### `negative_feedback`
Self-limiting loop — output dampens input.
- Not explicit in the three Phase 0 notes, but standard in control-theoretic mechanisms (e.g., balance-of-power restoration in politeia, price equilibration in oeconomia, logistic constraint in bellum). Retain.

### `threshold`
Sudden qualitative transition at a critical value.
- **oeconomia**: Minsky Moment — the accumulated Ponzi structure crosses a threshold at which arrest of asset-price appreciation triggers cascade failure.
- **bellum**: OODA mismatch threshold — the tempo differential crosses a point at which adversary cohesion collapses, not merely degrades.
- **politeia**: parity as danger zone — power transition crosses the value at which preventive-war logic becomes dominant.

### `reflexivity`
System's model of itself affects the system.
- **oeconomia**: risk models calibrated on stability rate the stability-induced fragility as safe, which produces more of it.
- **bellum**: each commander's model of the other shapes their actions, which shape the other's observations, which shape the other's model.
- **politeia**: signals of resolve partially create the reality they aim to deter (dominant power's deterrent posture reinforces rising power's perception of threat).

### `selection`
Differential persistence of competing units.
- **bellum**: faster-cycling OODA side wins; slower-cycling side is selected out.
- Common in evolutionary / market / institutional contexts. Appears in oeconomia (firms with hedge financing survive shake-outs that kill Ponzi-financed firms) and politeia (regimes with adaptive coalition management persist; rigid coalitions collapse).

### `accumulation`
Stock grows without a balancing release.
- **oeconomia**: Ponzi structures accumulate during boom; no mechanism releases them until the Minsky Moment.
- **politeia**: commitment network accumulates; each new commitment is path-dependent.
- **bellum**: in prolonged campaigns, cognitive load and decision fatigue accumulate without structural release mechanisms.

### `path_dependence`
History constrains present options.
- **oeconomia**: central bank interventions preserve Ponzi structures that then constrain future intervention options (each bailout sets the floor for the next).
- **politeia**: commitment to small allies constrains great-power strategic flexibility (Alliance Entrapment).
- **bellum**: doctrine written for prior wars shapes (and constrains) adaptation to current war.

---

## How to Use This Reference

When building a vault's `system-model.yaml`:

1. **Start with agents and structures** — these are the anchors. List them first.
2. **Identify states that matter** — what has a level that rises or falls in your mechanism? These are nodes, not claims about nodes.
3. **Add flows for states whose *rate* of change is part of the mechanism** — not every state needs a flow; only those where the tempo matters.
4. **List signals separately from the things they are about** — price is a state; observed price is a signal. The distinction is load-bearing.
5. **Constraints rule *out*, not in** — if your "constraint" produces something, it is a state or a structure, not a constraint.
6. **Connect with the core edges first** — produces, reinforces, dampens, gates, couples. Most mechanisms need nothing else.
7. **Patterns are identified, not invented** — if your subgraph does not clearly instantiate one of the 7 types, you may have a mechanism that is not yet dynamical (still at the claim level) or the pattern set is missing a category (flag for v0.2, do not improvise).

---

## Pattern-Name Warning

Patterns sharing a name across vaults (e.g., `reflexivity` in oeconomia Soros-style and bellum OODA-style) may encode mechanically different dynamics. This is a live risk for cross-vault bindings.

**Rule**: A `cross_vault_bindings` entry that pairs two pattern instances by name only is a *hypothesis*, not a fact. The hypothesis is tested at Phase 4 closure — does a cross-vault query over the shared pattern type return a meaningful answer, or a noise aggregate? Until that test passes, bindings that cross pattern types should be marked as provisional.

---

## See Also

- `framework/system-model-schema.yaml` — the canonical YAML schema.
- `framework/system-model-architecture.md` — design rationale and relationship to other framework layers.
- `framework/universal-commands/system-query.md` — how to query a system model.
- `framework/universal-commands/system-audit.md` — how to audit a system model for drift.
