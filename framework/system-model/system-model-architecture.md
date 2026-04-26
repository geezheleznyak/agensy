---
type: architecture
audience: claude
schema_version: 0.2
---

# Vault System Model Layer — Architecture

The System Model Layer is a machine-readable per-vault description of each vault's domain as nodes (roles), edges (relations), and patterns (dynamical shapes), plus bindings to peer vaults via the bridge concept. It sits below slash commands and MOCs, above note content, and references — but does not duplicate — vault-config and cross-vault-bridges.

## Why This Layer Exists

The existing framework stack maps ideas at three scales:

| Layer | Scale | Content |
|---|---|---|
| MOCs | Topical | Domain hubs — what topics exist |
| Theorist/concept maps | Thinker | A single thinker's or concept's internal logic |
| `cross-vault-bridges.md` | Conceptual overlap | Where two vault domains overlap; does not describe either vault's ontology |
| Note frontmatter | Per-note | domain · engagement-axis position · open_problems |

None of these answers the question: *what is the structural shape of this vault's domain?*  Which actors, states, constraints constitute the mechanism? Which dynamical patterns recur? Where is the feedback? A human reader answers these implicitly by reading the notes. An agent cannot.

The System Model Layer answers that question in one file per vault, so an agent can query the vault structurally without reading every note.

## What It Solves

Four user-requested capabilities drive the design:

1. **Structural overview** — one YAML + Mermaid pair gives the shape of the domain.
2. **Gap-finding beyond topic coverage** — `/system-audit` surfaces nodes with no linked notes, notes not referenced by any node, and drift against vault-config.
3. **Agent-mediated cross-vault consultation** — an agent working on an arc in vault A can query vault B's system model and find *structurally* matching nodes/patterns without knowing the vocabulary of vault B.
4. **Cross-vault bridge generation** — `/system-bridge` (Phase 3) enumerates shared pattern instances across vaults, surfacing bindings not yet captured in `cross-vault-bridges.md`.

## Three-Layer Vocabulary

Frozen from the Phase 0 experiment (`primitives-experiment.md`, 2026-04-20). Extended v0.2 based on Phase 2 and Phase 4 closure evidence (2026-04-24). Full reference: `primitives.md`.

- **Nodes (6 categories)**: agents · states · flows · signals · constraints · structures
- **Edges (5 core + 5 reserve)**: produces · reinforces · dampens · gates · couples [core]; consumes · reveals · conceals · requires · opposes [reserve]
- **Patterns (7 types)**: positive_feedback · negative_feedback · threshold · reflexivity · selection · accumulation · path_dependence
- **Pattern annotations (v0.2, optional)**: `timescale` (six bands) · `subtype` (emergent free-string) · `secondary_types` (dual-mechanism array)

Cross-vault bindings are enabled by the patterns layer: the same pattern type instantiated in two vaults with different local nodes is the coupling unit. Names matching does not guarantee mechanical compatibility — that was tested at Phase 4 closure and passed for `reflexivity` across six instances. v0.2 tightens the matching criterion by adding `subtype` and `timescale` so a binding can assert not only "same pattern type" but "same pattern subtype at the same timescale."

## What the System Model Is NOT

Reuse constraints — avoid duplicating content that already lives elsewhere.

| Layer | Relationship | Rule |
|---|---|---|
| `vault-config.md` | References | Node `domain` and `engagement_positions` must resolve to vault-config values. Does not restate mission or driving questions. |
| `cross-vault-bridges.md` | References | `cross_vault_bindings[].bridge_id` must exist in bridges file. Does not restate bridge descriptions. |
| Theorist maps | Complementary | Theorist maps index a single thinker's logic. System model indexes the domain's structural ontology. A theorist's map may point at nodes; a node may list `theorists` as a back-reference. Neither replaces the other. |
| MOCs | Complementary | MOCs list topics, not structural ontology. A MOC may reference the system-map Mermaid diagram; the Mermaid diagram may group nodes by MOC topic. Neither replaces the other. |
| Note frontmatter | Linked | Every node carries `linked_notes: [...]`. Notes do not carry a `system_model_node:` back-reference in v0.1 (that is auto-regeneration work, deferred to v2). |

