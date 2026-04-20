---
type: reference
audience: claude
---
# Slash Command Suite

Index of all commands across the synthesis vault system. **Source of truth for protocol logic**: universal commands live in `framework/universal-commands/[command-name].md`. Vault stubs in `.claude/commands/` are 3-line pointers — they contain no protocol logic.

**Command lifecycle and trigger types**: See `framework/command-lifecycle.md`.

---

## Stub Format

Every universal command has a thin stub in `[vault root]/.claude/commands/`:

```markdown
---
description: [one-line description]
---

# /[command-name] [args]

$ARGUMENTS

1. Read the protocol: `[AGENSY_PATH]/framework/universal-commands/[command-name].md`
2. Read vault configuration: `vault-config.md` (vault root)
3. Execute the protocol using this vault's parameters.
```

Vault-specific commands (unique to one vault) stay as full protocol files in `.claude/commands/`, but must read `vault-config.md` for parameters — no hardcoded vault values.

---

## Universal Commands (21 protocol files + 2 backward-compat aliases)

| Command | Trigger type | Protocol file |
|---|---|---|
| `/arc [subject] [type]` | User | `universal-commands/arc.md` |
| `/coverage-audit` | Milestone (15 notes) | `universal-commands/coverage-audit.md` |
| `/axis-survey` | Milestone (3+ T3 notes) | `universal-commands/axis-survey.md` |
| `/what-next` | Post audit / unclear intent | `universal-commands/what-next.md` |
| `/promote [note-path]` | Post domain-audit | `universal-commands/promote.md` |
| `/compare [s1] and [s2] on [q]` | User | `universal-commands/compare.md` |
| `/engage-problem [N or name]` | User / post-audit gap | `universal-commands/engage-problem.md` |
| `/synthesis [question]` | User (2+ arcs in domain) | `universal-commands/synthesis.md` |
| `/update-moc [moc-name]` | Auto (post-arc) | `universal-commands/update-moc.md` |
| `/evergreen-note [concept]` | User | `universal-commands/evergreen-note.md` |
| `/engage-deep [claim]` | User / post-arc | `universal-commands/engage-deep.md` |
| `/domain-audit [domain-slug]` | Post arc | `universal-commands/domain-audit.md` |
| `/quick-check` | Auto (end of arc) | `universal-commands/quick-check.md` |
| `/dialogue [topic]` | User | `universal-commands/dialogue.md` |
| `/positions` | User (3+ dialogues) | `universal-commands/positions.md` |
| `/revisit [note-path]` | Milestone (30+ days) | `universal-commands/revisit.md` |
| `/question-bank [add\|list\|resolve]` | User | `universal-commands/question-bank.md` |
| `/system-query [query]` | User | `universal-commands/system-query.md` |
| `/system-audit` | Milestone (post coverage-audit) | `universal-commands/system-audit.md` |
| `/system-build [mode] [args]` | User | `universal-commands/system-build.md` |
| `/system-bridge [mode] [peer]` | User | `universal-commands/system-bridge.md` |

**Backward-compat aliases** (adversarial vaults only): `/confront` = `/engage-deep`, `/fault-line-survey` = `/axis-survey`

**System Model Layer commands** (v0.1): `/system-query` is always available where a vault has a `system-model.yaml`; `/system-audit` fires on the same cadence as `/coverage-audit`. `/system-build` is the only write path into `system-model.yaml` — read-only commands never mutate it. `/system-bridge` is a read-only binding reconciliation tool that proposes edits and routes writes through `/system-build`. See `framework/system-model-architecture.md`.

---

## Generated Commands by Vault Type

Added during Phase 1, Document 9 of the Genesis Protocol. These live as full protocol files in `.claude/commands/` — they are vault-type specific and NOT in `universal-commands/`. Commands marked (→ universal) are now universal and stubs point to `universal-commands/` instead.

### Accumulation Vault Commands

**`/engage-deep [thinker/concept/claim]`** → see `universal-commands/engage-deep.md` (now universal)
*Note: adversarial vaults may also invoke as `/confront` (alias).*

**`/derive [step in derivation]`**
Attempt one step in the vault's core derivation (e.g., cosmology → anthropology → ethics). Protocol:
1. State the step: what does the derivation need to establish?
2. List vault notes that bear on this step
3. State the strongest available argument from vault material
4. State what is still missing (the gap the next arc should fill)
Output: structured derivation note in `00-Inbox/`

### Training Vault Commands

**`/wargame [scenario]`**
Generate a CPX/exercise training document. Protocol:
1. Establish scenario context (force, mission, theater, adversary)
2. Generate 5–7 decision points in sequence
3. For each decision point: situation → information available → options → model answer → key lesson
4. Identify which curriculum phase each decision point belongs to
Output: complete training document in `50-Curriculum/` or equivalent

**`/red-team [concept/plan]`**
Adversarial analysis. Protocol:
1. State the concept or plan to be red-teamed
2. Decompose its core assumptions (3–5 assumptions)
3. For each assumption: state the strongest counter-move an intelligent adversary would make
4. Identify which friction condition is most likely to break the concept
5. State what modifications would make the concept more robust
Output: red-team analysis in `00-Inbox/`

**`/stress-test [concept]`**
Systematic friction testing. Protocol:
1. State the concept
2. Test against each of 5 friction stressors: fog, friction, fear, fatigue, adaptive adversary
3. For each stressor: describe how the concept performs; where it breaks; what the failure mode is
4. State the fault-line position of the concept under stress
Output: stress-test analysis in `00-Inbox/`

### Expression Vault Commands

**`/draft [title or thought-note path]`**
Expand a Thought into an Essay. Protocol:
1. Read the source Thought note (or take the title as the seed claim)
2. Identify the core argument (one sentence)
3. Identify 3–5 supporting points and the strongest objection
4. Find source_refs that ground the argument (search the connected knowledge vault if available)
5. Write the Essay at `outline` status
Output: Essay note in `20-Essays/`

**`/argument-map [claim]`**
Build a structured argument tree. Protocol:
1. State the claim precisely
2. Identify all sub-claims that must be true for the main claim to hold
3. For each sub-claim: state what evidence or argument supports it
4. Identify the weakest link in the chain
5. State the strongest single objection to the main claim and the best response
Output: argument map in `00-Inbox/` or integrated into an Essay note

### Domain Commands (generated from Q6 priority domains)

**`/domain-audit [domain-slug]`** → see `universal-commands/domain-audit.md` (now universal)

**`/promote [note-path]`** → see `universal-commands/promote.md` (now universal)

---

## Adding Commands to `.claude/commands/`

Each universal command stub is a `.md` file. Example for a vault-specific command (full protocol inline):

```
---
description: Read a political situation structurally
---

# /situation-read [situation]

$ARGUMENTS

Read vault-config.md for domain slugs and open problem IDs.
[Full protocol text here for vault-specific commands only]
```

For universal commands, the stub is always the 3-line pointer format shown at the top of this file.
