---
description: Check a note's graduation criteria and write the promoted Tier 3 version if ready
type: universal-protocol
audience: claude
---
# /promote [note-path]

Check whether a Tier 2 synthesis note is ready to graduate to Tier 3, and write the promoted version if it is.

**[note-path]**: Path to the note to evaluate (relative to vault root).

**Runtime**: Read `vault-config.md` from the vault root before executing. Extract:
- `note_tiers.tier2.graduation_rule` — criteria for Tier 3 graduation
- `note_tiers.tier3.output_folder` — destination for promoted notes
- `note_tiers.tier3.type_value` — frontmatter type value for Tier 3 notes
- `note_template.synthesis.mandatory_sections` — sections that must be complete
- `intellectual_style.engagement_field` — name, escape_valve, graduation_gate settings
- `folder_structure.mocs` — for MOC updates after promotion

---

## Step 1 — Read the Note

Read the specified note. Extract:
- Title
- All frontmatter fields
- All section content

---

## Step 2 — Graduation Criteria Check

Apply all 5 criteria (consult `note_tiers.tier2.graduation_rule` for vault-specific wording):

**Criterion 1 — Atomic**: Is this note about exactly ONE structural claim? Would splitting it make two better notes?
- Pass / Fail: [assessment]

**Criterion 2 — Claim title**: Does the title state an insight (a claim that can be argued for or against), not just a label?
- Current title: [title]
- Claim or label? [assessment]
- If label: Proposed claim title: [proposed]

**Criterion 3 — Synthesis instrument complete**: Does the vault's synthesis instrument section exist (Judgment Instrument / Connection to the Project / vault-equivalent)? Does it have a specific `[engagement_field.name]` entry?
- Instrument present: [yes / no]
- `[engagement_field.name]` entry: [present / missing — if missing, note is NOT ready]
- **Escape valve check**: If the entry reads "No genuine [field] — [justification]" (escape valve), this is acceptable at Tier 2 but BLOCKS Tier 3 promotion (per `intellectual_style.engagement_field.graduation_gate`). Note as promotion blocker.

**Criterion 4 — Standalone**: Can a reader with NO vault access understand this note completely? Does it assume prior knowledge of other vault notes?
- Pass / Fail: [assessment]
- If fail: What context is assumed that must be made explicit?

**Criterion 5 — Links verified**: Are all See Also wikilinks pointing to existing, well-developed notes?
- Check each link against the vault
- Broken or underdeveloped links: [list]

**Open problems** (bonus check): Does the Open Questions section reference ≥1 open problem by number?

---

## Step 3 — Graduation Decision

**If all 5 criteria pass**: Ready for promotion. Proceed to Step 4.

**If any criterion fails**: Do not promote. State which criteria failed and what changes are needed. Offer to make the changes and re-evaluate before writing the Tier 3 version.

---

## Step 4 — Write the Promoted Version (if ready)

**Location**: vault-config.md `note_tiers.tier3.output_folder`
**Filename**: Keep the timestamp; update the title if a stronger claim title was identified
**Frontmatter**: Change `type` to vault-config.md `note_tiers.tier3.type_value`

Apply improvements identified in the graduation check:
- Sharpen the title to a stronger claim if needed
- Make the opening paragraph fully standalone (no assumed vault context)
- Fill in any missing synthesis instrument entries
- Fix any broken See Also links

After writing the Tier 3 version:
1. Add a pointer at the top of the original Tier 2 note: `→ Promoted to [[output_folder/filename]]`
2. Update the relevant domain MOC and the Master Index MOC in `folder_structure.mocs`
3. **Update `memory/note-index.md`**: Find the row for the original Tier 2 note by path. Update Tier to `T3` and Path to the new output folder location. If the note does not appear in the index, append a new row.
