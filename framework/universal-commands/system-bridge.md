---
description: Diff a vault's cross_vault_bindings against cross-vault-bridges.md; propose new, flag missing, detect drift
type: universal-protocol
---

# /system-bridge

Reconcile a vault's `cross_vault_bindings[]` against the canonical bridge registry in `agensy/cross-vault-bridges.md`. Reports: bridges this vault appears in but doesn't yet have bindings for (missing); bindings present but not in the registry (drift); bindings whose peer side has become invalid (broken); proposed new bindings based on heuristic scan of the vault's nodes and patterns (candidates).

Three modes:
- `diff` (default) — report only; no writes.
- `propose` — report + draft candidate binding blocks for user to accept into `/system-build`.
- `pair <peer-vault>` — focus the diff on bridges this vault shares with a single peer.

Read-only except when the user explicitly routes a proposed binding through `/system-build`.

**Runtime**: Read the following inputs:
- `vault-config.md` from the vault root — `domains[]`.
- `system-model.yaml` from the vault root. If absent: respond "No system model — run `/system-build bootstrap` first." and stop.
- `agensy/cross-vault-bindings.yaml` (v0.6+) — central bindings file; the source of truth for cross-vault binding data.
- `agensy/cross-vault-bridges.md` — canonical bridge registry (descriptions).
- `agensy/system-state.md` — Vault Registry (to know which peer vaults exist and their system-model status).
- Peer vaults' `system-model.yaml` where they exist and the user requested `pair`.

---

## Step 1 — Parse the Bridge Registry

Walk `agensy/cross-vault-bridges.md`. For each `## Bridge N — Title` heading, extract:
- `bridge_id` — derived from heading: `bridge-N-kebab-case-title` (e.g., `## Bridge 2 — Decision Theory and Rationality` → `bridge-2-decision-theory-and-rationality`). Be tolerant of shorter in-model ids — `bridge-2-decision-theory` is a valid alias when only the core noun matters.
- `which_vaults` — parse the "**Which vaults**:" line.
- `search_terms` — parse the "**Search terms**:" line.
- `bridge_tension` — the prose paragraph after "**Bridge tension**:".

Build an in-memory index: `{ bridge_id → { vaults, terms, tension } }`.

---

## Step 2 — Classify the Vault's Current Bindings

**v0.6 change**: bindings live in `agensy/cross-vault-bindings.yaml`. Read the central file and walk `bindings[]` where `contributions[this_vault]` has a non-empty `self_declared` block.

**Valid binding**: `bridge_id` resolves in the registry; the current vault is listed in that bridge's `which_vaults`.

**Drift**: `bridge_id` does not resolve in the registry (typo, renamed bridge, local invention). Flag.

**Orphan**: `bridge_id` resolves but this vault is NOT in that bridge's `which_vaults`. Either the registry is stale (add the vault) or the binding is overreaching (remove). Flag.

**Broken peer view**: an item in `peer_views[claimer].nodes` / `patterns` (under THIS vault's contribution block) does not resolve in this vault's `nodes[]` / `patterns[]`. Surfaces as `binding_drift` from `/system-audit` Step 5.

Report counts and one line per issue.

---

## Step 3 — Identify Missing Bridges

For every bridge in the registry where this vault is listed in `which_vaults`:
- If no entry in this vault's `cross_vault_bindings[]` has that `bridge_id` → **missing**.

A missing bridge is not necessarily a defect — the vault may not yet have nodes that anchor that bridge. But it is a writing-opportunity signal: the registry says this bridge applies here; the model hasn't caught up.

Report missing bridges with: the bridge title, the peer vaults on the other side, and the bridge's search terms (so the user can sanity-check whether this vault actually has relevant content).

---

## Step 4 — Propose Candidates (only in `propose` mode)

For each missing bridge, scan the current vault's nodes and patterns for evidence that content matching the bridge exists:
- Match node `label`s and `linked_notes` filenames against the bridge's `search_terms` (case-insensitive, partial match).
- Match pattern `type`s and `description`s against the bridge's `bridge_tension` keywords.

If at least 2 nodes or 1 pattern matches, draft a candidate binding block in v0.6 central-file shape:

```yaml
# Add to agensy/cross-vault-bindings.yaml under bindings[]:
- bridge_id: [bridge-N-slug]
  description: >
    [Copy first sentence of the bridge's prose from the registry.]
  contributions:
    [this-vault]:
      self_declared:
        local_nodes: [list of matched node ids]
        local_patterns: [list of matched pattern ids]
        linked_notes: []
```

Present as a candidate — not written. Writing is `/system-build add-binding` (which now edits the central file directly).

Suppress candidates where the match is thin (single node, no pattern) — report instead as "worth manual check" to avoid spray.

---

## Step 5 — Pair Mode (focused diff with one peer)

If the user invoked `/system-bridge pair <peer-vault>`:

1. Read the peer vault's `system-model.yaml` if it exists.
2. For every bridge where both this vault and the peer are listed in `which_vaults`:
   - Report the binding state: valid / drift / missing / broken.
   - If valid: diff the `paired_with[peer_vault]` block against the peer's model. Flag `local_nodes` expected on the peer side that don't resolve in their model (candidate updates).
3. If the peer vault has not bootstrapped: report `⏳ peer not bootstrapped` and skip the peer-side checks.

Pair mode is the day-before-a-bootstrap-extension pass — use it when adding oeconomia or bellum so the politeia-facing bindings can be validated.

---

## Step 6 — Pattern-Collision Pre-Warning

For every bridge where both vaults have populated `local_patterns`:
- Check whether any pattern id or pattern `type` appears in both sides.
- If yes, check whether the subgraphs have disjoint `linked_notes` AND disjoint node-category distributions. If so, warn: **potential pattern-name collision** — the pattern name may be shared but the mechanics may differ.

This is a soft warning — cross-vault pattern binding is provisional until Phase 4 closure. Reference `primitives.md` "Pattern-Name Warning" section.

---

## Step 7 — Produce the Report

Format:

```
# Bridge Diff — [vault]
Schema version: 0.1 · Date: YYYY-MM-DD · Mode: [diff|propose|pair <peer>]

## Summary
- Bridges in registry touching this vault: N
- Bindings in this vault's model: M
- Valid: X · Missing: Y · Drift: Z · Orphan: W · Broken peer: V

## Issues
[one line per issue, categorized]

## Candidates (propose mode only)
[YAML-fenced candidate binding blocks]

## Next Actions
1. [e.g., "Add binding for bridge-6 — `/system-build add-binding bridge-6-institutional-analysis`"]
2. [e.g., "Fix drift: `bridge-5-political-economy` doesn't match registry — rename to `bridge-5-political-economy-and-markets`"]
3. [≤5 actions total]
```

---

## Step 8 — Do Not Update System State

`/system-bridge` does not update `system-state.md`. Audit cadence (`/system-audit`) is the event that writes the `audited-YYYY-MM-DD` marker. Bridge diff is a read-only reconciliation tool; keep its footprint small.

---

## Not in Scope

- **Writing new bindings** — route through `/system-build add-binding`. Keep write paths scarce.
- **Inferring peer nodes from peer system-model** — mode `pair` reports what's there but does not auto-populate the `paired_with[peer].nodes[]`. That's a user classification step.
- **Creating new bridge entries in the registry** — `cross-vault-bridges.md` updates only when a new bridge is discovered during actual arc work (2+ arc notes referencing the domain crossing). Not automated by this command.
- **Phase 4 cross-vault query walks** — that is `/system-query across ...` (Shape F). This command prepares the bindings; the cross-vault query consumes them.
