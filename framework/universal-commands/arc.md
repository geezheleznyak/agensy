---
description: Full arc — map + 8–12 atomic Tier 2 notes for any thinker, concept, or framework
type: universal-protocol
audience: claude
---

# /arc [subject] [type]

Build the full arc for a thinker, concept, or framework. Produces one map + 8–12 atomic Tier 2 notes.

**[type]** options: `thinker` | `concept` | `framework` | (omit to infer from subject)

**Runtime**: Read `vault-config.md` from the vault root before executing. Extract:
- `domains[]` — slug, label, folder, evergreen_candidate (for routing)
- `reference_docs.map_reference` — path to the vault's map reference document
- `note_template.synthesis` — mandatory sections and synthesis instrument template
- `intellectual_style` — engagement_axis (config_key, label, positions[]) and engagement_field (name, prompt)
- **Backward compat**: If `intellectual_style:` absent, read `fault_line.positions[]` directly (treat config_key as `fault_line`)
- `note_tiers.tier2` — type_value and schema rules
- `folder_structure.mocs` — MOC folder location

---

## Step 1 — Map Type and File Routing

Determine map type from [type] or infer from subject:
- Named theorist or statesman → `thinker` → `[lastname]-systematic-map.md`
- Political concept or system → `concept` → `[concept]-concept-map.md`
- Analytical or operational framework → `framework` → `[framework]-framework-map.md`

Determine where to store the map:
1. If vault-config.md defines `folder_structure.maps`, store the map there.
2. Otherwise, determine domain folder from vault-config.md `domains[]` matching the subject's primary domain and store there.

This ensures vaults with a dedicated maps folder (e.g., `theory/maps/`) route maps correctly instead of placing them in the domain note folder.

---

## Step 1.5 — Cross-Vault Awareness (Optional)

**When to activate**: Check whether the subject falls within a bridge domain in `[AGENSY_PATH]/cross-vault-bridges.md`. If yes, activate. If no, skip silently — do not mention it.

**Bridge check**: Read `[AGENSY_PATH]/cross-vault-bridges.md`. Match the arc subject against the 10 bridge domains by topic (not keyword — use judgment). A thinker or concept may fall into 1–3 bridges simultaneously.

**If activated**:
1. Read the relevant bridge entries (the "which vaults" and "vault treatment" lines for each matched bridge).
2. Search 2–3 notes in the most relevant sibling vault(s) using the bridge's **Search terms** via Grep or vault note titles.
3. Note the **Bridge tension** — where the sibling vault's treatment diverges from or deepens this vault's treatment.
4. Carry this awareness into Step 2 (map) and Step 3 (notes): let it surface in Internal Tensions, Judgment Instrument Threatens entries, and Open Questions where it genuinely adds depth.

**What this step does NOT produce**:
- No mandatory cross-vault references in frontmatter or body
- No new section in the map or notes dedicated to cross-vault connections
- No fabricated note paths — only reference actual notes found during the search

**Cost**: ~30 seconds for non-bridge arcs (skip decision), ~2 minutes for bridge arcs (read bridges file + search sibling vault). Do not activate for pure technical/reference arcs (default `evergreen-candidate: false` domains) — the signal-to-noise ratio is too low.

---

## Step 2 — Build the Map

Read the vault's map reference document at `reference_docs.map_reference`. Follow the map type specification exactly.

**Universal map rules**:
1. Write YAML frontmatter FIRST — before any prose. Include: `type`, `domain` (slug from vault-config.md), `subject`, `[engagement_axis.config_key]` (one of `engagement_axis.positions[]`), `open_problems`.
2. Build the Mermaid dependency diagram SECOND — before writing any section prose. If you cannot draw the architecture, you do not yet understand the system.
3. Write the synthesis instrument / Judgment Instrument section LAST.

**Map sections by type** (consult `reference_docs.map_reference` for vault-specific section names and depth targets):
- **Thinker**: I. Context → II. Architecture Diagram → III. Intellectual Arc → IV–X. Branch Analysis → XI. Pressure Points → XII. Reception and Influence → XIII. Judgment Instrument
- **Concept**: I. Context → II. Architecture Diagram → III. Historical Emergence → IV–VIII. Branch Analysis → IX. Pressure Points → X. Judgment Instrument
- **Framework**: I. Context → II. Architecture Diagram → III. Application Conditions → IV–IX. Branch Analysis → X. Failure Modes → XI. Pressure Points → XII. Judgment Instrument

