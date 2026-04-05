---
type: vault-config-extract
vault: synthesis_politeia
audience: claude
---
# vault-config Extract — synthesis_politeia

Q1–Q7 answers extracted from `synthesis_politeia/vault-config.md`. Full runtime config lives in vault root.

---

```yaml
vault:
  name: synthesis_politeia
  path: "/path/to/synthesis_politeia/"
  type: accumulation

mission: >
  Build a comprehensive map of political and geopolitical reality — how power is built,
  contested, and exercised at every scale from domestic politics to great-power competition
  — enabling fluent situational diagnosis and optimal calculation in any decision shaped by
  political dynamics. Output: the capacity to move from raw events to structural diagnosis
  to the optimal move, without illusions.

driving_questions:
  q1:
    label: structural
    text: >
      What are the structural forces that generate political outcomes — the distributions
      of power, institutional configurations, and material constraints that shape what actors
      can do regardless of their intentions?
  q2:
    label: diagnostic
    text: >
      How do you accurately read a political situation — identifying what type of conflict
      it is, what structural forces are operating, and what options are actually available?
  q3:
    label: strategic
    text: >
      How do actors build, exercise, and project power effectively — and what are the
      characteristic errors that destroy political capacity?

intellectual_style:
  preset: adversarial
  engagement_axis:
    config_key: fault_line
    label: "Structure vs. Ideas in Political Causation"
    positions:
      - structuralist: "Political behavior is primarily explained by material interests and structural constraints — ideas and identities are epiphenomenal"
      - ideational: "Ideas, identities, and beliefs are independent causal forces that cannot be reduced to material conditions"
      - interactive: "Ideas and structures mutually constitute each other — neither is prior; the relationship is the explanation"
      - situational: "Which frame applies depends on the type of political conflict — no single lens is universally correct"
  engagement_field:
    name: Threatens
    prompt: "What does this challenge or destabilize in the project's map of political reality?"
  pressure_points:
    format: named_exploiter

fault_line:
  statement: >
    Is political behavior primarily driven by material interests and structural constraints
    — or by ideas, identities, and beliefs that cannot be reduced to material conditions?
  positions:
    - structuralist
    - ideational
    - interactive
    - situational

open_problems:
  - id: 1
    name: "The Agency and Structure Problem"
    question: "How much causal weight do individual leaders carry vs. structural forces? When does agent variance matter?"
    bears_on: q1+q2
  - id: 2
    name: "The Ideology and Interest Problem"
    question: "When do stated values and ideologies genuinely constrain actors, and when are they strategic cover for material interests?"
    bears_on: q1+q3
  - id: 3
    name: "The Legitimacy Problem"
    question: "What generates political legitimacy and why does it collapse? How does legitimacy interact with coercive capacity?"
    bears_on: q1+q2
  - id: 4
    name: "The Prediction Problem"
    question: "Why is political forecasting so consistently poor, and what kind of prediction is actually possible from structural analysis?"
    bears_on: q2+q3
  - id: 5
    name: "The Coalition Problem"
    question: "What determines whether a political coalition holds together or fragments under stress?"
    bears_on: q1+q3
  - id: 6
    name: "The Authoritarian Stability Problem"
    question: "What makes authoritarian regimes stable over time, and what actually triggers their collapse?"
    bears_on: q1+q2
  - id: 7
    name: "The Soft Power Problem"
    question: "Does soft power translate into hard influence, or is it an epiphenomenon that disappears under structural pressure?"
    bears_on: q1+q3
  - id: 8
    name: "The Information and Intelligence Problem"
    question: "How do political actors gather and act on information — and how do information asymmetries generate power?"
    bears_on: q2+q3
  - id: 9
    name: "The Transition Problem"
    question: "What determines whether political transitions produce durable new regimes or cycle back to the prior configuration?"
    bears_on: q1+q2
  - id: 10
    name: "The Technology and Power Problem"
    question: "How does technological disruption (AI, surveillance, information warfare) reshape the structure of political power?"
    bears_on: q1+q3
  - id: 11
    name: "The Great Power Competition Problem"
    question: "What structural features of multipolar competition make it more or less stable — and where is the current configuration?"
    bears_on: q1+q2
  - id: 12
    name: "The Identity Politics Problem"
    question: "When does ethnic, religious, or nationalist identity become an autonomous political force, and when is it instrumentalized?"
    bears_on: q1+q2

note_tiers:
  tier1:
    name: Source
    type_value: source
    description: Raw captures, debate summaries, primary source extracts. Lives in 10-Sources/.
    graduation_rule: When one structural insight can be extracted.
  tier2:
    name: Analysis
    type_value: analysis
    description: >
      Atomic concept notes explaining mechanisms, thinkers, historical cases.
      Zone 2 (synthesis schema) for project-connected insights.
      Zone 1 (reference schema) for technical scaffolding.
    graduation_rule: >
      When atomic, standalone, all mandatory sections complete, Threatens entry specific,
      and fault_line position set.
  tier3:
    name: Judgment
    type_value: judgment
    description: Permanent claim-titled notes — definitive positions on political mechanisms.
    graduation_rule: Never demoted.
    output_folder: "20-Judgment/"

domains:
  - slug: power-strategy
    label: "Power and Strategy"
    folder: "power-strategy/"
    priority: core
    evergreen_candidate: true
  - slug: state-institutions
    label: "State and Institutions"
    folder: "state-institutions/"
    priority: core
    evergreen_candidate: true
  - slug: geopolitics
    label: "Geopolitics and IR"
    folder: "geopolitics/"
    priority: core
    evergreen_candidate: true
  - slug: political-economy
    label: "Political Economy"
    folder: "political-economy/"
    priority: tier1
    evergreen_candidate: true
  - slug: identity-ideology
    label: "Identity and Ideology"
    folder: "identity-ideology/"
    priority: tier1
    evergreen_candidate: true
  - slug: information-intelligence
    label: "Information and Intelligence"
    folder: "information-intelligence/"
    priority: tier1
    evergreen_candidate: true
  - slug: technology-power
    label: "Technology and Power"
    folder: "technology-power/"
    priority: tier2
    evergreen_candidate: true

output_layer:
  type: judgment-notes
  description: >
    Permanent claim-titled notes that state structural mechanisms of political power —
    the vault's lenses for reading any political situation.
  graduation_folder: "20-Judgment/"

folder_structure:
  inbox: "00-Inbox/"
  sources: "10-Sources/"
  output: "20-Judgment/"
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
