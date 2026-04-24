---
created: 2026-03-16
updated: 2026-03-30
type: reference
---

# Genesis Protocol

The five-phase self-building procedure for scaffolding a new vault from scratch. Follow in order. Do not skip phases or run them out of sequence — each phase depends on the outputs of the prior one.

**Time estimate per phase**: Each phase is a single working session (1–3 hours). Do not try to run multiple phases in one session — the outputs of Phase 1 need to stabilize before Phase 2 can produce useful content.

---

## Phase 0 — Config Elicitation

**Output**: `vault-config.md` in vault root

**Who does this**: A single session between the user and Claude. Claude asks; user answers.

**Process**:

Ask Q0.5 first (intellectual style), then Q1–Q7 in sequence. For each question:
1. Ask the question in plain language (not just "answer Q1")
2. Offer examples from existing vaults (omega, belli, cogitationis) as anchors
3. Push back if the answer is too vague — a vault cannot be scaffolded from a vague mission
4. Record the answer in `vault-config.md` before moving to the next question

**Q0.5 — Intellectual Style**: "How does your domain primarily advance knowledge — through opposition, tension, and contested positions; through systems that generate each other; through deepening a core mystery; or through building and testing things?" Present the four options:

| Option | Style | Best for |
|---|---|---|
| A | **Adversarial** | Contested domains: politics, philosophy, law, strategy |
| B | **Dialectical** | Systems domains: economics, complexity, biology, science studies |
| C | **Contemplative** | Deep traditions: phenomenology, mathematics, art, theology |
| D | **Constructive** | Building domains: engineering, policy, design, product |

Record the chosen preset in `vault-config.md` as `intellectual_style.preset`. This determines: (1) how Q3 is framed, (2) what the engagement field is called, (3) how pressure points and internal tensions are structured. All four styles demand equal analytical rigor — they differ in framing, not depth.

If the user is unsure: ask "When you encounter a concept that challenges your project, do you want to know what it *attacks*, what it *complicates*, what it *reveals*, or what it *constrains*?" The answer usually identifies the style.

**Q1 — Mission**: "What is this vault for? Who is the intended reader in 10 years? What kind of output does it produce?" — Must be 1–2 sentences. If the user gives a paragraph, compress it to 2 sentences and confirm.

**Q2 — Three Driving Questions**: "What are the three questions that orient every note in this vault? They should be at three different levels — usually: foundational/theoretical, applied/operational, and normative/output." — If the user gives fewer than 3 or more than 3, explain why 3 is the right number and help them find the right scope.

**Q3 — Central Engagement Axis**: The prompt and key depend on the style chosen in Q0.5:

- **Adversarial** → *"What is the deepest unresolved tension in this domain? State it as a genuine opposition — not a preference, but a real dispute where both sides have strong arguments."* → config key: `fault_line`. Valid positions: named stances on the opposition (e.g., "structuralist", "interpretivist", "synthetic"). Failure mode: user states a preference, not a tension.
- **Dialectical** → *"What is the generative tension that drives conceptual development in this domain — the opposition that produces new insight rather than just disagreement?"* → config key: `central_dialectic`. Valid positions: named poles of the dialectic (e.g., "equilibrium lens", "complexity lens"). Failure mode: user gives a list of topics, not a single animating tension.
- **Contemplative** → *"What is the central question or mystery this domain progressively illuminates — never fully answering, always deepening?"* → config key: `central_mystery`. Valid positions: stances toward the mystery (e.g., "phenomenological", "analytic", "apophatic"). Failure mode: user gives a research question with an expected answer.
- **Constructive** → *"What is the core design problem — the constraint satisfaction challenge the domain keeps returning to?"* → config key: `design_problem`. Valid positions: named design orientations (e.g., "efficiency-first", "resilience-first", "equity-first"). Failure mode: user gives a technical specification, not a tension between competing values.

Must be statable in one sentence. If the user gives a list, pick the most foundational and confirm.