**v0.1 is hand-curated.** Per-vault `system-model.yaml` is written and maintained manually. Auto-regeneration from note frontmatter is v2 work — only after v0.1 has proven its value in Phases 2–4.

## File Layout

**In agensy (framework, not per-vault)**:

```
framework/
  system-model-schema.yaml              canonical schema, vocabulary locked
  system-model-architecture.md          this file
  primitives.md                         human-readable vocabulary reference
  primitives-experiment.md              Phase 0 gate decision (historical record)
  universal-commands/
    system-query.md                     read-only query protocol
    system-audit.md                     reconciliation protocol
    system-build.md                     interactive editor (Phase 3)
    system-bridge.md                    cross-vault binding diff (Phase 3)
```

**In each piloted vault (Phase 2 onward)**:

```
[vault-root]/
  system-model.yaml                     per-vault, extends the schema
  30-MOCs/system-map.md                 Mermaid diagram, hand-maintained v1
  .claude/commands/
    system-query.md                     3-line stub pointing at universal protocol
    system-audit.md                     3-line stub
    system-build.md                     3-line stub (Phase 3)
    system-bridge.md                    3-line stub (Phase 3)
```

## Integration Points

- **Command lifecycle** (`framework/protocols/command-lifecycle.md`): `/system-audit` fires at the same cadence as `/coverage-audit` (milestone trigger, every N notes or on phase completion).
- **System state** (`[AGENSY_PATH]/system-state.md`): Vault Registry gains a `System Model` column tracking per-vault status; a separate **System Model Freshness** table tracks drift (last_audit / dirt_level / outstanding_issues).
- **Genesis protocol** (`framework/protocols/genesis-protocol.md`): new vaults created post-v0.1 optionally bootstrap an empty `system-model.yaml` in Doc 12; population deferred to an explicit `/system-build` session.
- **Coverage-audit** (`framework/universal-commands/coverage-audit.md`): if a vault has a `system-model.yaml`, `/coverage-audit` Step 9 **mandatorily** invokes `/system-audit` as chained protocol and writes its summary line to `memory/session-state.md`. This is the primary staleness prevention mechanism.

## Self-Maintenance Policy

The System Model Layer is a curated human-written artifact, not a live index. Without explicit maintenance, the YAML drifts from the note corpus as new T3 notes are written, nodes are renamed, edges added, and vault-configs change.

**Three layers of staleness prevention**:

### Layer 1 — Automatic at `/coverage-audit` (primary)

`/coverage-audit` Step 9 (mandatory if `system-model.yaml` exists) fires `/system-audit` as a chained protocol. Because `/coverage-audit` is itself fired at milestone events (every ~10 new notes, phase completion, etc.), the system model is audited at the same natural cadence as the rest of the vault.

`/system-audit` Step 9 computes a **dirt level** and updates the **System Model Freshness** table in `system-state.md`:

| Level | Criterion | Response |
|---|---|---|
| 🟢 green | All issue counts ≤ 1 AND no broken linked_notes AND no binding type-mismatch | Informational — no action |
| 🟡 yellow | Any issue count 2–5 | Schedule audit within the next few notes; `/system-build` nudges surface at `/arc` |
| 🔴 red | Any issue count > 5 OR ≥ 1 broken linked_notes OR ≥ 1 binding type-mismatch | Top 3 drift items surface in the audit report as REMEDIATION RECOMMENDED; coverage-audit pulls them into its Step 5 gap list |

### Layer 2 — On-demand at `/system-audit` (manual)

The user can run `/system-audit` directly at any time. Same dirt-level output + freshness-table update. Useful before `/arc` or `/dialogue` in vaults where the last `/coverage-audit` was a while ago.

### Layer 3 — Auto-regeneration (deferred to v2)

Full auto-sync from note frontmatter is v2 work — reserved until v0.2 has demonstrated that hand-curated models survive their own hand-curation cost. Not on the current roadmap.

