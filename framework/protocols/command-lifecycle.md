---
type: reference
audience: claude
---

# Command Lifecycle Protocol

When to fire which command. The vault's analytical capacity is only fully deployed when commands are triggered at the right moments — not just when the user remembers to ask.

**Four trigger types**: Automatic (A), Milestone (B), Session (C), Analytical (D).

---

## Type A — Automatic (no user decision needed)

These commands fire as part of another command's internal protocol. No separate invocation needed.

| Trigger Event | Command Fired | Implementation |
|---|---|---|
| `/arc` completes | `/quick-check last-arc` | ✅ Built into arc Step 5 |
| `/arc` completes | `/update-moc` (internal) | ✅ Built into arc Step 4 |

---

## Type B — Milestone (fire after specific events)

Claude should suggest these without being asked when the trigger condition is met.

| Trigger Event | Command(s) to Run |
|---|---|
| 10–15 new notes accumulated since last audit | `/coverage-audit` |
| Phase or major milestone complete | `/coverage-audit` → `/axis-survey` → `/what-next` |
| Thinker/framework arc complete | `/domain-audit [domain]` |
| `/coverage-audit` reveals gap | `/what-next` or `/engage-problem [N]` |
| `/domain-audit` finds promotion candidates | `/promote [note]` for each candidate |
| 3+ T3/judgment notes written since last survey | `/axis-survey` |
| `/axis-survey` reveals underrepresented engagement axis position | `/arc` targeting that position |
| Dialogue-derived note is 30+ days old | `/revisit [note-path]` |
| `/arc` completes in domain where user has existing dialogue-derived notes | Flag: "You have N user positions in this domain — does the new material challenge any?" |

**Cascade rule**: When multiple commands chain in sequence (e.g., `/coverage-audit` → `/axis-survey` → `/what-next` after a phase), vault-config.md is read ONCE at the start of the chain. Subsequent commands inherit the loaded config — do not re-read. See Reading Conventions below.

---

## Type C — Session Protocol (every session start, ~15 seconds)

A **state check**, not full command execution. Run this silently at the start of each session before responding to the user's stated intent.

1. Read `memory/session-state.md` (see Session State below). This file pre-computes all diagnostic state — no vault globbing needed.
2. If `memory/session-state.md` does not exist, fall back: read `memory/MEMORY.md` and estimate state from what's available.
3. Check thresholds from session-state.md:
   - `notes_since_last_audit ≥ 15` → mention `/coverage-audit` is due
   - `last_axis_survey` more than ~60 days ago → mention `/axis-survey` is due
   - `open_actions` not empty → surface the top item
4. If user's intent is stated, proceed directly — do not run diagnostic commands.
5. If user's intent is unclear AND session-state.md is absent or stale → run `/what-next` as fallback.

**Output**: 1–3 sentences max. Mention any overdue commands. Then proceed to the user's request. Do not auto-run commands — only surface them.

---

## Type D — Analytical (user-initiated, with proactive suggestion)

Powerful but under-used commands. Claude should proactively suggest these when conditions are met — the user should not need to remember them.

| Command | When to Suggest It |
|---|---|
| `/engage-problem [N]` | After `/coverage-audit` shows an OP with <3 notes; user expresses interest in a challenge area |
| `/engage-deep [claim]` | After `/arc` when the subject's core claim challenges existing vault positions; user says "I'm not sure I agree with..." |
| `/compare [A] and [B]` | Two subjects in the same domain make overlapping or competing claims; user asks "how does X relate to Y?" |
| `/synthesis [question]` | Vault has 5+ notes relevant to a driving question; after 2+ arcs in the same domain |
| `/promote [note]` | After `/domain-audit` identifies candidates; user flags a note as especially important |
| `/dialogue` | User expresses a personal position, asks an open question, or shows uncertainty about their own view |
| `/revisit [note]` | Dialogue-derived note is 30+ days old; major arc completed in same domain since the note was written |
| `/question-bank list` | At session start if question bank has open entries; after `/coverage-audit` to check for question-arc alignment |
| `/positions` | After 3+ dialogues have produced notes; before starting a new arc to check what the user already thinks |

---

## Lifecycle Flow Summary

```
Session Start (Type C check)
    ↓
Arc completes → Type A automatic (quick-check + update-moc)
    ↓  [if 10–15 notes accumulated]
/coverage-audit → reveals gaps → /what-next or /engage-problem  [Type B]
    ↓  [per thinker/domain arc]
/domain-audit → finds candidates → /promote  [Type B]
    ↓  [every 3+ T3 notes written]
/axis-survey → underrepresented position → new /arc  [Type B]
    ↓  [user expresses position or uncertainty]
/dialogue → note → /revisit after 30 days  [Type D → Type B]
    ↓  [periodically]
/positions  [Type D] — survey of user's own intellectual landscape
```