**Q4 — Open Problems**: "List 8–15 genuinely open problems in this domain — questions the vault exists to work on, not to answer definitively." — Each problem needs a short name (for frontmatter references) and a one-sentence question. If the user gives fewer than 8, push: "What else would you want this vault to eventually be able to say something about?"

**Q5 — Note Tier Structure**: "What are the three tiers of note in this vault? What is the minimal form (lookup/capture), the working form (mechanistic explanation), and the final form (permanent insight or output)? What triggers graduation from one tier to the next?" — Give the user the omega model and belli model as examples.

**Q6 — Domain Taxonomy**: "What are the major sub-domains? For each: give a label, a folder path, a priority (core / tier1 / tier2), and whether notes in this domain can graduate to Tier 3." — Must have at least 3 domains. If the user gives too many (>12), help them consolidate.

**Q7 — Output Layer**: "What does the final-form output look like? What is the artifact — an evergreen note, a doctrine document, a published essay, a training module? Who reads it? What does it do?" — Must match the vault type from Q1.

**Checklist before proceeding to Phase 1**:
- [ ] Q0.5 intellectual style preset chosen and recorded
- [ ] All 7 questions answered
- [ ] Q1 is 1–2 sentences, not a paragraph
- [ ] Q2 has exactly 3 questions at 3 different levels
- [ ] Q3 uses the correct config key for the chosen style (fault_line / central_dialectic / central_mystery / design_problem)
- [ ] Q3 is stated using the style-appropriate framing (opposition / generative tension / core mystery / design constraint), statable in one sentence
- [ ] Q4 has 8–15 problems, spanning all 3 driving questions
- [ ] Q5 graduation rules are specific enough to decide without judgment calls
- [ ] Q6 has 3–12 domains; each has a folder path and priority
- [ ] Q7 output type matches vault type

---

## Phase 1 — Document Generation

**Output**: 12 structural documents in order

**Who does this**: Claude, in a single session, from the completed `vault-config.md`

Generate these 12 documents in sequence. Each document depends on prior documents — do not reorder.

### Doc 1 — Folder Structure

Create all folders listed in Q6 domains. Standard folder slots (all vaults):

```
[vault-root]/
  00-Inbox/              ← Tier 1: zero-friction capture
  10-Sources/            ← Tier 1: processed input material
  [domain-folders/]      ← Tier 2: unnumbered, vault-specific (from Q6)
  20-Output/             ← Tier 3: final standalone notes
  30-MOCs/               ← Navigation: Maps of Content
  40-Templates/          ← Infrastructure: note templates
  _maps/                 ← Infrastructure: domain primer maps
  memory/                ← Framework: session memory
  .claude/
    commands/            ← Framework: slash command stubs
```

**Numbering rationale** — the gap at Tier 2 is intentional:

```
0x = CAPTURE (Tier 1) — raw, unprocessed input
1x = SOURCES (Tier 1) — processed input material
     [gap]   (Tier 2) — unnumbered domain folders, vault-specific from Q6
2x = OUTPUT  (Tier 3) — final standalone notes
3x = NAVIGATION — Maps of Content
4x = TEMPLATES  — note scaffolding
5x+ = EXTENSIONS — vault-type-specific (e.g., 50-Curriculum/ for training vaults)
```

Why no number for Tier 2? Domain folders are the vault's intellectual workspace — their names and structure are determined by Q6 and must not be homogenized across vaults. The numbered range skips straight from 1x (Sources) to 2x (Output) to make this explicit.

**Customizing the 20- folder name**: The default is `20-Output/`. During Q7, rename to match the vault's output type if a more specific name is warranted — e.g., `20-Judgment/` for analytical vaults. Whatever name is chosen becomes the `output` key in `folder_structure`. The key name (`output`) never changes; only the folder path does.

