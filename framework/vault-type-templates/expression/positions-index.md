---
title: "Positions Index"
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: positions-index
status: active
purpose: Cross-vault pointer table for substantive analytical claims earned in essays. Pre-loaded index only; T3 bodies loaded on-demand at `/article-seed` Step 2.6. Scales to hundreds of entries without bloating working context.
---

# Positions Index

Cross-vault register of substantive framework claims the writer holds. Each row points to a T3 judgment note in a source vault that carries the claim's mechanism, pressure, and backlinks. Essays surface new claims; the harvest loop at `/article-promote` Step 7 classifies and promotes them here.

**Pre-loaded**: this index is read by every `/article-*` command. **T3 bodies are not pre-loaded** — they are fetched on-demand when a topic match fires at seed-time.

**Distinct from**:
- `writer-positions.md` — bedrock commitments, methodological moves, dispositions. User-authored. Always active.
- Source-vault T3s — where the substantive claim *lives*. This index is a pointer, not the content.

---

## Schema

| Column | Meaning |
|---|---|
| **ID** | `P###` sequential. Never reused even if superseded/retired. |
| **Claim** | One-sentence compression of the position. Grep-readable. |
| **Source T3** | Wikilink to the T3 note carrying full mechanism + pressure + cases. |
| **Topics** | Comma-separated keyword list. Grepped at seed-time against source-map keywords. |
| **Originating Essay** | Wikilink to the essay in `40-Published/` that surfaced the claim. |
| **Status** | `active` \| `superseded` \| `retired` \| `under-review` |
| **Registered** | Date (YYYY-MM-DD) |

**Status meanings**:
- `active` — use and build on; surfaces in seed-time lookups.
- `superseded` — replaced by a later P###. Row kept; `Claim` column gets suffix `→ P###`.
- `retired` — claim no longer held. Row kept for traceability; does not surface in seed-time lookups.
- `under-review` — next essay will revisit; may promote back to `active` or demote to `retired`.

---

## Active Positions

*(Empty at bootstrap. Rows added automatically by `/article-promote` Step 7 harvest loop after each published essay.)*

| ID | Claim | Source T3 | Topics | Originating Essay | Status | Registered |
|---|---|---|---|---|---|---|

---

## Superseded / Retired

*(Populated when an active position is superseded by a later essay or retired by the author.)*

---

## Lookup protocol (seed-time)

At `/article-seed` Step 2.6, after preset inference:

1. Extract **topic keywords** from the source map(s): founding-problem nouns, first-principles nouns, core-concept names.
2. Grep this file's `Topics` column against keywords. Ignore `retired` and `superseded` rows.
3. Rank matches by keyword-overlap density (count of distinct topics matched).
4. Fetch T3 notes for the top 5 matches. Read each T3's claim + mechanism + pressure.
5. Classify the relation of each match to the current essay's thesis:
   - `supports` — the T3 claim reinforces what the essay will argue.
   - `extends` — the essay builds on the T3 claim into a new domain.
   - `tensions-with` — the T3 claim complicates or pressures the essay's thesis; must be engaged.
   - `orthogonal` — same topic, different question; cite for context at most.
6. Record in the seed frontmatter:
   ```yaml
   matched_positions:
     - id: P001
       relation: supports
       t3: "[[source_vault/20-Judgment/...]]"
   ```

Empty match list is fine and common. More than 5 matches: surface the top 5; user confirms which to load.

---

## Harvest protocol (promote-time)

At `/article-promote` Step 7, before archive move:

1. Diff essay claims vs source-map atomics + any `matched_positions` T3s.
2. Novel claims classified:
   - **Substantive framework claim** → new T3 in relevant source vault + new row here.
   - **Methodological claim** → append to `writer-positions.md` §"Preferred Analytical Moves" or §"Recurring Dispositions".
   - **Essay-specific** → remains in essay only; no promotion.
3. User confirms each classification before execution. Rejections do not block promote.
4. Accepted T3 promotions: write T3 file using the source vault's template; append row here with next `P###`.
5. Accepted methodological promotions: append a line to the appropriate writer-positions section with a one-line rationale + essay backlink.

---

## Maintenance

- **Pruning**: retain all rows (active/superseded/retired) for traceability. Seed-time lookup filters `active` only.
- **Renumbering**: never. IDs are permanent references.
- **Conflict resolution**: when two active positions contradict, seed-time surfacing lets the user choose which to build on and which to engage as `tensions-with`. Persistent conflict may trigger a position-revision essay.
- **Cross-vault applicability**: a claim may apply across vaults even if the T3 lives in only one. Capture cross-vault reach via the `Topics` column (include vault-level keywords when applicable).
