---
description: Walk all domains, compare against coverage plan, list gaps and update counts
type: universal-protocol
audience: claude
---
# /coverage-audit

Systematic audit of the entire vault against the coverage plan. Produces an updated count table and prioritized gap list.

**Runtime**: Read `vault-config.md` from the vault root before executing. Extract:
- `domains[]` — slug, label, folder, priority, evergreen_candidate (the full domain list)
- `reference_docs.coverage_plan` — path to this vault's coverage plan document
- `note_tiers` — type_value fields for T1, T2, T3 classification
- `folder_structure.output` — location of Tier 3 notes
- `open_problems[]` — IDs and names for coverage check

**Flat structure detection**: Before Step 1, check if multiple domains share the same `folder` value. If yes (flat structure vault), switch to frontmatter-based classification: glob the shared folder once, read each note's `domain:` frontmatter field, and assign it to the matching domain slug. Do NOT walk the same folder multiple times.

---

## Step 1 — Domain Walk

**Standard (per-folder) vaults**: For each domain in vault-config.md `domains[]`, walk the domain's unique `folder`. Count notes per domain by folder.

**Flat structure vaults** (multiple domains share a folder — detected above): Glob each unique folder path once. For each note, read its `domain:` frontmatter field and assign to the matching domain slug. Count per domain from frontmatter, not folder.

For all vaults, classify each note as:
- **T1**: type = source, or file in `folder_structure.inbox` / `folder_structure.sources`
- **T2-Ref**: type = `note_tiers.tier2.type_value` AND `evergreen-candidate: false`
- **T2-Syn**: type = `note_tiers.tier2.type_value` AND `evergreen-candidate: true`
- **T3**: type = `note_tiers.tier3.type_value` (located in `folder_structure.output`)
- **Maps**: files ending in `-map.md`

Read frontmatter from each note to classify correctly. Do not guess from filename.

---

## Step 2 — Open Problem Coverage

For each open problem in vault-config.md `open_problems[]`:
- Count notes whose `open_problems` frontmatter includes this problem's ID
- Flag problems with 0 notes as critical gaps
- Flag problems with 1 note as coverage risks (single point of failure)

---

## Step 3 — Planned Note Status

Read `reference_docs.coverage_plan`. For each planned note listed:
- Check if a note with a matching title (or clear equivalent) exists in the relevant domain folder
- Mark as: ✅ complete | 🔄 partial | ⬜ missing

---

## Step 4 — Updated Coverage Table

Produce an updated version of the Domain Summary table from the coverage plan:

| Domain | Slug | Priority | T1 | T2-Ref | T2-Syn | T3 | Maps | Target T2 | Gap |
|---|---|---|---|---|---|---|---|---|---|

Use domain labels, slugs, and priorities from vault-config.md `domains[]`.
Also produce the updated Open Problem Coverage table.

---

## Step 5 — Priority Gap List

List the top 5 gaps by priority:
1. Highest-priority domain with lowest coverage relative to target
2. Open problems with zero notes
3. Planned notes that are dependencies for other planned notes (build these first)

Format each gap as: **Gap**: [what's missing] → **Action**: `/arc [recommended subject]`

---

## Step 6 — Update Coverage Plan

Update the Domain Summary table and Open Problem Coverage table in `reference_docs.coverage_plan` with current counts from this audit. Update the "Last audit" line in the document header with today's date.

---

## Step 7 — Rebuild Note Index (Side Effect)

Since Step 1 already read every note's frontmatter, write a fresh `memory/note-index.md` from the collected data. This is zero extra cost — the data is already in context.

Write the full table with one row per note:

```markdown
# Note Index
Last updated: YYYY-MM-DD | Total: N | Last full rebuild: YYYY-MM-DD (coverage-audit)

| Path | Tier | Domain | EC | Axis | OPs | Source | Created |
|---|---|---|---|---|---|---|---|
```

Abbreviate engagement axis positions (e.g., `structural` → `struct`, `behavioral-ideational` → `behav`, `complex-interactive` → `cplx`). Use the vault's axis positions from vault-config.md for abbreviation keys.

---

## Step 8 — Update Session State

Update `memory/session-state.md`:
- Reset `notes_since_last_audit` to `0`
- Update `last_coverage_audit` to today's date
- Write top 3 gaps from Step 5 to `open_actions`
- Update `last_updated`

Update `[AGENSY_PATH]/system-state.md` Vault Registry:
- Set **Notes** to the total note count from Step 1 (all T2-Ref + T2-Syn + T3, excluding maps and T1)
- Set **Last Audit** to today's date
- If this vault has no row yet, add it
