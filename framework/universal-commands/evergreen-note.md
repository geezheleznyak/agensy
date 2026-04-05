---
description: Write a single Tier 3 judgment/evergreen note from a concept or source
type: universal-protocol
audience: claude
---
# /evergreen-note [concept from source]

Write a single atomic Tier 3 note. Use when one clear structural insight is ready to be distilled — not for generating batches (use `/arc` for that).

**[concept from source]**: The specific concept and its source (e.g., "Schelling's focal points from Arms and Influence").

**Runtime**: Read `vault-config.md` from the vault root before executing. Extract:
- `note_tiers.tier3.output_folder` — where to write the note
- `note_tiers.tier3.type_value` — frontmatter type value
- `note_tiers.tier3.graduation_rule` — Tier 3 placement criteria
- `note_template.synthesis` — mandatory sections and synthesis instrument template
- `intellectual_style` — engagement_axis (config_key, positions[]) and engagement_field (name, prompt, graduation_gate)
- `open_problems[]` — IDs for open questions referencing
- **Backward compat**: If `intellectual_style:` absent, read `fault_line.positions[]` directly

---

## Step 1 — Graduation Check

Before writing, confirm Tier 3 readiness:
1. **Atomic?** Only ONE claim — would splitting it make two better notes?
2. **Claim title?** Title states an arguable insight, not just a label? ("Declining powers initiate the most dangerous conflicts" — not "Hegemonic decline")
3. **Standalone?** A reader with NO vault access understands this note completely?
4. **No duplication?** Search `note_tiers.tier3.output_folder` first — no existing note with ≥70% overlap?

If any check fails: write a Tier 2 synthesis note in the relevant domain folder instead, and flag it as an evergreen candidate. Do not force graduation.

---

## Step 2 — Write the Note

**Filename**: `YYYYMMDDHHMM - Title as Claim.md` (actual current date)
**Location**: vault-config.md `note_tiers.tier3.output_folder`

```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: [note_tiers.tier3.type_value from vault-config.md]
domain: [slug from vault-config.md domains[]]
evergreen-candidate: true
[intellectual_style.engagement_axis.config_key]: "[one of engagement_axis.positions[] from vault-config.md]"
open_problems: [IDs from vault-config.md open_problems[]]
source: "[[Source]]"
aliases: []
---
```

Follow vault-config.md `note_template.synthesis.mandatory_sections` exactly. Every section is required.

**Requirements that cannot be omitted**:
- Opening paragraph: the structural problem this concept addresses, written as if the reader has zero vault context
- ≥1 case where the concept works AND ≥1 case where it fails or is complicated
- Synthesis instrument (Judgment Instrument / vault-equivalent): the `[engagement_field.name]` entry is MANDATORY; escape-valve entries ("No genuine [field] — justification") block Tier 3 placement
- Internal tensions: ≥1 grounded concretely using the style's format (read `intellectual_style.internal_tensions.format`)
- See Also: 4–8 wikilinks, ≥1 cross-domain
- Open Questions: ≥1 referencing an open problem by number (format from vault-config.md `open_problems[]`)

---

## Step 3 — Update Note Index

Append one row to `memory/note-index.md` (create with headers if absent):

```
| [relative-path] | T3 | [domain-slug] | true | [axis-position] | [op-ids] | — | [created-date] |
```
