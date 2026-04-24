---
description: Score maps in a source vault for article-readiness; update cogitationis source-map-registry
type: universal-protocol
audience: claude
---

# /article-scan [source-vault]

Audit the maps in a source vault and produce a ranked readiness table. Outputs feed `source-map-registry.md` in the expression vault (cogitationis).

**[source-vault]**: name of a source vault (e.g., `synthesis_politeia`, `synthesis_theoria`, `synthesis_bellum`, `synthesis_oeconomia`, `synthesis_historia`). Default: all source vaults listed in cogitationis's `vault-config.md` under `cross_vault_dependency.source_vaults`.

**V1 restriction**: runs only from cogitationis. Other vaults do not consume this command. Reject invocation if invoked from a non-expression vault.

**Runtime**: Read `vault-config.md` from the cogitationis vault root. Extract:
- `reference_docs.source_map_registry` — path to source-map-registry.md
- `cross_vault_dependency.source_vaults` — list of source vault names
- `reference_docs.map_to_article_schema` — path to extraction schema

---

## Step 1 — Discover Maps

For the named source vault (or each source vault if unspecified):

1. Read its `vault-config.md` to get `folder_structure.maps` and any map folders under `domains[]`.
2. Glob for files matching `*-systematic-map.md`, `*-concept-map.md`, `*-framework-map.md`, and `primer-*.md` in those folders.
3. Also glob for MOCs in `folder_structure.mocs` — they are Type C candidates (V2; skip in V1 but record path).

Produce a map list: `[(vault, path, map_type)]` where `map_type ∈ {thinker, concept, framework, primer, moc}`.

---

## Step 2 — Score Each Map

For each map in the list, read the file and score 0–5 on each axis:

### 2.1 Thesis clarity
- Read "Founding problem" and "First principles" / "Core claims" sections.
- **5**: Founding problem is a crisp historical crisis; first principles imply a single defensible claim.
- **3**: Founding problem is present but diffuse; first principles list has 4+ items without obvious hierarchy.
- **1**: No founding problem; first principles are summaries rather than claims.
- **0**: Map is indexical only (MOC-like).

### 2.2 Pressure points named
- Read "Pressure Points" (or vault-equivalent — check `intellectual_style.pressure_points.format` in source vault's config).
- **5**: 3+ pressure points, each grounded in a specific case/exploiter/failure-mode.
- **3**: 2 pressure points, at least one grounded concretely.
- **1**: Pressure points listed but abstract.
- **0**: No pressure points section.

### 2.3 Atomic support
- Count atomic notes linked from the map (wikilinks to T2 notes in the map body or "Atomic Notes" section).
- **5**: ≥10 atomic notes.
- **3**: 5–9 atomic notes.
- **1**: 1–4 atomic notes.
- **0**: No atomic notes referenced.

### 2.4 Project connection / stakes
- Read "Connection to the Project" or "Judgment Instrument" or vault-equivalent.
- **5**: Names ≥2 specific stakes (what the map gives + what it threatens); diagnostic framing explicit.
- **3**: States stakes abstractly.
- **1**: Boilerplate or generic.
- **0**: Section missing.

### 2.5 Standalone-ness test
- Mentally strip all wikilinks. Does the prose still make sense?
- **5**: Prose survives wikilink-stripping. A cold reader could follow the argument from the map alone.
- **3**: Prose survives with minor gaps; most wikilinks are decorative.
- **1**: Prose depends on wikilinks for coherence; cold reader gets lost.
- **0**: Map is mostly wikilinks with minimal prose.

### 2.6 Composite score and readiness tier
- **Ready** (≥20): pipeline immediately.
- **Developable** (12–19): seed candidate but expect a revision cycle to fix gaps.
- **Structural gap** (<12): do not seed. Log gap for potential future map revision.

---

## Step 3 — Extract Thesis Candidate

For each Ready and Developable map:
1. Apply the thesis-candidate heuristic from `map-to-article-extraction.md`:
   - Read Pressure Points.
   - Identify the first principle that pressure points attack.
   - State that principle as a one-sentence declarative claim.
2. Record the thesis candidate in the registry.

For Structural-gap maps: skip thesis extraction; record "N/A — gap".

---

## Step 4 — Detect Pair/Braid Candidates (V2 — skip in V1)

V1: do not run this step. V2 will compare founding-problem blocks across maps to surface shared problems (candidate pair/braid seeds).

V1 behavior: leave the Pair/Braid Candidates section of `source-map-registry.md` unchanged.

---

## Step 5 — Update source-map-registry.md

Read `reference_docs.source_map_registry` (from cogitationis vault-config.md). Update in place:

For each scanned map:
- If the map is new to the registry: append a row under the correct source-vault section.
- If the map exists and has been scanned before: update the Readiness and Thesis candidate columns; preserve Status and Essay columns (so in-progress essays are not clobbered).

Row format: `| [map filename] | Ready/Developable/Structural gap | [thesis candidate, one sentence] | [status] | [essay path] |`

Initial status for a newly scanned Ready map: `ready`. For Developable: `ready` (with a gap note in Thesis candidate column). For Structural gap: `skipped`.

---

## Step 6 — Report

Output to the user:

```
## /article-scan [source-vault] — YYYY-MM-DD

Scanned: [N] maps
- Ready: [count] → [list paths]
- Developable: [count] → [list paths]
- Structural gap: [count] → [list paths]

Top 3 seeds (highest readiness):
1. [map path] — [thesis candidate]
2. [map path] — [thesis candidate]
3. [map path] — [thesis candidate]

Registry updated: [absolute path to source-map-registry.md]

Next step: pick a map and run /article-seed [map-path] A
```

---

## Determinism

This command must be deterministic: scanning the same vault twice without map changes must produce identical rankings. Thesis extraction may vary slightly (LLM variance) but readiness tiers should not.

---

## Error modes

- If source vault has no `vault-config.md`: fail gracefully, report "vault lacks genesis doc".
- If source vault has no maps: report empty result, do not error.
- If cogitationis source-map-registry.md is missing: create it with the template from `synthesis_logos/source-map-registry.md` and note the creation in the report.