*Expression vaults may shift 30-MOCs and 40-Templates to higher numbers (e.g., `50-MOCs/`, `60-Templates/`) to accommodate content-tier folders in the 10–40 range.*

### Doc 2 — CLAUDE.md

Write from `claude-md-template.md` as a **slim vault-identity document** (~80–120 lines). Universal rules (core principles, two-zone concept, tier logic, tool rules, memory rules, output efficiency, slash command runtime) are already in `~/.claude/CLAUDE.md` (global, always loaded) — do NOT duplicate them.

The vault CLAUDE.md contains ONLY vault-specific content:
1. Role statement (1–2 lines)
2. Mission and vault-specific principles (not in the global file)
3. Vault structure (folder listing from Q6)
4. Three driving questions (compact — from Q2)
5. Engagement axis statement + positions (compact — from Q3; use the style-appropriate label)
6. Open problems (numbered list: name + one-line question — from Q4)
7. Domain defaults table (the vault-specific part of Two-Zone — from Q6)
8. Synthesis note schema summary (mandatory sections for THIS vault — from Q5)
9. Vault-specific slash commands only (commands unique to this vault — see Doc 9)
10. Any vault-specific behavioral rules (e.g., analytical tone, operational framing)

Do NOT include: universal principles, tier logic, tool rules, memory management rules, the concept of Two-Zone Architecture, or map type structures — these are in the global file.

### Doc 3 — Note Taxonomy

Write `note-taxonomy.md` from `note-tier-template.md`, adapted for this vault's Q5 answers. Include: tier names, descriptions, graduation rules, mandatory sections, decision tree. This is the reference document users read when they want to know what tier a note belongs to.

### Doc 4 — Development Plan

Write `development-plan.md` with:
- Vision (Q1 mission, expanded to ~1 paragraph)
- Domain Structure table (from Q6)
- Development Phases (blank template — to be filled as phases complete)
- Key Decisions section (the "Why" behind Q1–Q7 answers — write this now, before the reasoning is forgotten)

### Doc 5 — Coverage Plan

Write `coverage-plan.md` with:
- Domain-by-domain table of planned notes (start from Q6 domains, add ~5 planned notes per domain as placeholders)
- Tier classification for each planned note
- Gap column (all gaps at this point — the plan starts empty)
- Total counts by tier

This document will be updated by `/coverage-audit` on an ongoing basis.

### Doc 6 — Map Reference

Write `map-reference.md` from `map-type-template.md`, adapted for this vault's Q2/Q3/Q4. Include:
- YAML frontmatter schema for each map type used in this vault
- All mandatory sections
- Examples of how Connection to the Project is written for this vault's engagement axis and driving questions

### Doc 7 — Domain Primers

For each domain in Q6 at `core` or `tier1` priority, write a domain primer using the Domain Map format (map-type-template.md Map Type 3). Store in `_maps/`.

### Doc 8 — Initial MOCs

Write one MOC per domain, plus a Master Index MOC. Each domain MOC is nearly empty at this point — just frontmatter, a brief domain description, and placeholder sections. The Master Index MOC lists all domains and links to their MOCs.

### Doc 9 — Slash Commands

Write `.claude/commands/` files for all **12 universal commands** as **thin stubs** (~12 lines each) plus all vault-specific commands as full protocol files.

**Universal command stubs** (arc, coverage-audit, axis-survey, what-next, promote, compare, engage-problem, synthesis, update-moc, evergreen-note, engage-deep, domain-audit, dialogue, positions, revisit, question-bank):

Each stub has this format:
```markdown
---
description: [one-line description]
---

# /[command-name] [args]

$ARGUMENTS

1. Read the protocol: `[AGENSY_PATH]\framework\universal-commands\[command-name].md`
2. Read vault configuration: `vault-config.md` (vault root)
3. Execute the protocol using this vault's parameters.
```

The full protocol for each universal command lives in `[AGENSY_PATH]/framework/universal-commands/[command-name].md` — do NOT duplicate it in the vault's command file.

