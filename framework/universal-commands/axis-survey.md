---
description: Survey all maps' positions on the vault's central engagement axis
type: universal-protocol
audience: claude
---

# /axis-survey

Survey the vault's entire map library to build a comprehensive picture of where each thinker, concept, and framework sits on the vault's central engagement axis (Q3).

**Runtime**: Read `vault-config.md` from the vault root before executing. Extract:
- `domains[]` — folder paths for map discovery
- `intellectual_style.engagement_axis.config_key` — the frontmatter field name (fault_line / central_dialectic / central_mystery / design_problem)
- `intellectual_style.engagement_axis.positions[]` — valid positions for this vault
- `intellectual_style.engagement_axis.statement` — the engagement axis question being surveyed
- `intellectual_style.engagement_axis.label` — display label (Fault Line / Central Dialectic / Central Mystery / Design Problem)
- `folder_structure.maps` — domain primer location
- `open_problems[]` — IDs for implications analysis

**Backward compat**: If `intellectual_style:` is absent, read `fault_line.positions[]` and `fault_line.statement` directly, treating `config_key` as `fault_line`.

---

## Step 1 — Collect All Maps

**If `memory/note-index.md` exists and is current (< 30 days old)**:
- Filter the index for rows where Tier = `Map` or Path ends in `-map.md`
- Also collect `primer-*.md` rows from the maps folder
- This replaces globbing individual domain folders

**If no index or index is stale**: Glob every domain folder from vault-config.md `domains[]` for `*-map.md` files. Also glob `folder_structure.maps` for `primer-*.md` files. Rebuild `memory/note-index.md` as a side effect.

Collect the full list of maps found across the vault.

---

## Step 2 — Extract Engagement Axis Positions

For each map found:
1. Read YAML frontmatter — extract the `[config_key]` field and `subject`
2. Read the map's Connection to the Project section — extract the engagement axis position entry
3. Record: **Map** | **Subject** | **Position** | **Justification (one sentence)**

---

## Step 3 — Distribution Analysis

Tabulate results using the positions from vault-config.md `engagement_axis.positions[]`:

| Position | Count | Subjects |
|---|---|---|
| [position 1] | | |
| [position 2] | | |
| ... | | |

Identify:
- Which domains are predominantly on which side of the engagement axis?
- Are there direct contradictions — two maps arguing opposite positions for the same phenomenon?
- What is the vault's aggregate engagement axis lean?

---

## Step 4 — Tension Report

For each contradiction pair (two maps on opposite sides of the same phenomenon):
- Name the two maps and their positions
- State the specific disagreement: what phenomenon does each interpret differently?
- Assess which position the vault's existing evidence more strongly supports

---

## Step 5 — Implications

What does the current engagement axis distribution imply?
- Is the vault balanced or systematically biased toward one position?
- Which open problems (from vault-config.md `open_problems[]`) are most affected by the current distribution?
- Which engagement axis positions are underrepresented and would benefit from targeted building?

Output a recommendation: which position needs the most attention in the next building phase, and which `/arc` subject would best address it.

---

## Step 6 — Update Session State

Update `memory/session-state.md`:
- Update `last_axis_survey` to today's date
- Update `last_updated`
