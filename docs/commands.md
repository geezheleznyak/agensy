---
type: documentation
audience: human
---

# Command Reference

AGENSY provides **16 canonical commands** plus 3 additional files for legacy compatibility and arc sub-protocols. All commands are invoked inside an Obsidian vault that has Claude Code running.

Full protocol files live in `framework/universal-commands/[command-name].md`. The descriptions below tell you what each command does and when to use it — not how Claude executes it internally.

> **You don't need to memorize commands.** Slash commands are shorthand. You can describe any operation in plain English — "run a full arc on Keynes", "audit my domain coverage", "show me where my notes sit on the engagement axis" — and Claude will run the protocol. Commands exist for muscle-memory efficiency, not because they're required.

---

## Core Build Commands

### `/arc [subject]`
**What it does**: Runs a full synthesis sprint on one subject. Produces 8–12 Tier 2 notes covering the subject from multiple angles, updates the domain MOC, and automatically runs `/quick-check` to validate quality.

**When to use**: This is your primary work command. Use it whenever you want to build coverage on a subject. One arc per session is a good pace.

**Output**: 8–12 notes in the relevant domain subfolder + updated MOC. Each arc map includes a **Primary Sources** section — 3–5 canonical texts with one-line annotations on why each is load-bearing. If you're new to a subject and want reading suggestions first, ask Claude before invoking the command.

---

### `/evergreen-note [subject]`
**What it does**: Creates a single Tier 3 judgment note on a subject. Tier 3 notes are standalone, permanent, claim-titled. They represent your considered judgment, not analysis in progress.

**When to use**: When you have enough Tier 2 coverage on a subject to take a definitive position. Typically after 2–3 arcs on a topic.

**Output**: One T3 note in the vault's output folder.

---

### `/promote [note-path]`
**What it does**: Checks whether a Tier 2 note meets graduation criteria for Tier 3 and promotes it if it does. If not, explains what's missing.

**When to use**: When you have a T2 note you think is ready for permanent status.

**Output**: Promoted T3 note, or a gap report explaining what's needed.

---

## Diagnostic Commands

### `/coverage-audit`
**What it does**: Walks every domain in the vault, counts notes by type, identifies gaps (domains with thin or no coverage), and writes a gap report. Also updates `system-state.md` with your current note count and audit date.

**When to use**: After every 3–4 arcs. At the start of any session after a gap. When you don't know where to work next.

**Output**: Domain-by-domain coverage table + top 3 recommended gaps to fill.

---

### `/domain-audit [domain]`
**What it does**: Deep audit of one specific domain — note quality, coverage gaps, engagement axis distribution, missing connections.

**When to use**: When a domain feels thin or incoherent. More focused than `/coverage-audit`.

**Output**: Detailed domain analysis with specific note-level recommendations.

---

### `/axis-survey`
**What it does**: Surveys all synthesis notes and maps their positions on the vault's engagement axis. Produces a distribution showing where your vault's intellectual weight falls.

**When to use**: Monthly, or after a major arc run. Reveals if your vault is drifting toward one side of the axis or if you're avoiding the tension.

**Output**: Axis distribution table + diagnosis (balanced / skewed / avoiding).

---

### `/what-next`
**What it does**: Reviews your coverage audit results, open problems list, and current MOC state to recommend the highest-value next arc subject.

**When to use**: Any time you're not sure where to work. Also at the start of a session.

**Output**: Ranked list of recommended next subjects with rationale.

---

## Synthesis and Engagement Commands

### `/synthesis [question]`
**What it does**: Takes one of your vault's open problems and produces a position statement — your vault's current considered answer, drawing on existing notes.

**When to use**: When you want to crystallize your vault's position on a question rather than add more notes.

**Output**: A position statement note, or a gap analysis if coverage is insufficient.

---

### `/engage-problem [problem-number]`
**What it does**: Deep dive on one of your vault's 12 open problems. Marshals existing evidence, identifies what's missing, and produces either a position or a targeted arc recommendation.

