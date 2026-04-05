---
type: vault-config-extract
vault: synthesis_bellum
audience: claude
---
# vault-config Extract — synthesis_bellum

Q1–Q7 answers extracted from `synthesis_bellum/vault-config.md`. Full runtime config lives in vault root.

---

```yaml
vault:
  name: synthesis_bellum
  path: "/path/to/synthesis_bellum/"
  type: training

mission: >
  Build a complete training framework for developing a military commander from zero to one
  in an era of AI, drones, autonomous systems, electronic warfare, shifting great-power dynamics,
  and complex game-theoretic interactions. Three outputs: commanders who can read the operational
  environment (Strategic), design adaptive campaigns (Operational), and decide under pressure
  with AI/autonomous systems (Command).

driving_questions:
  q1:
    label: strategic
    text: >
      What is the nature of war in the AI/drone/EW era — what principles persist,
      what is genuinely new, and what strategic frameworks apply?
  q2:
    label: operational
    text: >
      How do you design and adapt military campaigns under uncertainty and technological
      disruption — what operational art survives the current revolution in military affairs?
  q3:
    label: command
    text: >
      How does a commander decide under pressure, fog, and time compression with
      AI/autonomous systems — what human judgment is required and where does it fail?

intellectual_style:
  preset: adversarial
  engagement_axis:
    config_key: fault_line
    label: "Continuity vs. Discontinuity in War"
    positions:
      - continuity: "Eternal principles of war persist — the AI/drone revolution requires reapplication, not reinvention of first principles"
      - discontinuity: "The current revolution is genuine — new first principles are required that classical doctrine cannot provide"
      - synthesis: "Core principles persist at the strategic level; operational and tactical doctrine requires fundamental revision"
      - domain-dependent: "Continuity holds at sea and in the air; land warfare faces genuine discontinuity from drone/autonomous proliferation"
  engagement_field:
    name: Threatens
    prompt: "What does this challenge or destabilize in current doctrine or operational assumptions?"
  pressure_points:
    format: named_exploiter

fault_line:
  statement: >
    Does the AI/drone/hypersonics/EW revolution create genuine discontinuity in the nature
    of war requiring new first principles — or do eternal principles of war maintain continuity
    and require only reapplication to new technology?
  positions:
    - continuity
    - discontinuity
    - synthesis
    - domain-dependent

open_problems:
  - id: 1
    name: "The Discontinuity Problem"
    question: "Is the current military revolution generating genuine discontinuity — new first principles — or repackaging old ones?"
    bears_on: q1
  - id: 2
    name: "The Command Authority Problem"
    question: "At what decisions should human authority be mandatory — and how does AI integration shift the locus of decisive judgment?"
    bears_on: q3
  - id: 3
    name: "The Friction Problem"
    question: "Does AI reduce Clausewitzian friction or transform it — creating new forms of uncertainty while eliminating old ones?"
    bears_on: q1+q2
  - id: 4
    name: "The Drone Swarm Problem"
    question: "How does mass autonomy change the calculus of attrition, maneuver, and surprise at the operational level?"
    bears_on: q2
  - id: 5
    name: "The EW Dependency Problem"
    question: "As forces become dependent on electromagnetic spectrum dominance, how does EW vulnerability reshape operational design?"
    bears_on: q2
  - id: 6
    name: "The OODA Compression Problem"
    question: "When AI compresses decision cycles, what remains of human OODA advantages — and where does human judgment become decisive?"
    bears_on: q3
  - id: 7
    name: "The Escalation Ladder Problem"
    question: "How does autonomous weapons proliferation alter escalation dynamics — and where are the new red lines?"
    bears_on: q1+q2
  - id: 8
    name: "The Training Doctrine Problem"
    question: "What does commander development look like in an era where technical competence and judgment competence may diverge?"
    bears_on: q3
  - id: 9
    name: "The Coalition Problem"
    question: "How do AI/autonomous systems affect interoperability — and what are the command implications of technology-divergent coalitions?"
    bears_on: q2+q3
  - id: 10
    name: "The Clausewitz Survival Problem"
    question: "Which elements of Clausewitz's theory survive the autonomous revolution — and which must be replaced?"
    bears_on: q1
  - id: 11
    name: "The Moral Agency Problem"
    question: "When autonomous systems cause harm, how is moral responsibility distributed — and what are the command implications?"
    bears_on: q3
  - id: 12
    name: "The Adaptation Rate Problem"
    question: "What institutional mechanisms allow militaries to adapt doctrine at the rate required by current technology cycles?"
    bears_on: q1+q2

note_tiers:
  tier1:
    name: Source
    type_value: source
    description: Doctrine documents, case studies, after-action reviews, primary texts. Lives in 10-Sources/.
    graduation_rule: When one operational insight can be extracted and linked to open problems.
  tier2:
    name: Concept
    type_value: concept
    description: >
      Atomic concept notes and doctrine analyses. Zone 2 (synthesis) for operational
      insights connected to driving questions. Zone 1 (reference) for technical scaffolding.
    graduation_rule: >
      When atomic, standalone, mandatory sections complete, Threatens entry names a
      specific threat to current doctrine, and fault_line position set.
  tier3:
    name: Doctrine
    type_value: doctrine
    description: >
      Permanent doctrine statements — claim-titled, fully standalone, ready for operational use.
    graduation_rule: Never demoted.
    output_folder: "50-Curriculum/"

domains:
  - slug: strategic-theory
    label: "Strategic Theory"
    folder: "theory/strategic/"
    priority: core
    evergreen_candidate: true
  - slug: operational-art
    label: "Operational Art"
    folder: "theory/operational/"
    priority: core
    evergreen_candidate: true
  - slug: command-decision
    label: "Command and Decision"
    folder: "theory/command/"
    priority: core
    evergreen_candidate: true
  - slug: emerging-tech
    label: "AI, Drones, and EW"
    folder: "emerging-tech/"
    priority: tier1
    evergreen_candidate: true
  - slug: case-studies
    label: "Operational Case Studies"
    folder: "case-studies/"
    priority: tier1
    evergreen_candidate: mixed
  - slug: theorists
    label: "Strategic Theorists"
    folder: "theorists/"
    priority: tier2
    evergreen_candidate: true

output_layer:
  type: doctrine-modules
  description: >
    Training curriculum modules — structured doctrine statements for commander development.
    Built from synthesis notes; organized into curriculum phases.
  graduation_folder: "50-Curriculum/"

folder_structure:
  inbox: "00-Inbox/"
  sources: "10-Sources/"
  output: "50-Curriculum/"
  mocs: "30-MOCs/"
  templates: "40-Templates/"
  maps: "theory/maps/"
  memory: "memory/"
  commands: ".claude/commands/"

reference_docs:
  map_reference: "theory/maps/map-reference.md"
  coverage_plan: "memory/coverage-plan.md"
  open_problems: "open-problems.md"
```
