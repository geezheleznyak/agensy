---
description: Reconcile a vault's system-model.yaml against the schema, vault-config, bridges, and the note corpus
type: universal-protocol
---

# /system-audit

Systematic reconciliation of `[vault]/system-model.yaml` against the canonical schema, the vault's config, the cross-vault bridges file, and the note corpus on disk. Produces a drift report — never writes to the system model itself.

**Runtime**: Read the following inputs before executing:
- `vault-config.md` from the vault root — `domains[]`, `engagement_axis.positions[]`, `folder_structure.output`.
- `system-model.yaml` from the vault root.
- `agensy/framework/system-model/system-model-schema.yaml` — canonical schema.
- `agensy/cross-vault-bridges.md` — valid bridge_ids.
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
- `bridge_id` exists in `agensy/cross-vault-bridges.md`.
- Every id in `local_nodes` / `local_patterns` resolves in this vault's system-model.
- Every vault name in `paired_with` exists in `agensy/system-state.md` Vault Registry.
- Every id in `paired_with[vault].nodes` / `paired_with[vault].patterns` resolves when the peer vault's system-model is readable. If the peer vault has no `system-model.yaml`, flag as `⏳ peer not bootstrapped` (not an error — expected during rollout).

Report: `⚠️ binding drift: N` with bridge_id, side, and broken id.

---

## Step 5b — Binding Mechanism Check (v0.2; rewritten v0.4)

**v0.4 change**: this step now fires ONLY on pairings explicitly declared in
`mechanism_pairings[]`. Cross-products of `local_patterns × paired_with[v].patterns`
that are NOT in `mechanism_pairings` are treated as implicit substrate overlap
and not type-checked. This eliminates the v0.1-v0.3 false-positive flood while
preserving strict mechanism validation where it is actually being claimed.

If a binding has no `mechanism_pairings` field, the binding is treated as
substrate-level only. Step 5b emits only an informational summary line
(`ℹ️ binding has no declared mechanism pairings`) — not a warning.

For every `cross_vault_bindings[]` entry with a `mechanism_pairings[]` list,
and for every entry within that list:

1. **Resolve** — each `peers[]` string of form `<peer_vault>.<peer_pattern_id>`
   must resolve to an existing pattern in the peer's `system-model.yaml`. If
   the peer vault is not bootstrapped, skip silently (informational note).
   If the peer is bootstrapped but the pattern id does not exist → flag as
   `⚠️ mechanism-pairing broken reference`.

2. **Type match** — compare the `type` field of the local pattern against the
   peer pattern.
   - Same `type` → pass silently.
   - Different `type` but one is in the other's `secondary_types` → `ℹ️ mechanism-pairing match via secondary_type` — pass with note.
   - Different `type` (no secondary_types escape) → `⚠️ mechanism-pairing failure`. The explicit assertion is invalidated; the user should either find a different peer pattern that genuinely matches, or remove this entry from mechanism_pairings (downgrading the claim to substrate-only).

3. **Subtype divergence** — if both patterns carry a `subtype` field, compare strings.
   - Same `subtype` → strong pairing (best case). Report silently.
   - Different `subtype` → `ℹ️ mechanism-pairing subtype-divergence` — informational. The pairing may still be meaningful at the coarser `type` level.
   - One side has `subtype`, the other does not → `ℹ️ mechanism-pairing subtype-asymmetric` — prompts annotating the unannotated side.

4. **Timescale divergence** — if both patterns carry a `timescale` field, compare bands.
   - Same band → silently pass.
   - Adjacent bands (e.g., `weeks-to-months` paired with `years`) → silently pass; natural cross-scale pairing.
   - Bands apart (e.g., `seconds-to-minutes` paired with `decades+`) → `ℹ️ mechanism-pairing timescale-gap` — the shared mechanism operates at incompatible speeds; query results should preserve the distinction.
   - `mixed` on either side → silently pass; explicit acknowledgment by definition.

5. **Aggregate report**:
   - `⚠️ mechanism-pairing failures: N` (errors — fix or downgrade to substrate).
   - `⚠️ mechanism-pairing broken references: N` (errors — peer pattern id stale).
   - `ℹ️ mechanism-pairing divergences: N` (subtype / timescale / asymmetry — informational).
   - `ℹ️ implicit substrate pairings: N` (cross-products in `paired_with` not declared in `mechanism_pairings` — informational only; v0.4 does not flag these).

This step is peer-readable — runs fully only when paired vaults' `system-model.yaml` files are accessible. If a peer is not bootstrapped, skip its comparisons silently with a `⏳ peer not bootstrapped` note.

