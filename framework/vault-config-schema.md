---
type: schema
audience: claude
---
# vault-config.md Schema

This is the genesis document for any new vault. Fill it in once, in a single session, before writing any other structural document. All other documents derive from these answers.

**Usage**: Copy this file to the new vault root as `vault-config.md`. Answer Q1–Q7 in order. Do not skip or defer any question — every structural decision downstream depends on having all seven answered.

---

## vault-config.md Template

```yaml
# vault-config.md
# Genesis document — fill in once, derives everything else.
# Created: [DATE]

vault:
  name: [short descriptive name, e.g. "synthesis_theoria"]
  path: [absolute path to vault root]
  type: [accumulation | training | expression | hybrid]
  # accumulation: builds up a knowledge base over time (theoria model)
  # training: develops a skill or competency through progressive curriculum (bellum model)
  # expression: turns knowledge/thinking into published output (logos model)
  # hybrid: explicitly combines two or more types (define below)
  created: [YYYY-MM-DD]
```

---

### Q0.5 — Intellectual Style

> **Asked once, during genesis, before Q1.** Determines the engagement framing for every note, map, and command in the vault. All four styles demand equal analytical rigor — they differ in framing, not depth. The invariant across all styles: *comfortable confirmation is not analysis.*

```yaml
intellectual_style:
  preset: [adversarial | dialectical | contemplative | constructive | custom]
  # adversarial:   Concepts threaten each other. The vault navigates a central fault line
  #                where positions genuinely oppose. Best for contested domains (politics,
  #                philosophy, law, military theory).
  # dialectical:   Concepts evolve through tension and synthesis. Best for sciences and
  #                complex systems (economics, biology, AI safety, complexity).
  # contemplative: Concepts reveal layers of a single inquiry. Best for deep traditions
  #                (phenomenology, pure mathematics, art, religious studies).
  # constructive:  Concepts solve problems under constraints. Best for building domains
  #                (engineering, policy design, software architecture, medicine).
  # custom:        All sub-fields below must be set explicitly.
  #
  # The preset populates all sub-fields below with defaults.
  # Any explicitly set sub-field overrides its preset default.

  engagement_axis:
    # Q3 LABEL — what the "central fault line" is called for this style.
    # adversarial:   label: "Central Fault Line",   config_key: fault_line
    # dialectical:   label: "Central Dialectic",    config_key: central_dialectic
    # contemplative: label: "Central Mystery",       config_key: central_mystery
    # constructive:  label: "Central Design Problem", config_key: design_problem
    label: [see preset]
    config_key: [see preset]  # used as the YAML key in Q3 and in note frontmatter
    statement: >
      [Set when answering Q3 — see Q3 prompt for your chosen style.]
    positions:
      - [name]: [description — one sentence]
      - [name]: [description — one sentence]
      - [name]: [description — one sentence]
    secondary_axes:  # OPTIONAL — add if the domain is genuinely multi-dimensional
      - label: [e.g., "Methodological Axis"]
        config_key: [e.g., method_axis]
        statement: >
          [Secondary tension or question]
        positions:
          - [name]: [description]
          - [name]: [description]

  engagement_field:
    # The mandatory field that forces engagement beyond surface understanding.
    # adversarial:   name: "Threatens"  — what assumption this attacks
    # dialectical:   name: "Complicates" — what prior understanding requires revision
    # contemplative: name: "Transforms" — what perception this changes
    # constructive:  name: "Constrains" — what design tradeoff this introduces
    name: [see preset]
    prompt: >
      [The question Claude asks itself when generating this field. Set by preset.]
    escape_valve: [true | false]
    # When true: "No genuine [field] — [mandatory justification]" is accepted at Tier 2.
    # Escape-valve entries always block Tier 3 promotion — a real engagement entry must
    # be acquired before graduation. Default: false for adversarial, true for others.
    graduation_gate: true
    # Always true — the engagement field is always required for Tier 3 graduation.
    # The escape valve allows provisional Tier 2 entries, not absence.

  pressure_points:
    # How maps express their internal tensions / limits.
    # adversarial:   format: "named_exploiter"  — "EXPLOITED BY [name] who [move]"
    # dialectical:   format: "boundary_condition" — "breaks down under [condition], demonstrated by [case]"
    # contemplative: format: "applicability_limit" — "reaches its limit at [boundary], shown by [case]"
    # constructive:  format: "failure_mode"       — "fails when [condition], producing [failure], as in [case]"
    format: [see preset]
    prompt: [see preset]
    required_count: "3-7"  # reduce to "2-5" for training vaults or lighter-engagement projects

  internal_tensions:
    # How notes express their internal limitations.
    # adversarial:   format: "exploiter_and_move" — "who exploited it + how they entered"
    # dialectical:   format: "context_and_limit"  — "context that exposed it + structural limitation"
    # contemplative: format: "unresolved_depth"    — "unresolved depth + who/tradition addressed it"
    # constructive:  format: "tradeoff_and_degradation" — "tradeoff + degradation under condition"
    format: [see preset]
    allow_stable_justification: true
    # When true: "No significant internal tensions — [justification]" is accepted for
    # genuinely stable concepts. Justification is mandatory and checked for non-triviality.

  dialogue_philosophy:
    convergence_rule: [block | synthesis_only | inhabit_first | after_testing]
    # adversarial:   block         — "Do not resolve. Deepen."
    # dialectical:   synthesis_only — "Do not flatten. Synthesize upward."
    # contemplative: inhabit_first  — "Do not summarize. Inhabit."
    # constructive:  after_testing  — "Do not assert. Test."
    principle: [set by preset — see mapping above]

  graduated_depth:
    # Allows lighter engagement at Tier 2 (escape valve permitted) vs full rigor at Tier 3.
    # Recommended: true for adversarial, false for other styles (all tiers equal depth).
    tier2_intensity: [full | light]
    tier3_intensity: full  # always full — Tier 3 never gets reduced rigor
```

