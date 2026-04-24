---
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: registry
---

# Source Map Registry

Manifest of maps across source vaults (listed in your vault-config.md `cross_vault_dependency.source_vaults`) and their article-production status. Populated by `/article-scan`; consumed by `/article-seed` (to avoid double-drafting) and `/article-promote` (to record published essays against source maps).

**Row format**: `| map path | readiness tier | thesis candidate | essay status | essay path |`

**Readiness tiers** (scored 0–25 across five axes in `/article-scan` Step 2):
- **Ready** (≥20/25) — has thesis, pressure points, atomic support, standalone-ness, clear stakes; draftable immediately
- **Developable** (12–19/25) — structural gaps; one or two sections need work before drafting
- **Structural gap** (<12/25) — map is thin or indexical; not article-ready

**Essay status values**: `unscanned` · `ready` · `seeded` · `outlined` · `drafted` · `revised` · `published` · `skipped`

---

## How to populate

Run `/article-scan <source-vault-name>` from this vault. The command walks the source vault's `folder_structure.maps` and any map folders under `domains[]`, reads each map, scores it on the five axes, and writes the rows below. Repeat per source vault.

Re-running `/article-scan` updates existing rows without overwriting manual edits to `essay status` / `essay path`.

---

## Source Vault Sections

*(One `## <source_vault_name>` section per source vault declared in your `cross_vault_dependency.source_vaults`. Each section is populated by a separate `/article-scan <vault>` invocation.)*

### `<source_vault_name_1>`

*(Populate via `/article-scan <source_vault_name_1>`. Once populated: scan summary line — "Scanned YYYY-MM-DD. N maps. X Ready, Y Developable, Z Structural gap. Published essays: P.")*

| Map | Readiness | Thesis candidate | Status | Essay |
|---|---|---|---|---|

### `<source_vault_name_2>`

*(Populate via `/article-scan <source_vault_name_2>`.)*

| Map | Readiness | Thesis candidate | Status | Essay |
|---|---|---|---|---|

---

## Pair and Braid Candidates

*(Populated by `/article-scan` when it detects maps across vaults that share a founding problem or pressure point. Or added manually when a cross-framework braid essay is seeded. V1 implements Type D braids; Type B pairs and Type C MOC positions are V2.)*

| Type | Maps | Shared problem | Status | Essay |
|---|---|---|---|---|
