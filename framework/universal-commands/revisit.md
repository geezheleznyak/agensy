---
description: Re-engage a dialogue-derived note with current vault context
type: universal-protocol
audience: claude
---

# /revisit [note-path]

Re-engage a dialogue-derived note against the vault's current state. The vault has grown since the note was written. Does the position still hold? Has new material confirmed, challenged, or complicated it?

**When to use**:
- A dialogue-derived note is 30+ days old (lifecycle protocol flags this)
- A major arc has been completed in the same domain as a dialogue-derived note
- The user says "I'm not sure I still believe what I wrote about X"

**Runtime**: Read `vault-config.md` from the vault root before executing. Extract:
- `folder_structure.output` — where user-dialogue notes live
- `open_problems[]` — for checking whether the note's OP connections still hold
- `fault_line` — for checking whether the fault-line position has shifted

---

## Step 1 — Read the Original Note

Read `[note-path]`. Record:
- The core claim (note title + opening paragraph)
- The fault-line position
- Creation date
- Open problems addressed
- Which notes it links to in See Also

---

## Step 2 — Find New Vault Material

Search for notes added **after** the original's creation date that are relevant to the same domain or open problems:

1. Glob all notes in the relevant domain folder.
2. Filter to notes with `created:` date AFTER the original's creation date.
3. Read frontmatter and opening paragraphs of candidates.
4. Identify: which new notes are **relevant** to the original's claim? (Same domain, same OP, or overlapping fault-line position.)

---

## Step 3 — Assess Impact

For each relevant new note found, assess its relationship to the original claim:

| Relationship | Definition | Example |
|---|---|---|
| **Supports** | New note provides evidence or a mechanism that strengthens the original claim | New historical case confirms the pattern |
| **Challenges** | New note's core claim contradicts or significantly qualifies the original | New thinker argues the opposite mechanism |
| **Complicates** | New note introduces a condition or exception that limits when the original holds | New note shows the claim is domain-specific |
| **Orthogonal** | New note is in the same domain but does not bear on the original claim | Different aspect of the same problem |

---

## Step 4 — Present to User

State: "Since you wrote [note title] on [date], the vault has added [N] relevant notes in [domain]. Here is what they do to your position:"

For each **challenges** or **complicates** relationship: state precisely what is threatened and how.
For each **supports** relationship: state what evidence has accumulated.

Then ask: **"Has your position changed?"**

Offer three options:
1. "Position holds" → Annotate the note's frontmatter: `revisited: YYYY-MM-DD`
2. "Position has evolved" → Update the note OR write a successor note with `source: user-dialogue, supersedes: [original path]`
3. "Position is now uncertain" → Enter `/dialogue` mode to work through the tension

---

## Step 5 — Write (if position evolved)

**If updating existing note**: Edit the note's body to reflect the evolved position. Update `updated:` frontmatter. Add a `## Revision Note` section at the bottom explaining what changed and why.

**If writing successor note**: Run `/evergreen-note` protocol with `source: user-dialogue`. Link back to the original note in See Also with: `[[Original Note]] (superseded — see this note for evolved position)`. Update the original note's frontmatter: `superseded_by: [new path]`.

**If position holds**: Add `revisited: YYYY-MM-DD` to the note's frontmatter. No other changes.

---

## Step 6 — Log

Update the vault's dialogue log:
```
- YYYY-MM-DD | revisit: [note title] | outcome: [holds / evolved → new path / uncertain → entered dialogue]
```
