---
type: template
audience: claude
---

# Map Type Template

Four universal map types. All maps share a five-element structural core — the parts that never change. Each type adds domain-specific sections. This document defines both the universal core and the type-specific extensions.

Maps are distinct from notes. Notes are atomic; maps are architectural. A map's job is not to teach a concept but to make visible the structural relationships among concepts. The Mermaid diagram is the map's heart — it must be built before any prose.

---

## Universal Map Rule

**Build the Mermaid diagram before writing any section prose.**

If you cannot draw the dependency architecture, you do not yet understand the system. The diagram forces the architecture to be explicit before it gets buried in prose. A map written without a diagram first is almost always a list dressed up as architecture.

---

## Five Structural Elements (All Map Types)

Every map must contain these five elements, in this order, before any type-specific sections:

### Element 1 — Context

Why this person/concept/domain/framework exists. What problem forced it into existence. What the prior landscape looked like before this emerged, and what it failed to do. The reader must understand WHY this subject matters before they encounter WHAT it is.

Quality test: if you removed this section, could the reader still assess why the subject is important? If yes, the Context section has not done its job.

### Element 2 — Architecture Diagram (Mermaid)

```mermaid
graph TD
    [concept/module A] --> [concept/module B]
    [concept/module B] --> [concept/module C]
    [concept/module A] --> [concept/module D]
```

The diagram must show:
- All major components (concepts, modules, phases, arguments)
- Their dependency relationships (which requires which; which generates which)
- Any feedback loops

The diagram must be intelligible without reading the prose. Label every node clearly. Direction matters: arrows should indicate "requires" or "generates," not just "relates to."

### Element 3 — Branch Analysis

One section per major component in the diagram. Each branch section must:
- Define what the component does (not just what it is)
- State what it depends on (which other component it requires)
- State what it enables or generates (downstream effects)
- Identify where it can fail or be contested

Depth over breadth. If a component is genuinely simple, say so in one paragraph and move on. If it is complex, give it the space it needs.

### Element 4 — Pressure Points

Where the system is internally stressed, limited, or strained. Required count: 3–7. Fewer = the system has not been analyzed critically enough. More = the analysis is disorganized.

For each pressure point, state the tension/limit precisely and then ground it concretely using the format from `intellectual_style.pressure_points.format`:

- *Adversarial* (`named_exploiter`): Name who identified or exploited this tension (a later thinker, historical event, empirical finding) and explain the exploitation move — how they entered through the gap. "This tension was exploited by [name] who [move]."
- *Dialectical* (`boundary_condition`): State the boundary condition under which the framework breaks down and the demonstration that revealed it. "This framework breaks down under [condition], as demonstrated by [case/proof/experiment]."
- *Contemplative* (`applicability_limit`): State the limit of the framework's explanatory reach and what exposes it. "This framework reaches its limit at [boundary], shown by [case/tradition/phenomenon]."
- *Constructive* (`failure_mode`): State the condition that triggers failure and what the failure produces. "This approach fails when [condition], producing [failure mode], as experienced in [case/system/incident]."

**The grounding requirement is universal**: regardless of style, every pressure point must reference a concrete case, thinker, demonstration, or incident. Abstract tensions without grounding do not qualify.

### Element 5 — Connection to the Project

This section is mandatory and must force engagement beyond affirmation — not just what this subject gives, but how it forces deeper thinking. Read `intellectual_style.engagement_field` for the exact engagement framing. Reference open problems by number and name.

```markdown
## Connection to the Project

### Resources
- **Gives [Q2.q1.label]**: [what this contributes to driving question 1]
- **Gives [Q2.q2.label]**: [what this contributes to driving question 2]
- **Gives [Q2.q3.label]**: [what this contributes to driving question 3]

### [engagement_field.name]
# Use the engagement field name from intellectual_style.engagement_field.name:
#   Adversarial:   "Threats" — what this challenges or destabilizes
#   Dialectical:   "Complicates" — what prior understanding this forces revision of
#   Contemplative: "Transforms" — what perception this changes
#   Constructive:  "Constrains" — what design tradeoffs this introduces
- **[engagement_field.name] [open problem N]**: [specific engagement with this open problem]
- **[engagement_field.name] [assumption/framework/conclusion]**: [concrete analysis]

### [engagement_axis.label] Position
# Use the engagement axis label and positions from intellectual_style.engagement_axis:
This [person/concept/domain/framework] [position from engagement_axis.positions[]] the [engagement_axis.label] because: [one sentence explanation].

### Atomic Notes to Generate
List of 8–15 candidate Tier 2 notes that should be created from this map's content. These are the map's deliverables.

For each note, set `evergreen-candidate` according to the domain default (see vault's Two-Zone Architecture). Override at note level if the note's content warrants synthesis schema.
- `YYYYMMDDHHMM - [Title as claim]`
- ...
```

---

## Map Type 1 — Person/Thinker Map

**Purpose**: Systematic analysis of one person's complete intellectual framework.

**Naming**: `[lastname]-systematic-map.md`

**Location**: Domain subfolder (accumulation vault) or `theory/maps/` (training vault)

**Additional sections** (beyond the five universal elements):