**Backward compatibility**: Existing vaults with `fault_line:` at the top level (without `intellectual_style:`) default to `preset: adversarial`. All existing behavior is preserved. Add `intellectual_style:` when migrating or building a new vault.

**Style selection prompt** (for /new-vault):
> "This framework supports four intellectual styles. Each demands equal analytical rigor — they differ in how engagement is framed. Which fits your domain?
> 1. **Adversarial** — concepts threaten each other; the vault navigates a central fault line
> 2. **Dialectical** — concepts evolve through tension and synthesis; the vault navigates a generative dialectic
> 3. **Contemplative** — concepts reveal layers of a single inquiry; the vault illuminates a central mystery
> 4. **Constructive** — concepts solve problems under constraints; the vault addresses a design problem
>
> You may also combine elements or specify custom framing."

---

### Q1 — Mission

```yaml
mission: >
  [1–2 sentences. What is this vault for?
   Who is the intended reader in 10 years — you, a student, a practitioner?
   What kind of thinking does it produce?]
```

**Example (theoria)**: Build a comprehensive philosophical and metaphysical framework — spanning ontology, philosophy of mind, epistemology, and philosophy of science — that yields integrated understanding of what is real, what can be known, and what the human being fundamentally is, in a world shaped by complexity, information, and artificial intelligence.

**Example (bellum)**: Build a unified, complete, and operationally tested knowledge framework for training a fresh military commander from zero to one in a rapidly changing environment characterized by AI-enabled warfare, drone proliferation, and shifting great-power competition.

---

### Q2 — Three Driving Questions

```yaml
driving_questions:
  q1:
    label: [e.g., metaphysical | strategic | conceptual | design]
    text: >
      [The question. Full sentence. This should be the hardest, most generative question
       in the domain — the one that orients everything else.]
  q2:
    label: [e.g., anthropological | operational | empirical | practical]
    text: >
      [The second question. Should be at a different level than Q1.]
  q3:
    label: [e.g., normative | command | ethical | expressive]
    text: >
      [The third question. Often the "so what" — what follows from Q1 and Q2?]
```

**Note**: Three is the right number. Fewer loses coverage; more loses focus. If you cannot identify three distinct questions, the vault's scope is either too narrow (one question) or too diffuse (unclear mission — return to Q1).

---

### Q3 — Central Engagement Axis

> **The Q3 prompt adapts to the intellectual style selected in Q0.5.** Use the variant below that matches your preset. The `config_key` value you set here also populates `intellectual_style.engagement_axis.config_key` and appears as a frontmatter field in every synthesis note.