### What this does NOT prevent

- **Novel patterns emerging in notes but not yet encoded**: the audit flags unreferenced notes but does not guess the pattern. The user must run `/system-build` to encode.
- **Stale understanding when `vault-config.md` changes**: the audit catches orphaned `domain` or `engagement_positions` references, but not semantic drift (e.g., if the engagement-axis *statement* changes while the positions stay named the same).
- **Drift in peer vaults**: if vault A's nodes are renamed, vault B's bindings reference the old name. `/system-bridge verify` catches this; `/system-audit` in the binding vault flags it as `⚠️ binding drift` during `paired_with` resolution.

### Escalation

If any vault reaches `🔴 red` and remains red across two consecutive `/coverage-audit` runs, the user should treat that as a signal that either (a) the system-model needs a structural refresh (new nodes, removed dead references) or (b) the vault's substantive work has outpaced the model's capacity and the next natural step is a re-bootstrap. The closure records (`phase-N-closure.md`) are the precedents for this kind of refresh.

## Rollout Status

| Phase | Scope | Status |
|---|---|---|
| 0 | Primitive discovery experiment | ✅ Complete 2026-04-20 — gate CLEAN |
| 1 | Schema + docs (agensy only) | ✅ Complete 2026-04-20 |
| 2 | politeia pilot — bootstrap system-model.yaml + Mermaid | ✅ Complete 2026-04-20 — closure PASS |
| 3 | `/system-build` + `/system-bridge` + dogfood | ✅ Complete 2026-04-20 |
| 4 | Extend to oeconomia, bellum; cross-vault closure test | ✅ Complete 2026-04-20 — reflexivity PASS |
| v0.2 | Schema v0.2 — timescale, subtype, secondary_types; binding mechanism check | ✅ Complete 2026-04-24 |
| 5a | historia system model bootstrap | ✅ Complete 2026-04-24 — partial (gate unmet) |
| 5b | theoria system model bootstrap — universality test | ✅ Complete 2026-04-24 — closure PASS (bounded) |
| Deferred | auto-regeneration, Canvas, MCP | deferred |

See the plan file for phase gates, kill criteria, and verification.

## Risks and Live Concerns

1. **Pattern-name collisions across vaults** — `reflexivity` in oeconomia Soros-style and in bellum OODA-style may encode mechanically incompatible dynamics. **Status**: Phase 4 closure gate PASSED (six reflexivity instances across three vaults all share Soros observer-effect mechanism). v0.2 further tightens this via `subtype` + `timescale` annotations and `/system-audit` Step 5b binding mechanism check.
2. **Schema churn** — v0.1 predicted 1–2 revisions during rollout; v0.2 shipped 2026-04-24 with additive-only changes (timescale, subtype, secondary_types). All v0.1 YAMLs remain valid. v0.3 candidates: node quality/confidence, edge weight.
3. **Bootstrap labor** — classifying ~200 notes per vault into nodes is multi-session work. Must be incremental and interactive, not batched. Omega (~249 notes) is the largest remaining bootstrap and is also the universality test — acceptance of actor/process ontology by a concept-lattice-shaped vault is the v0.2-era claim under test.
4. **Maintenance decay** — without regular `/system-audit`, the YAML rots relative to the note corpus. Mitigation: fire `/system-audit` at `/coverage-audit` and phase-completion events.
5. **Subtype proliferation** (new in v0.2) — free-string `subtype:` risks taxonomy drift. Mitigation: primitives.md documents the observed subtype vocabulary; new subtypes should reuse existing strings when mechanistically identical, coin new strings only when divergent.

## See Also

- `primitives.md` — the vocabulary with worked examples.
- `primitives-experiment.md` — Phase 0 gate decision.
- `system-model-schema.yaml` — canonical schema.
- `universal-commands/system-query.md` — read-only queries.
- `universal-commands/system-audit.md` — drift detection.
- `cross-vault-bridges.md` — bridge domains referenced by cross_vault_bindings.
- `vault-config-schema.md` — the genesis config each system model extends.