**When to use**: When working on a specific open problem directly.

**Output**: Problem analysis + either a synthesis position or a targeted arc recommendation.

---

### `/engage-deep [subject]`
**What it does**: Rigorous adversarial encounter with a subject — challenges your existing notes, pushes on the engagement axis, identifies where your analysis is weakest.

**When to use**: When you want genuine intellectual friction rather than synthesis. Use on subjects where you feel you've reached easy agreement with yourself.

**Output**: Challenge report + recommended responses.

---

### `/dialogue [topic] [mode]`
**What it does**: Turns the vault into a thinking partner for multi-turn conversation. Three modes:
- **Probe** — Claude probes your reasoning with targeted questions
- **Challenge** — Claude argues against your current position
- **Bridge** — Claude connects this vault's thinking to another vault's domain

Positions that emerge in `Bridge` mode are tracked in `system-state.md`.

**When to use**: When you want to think through a problem, not just build notes. Use it when you're stuck or when a position feels too comfortable.

**Output**: Dialogue transcript + optional new synthesis note (Route 1/2/3 depending on what emerges).

---

## Orientation Commands

### `/update-moc [domain]`
**What it does**: Refreshes a domain MOC with recently added notes, reorganizes by theme if needed, and surfaces notes that should be promoted.

**When to use**: Automatically triggered after `/arc`. Also run manually if a domain MOC feels stale.

**Output**: Updated MOC file.

---

### `/arc-survey` (alias: `/axis-survey`)
See `/axis-survey` above.

---

### `/compare [subject-A] [subject-B]`
**What it does**: Structural comparison of two subjects, thinkers, or frameworks — similarities, divergences, and what the comparison reveals about the engagement axis.

**When to use**: When you want to understand the relationship between two things your vault covers. Especially useful for thinker-level comparisons.

**Output**: Comparison note in the relevant domain.

---

### `/positions`
**What it does**: Cross-vault survey of all positions you've taken in dialogues. Pulls from `system-state.md` and dialogue logs to give you a map of your own intellectual commitments across all vaults.

**When to use**: When you want a bird's-eye view of your own positions — useful before writing, before a dialogue, or when checking for contradictions.

**Output**: Position survey across all registered vaults.

---

### `/revisit [note-path]`
**What it does**: Re-engages a note that emerged from a previous dialogue. Checks if your position has evolved, whether new notes should be incorporated, and whether it's ready for Tier 3.

**When to use**: When revisiting older dialogue-derived notes that may have been superseded by new arcs.

**Output**: Updated note + progression recommendation.

---

### `/question-bank [subcommand]`
**What it does**: Manages the persistent cross-vault question register. Subcommands: `list`, `add "[question]" --vault [name] --op [N]`, `resolve [N] [note-path]`.

**When to use**: When a `/dialogue` session generates a question too big to answer in the current arc. Captures it for future work instead of losing it.

**Output**: Updated `question-bank.md`.

---

## Additional Files (Not Standalone Commands)

| File | Purpose |
|---|---|
| `quick-check.md` | Sub-protocol invoked automatically by `/arc` — validates arc output quality. Not a standalone command. |
| `confront.md` | Legacy protocol for adversarial engagement (pre-v1.0). Superseded by `/engage-deep`. Kept for backward compatibility. |
| `fault-line-survey.md` | Legacy protocol for engagement axis survey (pre-v1.0). Superseded by `/axis-survey`. Kept for backward compatibility. |

---

## Command Trigger Reference

| Type | Commands |
|---|---|
| **Automatic (A)** | `quick-check` (after arc), `update-moc` (after arc) |
| **Milestone (B)** | `promote`, `evergreen-note` |
| **Session start (C)** | `what-next`, `coverage-audit` |
| **Analytical (D)** | `dialogue`, `engage-deep`, `engage-problem`, `synthesis`, `compare`, `axis-survey`, `domain-audit`, `positions`, `revisit`, `question-bank` |

See `framework/command-lifecycle.md` for the full trigger protocol.
