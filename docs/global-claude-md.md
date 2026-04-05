---
type: documentation
audience: human
---

# Global CLAUDE.md Template

This file must be copied to `~/.claude/CLAUDE.md` on your machine. It loads automatically in every Claude Code session and gives Claude the universal framework rules that apply across all your synthesis vaults.

**Setup**: Copy everything from the `---BEGIN---` line below to `---END---`, paste it into a new file at `~/.claude/CLAUDE.md`, and replace `[AGENSY_PATH]` with the absolute path to your local `agensy/` folder.

Example: if you cloned to `/Users/alice/vaults/agensy/`, replace `[AGENSY_PATH]` with `/Users/alice/vaults/agensy`.

---BEGIN---
# Universal Framework Rules

*These rules apply to all synthesis vaults and are loaded in every session. Vault-specific parameters (mission, domains, open problems, engagement axis, note schema details) are in each vault's CLAUDE.md and vault-config.md.*

## Core Principles (Never Break These)

- **Atomic**: Exactly ONE idea, concept, principle, or insight per note.
- **Evergreen**: Rewrite 100% in the user's natural voice — clear, timeless, standalone. Someone should understand it perfectly in 5–10 years without the original source.
- **Strong linking**: Every note must contain 4–8 relevant wikilinks. Search the vault aggressively for best conceptual matches, not just keyword matches.
- **No duplication**: Before creating any new note, search the output folder for similar content. If ≥70% overlap → merge by appending instead.
- **Project-facing**: Every synthesis-schema note must state both what it gives the project AND how it forces engagement beyond surface understanding. The engagement field (configured per vault: Threatens / Complicates / Transforms / Constrains) is mandatory and must be specific. Comfortable confirmation is not analysis.

## Two-Zone Architecture (Universal Concept)

All synthesis vaults split notes into two schemas, determined at the note level by `evergreen-candidate`:

| Zone | `evergreen-candidate` | Schema | Purpose |
|---|---|---|---|
| Zone 1 — Reference Substrate | `false` | Reference schema | Mechanistic scaffolding — HOW things work, technical procedures |
| Zone 2 — Synthesis Core | `true` | Synthesis schema | Project-facing insights — connected to driving questions and engagement axis |

**Universal logic rules**:
- Domain default applies when creating new notes; note-level value overrides the domain default.
- Direction is `false` → `true` only. A note is never downgraded from synthesis to reference.
- When unsure: apply the domain default. Override only when the note clearly connects to the project's driving questions or engagement axis.

**Domain defaults, mandatory schema sections, and engagement axis positions** are vault-specific — defined in each vault's CLAUDE.md and vault-config.md.

## Three-Tier Note System (Universal Logic)

All synthesis vaults use a three-tier note progression:

| Tier | Role | Location |
|---|---|---|
| Tier 1 | Source / capture | Raw input — 00-Inbox/, 10-Sources/, or equivalent |
| Tier 2 | Analysis / concept | Atomic explanation with structural depth — domain subfolders |
| Tier 3 | Output / judgment | Permanent, standalone, claim-titled — vault's output folder |

**Universal graduation logic**:
- Graduation is always Tier 1 → Tier 2 → Tier 3. Never reversed.
- Tier 3 notes are never demoted once placed in the output folder.
- Tier 3 title must state a claim or insight, not just a concept name.
- Tier 3 must be fully standalone — no vault access required for comprehension.

**Tier names, graduation criteria, mandatory sections, and output folder** are vault-specific — defined in each vault's CLAUDE.md and vault-config.md.

## Slash Commands — Runtime Instruction

When a slash command is invoked in any synthesis vault:
1. Read `vault-config.md` from the vault root for all vault-specific parameters.
2. For universal commands, read the full protocol from `[AGENSY_PATH]/framework/universal-commands/[command-name].md`.
3. Execute the protocol using this vault's parameters.

**Universal commands** (16 total — protocols in agensy/):
arc · coverage-audit · axis-survey · what-next · promote · compare · engage-problem · synthesis · update-moc · evergreen-note · engage-deep · domain-audit · dialogue · positions · revisit · question-bank

**Command lifecycle**: See `[AGENSY_PATH]/framework/command-lifecycle.md` for when to fire each command — four trigger types (automatic, milestone, session, analytical). Run the Type C session check at every session start.

**Vault-specific commands** stay in that vault's `.claude/commands/` as full protocol files.

## Output Efficiency

Go straight to the point. Try the simplest approach first. Be extra concise in text output. Lead with the answer or action. Skip preamble and unnecessary transitions.

## Claude Code Tool & Skill Rules

### Automatic skill invocation
- **Writing any vault `.md` file** → invoke `obsidian:obsidian-markdown` skill to verify syntax
- **Creating `.canvas` files** → invoke `obsidian:json-canvas`
- **Creating `.base` files** → invoke `obsidian:obsidian-bases`
- **Reading a URL** → invoke `obsidian:defuddle` instead of WebFetch
- **Interacting with the live Obsidian app** → invoke `obsidian:obsidian-cli` (warn user if binary not installed)

### Primary tools
Direct file operations (Read / Write / Edit / Grep / Glob) are the primary tools. Skills augment them.

## Memory Management

Memory lives in `memory/MEMORY.md` and topic files in `memory/`. Rules:
- `MEMORY.md` stays under 150 lines (hard truncation at 200 — 150 is the safety threshold)
- `MEMORY.md` is an index only — detailed content goes in topic files
- Save: hard-won technical discoveries, architectural decisions with rationale, dead ends with WHY, vault state changes
- Do NOT save: anything already in vault CLAUDE.md files; session-specific context; speculative conclusions; information trivially re-derivable from vault content
- Update immediately on discovery — not at end of session
- Biweekly: audit for stale entries (~30% redundancy accumulates after 10 sessions)
---END---