---

**Q3-A (Adversarial preset) — Central Fault Line**

```yaml
fault_line:
  statement: >
    [What is the deepest unresolved tension in this domain? State it as an opposition
     between two genuine positions — not a false dichotomy, but a real intellectual dispute
     where both sides have strong arguments. One sentence.]
  positions:
    # At minimum: two polar positions + a synthesis position.
    - [name]: [description — one sentence]
    - [name]: [description — one sentence]
    - [name]: [description — one sentence]
```

*Failure mode*: "Is X good or bad?" or "Should we do X?" — these are preferences, not fault lines. The tension must be between genuine intellectual positions with real evidence on both sides.

**Example (theoria)**: Does reality have intrinsic rational structure — a logos the mind tracks when it reasons — or is structure always imposed by minds, models, and practices on a fundamentally neutral substrate?
Positions: `realist` | `constructivist` | `pragmatist` | `dissolves`

**Example (bellum)**: Is the AI/drone revolution creating genuine discontinuity requiring new first principles, or do eternal principles maintain continuity?
Positions: `continuity` | `discontinuity` | `synthesis`

---

**Q3-B (Dialectical preset) — Central Dialectic**

```yaml
central_dialectic:
  statement: >
    [What is the generative tension driving this domain's conceptual development?
     State it as a productive contradiction where both thesis and antithesis capture
     something real — and where synthesis is possible but not trivial. One sentence.]
  positions:
    # At minimum: thesis position + antithesis position + synthesis position.
    - [name]: [description — one sentence]
    - [name]: [description — one sentence]
    - [name]: [description — one sentence]
```

*Failure mode*: A binary opposition with no synthesis path — that is adversarial framing, not dialectical.

**Example (oeconomia)**: Do economic dynamics emerge primarily from structural forces (institutions, power, path-dependence) or from ideational/behavioral patterns (narratives, beliefs, animal spirits), and what integrative account captures both without collapsing either?
Positions: `structural` | `behavioral-ideational` | `complex-interactive`

---

**Q3-C (Contemplative preset) — Central Mystery**

```yaml
central_mystery:
  statement: >
    [What is the core question this domain exists to investigate — the question that
     can be progressively illuminated but not definitively resolved? State it as an
     open inquiry, not a resolvable problem. One sentence.]
  positions:
    # Label the major perspectives from which this mystery is approached.
    - [name]: [description — one sentence]
    - [name]: [description — one sentence]
    - [name]: [description — one sentence]
```

*Failure mode*: A resolvable question — if it has a definitive answer, it is not a mystery.

**Example (a mathematics vault)**: What is the relationship between formal mathematical structure and the structure of physical reality — and why does abstract mathematics developed for purely formal reasons repeatedly describe nature?
Positions: `platonist` | `structuralist` | `constructivist` | `naturalist`

---

**Q3-D (Constructive preset) — Central Design Problem**

```yaml
design_problem:
  statement: >
    [What is the design problem this vault solves? State it as a constraint satisfaction
     challenge: How do you achieve X while maintaining Y under condition Z?
     One sentence.]
  positions:
    # Label the major design approaches or schools of practice.
    - [name]: [description — one sentence]
    - [name]: [description — one sentence]
    - [name]: [description — one sentence]
```

*Failure mode*: An unconstrained goal ("make X better") — not a design problem without constraints.

**Example (a policy design vault)**: How do you increase systemic resilience while maintaining operational efficiency under resource constraints and democratic accountability?
Positions: `redundancy-first` | `efficiency-first` | `adaptive-hybrid`

---

### Q4 — Open Problems

```yaml
open_problems:
  # 8–15 problems. Fewer = vault lacks intellectual depth. More = scope unclear.
  # Each problem must be genuinely open — no settled answer.
  # Problems should span Q1, Q2, and Q3.
  - id: 1
    name: [Short name — used in frontmatter references]
    question: [The open question. One sentence.]
    bears_on: [q1 | q2 | q3 | q1+q2 | all]
  - id: 2
    name: [...]
    question: [...]
    bears_on: [...]
  # ... continue to 8–15

  # Expression vaults may inherit open problems from their source accumulation vault.
  # If inherited, specify:
  # inherited_from: [vault-name]
  # Then list the inherited problem IDs explicitly (do not just point to a file).
```

