---
description: Reconcile a vault's system-model.yaml against the schema, vault-config, bridges, and the note corpus
type: universal-protocol
audience: claude
---

# /system-audit

Systematic reconciliation of `[vault]/system-model.yaml` against the canonical schema, the vault's config, the cross-vault bridges file, and the note corpus on disk. Produces a drift report — never writes to the system model itself.

**Runtime**: Read the following inputs before executing:
- `vault-config.md` from the vault root — `domains[]`, `engagement_axis.positions[]`, `folder_structure.output`.
- `system-model.yaml` from the vault root.
- `[AGENSY_PATH]/framework/system-model-schema.yaml` — canonical schema.
- `[AGENSY_PATH]/cross-vault-bridges.md` — valid bridge_ids.
- Directory listing under the vault root (for `linked_notes` existence checks).

If `system-model.yaml` does not exist at the vault root, respond: "No system model to audit — run `/system-build` first." and stop.

---

## Step 1 — Schema Conformance

For every node / edge / pattern / cross_vault_binding:
- **Required fields present** — report any missing keys.
- **Category / type values valid** — every `node.category` in `node_categories`; every `edge.type` in `edge_types`; every `pattern.type` in `pattern_types`.
- **Unknown keys** — any key outside the schema's required + optional list is flagged as a warning (may indicate an extension; user confirms).

Output: `⚠️ schema violations: N` with one line per violation.

---

## Step 2 — Vault-Config Integrity

For every node:
- `domain` must exist in `vault-config.md domains[].slug`.
- Every `engagement_positions` value must exist in `vault-config.md engagement_axis.positions[]`.

Report: `⚠️ config drift: N` with the offending id, field, and actual-vs-expected value.

---

## Step 3 — Linked-Notes Integrity

For every `linked_notes` entry across nodes / edges / patterns / bindings:
- Check the path resolves to an existing file under the vault root.
- Count broken paths per entity.

Report: `⚠️ broken linked_notes: N` with the entity id and the broken path(s).

---

## Step 4 — Coverage (Bidirectional)

A. **Unlinked entities** — nodes, edges, or patterns with empty `linked_notes`. These are writing targets: the structural claim exists in the YAML but no note grounds it.

B. **Unreferenced notes** — walk `folder_structure.output` and every domain folder from vault-config. For each Tier 3 note (and key Tier 2-Syn notes), check whether its path appears in any `linked_notes` list. Notes not referenced by any system-model entity are classification targets.

Skip `00-Inbox/`, `10-Sources/`, `40-Templates/`, `memory/`, `_maps/` — these are not expected to be referenced.

Report:
- `📝 unlinked entities: N` (writing targets; list first 10 sorted by category).
- `📥 unreferenced notes: N` (classification targets; list first 10 sorted by folder).

---

## Step 5 — Cross-Vault Binding Integrity

For every entry in `cross_vault_bindings[]`:
- `bridge_id` exists in `[AGENSY_PATH]/cross-vault-bridges.md`.
- Every id in `local_nodes` / `local_patterns` resolves in this vault's system-model.
- Every vault name in `paired_with` exists in `[AGENSY_PATH]/system-state.md` Vault Registry.
- Every id in `paired_with[vault].nodes` / `paired_with[vault].patterns` resolves when the peer vault's system-model is readable. If the peer vault has no `system-model.yaml`, flag as `⏳ peer not bootstrapped` (not an error — expected during rollout).

Report: `⚠️ binding drift: N` with bridge_id, side, and broken id.

---

## Step 6 — Pattern-Name Collision Warning

For patterns with `type ∈ {reflexivity, positive_feedback, threshold, ...}` that appear in multiple vaults (if cross-vault bindings touch them):
- Compare the `subgraph.nodes` node-categories distribution across the paired vaults.
- If the category distributions diverge sharply (e.g., one side is agent-heavy and the other is structure-heavy), flag as a **potential pattern-name collision**.

This is a heuristic, not a hard error. Report as `⚠️ potential pattern-name collision: N` — the user decides whether the binding is provisional or confirmed. Reference `primitives.md` "Pattern-Name Warning" section.

---

## Step 7 — Produce the Audit Report

Format:

```
# System Model Audit — [vault-name]
Schema version: 0.1 · Date: YYYY-MM-DD

## Summary
- Nodes: N (by category: agents=X, states=Y, …)
- Edges: N (by type)
- Patterns: N (by type)
- Cross-vault bindings: N

## Issues
⚠️ schema violations: N
⚠️ config drift: N
⚠️ broken linked_notes: N
📝 unlinked entities: N
📥 unreferenced notes: N
⚠️ binding drift: N
⚠️ potential pattern-name collision: N

## Details
[per-issue detail, capped at 10 items per category — narrower query via /system-query for more]

## Next Actions
[prioritized action list — see Step 8]
```

---

## Step 8 — Next Actions

Prioritize:
1. Broken linked_notes → fix paths via `/system-build` or remove the reference.
2. Config drift → align `system-model.yaml` with `vault-config.md` (or update vault-config if the model is authoritative).
3. Binding drift → update bridge_id references or the peer vault's system-model.
4. Unlinked entities with no linked notes → writing targets for `/arc` or `/evergreen-note`.
5. Unreferenced notes in mechanism-rich folders → classification targets for `/system-build`.

Produce 3–5 concrete next actions at the end. Not an exhaustive list — just the highest-leverage.

---

## Step 9 — Update System State

Update `[AGENSY_PATH]/system-state.md` Vault Registry — set this vault's `System Model` column to `audited-YYYY-MM-DD`. If the row does not yet have a system-model column populated, add one with the current audit date.

Do NOT modify `system-model.yaml` itself — the audit is read-only by design. Remediation is `/system-build`.

---

## Not in Scope

- **Auto-fixing drift** — the user decides whether to update the model or update vault-config; `/system-audit` surfaces, `/system-build` edits.
- **Populating unreferenced notes into the model** — classification is a human judgment call; the audit flags candidates, does not auto-classify.
- **Discovering new patterns** — the audit validates against the schema's 7 pattern types. Novel patterns surface in experiments like Phase 0, not in audits.
