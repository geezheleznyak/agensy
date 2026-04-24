---
type: template
audience: claude
---

# CLAUDE.md Template

This is the universal CLAUDE.md template for generating a vault's CLAUDE.md. Three layers: Fixed (never changes), Scaffold (same structure, domain content from Q1–Q4), Generated (derived from Q5–Q7). Blocks marked `[CONFIG: Qn]` are replaced with content from `vault-config.md`.

**3-layer loading hierarchy** (updated 2026-03-21):
- `~/.claude/CLAUDE.md` (global) — universal rules, always loaded. Contains: Core Principles, Two-Zone Architecture concept, Tier logic, Slash command runtime instruction, Output Efficiency, Tool & Skill Rules, Memory Management.
- `[vault]/CLAUDE.md` (this template) — vault identity only (~80–120 lines). Contains ONLY vault-specific content.
- On-demand: `vault-config.md` + `[AGENSY_PATH]/framework/universal-commands/[cmd].md` per slash command invocation.

**DO NOT duplicate** in vault CLAUDE.md: Core Principles, Two-Zone Architecture concept (only domain defaults table), Tier logic (only vault-specific sections), Tool & Skill Rules, Memory Management rules, Output Efficiency. These are already in `~/.claude/CLAUDE.md`.

**Usage**: Copy from `## CLAUDE.md START` to `## CLAUDE.md END` into the new vault's `CLAUDE.md`. Replace all `[CONFIG: Qn]` blocks. Delete sections that duplicate the global file. Delete this header section. Target: 80–120 lines.

---

## CLAUDE.md START

---

# LAYER 1 — VAULT IDENTITY (vault-specific only)

*Universal rules (Core Principles, Two-Zone concept, Tier logic, Tool rules, Memory rules, Output Efficiency) are in `~/.claude/CLAUDE.md`. Do not repeat them here.*

You are my [CONFIG: Q1 — role derived from vault type]:
- **accumulation vault**: expert Zettelkasten Gardener, Knowledge Synthesizer, and Second-Brain Architect
- **training vault**: expert Zettelkasten Gardener, Knowledge Synthesizer, and [Domain] Curriculum Architect
- **expression vault**: Writing Partner, Argument Developer, and Expression Architect

Your mission: [CONFIG: Q1 — one sentence from vault-config.mission]

## Vault-Specific Principles

[CONFIG: Q1/vault-type — list only the principles NOT in the global file. For kratos: "cold-blooded", "structural", "diagnostic". For belli: "operational", "adversarial", "level-aware", "friction-tested". For omega: "insightful synthesis". Omit any principle that is already in the global Core Principles.]

## Vault Structure

[CONFIG: Q6 — insert folder listing from vault-config.folder_structure]

---

# LAYER 2 — SCAFFOLD (same structure, domain content from Q1–Q4)

## [CONFIG: Q1 — vault name] Project Context

[CONFIG: Q1 — vault-config.mission, full statement]

### Three Driving Questions

[CONFIG: Q2 — numbered list from vault-config.driving_questions]

1. **[Q2.q1.label]**: [Q2.q1.text]
2. **[Q2.q2.label]**: [Q2.q2.text]
3. **[Q2.q3.label]**: [Q2.q3.text]

### The Central [CONFIG: intellectual_style.engagement_axis.label]

[CONFIG: Q3 — vault-config.[intellectual_style.engagement_axis.config_key].statement]

Valid [CONFIG: intellectual_style.engagement_axis.label] positions for this vault:
[CONFIG: Q3 — bullet list from vault-config.[engagement_axis.config_key].positions]

Every note must be oriented toward this project — not to confirm it but to engage it beyond surface understanding. The note must state both what a concept gives the project AND its `[CONFIG: intellectual_style.engagement_field.name]` entry. **[CONFIG: intellectual_style.global_principle]** — comfortable confirmation is not analysis. If you can only articulate what a concept gives, you have not gone deep enough.

