---
type: architecture
schema_version: 0.1
audience: claude
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

Frozen from a Phase 0 primitive-discovery experiment (2026-04-20). Full reference: `primitives.md`.

- **Nodes (6 categories)**: agents · states · flows · signals · constraints · structures
- **Edges (5 core + 5 reserve)**: produces · reinforces · dampens · gates · couples [core]; consumes · reveals · conceals · requires · opposes [reserve]
- **Patterns (7 types)**: positive_feedback · negative_feedback · threshold · reflexivity · selection · accumulation · path_dependence

Cross-vault bindings are enabled by the patterns layer: the same pattern type instantiated in two vaults with different local nodes is the coupling unit. Names matching does not guarantee mechanical compatibility — that is tested at Phase 4 closure, not assumed.

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

**In AGENSY (framework, not per-vault)**:

```
framework/
  system-model-schema.yaml              canonical schema, vocabulary locked
  system-model-architecture.md          this file
  primitives.md                         human-readable vocabulary reference
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

- **Command lifecycle** (`framework/command-lifecycle.md`): `/system-audit` fires at the same cadence as `/coverage-audit` (milestone trigger, every N notes or on phase completion).
- **System state** (`[AGENSY_PATH]/system-state.md`): Vault Registry gains a `System Model` column tracking per-vault status (absent / bootstrapped / audited-YYYY-MM-DD).
- **Genesis protocol** (`framework/genesis-protocol.md`): new vaults created post-v0.1 optionally bootstrap an empty `system-model.yaml` in Doc 12; population deferred to an explicit `/system-build` session.
- **Coverage-audit** (`framework/universal-commands/coverage-audit.md`): when a vault has a `system-model.yaml`, `/coverage-audit` Step 8 optionally invokes `/system-audit`.

## Rollout Status

| Phase | Scope | Status |
|---|---|---|
| 0 | Primitive discovery experiment | ✅ Complete 2026-04-20 — gate CLEAN |
| 1 | Schema + docs | ✅ Complete |
| 2 | First-vault pilot — bootstrap system-model.yaml + Mermaid | pending |
| 3 | `/system-build` + `/system-bridge` + dogfood | pending |
| 4 | Extend to additional vaults; cross-vault closure test | pending |
| 5 | Deferred — auto-regeneration, Canvas, MCP | deferred |

## Risks and Live Concerns

1. **Pattern-name collisions across vaults** — `reflexivity` in one vault Soros-style and in another OODA-style may be mechanically incompatible. Phase 4 closure gate catches this. Until closure passes, cross-vault bindings that rely on pattern-name matching only are provisional.
2. **Schema churn** — v0.1 is expected to need 1–2 minor revisions during Phase 2 as the first hand-bootstrap surfaces edge cases. Budget for v0.2 after the pilot.
3. **Bootstrap labor** — classifying ~200 notes per vault into nodes is multi-session work. Must be incremental and interactive, not batched.
4. **Maintenance decay** — without regular `/system-audit`, the YAML rots relative to the note corpus. Mitigation: fire `/system-audit` at `/coverage-audit` and phase-completion events.

## See Also

- `primitives.md` — the vocabulary with worked examples.
- `system-model-schema.yaml` — canonical schema.
- `universal-commands/system-query.md` — read-only queries.
- `universal-commands/system-audit.md` — drift detection.
- `cross-vault-bridges.md` — bridge domains referenced by cross_vault_bindings.
- `vault-config-schema.md` — the genesis config each system model extends.