**Pressure Points rule**: Every pressure point must be grounded concretely using the vault's style format (read `intellectual_style.pressure_points.format`). Not a general tension — must reference a specific case, thinker, demonstration, or incident appropriate to the style.

**Judgment Instrument / Connection to the Project must include**:
- ≥2 specific `[engagement_field.name]` entries (not just resources; see `intellectual_style.engagement_field.prompt` for the right question to answer)
- Engagement axis position (one of `engagement_axis.positions[]`)
- Atomic Notes to Generate list (8–15 candidates)

**Quality check before finishing map**:
- [ ] Mermaid diagram built before prose?
- [ ] Every pressure point grounded concretely using the style's format?
- [ ] Judgment Instrument / Connection to the Project has ≥2 specific engagement field entries?
- [ ] Atomic Notes to Generate list has 8–15 candidates?

---

## Step 3 — Generate Atomic Notes

Generate 8–12 atomic Tier 2 notes from the map's "Atomic Notes to Generate" list.

**Frontmatter** for each note:
```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: [note_tiers.tier2.type_value from vault-config.md]
domain: [slug from vault-config.md domains[]]
evergreen-candidate: [domain's evergreen_candidate default, or true if clearly synthesis]
[intellectual_style.engagement_axis.config_key]: "[one of engagement_axis.positions[] from vault-config.md]"
open_problems: [list of problem IDs from vault-config.md open_problems[]]
source: "[[Map filename]]"
aliases: []
---
```

**Mandatory sections**: follow vault-config.md `note_template.synthesis.mandatory_sections` exactly. Every section is required.

**Synthesis instrument** (from `note_template.synthesis` — named "Judgment Instrument", "Connection to the Project", or vault-equivalent): the `[engagement_field.name]` entry is MANDATORY and cannot be omitted (read `intellectual_style.engagement_field.prompt` for the required framing).

**Filename**: `YYYYMMDDHHMM - Title as Claim.md` — actual current date, 5-minute increments.
**Location**: domain folder from vault-config.md `domains[]`.

---

## Step 4 — Update MOC

After all notes are written:
1. Find the relevant domain MOC in vault-config.md `folder_structure.mocs`
2. Add the new map to the "Thinker & Framework Maps" section
3. Add each new note to the "Tier 2 — Core Concepts" section with wikilink
4. Update the MOC's modification date

Also update the Master Index MOC (in `folder_structure.mocs`):
- Increment note count for the domain
- Increment map count if a map was added

---

## Step 5 — Validate Arc (Automatic)

After the MOC update, invoke `/quick-check last-arc` automatically. Do not wait for the user to request it.

Read `[AGENSY_PATH]/framework\universal-commands\quick-check.md` and execute with scope `last-arc`. The arc is not complete until the quick-check report is delivered.

**Cascade context**: vault-config.md is already in context from Step 0 (Runtime). When chaining into `/update-moc` and `/quick-check`, do NOT re-read vault-config.md — pass the loaded configuration forward. Re-read vault-config.md only if this arc is invoked standalone at a later point in a long session.

**If the report contains BLOCKED notes** (broken wikilinks, schema mismatch): fix them before declaring the arc done.
**If the report contains NEEDS REVISION notes**: surface them in the arc summary so the user can decide whether to fix now or log as debt.
**If all notes are READY**: declare the arc complete.

---

## Step 6 — Update Session State and Note Index

After arc completion:

1. **Update `memory/session-state.md`**:
   - Increment `notes_since_last_audit` by the number of notes written in this arc
   - Append to `recent_arcs`: `"[subject] ([domain-folder]) — YYYY-MM-DD"`
   - Update `last_updated`

2. **Append to `memory/note-index.md`** (create with headers if it does not exist):
   - Add one row per new note written, using the format: `| [relative-path] | T2 | [domain-slug] | [true/false] | [axis-position] | [op-ids] | — | [created-date] |`
   - Add one row for the map written: `| [map-path] | Map | [domain-slug] | true | [axis-position] | — | — | [created-date] |`