**Naming convention**: These IDs are referenced in note frontmatter as `open_problems: [1, 3, 7]`. Keep names short and stable — changing them later requires updating all notes.

---

### Q5 — Note Tier Structure

```yaml
note_tiers:
  schema_rule: >
    [How is the schema (full synthesis vs simplified reference) determined?
     Default: by the note's evergreen-candidate field.
     Domain setting is the default; note-level overrides.
     For mixed-domain accumulation vaults: synthesis schema = evergreen-candidate true;
     reference schema = evergreen-candidate false. Training and expression vaults use
     synthesis schema for all Tier 2 notes.]

  tier1:
    name: [e.g., Reference | Raw | Stub | Source]
    description: >
      [What qualifies as Tier 1? What is it for?
       Usually: lookup material, raw captures, image-only stubs, procedure tables.]
    type_value: [the string used in frontmatter type: field, e.g. "reference"]
    graduation_rule: >
      [What must be true before a Tier 1 note can be promoted to Tier 2?
       Be specific — this determines when notes get expanded.]

  tier2:
    name: [e.g., Concept | Analytical | Operational | Thought]
    description: >
      [What qualifies as Tier 2? The main working tier — most notes live here.]
    type_value: [e.g. "concept" | "analytical" | "operational"]
    graduation_rule: >
      [What must be true before a Tier 2 note can graduate to Tier 3?
       For synthesis-schema notes: atomicity + standalone intelligibility + project-facing analysis complete.
       For reference-schema notes: first upgrade to synthesis schema (override evergreen-candidate to true),
       then apply synthesis graduation criteria.]

  tier3:
    name: [e.g., Evergreen | Doctrine | Essay | Published]
    description: >
      [What qualifies as Tier 3? The permanent, final-form tier.]
    type_value: [e.g. "evergreen" | "doctrine" | "essay"]
    graduation_rule: >
      [Once a note is Tier 3, can it be demoted? Usually: never.
       Or: specify the condition (e.g., "when published" moves to 40-Published/).]
    output_folder: [the folder where Tier 3 notes live — default "20-Output/", customizable per Q7]
```

---

### Q6 — Domain Taxonomy

```yaml
domains:
  # List every sub-domain that will have its own folder and frontmatter slug.
  # Priority determines build order: core domains are built first.
  - slug: [lowercase-hyphenated, e.g. "philosophy-of-mind"]
    label: [Display name, e.g. "Philosophy of Mind & AI"]
    folder: [relative path from vault root, e.g. "AI/Philosophy of Mind & AI/"]
    priority: [core | tier1 | tier2 | reference]
    evergreen_candidate: [true | false]
    # Required for accumulation vaults. Optional/omit for training and expression vaults.
    # false for purely technical/reference domains (lookup tables, procedures)
    # true for conceptual/analytical domains where insights graduate to Tier 3
```

**Note**: The `slug` value is what goes in note frontmatter as `domain: [slug]`. Keep it short and stable. The `label` can change; the `slug` should not.

**Note on `evergreen_candidate`**: This is a DEFAULT for new notes in this domain — not a fixed rule. Any individual note overrides it by setting its own `evergreen-candidate` value in frontmatter. The domain default determines what Claude writes when creating a new note; the note-level value determines which schema applies. Override direction: `false` → `true` only.

---

### Q7 — Output Layer

```yaml
output_layer:
  type: [evergreen-notes | training-curriculum | published-essays | doctrine-notes | hybrid]
  description: >
    [What does the final-form output look like? Who reads it? What does it do?
     Be concrete. "Timeless atomic notes" is too vague — describe the artifact.]
  graduation_folder: [the folder Tier 3 notes live in]
  graduation_command: [the slash command that produces this output, e.g. "/evergreen-note"]
  publication_target: [if expression vault: venue, audience, format. Otherwise: N/A]
```

---

---

### Post-Q7 — Runtime Blocks

These three blocks are **required for universal command execution**. They are formally added in Phase 1 (Doc 11) of the Genesis Protocol, but should be drafted now while the Q1–Q7 answers are fresh. Universal commands fail without them.