**Vault-specific commands** (commands unique to this vault, from Q6/Q7): write as full protocol files. These read `vault-config.md` for their parameters instead of hardcoding vault-specific values.

### Doc 10 — Open Problems File

Write `open-problems.md` at vault root with the full list from Q4. Standard format per problem:

```markdown
## Problem [N]: [Name]

**Question**: [The open question, one sentence]
**Bears on**: [which of the three driving questions]
**Status**: open
**Current vault position**: [what the vault currently argues, if anything]
**Notes addressing this**: [wikilinks — empty at start]
```

### Doc 11 — vault-config.md

The `vault-config.md` from Phase 0 should already be in the vault root. In this step, **extend it** with three additional blocks required for universal command execution:

- **`folder_structure:`** — explicit key→path mapping of every functional folder (inbox, sources, output, mocs, templates, domain folders, maps, memory, commands). Universal commands use these paths instead of hardcoding.
- **`note_template:`** — vault-specific mandatory sections for synthesis notes and reference notes, including the synthesis instrument template (Judgment Instrument / Connection to the Project / vault-equivalent). Universal commands use this to check quality and generate notes.
- **`reference_docs:`** — paths to the vault's coverage plan, development plan, map reference, open problems file, and any other reference documents universal commands need to read.

See `framework/vault-config-schema.md` for the full schema. See `synthesis_politeia/vault-config.md` as the reference implementation.

### Doc 12 — Memory Initialization

Write `memory/MEMORY.md` with initial entries:
- Vault location and type
- Folder structure summary
- Q1–Q7 summary (brief)
- Note counts (all zeros at start)

Write `memory/session-state.md` with initialized values:
```markdown
# Session State
last_updated: YYYY-MM-DD
notes_since_last_audit: 0
last_coverage_audit: never
last_axis_survey: never
last_what_next: never
open_actions: []
recent_arcs: []
```

Write `memory/note-index.md` with headers only (empty table, populated by first `/arc`):
```markdown
# Note Index
Last updated: YYYY-MM-DD | Total: 0 | Last full rebuild: never

| Path | Tier | Domain | EC | Axis | OPs | Source | Created |
|---|---|---|---|---|---|---|---|
```
- First session date

### Doc 13 — Vault-Type Substrate (conditional: expression, training)

Copy the vault-type-specific substrate templates into the vault root based on the type chosen in Q0.5 / Q7:

- **Expression vault** → copy every file from `[AGENSY_PATH]/framework/vault-type-templates/expression/` (except the sub-folder `README.md`) into the new vault's root. Files copied: `voice-profile.md`, `writer-positions.md`, `positions-index.md`, `article-presets.md`, `article-design-principles.md`, `source-map-registry.md`. These are scaffolds — the user will fill them during and after genesis. `/article-draft` will refuse to run until `voice-profile.md` is moved out of `status: unseeded`.
- **Training vault** → copy every file from `[AGENSY_PATH]/framework/vault-type-templates/training/` (except the sub-folder `README.md`) into the new vault's root. Files copied: `curriculum-template.md` (rename to vault-specific, e.g., `[vault-name]-curriculum.md`), `principles-and-postulates-template.md` (rename to e.g., `principles-and-postulates.md`), `sources-master-list-template.md` (rename to e.g., `sources-master-list.md`). These are scaffolds — the user fills them during and after genesis.
- **Accumulation vault** → skip this step. Accumulation vaults do not need additional substrate; the 12 preceding documents cover everything.

Also extend `vault-config.md` with the `reference_docs.*` entries that point to the copied substrate files. For expression vaults this means adding `voice_profile`, `writer_positions`, `positions_index`, `article_presets`, `article_design_principles`, `source_map_registry`, and `map_to_article_schema` keys. For training vaults, add keys pointing to the curriculum, postulates, and sources files.

See `framework/vault-type-templates/README.md` for which files each vault type needs and the fill-in order the vault owner should follow after genesis.

