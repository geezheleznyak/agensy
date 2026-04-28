---
description: Interactively add, update, or remove nodes / edges / patterns / bindings in a vault's system-model.yaml
type: universal-protocol
---

# /system-build

Write-side counterpart to `/system-query` and `/system-audit`. Proposes safe, schema-conforming edits to a vault's `system-model.yaml`. Every write is preceded by a preview diff and requires user confirmation. Never edits silently; never bypasses schema validation.

**Runtime**: Read the following inputs before executing:
- `vault-config.md` from the vault root — `domains[]`, `engagement_axis.positions[]`.
- `system-model.yaml` from the vault root (create it if missing — see Step 0).
- `agensy/framework/system-model/system-model-schema.yaml` — canonical per-vault schema.
- `agensy/framework/system-model/cross-vault-bindings-schema.yaml` — central-file schema (for binding ops in v0.6+).
- `agensy/cross-vault-bindings.yaml` — central bindings file (for binding ops; created if missing).
- `agensy/cross-vault-bridges.md` — valid bridge_ids (for binding ops).

If `system-model.yaml` does not exist at the vault root, offer to bootstrap it (Step 0). Otherwise jump to Step 1.

---

## Operation Modes

`/system-build` accepts free-text intent; classify the request into one of the operation modes below and execute. The command is an editor — each mode is a single-purpose operation.

| Mode | Shorthand | Effect |
|---|---|---|
| `add-node` | "add node X" | Append a new node block under `nodes:` |
| `add-edge` | "add edge X → Y of type T" | Append a new edge block under `edges:` |
| `add-pattern` | "add pattern X of type T" | Append a new pattern block under `patterns:` |
| `add-binding` | "add binding to bridge B" | Append/extend a binding entry in `agensy/cross-vault-bindings.yaml` (v0.6+; pre-v0.6 was per-vault `cross_vault_bindings:`) |
| `update` | "update node X set domain=Y" | Modify a specific field on an existing entity |
| `rename` | "rename node X to Y" | Change an id; also updates all references (edges, patterns, bindings) |
| `remove` | "remove node X" | Delete an entity; refuse if still referenced unless `--force` |
| `link-notes` | "link notes to X" | Add note paths to an entity's `linked_notes[]` |
| `bootstrap` | "bootstrap" | Create `system-model.yaml` from a vault that has none |

If the request does not match any mode, state the closest match and ask the user to confirm.

---

## Step 0 — Bootstrap Mode (only if system-model.yaml is missing)

If the vault has no `system-model.yaml`:
1. Propose a minimal skeleton at the vault root (v0.6+ — note: no `cross_vault_bindings:` section; bindings live in the central file):
   ```yaml
   vault: [vault-name from vault-config]
   schema_version: 0.6
   extends: ../agensy/framework/system-model/system-model-schema.yaml

   nodes: []
   edges: []
   patterns: []
   ```
2. Confirm with the user before writing.
3. After creation, add the vault's row in `agensy/system-state.md` Vault Registry — set `System Model` = `bootstrapped-YYYY-MM-DD`.
4. Stop. The user invokes `/system-build` again with the first real edit.

Do **not** auto-populate nodes from the note corpus in bootstrap mode. Bootstrap is intentionally empty. The Phase 2 pilot (politeia) was hand-curated — future bootstraps should follow the same pattern, with explicit user choice on every entity.

---

## Step 1 — Classify the Operation

Determine the mode from the user's free-text request. If the request names an entity id or a relation that already exists, offer to route to the correct mode (e.g., a user says "add node X" but X already exists → route to `update` or `link-notes`).

Never proceed silently past ambiguity.

---

## Step 2 — Validate Against Schema BEFORE Writing

Every proposed edit must pass schema conformance before it is offered to the user:

**For `add-node`**:
- `id` is a snake_case string; does not collide with any existing node id.
- `category` ∈ `node_categories` (schema §1).
- `domain` ∈ `vault-config.md domains[].slug`.
- `engagement_positions[]` each ∈ `vault-config.md engagement_axis.positions[]`.
- `label` present, `linked_notes` may be empty but must be a list.
- Any `levels:` field values are strings.

**For `add-edge`**:
- `id` unique. `from` and `to` resolve to existing node ids.
- `type` ∈ `edge_types` (schema §2). If user used a reserve edge type (`consumes`, `reveals`, `conceals`, `requires`, `opposes`), flag that this activates a reserve type and confirm.

**For `add-pattern`**:
- `id` unique. `type` ∈ `pattern_types` (schema §3).
- `subgraph.nodes[]` each resolves. `subgraph.edges[]` each resolves.
- `domain` ∈ vault-config domains.
- `description` is present (non-empty prose; one paragraph minimum — patterns without a description are placeholders and rot).