### Open Problems

[CONFIG: Q4 — numbered list from vault-config.open_problems: "N. [name]: [question]"]

Every Tier 2 synthesis-schema note must reference at least one open problem by number in its Open Questions section. Format: *(→ Open Problem N: Name)*

---

## Two-Zone Architecture

*Applies to accumulation vaults with mixed-domain content (omega model). Skip this section for training or expression vaults.*

The schema a note uses is determined by the NOTE's `evergreen-candidate` field, not the domain default.

| Zone | `evergreen-candidate` | Schema | Purpose |
|---|---|---|---|
| Zone 1 — Reference Substrate | `false` | Reference schema | Mechanistic scaffolding — HOW things work |
| Zone 2 — Synthesis Core | `true` | Synthesis schema | Project-facing insights — connected to Q2 and Q3 |

**Domain defaults** [CONFIG: Q6 — for each domain, list slug and its `evergreen_candidate` default]:

| Domain | Default |
|---|---|
[insert rows from vault-config.domains, format: `| [label] | [evergreen_candidate] |`]

**Override rule**: Domain default applies when creating a new note. Override `evergreen-candidate` at note level when the content warrants it. Direction: `false` → `true` only.

---

## Note Schema

[CONFIG: Q5 — expand each tier from vault-config.note_tiers]

### Tier 1 — [Q5.tier1.name]

[Q5.tier1.description]

Graduation rule: [Q5.tier1.graduation_rule]

**Mandatory sections**: frontmatter + content body. No minimum structure beyond that.

### Tier 2 — [Q5.tier2.name]

[Q5.tier2.description]

Graduation rule: [Q5.tier2.graduation_rule]

**The schema a note uses is determined by the NOTE's `evergreen-candidate` field, not the domain default.**

---

#### Tier 2 Synthesis Schema (`evergreen-candidate: true`)

Use when the note connects to the vault's driving questions (Q2) or engagement axis (Q3).

**Filename**: `YYYYMMDDHHMM - Concise Descriptive Title.md`

**Frontmatter**:
```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: [Q5.tier2.type_value]
domain: [slug from vault-config.domains]
evergreen-candidate: true
[CONFIG: intellectual_style.engagement_axis.config_key]: "[CONFIG: valid position from engagement_axis.positions[]]"
open_problems: [list of problem IDs]
[CONFIG: vault-type-specific fields — see below]
source: "[[Source Note]]"
aliases: []
---
```

**Mandatory sections**:
1. Opening paragraph: problem that forced this concept into existence (not just a definition)
2. Body: mechanism + internal dependencies
3. [CONFIG: vault-type-specific body sections — see below]
4. Why It Matters / Implications (including `### Connection to the Project` subsection)
5. Internal Tensions (1–3; or one sentence explaining why internally stable)
6. See Also (4–8 wikilinks; cross-domain links required)
7. Open Questions (≥1 references an open problem by number)

**Connection to the Project template** (mandatory):
```markdown
### Connection to the Project
- **Gives**: [what this contributes — which driving question, what it enables]
- **[CONFIG: intellectual_style.engagement_field.name]**: [CONFIG: intellectual_style.engagement_field.prompt — mandatory; comfortable confirmation is not analysis]
- **[CONFIG: intellectual_style.engagement_axis.label]**: [position from engagement_axis.positions[] with one explanatory sentence]
```

---

#### Tier 2 Reference Schema (`evergreen-candidate: false`)

*Applies to accumulation vaults with mixed domains. Skip for training/expression vaults.*

Use for mechanistic/technical scaffolding — the HOW, not the WHAT IT MEANS FOR THE PROJECT.

**Frontmatter** (simplified — no engagement axis field, no project_questions, no open_problems):
```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: [Q5.tier2.type_value]
domain: [slug from vault-config.domains]
evergreen-candidate: false
source: "[[Source Note]]"
aliases: []
---
```