**Register in system-state.md**: After writing the three memory files and (if applicable) copying substrate templates, open `[AGENSY_PATH]\system-state.md` and add one row to the **Vault Registry** table:

```
| [vault-name] | Phase 0 (bootstrapped) | 0 | never |
```

This tracks dynamic operational state (note counts, audit cadence). Vault identity, mission, and connection types are registered separately in `vault-registry.md` per agensy CLAUDE.md Task 1 steps 6–7.

---

## Phase 2 — Self-Audit Initialization

**Output**: Completed baseline `[vault-name]-coverage-plan.md`

**Who does this**: Claude, immediately after Phase 1

Run `/coverage-audit` immediately after Phase 1 documents are complete. This is the first real test that the structure is coherent. The audit should:
1. Walk all domain folders
2. Find exactly zero notes (all planned, none written yet) — this is correct and expected
3. Verify that all domain primers exist (from Doc 7)
4. Verify that all MOCs exist (from Doc 8)
5. Output the baseline coverage plan with all gaps flagged

If `/coverage-audit` finds unexpected content or missing structure, diagnose and fix before proceeding to Phase 3.

---

## Phase 3 — First Content Arc

**Output**: One complete map + 8–12 atomic notes

**Who does this**: User + Claude, in the first content session

Run `/arc [highest-priority subject] [type]` on the domain identified in Q6 as `core` priority, for the subject most central to the engagement axis (Q3).

This is the structural test of the generated framework. A successful first arc means:
1. The map is produced at full depth (400+ lines for person/framework maps; 250+ for concept maps)
2. 8–12 Tier 2 notes are produced meeting all mandatory sections
3. At least 2 notes reference open problems from Q4
4. The engagement axis frontmatter field is populated in every synthesis-schema note
5. At least 3 cross-domain links exist among the new notes

If the first arc reveals structural problems (wrong tier definitions, missing mandatory sections, ill-defined domains), diagnose and fix vault-config.md and CLAUDE.md before continuing. The first arc is the calibration run.

---

## Phase 4 — Ongoing Self-Regulation

**Output**: Maintained, growing vault

After the first arc, the vault is self-regulating through three standing mechanisms:

1. **`/coverage-audit`** — run after every 10–15 new notes to update the coverage plan
2. **`/what-next`** — run at the start of any session when the user is unsure what to build
3. **`/axis-survey`** — run every 2–3 months to track how the vault's position on Q3 is developing

These three commands replace project management overhead. The vault tells you what it needs next.

---

## Failure Modes in Genesis

**Failure 1: Q1 is too broad**
"Build a comprehensive knowledge base about philosophy" — not actionable. The vault cannot derive a fault line, driving questions, or domain taxonomy from this. Fix: compress to a specific intellectual project with a specific kind of output.

**Failure 2: Q3 does not match the chosen style**
Adversarial vaults need a genuine opposition where both sides have strong arguments — not a preference. Dialectical vaults need a generative tension, not a research question with an expected answer. Contemplative vaults need an open mystery, not a solvable puzzle. Constructive vaults need competing constraints, not a technical specification. Fix: use the style-specific Q3 framing from Q0.5 and confirm the result fits the style's failure-mode test.

**Failure 3: Q4 has too few problems**
Fewer than 8 problems means the vault's intellectual scope is too narrow, or the user hasn't been asked hard enough questions. Fix: ask "If this vault never answered [problem N], what would be missing? What question would it have failed to address?"

**Failure 4: Phases 1 and 2 are collapsed**
Writing content notes during Phase 1, before structural documents are complete, produces notes without a proper schema and requires retroactive fixing. Fix: complete all 12 Phase 1 documents before writing a single content note.

**Failure 5: First arc skipped or abbreviated**
The first arc is the calibration run. Skipping it leaves structural problems undetected until they are widespread. Fix: always run the first arc before building more than 5 content notes.