**For `add-binding`** (v0.6+ — writes to `agensy/cross-vault-bindings.yaml`, NOT to the per-vault YAML):
- `bridge_id` ∈ bridge IDs defined in `agensy/cross-vault-bridges.md`.
- `local_nodes[]` / `local_patterns[]` each resolves in this vault's `system-model.yaml`.
- The new entry is added under `bindings[].contributions[this_vault].self_declared`. If a binding for `bridge_id` already exists in the central file, extend the existing block (don't duplicate).
- To claim peer contributions ahead of peer ratification, add to `contributions[peer].peer_views[this_vault]` instead. The audit will surface those as `unratified_peer_views` (informational) until the peer adds them to `self_declared`.
- mechanism_pairings are added under `bindings[bridge_id].mechanism_pairings[]` with `claimer: this_vault`.

**For `rename` / `remove`**:
- Find all references across `nodes`, `edges`, `patterns`, `cross_vault_bindings`.
- `rename` updates every reference atomically.
- `remove` refuses if references exist; the user must remove the references first (or pass `--force`, which removes the entity and leaves references broken for `/system-audit` to flag — not recommended).

**For `link-notes`**:
- Each note path must resolve to an existing file under the vault root. If a path is invalid, flag and ask the user to correct (typo, wrong folder, moved note).

If any check fails: report the specific failure, do not attempt the write, and ask the user to correct.

---

## Step 3 — Preview the Diff

Before writing, show the user a YAML-fenced diff of the change:

```diff
  nodes:
    - id: ruler
      ...
+   - id: private_preference_distribution
+     label: Hidden collective belief distribution under authoritarian compliance
+     category: states
+     domain: state-governance
+     engagement_positions: [materialist, interactive]
+     levels: [falsified_stable, falsified_cascade_ready, revealed]
+     linked_notes:
+       - cases/202603182210 - Information Cascades Enable Revolutionary Tipping — Each Defection Changes Others' Calculations.md
```

For multi-step edits (e.g., `rename`), preview every touched entity in one block. Do not batch unrelated edits into a single diff — one mode per invocation.

Explicit user confirmation is required before Step 4. A silent "proceed" from context is not enough — require an affirmative signal for writes.

---

## Step 4 — Write the Edit

Modify `system-model.yaml` in-place. Preserve existing key ordering where possible (YAML stability helps diffs over time). Append new entries at the end of their respective section (nodes, edges, patterns, bindings) rather than inserting mid-list.

After writing, re-read the file and parse as YAML to confirm it is still valid. If parsing fails, restore the prior state and report.

---

## Step 5 — Light Audit Pass

Run a subset of `/system-audit` checks against only the newly-written region:
- Schema conformance (Step 1 of audit).
- Referenced ids resolve (Step 3 of audit).
- For new bindings only: bridge_id validity (Step 5 of audit).

If any light-audit issue surfaces, report it to the user but do not auto-revert — the user decides whether to fix via a follow-up `/system-build` call or accept as-is.

---

## Step 6 — Update System State (only on bootstrap or first write)

If this was the vault's first write of the session or a bootstrap:
- Set `agensy/system-state.md` Vault Registry row → `System Model` column = `bootstrapped-YYYY-MM-DD` (if not already set).

Do not update on routine edits — Audit cadence is what drives the `audited-YYYY-MM-DD` state, not every small edit.

---

## Step 7 — Summarize

One-line header: `/system-build · [mode] · [entity id or path] · written`.
Brief (≤3 lines) description of what was added / changed. Point the user at `/system-audit` as the next sanity check if the edit was substantial (new pattern, new binding, rename, remove).

---

## Not in Scope

- **Auto-classifying notes into nodes** — the audit flags unreferenced notes; the human decides which note belongs to which entity. `/system-build link-notes` is the right tool once that decision is made.
- **Pattern discovery** — novel patterns (beyond the 7 schema types) belong in a Phase 0-style experiment, not an inline command. If the user insists a note exhibits a new pattern type, route them to a structured experiment; do not silently extend the schema.
- **Merging two nodes** — a genuine refactor that needs care (`merge` is a candidate for v0.2; not implemented here). Until then: `rename A → A_merged` on one, then `remove A_merged` after manual migration of references.
- **Batch edits from a file** — intentionally absent. Every entity edit requires its own preview + confirmation. Batch mutations without review is how ontologies rot.

---

## Relationship to /system-audit and /system-query

`/system-build` is the only command that writes to `system-model.yaml`. `/system-query` is read-only. `/system-audit` is read-only (flags drift, remediation is `/system-build`). This tri-command separation is deliberate — keep write paths scarce.
