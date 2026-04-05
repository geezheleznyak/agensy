---
description: Refresh a MOC with new notes added since last update
type: universal-protocol
audience: claude
---
# /update-moc [moc-name]

Refresh a Map of Content with all notes added since its last update.

**[moc-name]**: The MOC to update. Accepts partial name (e.g., "power" matches `MOC - Power & Strategy.md`).

**Runtime**: Read `vault-config.md` from the vault root before executing. Extract:
- `folder_structure.mocs` — MOC folder location
- `domains[]` — slug → folder mapping for domain scanning

**Cascade context**: If invoked as part of a chain (e.g., from `/arc` Step 5), vault-config.md is already in context — skip the re-read above. If invoked standalone, always read vault-config.md fresh.

---

## Step 1 — Identify MOC

Find the specified MOC in vault-config.md `folder_structure.mocs`. Read its current content and note the `updated` date in its frontmatter (or the last modification date if no frontmatter).

---

## Step 2 — Domain Scan

Determine which domain(s) this MOC covers. Scan the relevant domain folder(s) (from vault-config.md `domains[]`) for:
- Notes added after the MOC's last update date
- Maps added after the MOC's last update date
- Any notes that were moved, renamed, or deleted

---

## Step 3 — Classification

For each new note found:
- Read its frontmatter to confirm type, domain, and evergreen-candidate
- Classify: Tier 2 Synthesis | Tier 2 Reference | Tier 3 Judgment | Map

---

## Step 4 — MOC Update

Update the MOC:
- Add new Tier 2 synthesis notes to the "Tier 2 — Core Concepts" section as wikilinks
- Add new maps to the "Thinker & Framework Maps" section
- Add new Tier 3 notes to the "Tier 3 Judgment Notes" section (if the MOC tracks these)
- Update the `updated` date in frontmatter

Do not reorder existing entries — append only.

---

## Step 5 — Master Index Update

Find the Master Index MOC in vault-config.md `folder_structure.mocs`.
- Update the note count for the relevant domain
- Update the map count if new maps were added
- Update the "Last Updated" date for the domain