**Quarterly cross-vault check** (every ~90 days): Run `/coverage-audit` in each active vault, then `/axis-survey` if 3+ T3 notes exist. This ensures note-index.md and session-state.md stay accurate across all vaults. Session-state.md `last_coverage_audit` field tracks this per vault — the Type C check surfaces it when overdue. Use the `/schedule` skill to set up an automated reminder if desired.

---

## Reading Conventions

### Cascade reading rule

vault-config.md is re-read fresh for each **standalone** command invocation. Context compression in long sessions can degrade earlier reads, so re-reading ensures accuracy.

**Exception — within a tight cascade**: When a protocol chains sub-commands immediately (e.g., `/arc` → `/update-moc` → `/quick-check`), vault-config.md is already fresh in context from the parent command. Chained sub-commands should skip their vault-config.md read. This is enforced by "if chained" notes in the individual protocol files — not by a session-wide rule.

### Session State (`memory/session-state.md`)

Maintained in each vault's `memory/` folder. Updated by commands at protocol end.

```markdown
# Session State
last_updated: YYYY-MM-DD
notes_since_last_audit: N
last_coverage_audit: YYYY-MM-DD
last_axis_survey: YYYY-MM-DD
last_what_next: YYYY-MM-DD
open_actions:
  - "[action item from last what-next or coverage-audit]"
recent_arcs:
  - "[subject] ([domain-folder]) — YYYY-MM-DD"
```

**Update triggers** (written at end of protocol execution):
- `/arc`: increment `notes_since_last_audit` by number of notes written; append to `recent_arcs`
- `/coverage-audit`: reset `notes_since_last_audit` to 0; update `last_coverage_audit`; write `open_actions` from gap list
- `/axis-survey`: update `last_axis_survey`
- `/what-next`: update `last_what_next`; write `open_actions` from recommendation

### Note Index (`memory/note-index.md`)

A single-file cache of all notes' frontmatter metadata. Replaces hundreds of individual file reads for bulk classification commands.

```markdown
# Note Index
Last updated: YYYY-MM-DD | Total: N | Last full rebuild: YYYY-MM-DD (coverage-audit)

| Path | Tier | Domain | EC | Axis | OPs | Source | Created |
|---|---|---|---|---|---|---|---|
| theory/power/202603281200 - Title.md | T2 | power | true | materialist | 1,4 | — | 2026-03-28 |
| 20-Output/Claim Title.md | T3 | theory | true | interactive | 2 | — | 2026-03-27 |
```

**Column key**: EC = evergreen-candidate | Axis = engagement axis position (abbreviated) | OPs = open_problem IDs | Source = user-dialogue/user-reflection/—

**Incremental updates** (appended by note-creating commands):
- `/arc`: append 8–12 rows after note creation
- `/evergreen-note`: append 1 row
- `/dialogue` Route 1: append 1 row with `Source: user-dialogue`
- `/promote`: update Tier field (T2 → T3) and Path for the promoted note

**Full rebuild** (zero extra cost — `/coverage-audit` already reads every note):
- `/coverage-audit` rebuilds the entire index as a side effect of Step 1

**Fallback**: If `memory/note-index.md` does not exist or `Last updated` is more than 30 days old, any command that reads it should fall back to direct glob-and-read and rebuild the index as a side effect.

**Commands that read the index** (instead of globbing individual files):
- `/coverage-audit` — after rebuild: analyzes from index
- `/domain-audit` — filter index by Domain column
- `/axis-survey` — filter index by Axis column
- `/positions` — filter index by Source column (cross-vault: read one index per vault)

---

## Dialogue Log

Track dialogue activity in each vault's `memory/MEMORY.md` under a **Dialogue Log** section:

```
## Dialogue Log
- YYYY-MM-DD | topic | mode (interrogate/reflect/challenge/bridge) | position (one-sentence user stance, or —) | outcome (Route N: note path / question-bank entry / no output)
```

This log enables:
- Session protocol Step 5 (surface relevant question-bank entries)
- `/revisit` trigger (30-day check for dialogue-derived notes)
- `/positions` (cross-vault survey of user-originated knowledge)

**Bridge mode**: When mode = `bridge` and a clear position emerged, `/dialogue` Step 6 also appends to `[AGENSY_PATH]/system-state.md` Cross-Vault Positions — see that file.