Reference: `primitives.md` "Pattern-Name Warning" section (updated for v0.4) and Layer 3b–3c.

### Migration note for v0.3 → v0.4 readers

Pre-v0.4 yamls have no `mechanism_pairings` field. Under v0.4 audit semantics,
pre-v0.4 bindings produce zero mechanism-pairing failures (correct: no claims
were made). They also produce no `binding type-mismatch` warnings (the v0.2-v0.3
warning class is retired in v0.4). To gain back mechanism validation on a
binding, declare the genuine alignments in `mechanism_pairings[]`. Aspirational
or weak pairings should not be declared — substrate is the right default.

---

## Step 6 — Pattern-Name Collision Warning (heuristic, retained from v0.1)

For patterns with `type ∈ {reflexivity, positive_feedback, threshold, ...}` that appear in multiple vaults (if cross-vault bindings touch them):
- Compare the `subgraph.nodes` node-categories distribution across the paired vaults.
- If the category distributions diverge sharply (e.g., one side is agent-heavy and the other is structure-heavy), flag as a **potential pattern-name collision**.

This is a heuristic, not a hard error. Report as `⚠️ potential pattern-name collision: N` — the user decides whether the binding is provisional or confirmed. v0.2 Step 5b provides more direct type/subtype/timescale checks; this step remains as a categorical-distribution backstop.

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
⚠️ mechanism-pairing failures: N        # v0.4 — replaces "binding type-mismatch"
⚠️ mechanism-pairing broken refs: N     # v0.4 — peer pattern id stale
ℹ️ mechanism-pairing divergences: N
ℹ️ implicit substrate pairings: N       # v0.4 — informational only
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

## Step 9 — Update System State + Compute Dirt Level

Update `agensy/system-state.md` Vault Registry — set this vault's `System Model` column to `audited-YYYY-MM-DD`. If the row does not yet have a system-model column populated, add one with the current audit date.

**Compute dirt level** from this audit's issue counts (v0.4: mechanism-pairing failures replace binding type-mismatch as the cross-vault drift trigger):

| Level | Criterion |
|---|---|
| 🟢 green | All issue counts ≤ 1 AND no broken linked_notes AND no mechanism-pairing failures AND no mechanism-pairing broken refs |
| 🟡 yellow | Any issue count 2–5 AND no broken linked_notes AND no mechanism-pairing failures AND no mechanism-pairing broken refs |
| 🔴 red | Any issue count > 5 OR ≥ 1 broken linked_notes OR ≥ 1 mechanism-pairing failure OR ≥ 1 mechanism-pairing broken ref |

**Note (v0.4)**: `unreferenced notes` and `implicit substrate pairings` are informational-only counts. They do NOT contribute to the "any issue count > 5" trigger. Treat them as visibility surfaces, not drift signals. This refines the v0.1 over-broad rule that conflated all counts.

**Counts that DO contribute to the > 5 rule**: schema violations, config drift, broken linked_notes, unlinked entities, binding drift, mechanism-pairing failures, mechanism-pairing broken refs, potential pattern-name collision.

Update the **System Model Freshness** table in `system-state.md` with:
- `last_audit`: today's date
- `dirt_level`: green / yellow / red (with emoji)
- `outstanding_issues`: the dominant issue type (e.g., "3 unlinked entities + 2 unreferenced notes")

**Escalation policy** — if `dirt_level` is `red`, surface the top 3 drift items to the user at the end of the audit report with a "REMEDIATION RECOMMENDED" header. For `yellow` or `green`, the report is informational only.

**One-line summary** — emit a single structured line at the end of the report for downstream capture by `/coverage-audit` Step 9 (v0.4: rename `type_mismatch` → `mech_failures`, add `mech_broken_refs` and `substrate_pairings`):

```
SYSTEM_AUDIT_SUMMARY: vault=<name> dirt=<green|yellow|red> schema=N config=N broken_notes=N unlinked=N unref=N binding_drift=N mech_failures=N mech_broken_refs=N divergences=N substrate_pairings=N
```

Do NOT modify `system-model.yaml` itself — the audit is read-only by design. Remediation is `/system-build`.

---

## Not in Scope

- **Auto-fixing drift** — the user decides whether to update the model or update vault-config; `/system-audit` surfaces, `/system-build` edits.
- **Populating unreferenced notes into the model** — classification is a human judgment call; the audit flags candidates, does not auto-classify.
- **Discovering new patterns** — the audit validates against the schema's 7 pattern types. Novel patterns surface in experiments like Phase 0, not in audits.
