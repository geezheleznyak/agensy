---
description: Manage persistent unresolved questions across vaults and sessions
type: universal-protocol
audience: claude
---
# /question-bank [add|list|resolve]

Manage the cross-vault question bank. Questions that emerge from dialogue but cannot yet be answered — questions that span vaults, require future arcs, or reveal gaps the vault cannot yet fill — are logged here and surface in future sessions.

**Data file**: `[AGENSY_PATH]/question-bank.md`

**Why agensy**: Questions span vaults. "Does the recon-strike complex make operational maneuver obsolete?" touches bellum (tactics), but answering it draws on politeia (industrial capacity) and oeconomia (cost-exchange economics). The framework vault is the cross-vault coordination layer.

---

## Subcommand: `list`

Show all questions in `[AGENSY_PATH]/question-bank.md`.

1. Read `[AGENSY_PATH]/question-bank.md`.
2. Group questions by `status`: show `open` first, then `explored`, then `resolved`.
3. Within `open`: flag questions older than 30 days with ⚠️.
4. For each question: show ID, question text, vaults, open problems, age in days, source.

**Output format**:
```
## Open Questions (N total, M flagged ⚠️)

[N] [question text]
    Vaults: [vault1, vault2] | OPs: [vault: N] | Age: [days] | Source: [dialogue description]
    ⚠️ 45 days old — consider arc or /engage-problem

## Explored Questions (partial progress)
...

## Resolved Questions (for reference)
...
```

---

## Subcommand: `add "[question]" --vault [name] --op [N]`

Add a new question to the bank.

1. Read `[AGENSY_PATH]/question-bank.md`.
2. Check for near-duplicate questions (≥70% semantic overlap with existing open questions). If duplicate found → point to existing entry, do not add.
3. Assign the next sequential ID.
4. Append the new entry using the schema below.
5. Write the updated file.

**Entry schema**:
```yaml
- id: [N]
  question: "[question text]"
  vaults: [[vault names]]
  open_problems: [[vault]: [N], ...]
  generated: YYYY-MM-DD
  source: "[brief description of dialogue that generated this]"
  status: open
  resolution: null
```

**Can also be called implicitly** from `/dialogue` Step 4 (Route 3) — when dialogue generates an unresolved question, Claude runs this command automatically.

---

## Subcommand: `resolve [N] [note-path]`

Mark question N as resolved by a specific note.

1. Read `[AGENSY_PATH]/question-bank.md`.
2. Find question with `id: N`.
3. Update: `status: resolved`, `resolution: "[note-path] — [one sentence: how the note resolves the question]"`.
4. Write the updated file.
5. Confirm: "Question [N] resolved → [note-path]"

---

## Integration With Other Commands

| Command | Integration |
|---|---|
| `/dialogue` | Step 4 Route 3 calls `/question-bank add` automatically when dialogue generates an unresolved question |
| `/what-next` | Step 1 reads question bank. If open questions align with coverage gaps → surfaces the connection |
| `/coverage-audit` | Not integrated (question bank is meta-level, not domain coverage) |
| Session protocol | Type C check Step 5: surface question-bank entries relevant to the vault or stated intent |
| `/engage-problem` | Natural follow-up for questions tagged to a specific OP: "You have an open question on OP-4. An arc on [thinker] would address it." |
