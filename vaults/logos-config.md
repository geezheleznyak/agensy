---
type: vault-config-extract
vault: synthesis_logos
audience: claude
---
# vault-config Extract — synthesis_logos

Q1–Q7 answers extracted from `synthesis_logos/vault-config.md`. Full runtime config lives in vault root.

**Note**: logos is an expression vault — its architecture differs from accumulation and training vaults. Driving questions (Q2) and fault line (Q3) are inherited from synthesis_theoria rather than defined independently. The vault's structural distinctives are in Q5 (note tier structure) and Q7 (output layer).

---

```yaml
vault:
  name: synthesis_logos
  path: "/path/to/synthesis_logos/"
  type: expression

mission: >
  Turn raw thinking into published essays and arguments in the user's own voice —
  expressing the positions, insights, and arguments that emerge from synthesis_theoria's
  knowledge base, for audiences ranging from general readers to philosophical audiences.
  The vault does not generate new knowledge; it distills, sharpens, and voices it.

driving_questions:
  # Inherited from synthesis_theoria — expression vault does not define independent questions
  q1:
    label: metaphysical
    text: "(inherited from synthesis_theoria)"
  q2:
    label: anthropological
    text: "(inherited from synthesis_theoria)"
  q3:
    label: normative
    text: "(inherited from synthesis_theoria)"

fault_line:
  # Inherited from synthesis_theoria
  statement: "(inherited — Is the universe's tendency toward increasing complexity ontologically real with normative significance, or epistemic/neutral?)"
  positions:
    - real-and-normative
    - epistemic-or-neutral
    - contested
    - dissolves

intellectual_style:
  # Inherited from synthesis_theoria — adversarial preset
  preset: adversarial

open_problems:
  # Inherited from synthesis_theoria open-problems list

note_tiers:
  tier1:
    name: Fragment
    type_value: fragment
    description: Raw thinking, argument sketches, draft passages — lives in 00-Inbox/
    graduation_rule: When a fragment connects to a specific synthesis_theoria note and stakes a claim.
  tier2:
    name: Argument
    type_value: argument
    description: >
      Developed argument unit — one claim, fully defended, with evidence from synthesis_theoria.
      Not a summary: an argument. Lives in domain subfolders.
    graduation_rule: >
      When the argument is complete, evidence is from synthesis_theoria notes (linked),
      and the argument can stand alone without the underlying vault.
  tier3:
    name: Essay
    type_value: essay
    description: >
      Complete publishable essay — assembled from Tier 2 arguments, in the user's voice,
      ready for an external audience. Lives in 20-Essays/.
    graduation_rule: Never demoted once published.
    output_folder: "20-Essays/"

domains:
  - slug: philosophy-essays
    label: "Philosophy and Metaphysics Essays"
    folder: "philosophy/"
    priority: core
    evergreen_candidate: true
  - slug: ai-human-essays
    label: "AI and Human Nature Essays"
    folder: "ai-human/"
    priority: core
    evergreen_candidate: true
  - slug: ethics-essays
    label: "Ethics and Virtue Essays"
    folder: "ethics/"
    priority: tier1
    evergreen_candidate: true

output_layer:
  type: published-essays
  description: >
    Complete essays in the user's voice — the public-facing output of the synthesis_theoria
    knowledge base. Organized by theme and publication target.
  graduation_folder: "20-Essays/"
  connection: >
    Type 1 — receives from synthesis_theoria. Does not contribute back to accumulation arcs.

folder_structure:
  inbox: "00-Inbox/"
  drafts: "10-Drafts/"
  output: "20-Essays/"
  mocs: "30-MOCs/"
  templates: "40-Templates/"
  memory: "memory/"
  commands: ".claude/commands/"

reference_docs:
  coverage_plan: "memory/coverage-plan.md"
```
