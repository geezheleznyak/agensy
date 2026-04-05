---
type: vault-config-extract
vault: synthesis_theoria
audience: claude
---
# vault-config Extract — synthesis_theoria

Q1–Q7 answers extracted from `synthesis_theoria/vault-config.md`. Full runtime config lives in vault root.

---

```yaml
vault:
  name: synthesis_theoria
  path: "/path/to/synthesis_theoria/"
  type: accumulation

mission: >
  Build a comprehensive metaphysical and anthropological framework for post-AI humanity
  — connecting cosmology, anthropology, and ethics — that yields the highest human virtues
  given the deep structure of reality, the nature of the human being, and the challenge of
  artificial intelligence. The vault's output is a derivation: cosmology → anthropology → ethics.

driving_questions:
  q1:
    label: metaphysical
    text: >
      What is the deep structure of reality — especially with respect to becoming,
      creativity, complexity, and value?
  q2:
    label: anthropological
    text: >
      What is the human being, such that this structure matters to it?
      How does the human relate to (or differ from) artificial intelligence?
  q3:
    label: normative
    text: >
      What follows for how humans should live? What are the highest human virtues
      given this metaphysics and this anthropology?

intellectual_style:
  preset: adversarial
  engagement_axis:
    config_key: fault_line
    label: "Complexity and Normativity"
    positions:
      - real-and-normative: >
          The complexity trend is ontologically real and normatively significant —
          it grounds a genuine derivation from cosmology to ethics
      - epistemic-or-neutral: >
          The trend is epistemic or normatively neutral — no normative conclusion follows
          from cosmological description
      - contested: >
          The trend is real in some sense but the normative significance is limited
          or qualified — a partial challenge without full denial
      - dissolves: >
          The question as posed is ill-formed — the fact/value distinction makes it
          meaningless to ask whether a cosmological trend has normative significance
  engagement_field:
    name: Threatens
    prompt: "What does this challenge, destabilize, or undermine in the project's derivation?"
  pressure_points:
    format: named_exploiter

fault_line:
  statement: >
    Is the universe's tendency toward increasing complexity an ontologically real tendency
    with normative significance — or is it an epistemic imposition or a normatively neutral
    mechanical byproduct?
  positions:
    - real-and-normative
    - epistemic-or-neutral
    - contested
    - dissolves

open_problems:
  - id: 1
    name: "The Three Questions — Can They Be Unified?"
    question: "Can the cosmology → anthropology → ethics derivation be logically unified, or do unbridgeable gaps remain between its levels?"
    bears_on: q1+q2+q3
  - id: 2
    name: "The Framing Problem — Philosophy or Ideology?"
    question: "Is the project genuine philosophy (following evidence wherever it leads) or ideology (selecting metaphysics to support desired normative conclusions)?"
    bears_on: q1+q3
  - id: 3
    name: "Post-AI Assumption — Rupture or Continuity?"
    question: "Does AI represent a genuine rupture in human self-understanding that demands a new framework, or does it extend familiar challenges?"
    bears_on: q2+q3
  - id: 4
    name: "Epistemic vs. Ontological Emergence"
    question: "Is emergence in complex systems a feature of reality itself (ontological) or only of our descriptions and models (epistemic)?"
    bears_on: q1
  - id: 5
    name: "The Teleology Dilemma"
    question: "Does the complexity trend imply directionality or purpose in nature, or is teleological language always an illusion projected onto mechanism?"
    bears_on: q1+q3
  - id: 6
    name: "The Agency Problem"
    question: "How is genuine agency possible in a world of causal determination — and does the answer differ for biological vs. artificial agents?"
    bears_on: q2+q3
  - id: 7
    name: "Is Intelligence Substrate-Independent?"
    question: "Does the nature of the physical substrate (biological vs. silicon) matter to the nature of intelligence, consciousness, or value?"
    bears_on: q2+q3
  - id: 8
    name: "Does the Complexity Trend Imply Replacement?"
    question: "If AI is the next complexity node, does the project's own metaphysics imply that AI supersedes biological intelligence as the highest form?"
    bears_on: q2+q3
  - id: 9
    name: "The Consciousness Question"
    question: "Is consciousness reducible to information processing (making AI consciousness possible) or does it require biological substrate?"
    bears_on: q2
  - id: 10
    name: "Is Human Nature Fixed or Process?"
    question: "Is there a stable human nature that grounds ethics, or is human nature itself a process — and if the latter, what does ethics become?"
    bears_on: q2+q3
  - id: 11
    name: "Can Process Metaphysics Resist Accelerationism?"
    question: "Does process philosophy have resources to resist accelerationist conclusions about capital-AI convergence as the next complexity node?"
    bears_on: q1+q3
  - id: 12
    name: "The Structural Isomorphism Trap"
    question: "When similar structures appear across cosmology, biology, and cognition, does this reflect deep unity in reality, or superficial analogy that misleads synthesis?"
    bears_on: q1+q2

note_tiers:
  tier1:
    name: Source
    type_value: source
    description: Raw highlights, captures, reading notes. Lives in 10-Sources/ or 00-Inbox/.
    graduation_rule: When one insight can be extracted that connects to the driving questions.
  tier2:
    name: Concept
    type_value: concept
    description: >
      Atomic permanent notes. Zone 2 (synthesis schema, evergreen-candidate: true) for
      project-connected insights. Zone 1 (reference schema, evergreen-candidate: false) for
      technical scaffolding.
    graduation_rule: >
      When the note is atomic, fully standalone, all mandatory sections complete,
      Threatens entry names a specific threat, and fault_line is set.
  tier3:
    name: Evergreen
    type_value: evergreen
    description: >
      Fully matured permanent notes — the vault's output artifacts. Title states a claim;
      fully standalone; all See Also links verified.
    graduation_rule: Never demoted.
    output_folder: "20-Evergreen/"

domains:
  - slug: cosmology
    label: "Cosmology and Complexity"
    folder: "cosmology/"
    priority: core
    evergreen_candidate: true
  - slug: philosophy-of-mind
    label: "Philosophy of Mind and AI"
    folder: "philosophy-of-mind/"
    priority: core
    evergreen_candidate: true
  - slug: ethics
    label: "Ethics and Anthropology"
    folder: "ethics/"
    priority: core
    evergreen_candidate: true
  - slug: epistemology
    label: "Epistemology"
    folder: "epistemology/"
    priority: tier1
    evergreen_candidate: true
  - slug: process-philosophy
    label: "Process Philosophy"
    folder: "process-philosophy/"
    priority: tier1
    evergreen_candidate: true
  - slug: cognitive-science
    label: "Cognitive Science"
    folder: "cognitive-science/"
    priority: tier2
    evergreen_candidate: mixed

output_layer:
  type: evergreen-notes
  description: >
    Atomic synthesis notes advancing the cosmology → anthropology → ethics derivation.
    The vault's output is the derivation itself, assembled from these notes.
  graduation_folder: "20-Evergreen/"

folder_structure:
  inbox: "00-Inbox/"
  sources: "10-Sources/"
  output: "20-Evergreen/"
  mocs: "30-MOCs/"
  templates: "40-Templates/"
  maps: "_maps/"
  memory: "memory/"
  commands: ".claude/commands/"

reference_docs:
  map_reference: "_maps/map-reference.md"
  coverage_plan: "memory/coverage-plan.md"
  open_problems: "open-problems.md"
```