```yaml
# ── NUMBERING RATIONALE ──────────────────────────────────────────────────────
# 0x = CAPTURE (Tier 1) — raw, unprocessed input
# 1x = SOURCES (Tier 1) — processed input material
#      [gap]   (Tier 2) — unnumbered domain folders, vault-specific from Q6
# 2x = OUTPUT  (Tier 3) — final standalone notes
# 3x = NAVIGATION — Maps of Content
# 4x = TEMPLATES  — note scaffolding
# 5x+ = EXTENSIONS — vault-type-specific (e.g., 50-Curriculum/ for training vaults)
# Why no number for Tier 2? Domain folders are the vault's intellectual workspace —
# their names come from Q6 and must not be homogenized across vaults.
# ─────────────────────────────────────────────────────────────────────────────

folder_structure:
  # ── REQUIRED (consumed by universal commands — must exist in every vault) ──
  inbox: "00-Inbox/"
  sources: "10-Sources/"
  output: "20-Output/"             # customizable name — set by Q7 (e.g., "20-Judgment/", "20-Evergreen/")
  mocs: "30-MOCs/"
  templates: "40-Templates/"
  maps: "_maps/"                   # domain primer maps — always at vault root, never nested
  memory: "memory/"
  commands: ".claude/commands/"

  # ── DOMAIN (vault-specific, from Q6 — add one key per domain folder) ──
  # [domain_slug]: "[folder-path]/"
  # theory: "theory/"
  # complexity: "complexity/"

  # ── EXTENSIONS (vault-type-specific additions) ──
  # curriculum: "50-Curriculum/"   # training vaults
  # navigation: "navigation/"      # analytical sub-folders
```

```yaml
note_template:
  synthesis:
    additional_frontmatter:
      - "field: value  # vault-type-specific frontmatter beyond type/domain/evergreen-candidate"
      # Examples (use engagement_axis.config_key from intellectual_style for the axis field):
      # accumulation: "project_questions: []", "[config_key]: [position]", "open_problems: [N]"
      # training:     "level: [tactical|operational|strategic|all]", "[config_key]: [position]", "open_challenges: [N]"
      # expression:   "status: [raw|seed|outline|draft|revision|final]", "source_refs: []"
      # Where [config_key] = fault_line | central_dialectic | central_mystery | design_problem
    mandatory_sections:
      - "Section name: description of what this section requires"
      # List ALL mandatory body sections for Tier 2 synthesis notes in this vault.
      # Include the synthesis instrument (Connection to the Project / Judgment Instrument).
    five_questions:
      - "Question 1: quality-check question specific to this vault's principles"
      # List 5 yes/no questions that must all be "yes" before a note is finalized.
  reference:  # Omit this entire block for training and expression vaults
    mandatory_sections:
      - "Core idea (2-4 sentences)"
      - "Mechanism / Intuition"
      - "Brief implications"
```

```yaml
reference_docs:
  # Canonical file names — no vault/domain prefixes — all at vault root.
  open_problems: "open-problems.md"
  coverage_plan: "coverage-plan.md"
  development_plan: "development-plan.md"
  map_reference: "map-reference.md"
  note_taxonomy: "note-taxonomy.md"
  note_index: "memory/note-index.md"    # optional — auto-maintained cache; see command-lifecycle.md
```

**Note**: All paths are relative to vault root. Verify every path resolves before running universal commands. If a file does not exist yet, create a stub — commands that read missing reference_docs paths will fail at that step.

---

## Checklist Before Proceeding

Before running the Genesis Protocol, verify:

- [ ] Q1 mission is 1–2 sentences, not a paragraph
- [ ] Q2 has exactly 3 questions at 3 different levels (not 3 versions of the same question)
- [ ] Q0.5 intellectual style preset is selected
- [ ] Q3 engagement axis matches the selected style and passes the failure-mode check for that style
- [ ] Q4 has 8–15 problems, spanning all three driving questions
- [ ] Q5 graduation rules are specific enough to make decisions without judgment calls
- [ ] Q6 has at least 3 domains; none overlap significantly
- [ ] Q7 output type matches vault type (accumulation → evergreen-notes; training → doctrine; expression → essays)
- [ ] Post-Q7 runtime blocks (`folder_structure`, `note_template`, `reference_docs`) are drafted
- [ ] All `reference_docs` paths point to existing files (or stubs created for them)

If any item fails the check, fix vault-config.md before proceeding.
