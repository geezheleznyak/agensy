---
description: Survey all maps' positions on the vault's central fault line
type: universal-protocol
audience: claude
---

# /fault-line-survey

Survey the vault's entire map library to build a comprehensive picture of where each thinker, concept, and framework sits on the vault's central fault line.

**Runtime**: Read `vault-config.md` from the vault root before executing. Extract:
- `domains[]` — folder paths for map discovery
- `fault_line.positions[]` — valid positions for this vault (e.g., materialist / ideational / interactive / situational)
- `fault_line.statement` — the fault line question being surveyed
- `folder_structure.maps` — domain primer location
- `open_problems[]` — IDs for implications analysis

---

## Step 1 — Collect All Maps

Glob every domain folder from vault-config.md `domains[]` for `*-map.md` files.
Also glob `folder_structure.maps` for `primer-*.md` files.

Collect the full list of maps found across the vault.

---

## Step 2 — Extract Fault Line Positions

For each map found:
1. Read YAML frontmatter — extract the `fault_line` field and `subject`
2. Read the map's synthesis instrument / Judgment Instrument section — extract the "Fault line" entry
3. Record: **Map** | **Subject** | **Position** | **Justification (one sentence)**

---

## Step 3 — Distribution Analysis

Tabulate results using the positions from vault-config.md `fault_line.positions[]`:

| Position | Count | Subjects |
|---|---|---|
| [position 1] | | |
| [position 2] | | |
| ... | | |

Identify:
- Which domains are predominantly on which side of the fault line?
- Are there direct contradictions — two maps arguing opposite positions for the same phenomenon?
- What is the vault's aggregate fault line lean?

---

## Step 4 — Tension Report

For each contradiction pair (two maps on opposite sides of the same phenomenon):
- Name the two maps and their positions
- State the specific disagreement: what phenomenon does each explain differently?
- Assess which position the vault's existing evidence more strongly supports

---

## Step 5 — Implications

What does the current fault line distribution imply?
- Is the vault balanced or systematically biased toward one position?
- Which open problems (from vault-config.md `open_problems[]`) are most affected by the current distribution?
- Which fault line positions are underrepresented and would benefit from targeted building?

Output a recommendation: which fault line position needs the most attention in the next building phase, and which `/arc` subject would best address it.