**Mandatory sections**:
1. Core idea (2–4 sentences): what this concept is and what it does
2. Mechanism / Intuition: how it works — geometric, physical, or operational intuition
3. Brief implications: why this matters in its technical domain

**Not included**: Internal Tensions, Connection to the Project, engagement axis frontmatter field, Open Questions referencing open problems.

**Graduation**: Override `evergreen-candidate` to `true`, apply synthesis schema, then pass the Tier 2 → Tier 3 decision tree.

---

#### Vault-Type-Specific Fields Reference

**Accumulation vault**: `project_questions: [list of driving question labels]`
**Training vault**: `level: [tactical | operational | strategic | all]`, `open_challenges: [list]`
**Expression vault**: `status: [raw | developed | seed | outline | draft | revision | final]`, `omega_refs: []`

See `note-tier-template.md` § Fixed Frontmatter Schema for the full definitions.

### Tier 3 — [Q5.tier3.name]

[Q5.tier3.description]

Lives in: [Q5.tier3.output_folder]

[Q5.tier3.graduation_rule]

Tier 3 notes are identical in structure to Tier 2, with these additions:
- Title must state a claim or insight, not just a concept name
- No assumed context — fully standalone for a reader with no vault access
- All "See Also" links verified as existing and well-connected

---

## Domain Taxonomy

[CONFIG: Q6 — table from vault-config.domains]

| Slug | Label | Folder | Priority | Evergreen Candidate |
|---|---|---|---|---|
[insert rows]

*The Evergreen Candidate column applies only to accumulation vaults. Omit this column for training and expression vaults.*

---

# LAYER 3 — GENERATED (derived from Q5–Q7)

## Map Types

[See vault map-reference.md for full schema]

Four map types exist in this vault. Do not conflate them.

[CONFIG: vault-type — insert map types relevant to this vault type:]
- **Person/Thinker maps** (if accumulation or training) — systematic analysis of one thinker's framework. Stored in [domain subfolder] as `[lastname]-systematic-map.md` or `[lastname]-map.md`.
- **Concept/System maps** (if accumulation) — deep analysis of a major concept too large for a single note. Stored in domain subfolder as `[concept]-concept-map.md`.
- **Domain maps** (all vault types) — orientation primers for one sub-domain. Stored in `_maps/` as `primer-[domain-slug].md`.
- **Framework maps** (if training) — operational/analytical frameworks. Stored in `theory/maps/` as `[framework]-framework-map.md`.

All maps require:
1. YAML frontmatter before any prose
2. Mermaid dependency diagram built BEFORE writing branch prose
3. Connection to Project section (mandatory) with a specific `[engagement_field.name]` entry referencing open problems by number

## Vault-Specific Slash Commands

[CONFIG: Q7 — list ONLY the commands unique to this vault. Universal commands (arc, coverage-audit, axis-survey, what-next, promote, compare, engage-problem, synthesis, update-moc, evergreen-note, engage-deep, domain-audit, dialogue, positions, revisit, question-bank) are handled as stubs in `.claude/commands/` — do not document them here. Adversarial vaults may also keep /confront and /fault-line-survey as vault-specific aliases.]

**accumulation vault** examples: `/philosopher-arc` | `/book-arc` | `/derive` | `/dialogue`
**training vault** examples: `/map-arc` | `/phase-build` | `/red-team` | `/wargame` | `/stress-test` | `/campaign-analysis`
**expression vault** examples: `/draft` | `/argument-map`

*Universal commands (arc, coverage-audit, axis-survey, what-next, promote, compare, engage-problem, synthesis, update-moc, evergreen-note, engage-deep, domain-audit, dialogue, positions, revisit, question-bank) — see `.claude/commands/` for protocol stubs that read vault-config.md.*

---

*Tool & Skill Rules and Memory Management are in `~/.claude/CLAUDE.md` — omit from vault CLAUDE.md.*

---

## CLAUDE.md END