| Section | Content |
|---|---|
| YAML Frontmatter | Schema from vault's map-reference.md — populated BEFORE any prose |
| I. Context | (universal Element 1) |
| II. Architecture Diagram | (universal Element 2) |
| III. Intellectual Arc | Major phases of this thinker's development; what changed and why |
| IV–X. Branch Analysis | (universal Element 3 — one section per major concept) |
| XI. Pressure Points | (universal Element 4) |
| XII. Reception & Influence | Who used this thinker, how, and what they got wrong |
| XIII. Connection to the Project | (universal Element 5) |

**Typical sections**: ~13 (varies with branch count — IV–X expand or contract to match the thinker's major concepts)

**Depth target**: 400–600 lines. Less means insufficient analysis; more means poor organization.

**Hard rules**:
- YAML frontmatter is NOT one of the 13 sections — it comes before all sections
- Section XI (Pressure Points) must ground each tension concretely using the style's format (see Element 4)
- Section XIII (Connection to the Project) must engage the project beyond affirmation — the engagement field entry cannot be left empty or generic

---

## Map Type 2 — Concept/System Map

**Purpose**: Deep structural analysis of a major concept or technical system too large for a single note and not tied to one person.

**Naming**: `[concept-slug]-concept-map.md`

**Location**: Relevant domain subfolder

**Additional sections** (beyond five universal elements):

| Section | Content |
|---|---|
| YAML Frontmatter | Type: concept-map, domain, status, connects-to |
| I. Context | (universal Element 1) |
| II. Architecture Diagram | (universal Element 2) |
| III. Historical Emergence | How did this concept develop? What attempts failed before this formulation? |
| IV–VIII. Branch Analysis | (universal Element 3 — one section per major component of the concept) |
| IX. Pressure Points | (universal Element 4) |
| X. Connection to the Project | (universal Element 5) |

**Total sections**: 10

**Depth target**: 250–400 lines.

---

## Map Type 3 — Domain Map (Primer)

**Purpose**: Orientation document for one sub-domain. Answers: "Why does this domain exist and how does it fit?" Not deep analysis — navigational and conceptual overview.

**Naming**: `primer-[domain-slug].md`

**Location**: `_maps/` or `maps/` folder in vault root

**Sections**:

| Section | Content |
|---|---|
| YAML Frontmatter | Type: domain-primer, domain, connects-to |
| I. What This Domain Is | Scope, organizing question, key insight (not a list of topics) |
| II. Why the Project Needs This Domain | What gap it fills; what it makes possible that nothing else does |
| III. Core Objects / Primitives | The fundamental units this domain operates with |
| IV. Key Results | 3–6 major findings, theorems, or arguments — brief but precise |
| V. Geometric / Physical Intuition | A spatial or physical metaphor that makes the domain's structure vivid |
| VI. Domain Connections | How this domain connects to adjacent domains in the vault |
| VII. Vault Connections | 4–8 wikilinks to existing vault notes this domain speaks to |
| VIII. Note Index | Grouped list of all notes in this domain (updated as notes are added) |

**Total sections**: 8

**Depth target**: 80–130 lines. Primers are navigation documents, not comprehensive treatments.

---

## Map Type 4 — Framework Map

**Purpose**: Deep structural analysis of an operational or analytical framework — a structured method for doing something (planning, analysis, decision-making). Distinct from a concept map (which analyzes an idea) and a thinker map (which analyzes a person).

**Naming**: `[framework-slug]-framework-map.md`

**Location**: `theory/maps/` (training vault) or domain subfolder (others)

**Additional sections** (beyond five universal elements):

| Section | Content |
|---|---|
| YAML Frontmatter | Type: framework-map, domain, level, [engagement_axis.config_key] |
| I. Context | (universal Element 1 — the operational failure that forced this framework) |
| II. Architecture Diagram | (universal Element 2) |
| III. Application Conditions | When to use this framework; what conditions it requires; what conditions invalidate it |
| IV–IX. Branch Analysis | (universal Element 3 — one section per major step/component) |
| X. Failure Modes | Conditions under which the framework breaks; common misapplications |
| XI. Pressure Points | (universal Element 4) |
| XII. Connection to the Project | (universal Element 5) |

**Typical sections**: ~12 (branch count varies — IV–IX expand or contract to match the framework's major components)

**Depth target**: 350–500 lines.

---

## Common Map Failures

**Failure 1: Diagram built after prose**
The diagram becomes a summary of the prose instead of its architecture. The prose organization then mirrors the diagram instead of following logical dependencies. Fix: always start with the diagram.

**Failure 2: Branch sections are summary paragraphs**
Sections that describe "what X believed about Y" without analyzing internal dependencies. Fix: every branch section must answer "what does this depend on?" and "what does this enable?"

**Failure 3: Pressure points without grounding**
Listing tensions as abstract claims without a concrete case, thinker, demonstration, or incident. Fix: every pressure point must reference something real, using the style's format (named exploiter / boundary condition / applicability limit / failure mode). Abstract tensions do not qualify.

**Failure 4: Connection to Project lists only resources**
Section XIII/X/XII reads as an endorsement, not an analysis. Fix: the engagement field entry must name something specific — a specific assumption challenged, a specific understanding revised, a specific perception transformed, a specific tradeoff introduced. Generic or empty engagement field entries fail.

**Failure 5: Map and notes conflated**
Writing a map that tries to be a comprehensive collection of atomic notes, or writing atomic notes that are really branches of a map. Fix: if a document is trying to cover multiple independent claims, it is a map. If it is trying to cover one claim deeply, it is a note.
