---
description: Read-only query against a vault's system-model.yaml
type: universal-protocol
audience: claude
---

# /system-query

Query the structural ontology of one or more vaults via their `system-model.yaml`. Read-only — never writes. Returns node / edge / pattern listings with linked-note paths resolved.

**Runtime**: Read `vault-config.md` from the vault root. Check that `system-model.yaml` exists at the vault root. If it does not exist, respond: "No system model bootstrapped for this vault — run `/system-build` first." and stop. If the vault is `agensy`, the query targets `framework/system-model/system-model-schema.yaml` instead (schema-level questions, not vault-level).

Also extract from vault-config.md:
- `domains[]` — for validating query scope by domain.
- `engagement_axis.positions[]` — for validating engagement_positions filters.

If the query is cross-vault (`/system-query across <vaults>`), read each peer vault's `system-model.yaml` and `[AGENSY_PATH]/cross-vault-bridges.md`.

---

## Supported Query Shapes

The command accepts free-text queries; classify the query into one of the shapes below and execute. If the query does not match any shape, answer the closest shape and say which it matched.

### Shape A — List by category
Examples: "core actors in politeia", "all constraints", "structures and states".
Output: a table per requested category with `id`, `label`, `domain`, `linked_notes` count, and `engagement_positions`.

### Shape B — Trace edges from a node
Examples: "what does `dominant_power_anxiety` produce?", "what gates `individual_exit`?", "what reinforces `credibility_rigidity`?".
Output: the matching edges with `from`, `type`, `to`, and `linked_notes` count. Also list the reverse direction if the query is ambiguous (e.g., "edges touching X").

### Shape C — Find pattern instances
Examples: "all positive_feedback patterns in politeia", "reflexivity instances", "patterns in domain X".
Output: each pattern's `id`, `type`, `subgraph.nodes`, `linked_notes` count, optional `description`.

### Shape D — Resolve linked notes for a node / edge / pattern
Examples: "notes for `thucydidean_trap` pattern", "notes linked to `rising_power` node".
Output: list of `linked_notes` paths, each marked ✅ (resolves to existing file) or ❌ (broken reference — report as a Phase 2 closure issue).

### Shape E — Show full detail for a single entity
Examples: "show node `rising_power`", "show pattern `legitimacy_erosion_feedback`".
Output: full YAML block for that entity plus resolved linked-note titles (read frontmatter `aliases` / first heading to extract).

### Shape F — Cross-vault query (Phase 4+)
Examples: "all positive_feedback patterns across all vaults", "reflexivity in politeia and oeconomia".
Procedure: read each vault's `system-model.yaml`, match by `pattern_type` or `bridge_id`. Output a per-vault table; flag when pattern instances share a name but disjoint `linked_notes` (possible pattern-name collision — see risk noted in `primitives.md`).

---

## Step 1 — Classify the Query

Determine which shape (A–F) the user's query matches. If unclear, pick the best fit and say which shape you matched. If cross-vault is implied but the current vault lacks bindings, report the gap instead of silently falling back to single-vault.

---

## Step 2 — Execute the Query

Read `system-model.yaml` as YAML. Do not parse the note corpus — the system model is the authoritative source for this command.

- **Shape A**: iterate `nodes[category]` for requested categories, filter if domain is specified.
- **Shape B**: iterate `edges[]`, filter by `from` / `to` / `type`.
- **Shape C**: iterate `patterns[]`, filter by `type` / domain.
- **Shape D**: look up the entity by id, return its `linked_notes`. For each path, call the filesystem to check existence (do NOT read contents — existence only).
- **Shape E**: look up the entity by id, return all its fields. For linked notes, read frontmatter only to extract `aliases` or first heading.
- **Shape F**: execute Shape C per vault, aggregate, flag collisions.

---

## Step 3 — Format Output

Always begin with a one-line header: `Query shape: [A–F] · Vault: [name] · Hits: [N]`.

For tabular outputs (Shapes A, C, F), use a markdown table.
For detail outputs (Shape E), use a fenced YAML block for the entity + a short bulleted list of linked-note titles.
For broken references found during Shape D, output as a **warnings** section at the end.

Keep the response tight — if the hit count exceeds 30, paginate (show first 30, note the total, suggest a narrower query). Do not dump hundreds of rows into context.

---

## Step 4 — Cross-Reference Checks (Lightweight)

Before returning, verify at minimum:
- Every id referenced in the response resolves in the source YAML (no dangling ids).
- Every `engagement_positions` value matches `vault-config.md engagement_axis.positions[]`.

If either check fails, flag inline as a `⚠️ schema drift` note — do not silently pass. These are softer checks than `/system-audit` runs; the point is only to warn the user that the vault's system model may have rotted since last audit.

---

## Not in Scope (Deferred)

- **Writing / mutation** — that is `/system-build`.
- **Full audit and drift reporting** — that is `/system-audit`.
- **Bridge enumeration with bindings diff** — that is `/system-bridge` (Phase 3).
- **Natural-language queries that require reading note content** — the system model is the source of truth; if the answer requires prose content, route to `/compare` or `/engage-deep` instead.
