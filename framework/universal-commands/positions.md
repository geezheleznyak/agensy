---
description: Cross-vault survey of the user's own intellectual positions
type: universal-protocol
audience: claude
---

# /positions

Survey all knowledge vaults for notes the user has originated through dialogue or reflection. Output a structured map of the user's current intellectual positions, grouped by vault and open problem, with internal tensions flagged.

**When to use**:
- Periodically (every 1–2 months) to see how thinking has evolved
- After a burst of dialogues
- Before starting a major new arc, to check what the user already thinks in that domain

**Runtime**: This command reads across vaults. It does not require vault-config.md — it operates on any vault specified by the user, or all active knowledge vaults by default.

---

## Step 1 — Search All Vaults

For each active knowledge vault (omega, belli, kratos, oikos):

**If `memory/note-index.md` exists in that vault and is current (< 30 days old)**:
- Read the vault's `memory/note-index.md` — one file read per vault
- Filter rows where Source = `user-dialogue` or `user-reflection`
- Collect from index: path, vault, domain, axis position, open problem IDs, created date

**If no index or index is stale for a vault**: Fall back to globbing that vault's output and Tier 2 folders; read frontmatter of every note found. Rebuild that vault's `memory/note-index.md` as a side effect.

At scale (4 vaults × ~200 notes each), the index reduces ~800 file reads to 4 file reads.

---

## Step 2 — Group by Vault and Open Problem

For each vault:
1. Group user-originated notes by domain.
2. Within each domain, list: note title (= the user's position) + creation date.
3. Map each note to the open problem(s) it addresses.
4. Identify open problems in each vault with **no** user-originated notes.

---

## Step 3 — Extract Core Claims

For each user-originated note found:
- State the core claim in one sentence (note title + opening paragraph).
- State the engagement axis position.
- State the date written.

---

## Step 4 — Flag Tensions

Scan across all vaults for internal tensions in the user's own positions:

**Intra-vault tensions**: Two user-originated notes in the same vault that take opposing positions on the same question. Example: "In Note A you argue X. In Note B (same vault) you argue not-X."

**Cross-vault tensions**: User-originated notes in different vaults that make claims that conflict when applied to the same situation. Example: "In belli you argue that technology creates discontinuity. In omega you argue that structural complexity is continuous. These positions conflict when applied to AI-driven warfare."

For each tension: name the two notes, state the conflict precisely, ask whether this is an unresolved contradiction or a domain-specific qualification.

---

## Step 5 — Output: Position Map

```markdown
## User Position Map — [date]

### [Vault Name]

**Domain: [slug]**
- [Note title] — [engagement axis position] — [date] — [open problems covered]
- ...

**Open problems with no user position yet**: OP-N, OP-M, ...

---

### Cross-Vault Tensions (flag for discussion)

1. **[Note A in vault X]** vs **[Note B in vault Y]**: [precise statement of conflict]
   → Unresolved contradiction / Domain-specific qualification?

---

### Coverage Summary

| Vault | User notes | OPs with user positions | OPs without |
|---|---|---|---|
| omega | N | N | list |
| belli | N | N | list |
| kratos | N | N | list |
| oikos | N | N | list |
```

---

## Step 6 — Suggest Next Dialogue

Based on the coverage gaps and tensions identified:
- Which open problem most needs a user position?
- Which cross-vault tension most needs resolution?

Suggest a specific `/dialogue` prompt that would address the highest-priority gap.
