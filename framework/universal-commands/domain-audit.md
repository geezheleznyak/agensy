---
description: Deep audit of one domain — inventory, quality check, promotion candidates, coverage gaps
type: universal-protocol
audience: claude
---
# /domain-audit [domain-slug]

Deep audit of a single domain. More thorough than `/coverage-audit` for the same domain — includes quality checks and promotion candidates.

**[domain-slug]**: A slug from vault-config.md `domains[].slug`.

**Runtime**: Read `vault-config.md` from the vault root before executing. Extract:
- `domains[]` — find the entry matching [domain-slug]: label, folder, priority, evergreen_candidate
- `reference_docs.coverage_plan` — path to coverage plan for gap analysis
- `note_template.synthesis.mandatory_sections` — quality check criteria
- `intellectual_style` — engagement_field (name) for quality checks
- `note_tiers` — type_value fields for inventory classification
- `folder_structure.output` — location of Tier 3 notes

---

## Step 1 — Inventory

**If `memory/note-index.md` exists and is current (< 30 days old)**:
- Filter index rows by Domain = `[domain-slug]`. No globbing needed.
- Use the index data directly for the inventory table below.

**If no index or index is stale**: Glob the domain's folder (from vault-config.md `domains[]` matching [domain-slug]). Append any new rows to `memory/note-index.md` as a side effect.

For each note found, read frontmatter and record:
- Filename and title
- Type (source | Tier 2 type | Tier 3 type — from vault-config.md `note_tiers`)
- Schema (`evergreen-candidate: true` | `false`)
- Engagement axis position (from `[engagement_axis.config_key]` frontmatter field)
- Open problems referenced
- Created date

---

## Step 2 — Quality Check

For each synthesis-schema note (`evergreen-candidate: true`), check each mandatory section from vault-config.md `note_template.synthesis.mandatory_sections`:

- [ ] Opening paragraph states the structural problem that forced this concept into existence?
- [ ] Synthesis instrument section (Judgment Instrument / vault-equivalent) exists with a `[engagement_field.name]` entry?
- [ ] Internal Tensions has ≥1 tension grounded concretely using the vault's style format (read `intellectual_style.internal_tensions.format`)?
- [ ] See Also has 4–8 wikilinks with ≥1 cross-domain link?
- [ ] Open Questions references ≥1 open problem by number?

Flag notes failing quality checks. These need revision before graduation.

---

## Step 3 — Promotion Candidates

For each synthesis-schema note, apply the Tier 2 → Tier 3 graduation criteria (vault-config.md `note_tiers.tier2.graduation_rule`):
1. Atomic (ONE claim)?
2. Title states a claim, not just a label?
3. Synthesis instrument complete, including a specific `[engagement_field.name]` entry (escape-valve entries block promotion)?
4. Standalone — reader with no vault access understands completely?
5. All See Also links verified as existing and well-developed?

Flag notes meeting all 5 criteria as **promotion candidates**.

---

## Step 4 — Coverage Gap Analysis

Read vault-config.md `reference_docs.coverage_plan`. Compare domain inventory against planned notes for this domain:
- Which planned notes exist (matched by title)?
- Which planned notes are missing?
- Which open problems in the domain plan have no notes yet?

---

## Step 5 — Domain Report

Produce a structured report:

**Domain**: [label from vault-config.md]
**Note counts**: T1: N | T2-Ref: N | T2-Syn: N | T3: N | Maps: N

**Quality issues**: Notes needing revision + what's missing from each

**Promotion candidates**: Notes meeting all 5 graduation criteria, ready for `/promote`

**Coverage gaps**: Planned notes not yet written, ordered by priority

**Recommended next action**: The single highest-value action to take in this domain right now
