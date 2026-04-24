---
type: template
audience: claude
---

# Note Tier Template

Universal three-tier note system. The tier names and graduation criteria are domain-adapted in each vault's `vault-config.md`, but the structure is invariant. This document defines the universally fixed elements — the parts that never change regardless of domain.

---

## Universal Tier Logic

Every vault has exactly three tiers. The same note never lives in two tiers. Promotion is always possible; demotion never happens. The tiers serve different cognitive functions:

| Tier | Cognitive Function | Typical Lifetime |
|---|---|---|
| 1 | Capture and lookup — preserve information without losing it | Days to weeks; most promote or get deleted |
| 2 | Mechanistic explanation — understand HOW and WHY | Months; most eventually graduate or stay here |
| 3 | Atomic permanent insight — a distilled claim that stands forever | Indefinite; never demoted |

The error pattern in every new vault is the same: too many notes stuck at Tier 1 (undeveloped), too few at Tier 3 (over-generalized, not atomic). The graduation rules exist to force the movement.

---

## Fixed Frontmatter Schema

These fields are present in every note in every vault, regardless of type:

```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: [tier-specific type_value from vault-config.note_tiers]
domain: [slug from vault-config.domains]
source: "[[Source Note Name]]"
aliases: []
```

These fields are present in every Tier 2 and Tier 3 **synthesis-schema** note (added at promotion from Tier 1):

```yaml
[engagement_axis.config_key]: "[one of engagement_axis.positions[]]"
# engagement_axis.config_key is determined by the vault's intellectual_style preset:
#   adversarial   → fault_line
#   dialectical   → central_dialectic
#   contemplative → central_mystery
#   constructive  → design_problem
open_problems: [list of open problem IDs from vault-config.open_problems]
```

*Reference-schema notes (accumulation vaults, `evergreen-candidate: false`) omit these fields. See § Tier 2 Reference Schema.*

Domain-specific fields (defined per vault type, added alongside universal fields):

**Accumulation vault (omega model)**:
```yaml
project_questions: [list of driving question labels, e.g. metaphysical, anthropological, normative]
evergreen-candidate: [true | false]
```

**Training vault (belli model)**:
```yaml
level: [tactical | operational | strategic | all]
open_challenges: [list of open problem IDs]
```

**Expression vault (cogitationis model)**:
```yaml
status: [raw | developed | seed | outline | draft | revision | final]
omega_refs: []   # wikilinks to source vault notes this relies on
```

---

## Schema Selection Rule

In accumulation vaults with mixed domains (the omega model), Tier 2 notes come in two schemas: **Synthesis** and **Reference**. The governing rule:

- The `evergreen-candidate` field at **note level** determines the schema — not the domain.
- The domain's `evergreen_candidate` value in `vault-config.md` is the **default for new notes** in that domain.
- Any individual note overrides the domain default by setting its own `evergreen-candidate` value.
- Override direction: `false` → `true` only. Never demote a synthesis note to reference schema.

When creating a new note: check the domain default. Apply the matching schema. If the note grows to connect with the vault's driving questions or engagement axis, override `evergreen-candidate` to `true` and upgrade to synthesis schema.

---

## Fixed Note Sections by Tier

### Tier 1 — Minimal Structure

Tier 1 notes have no mandatory sections beyond frontmatter and content body. The content body can be:
- A lookup table
- A procedure list
- An embedded image with a caption
- A raw capture / inbox note
- A list of definitions

No body structure is required at Tier 1. The ONLY requirement is that the note not be empty.

### Tier 2 — Two Schema Variants

Tier 2 notes come in two schemas determined by `evergreen-candidate`. See Schema Selection Rule above.

---

### Tier 2 Synthesis Schema (`evergreen-candidate: true`)

Use when the note connects to the vault's driving questions (Q2) or engagement axis (Q3). All sections mandatory.

**1. Opening paragraph (no heading)**

The first paragraph after the title must state:
- The PROBLEM that forced this concept into existence (not just a definition)
- Why the prior framework could not handle the problem
- What the concept does to resolve it

Quality test: a reader who sees only the opening paragraph should understand not just *what* the concept is but *why it had to be formulated*.

**2. Body**

Explains the concept mechanically — how it works, what it operates on, what it produces. Must include an **Internal Dependencies** statement: what does this concept depend on within its framework? What does it enable or constrain? What would break if it were removed?

**3. Vault-type body sections** (varies; defined in vault's CLAUDE.md):

- Accumulation vault: `## Examples / Analogies`
- Training vault: `## Why This Had to Be Developed` + `## Stress Test` + `## Adversarial Mirror`
- Expression vault: none additional — body and argument carry the load

**4. Why It Matters / Implications**

Implications for the vault's mission (Q1). Must end with `### Connection to the Project` containing:
- **Gives**: concrete resource for the vault's driving questions (Q2)
- **[engagement_field.name]**: forced engagement beyond surface understanding — this entry is MANDATORY; comfortable confirmation is not analysis. Read `intellectual_style.engagement_field.prompt` for the exact question to answer.
  - *Adversarial*: what assumption or desired conclusion does this attack?
  - *Dialectical*: what prior understanding does this force revision of?
  - *Contemplative*: what can the reader perceive or distinguish after absorbing this that they could not before?
  - *Constructive*: what design tradeoff does this introduce?
  - **Escape valve** (if `intellectual_style.engagement_field.escape_valve: true` and at Tier 2): "No genuine [field] — [mandatory justification]" is accepted. Escape-valve entries block Tier 3 promotion.
- **[engagement_axis.label] position**: explicit position from `engagement_axis.positions[]` with one explanatory sentence.

**5. Internal Tensions** (1–3 items)

Each tension must be internal to the concept's own commitments, not external disagreement. Format adapts by style (read `intellectual_style.internal_tensions.format`):

- *Adversarial* (`exploiter_and_move`): "Named with who exploited it and how they entered through it."
- *Dialectical* (`context_and_limit`): "Named with the context that exposed it and the structural limitation revealed."
- *Contemplative* (`unresolved_depth`): "Named as an unresolved depth, with who/which tradition addressed it and how."
- *Constructive* (`tradeoff_and_degradation`): "Named as a design tradeoff with the degradation it produces under specific conditions."

If `intellectual_style.internal_tensions.allow_stable_justification: true`: "No significant internal tensions — [mandatory justification]" is accepted for genuinely stable concepts.

**What does NOT count as an internal tension**: mere external disagreement from another tradition; anachronistic objection; empirical refutation from outside the concept's domain.

**6. See Also**

4–8 wikilinks. Requirements:
- At least one cross-domain link (links to a different domain than this note's domain)
- All links must be to existing notes (verify before writing)

**7. Open Questions**

At least one question must reference a specific open problem from the vault's `open_problems` list by number and name. Format: *(→ Open Problem N: Name)*

---

### Tier 2 Reference Schema (`evergreen-candidate: false`)

*Applies to accumulation vaults with mixed domains. Skip for training/expression vaults.*

Use for mechanistic/technical scaffolding notes — the HOW, not the WHAT IT MEANS. Simplified structure.

**Frontmatter**: no `[engagement_axis.config_key]` field, no `project_questions`, no `open_problems`.

**1. Core idea** (2–4 sentences): What this concept is and what it does.

**2. Mechanism / Intuition**: How it works — geometric, physical, or operational intuition. What would be lost without it?

**3. Brief implications**: Why this matters in its technical domain. No project connection required. Cross-domain links are the graduation signal.

**Not included**: Internal Tensions, Connection to the Project, fault_line frontmatter, Open Questions referencing open problems.

**Graduation path**: Reference-schema notes graduate by first overriding `evergreen-candidate` to `true` (upgrading to synthesis schema), then passing the Tier 2 → Tier 3 decision tree. The Tier 2 → Tier 3 graduation decision tree applies only to synthesis-schema notes.

### Tier 3 — Elevated Tier 2

Tier 3 notes are structurally identical to Tier 2 with these additions:

*This describes the default Tier 3 structure for accumulation vaults. Training vaults (Doctrine tier) and expression vaults (Published tier) define vault-specific Tier 3 structures in their CLAUDE.md.*

**Title must state a claim or insight** — not just a concept name. The title IS the atomic insight.
- Wrong: "Conatus"
- Right: "Conatus — Striving of Each Thing to Persist in Its Being"
- Right: "The Chinese Room Shows Syntax Cannot Generate Semantics"

**No assumed context** — the note must be fully self-contained. A reader with no access to the vault must understand the note completely.

**All See Also links verified** — every wikilink must point to an existing, well-developed note. Dead links are graduation blockers.

---

## The Graduation Decision Tree

### Tier 1 → Tier 2

Ask:
1. Does the note have an explanatory body (not just lookup content)?
2. Can the central insight be stated in 1–3 sentences?
3. Can you name the problem that forced this concept into existence?

If yes to all three: the note is ready for Tier 2. Write the full structure.

### Tier 2 → Tier 3

Ask:
1. Is the insight atomic? (Only ONE claim — would splitting it make two better notes?)
2. Is the title a claim or insight, not just a label?
3. Is "Connection to the Project" complete, including a specific `[engagement_field.name]` entry? (Escape-valve entries do not satisfy this criterion for Tier 3.)
4. Can a reader with no vault access understand this note completely?
5. Are all See Also links to existing, developed notes?

If yes to all five: the note is ready for Tier 3. Move to output folder.

### Note the Compression Error

The most common mistake: merging two concepts into one Tier 2 note to save time. The test: if removing either concept would leave the note incoherent, they needed each other — keep them merged. If either concept stands alone, split them.

---

## What Does NOT Graduate

- Pure lookup tables (Tier 1 forever, or delete if superseded)
- Notes about procedure (how to use a tool, format) — these are reference material, not insights
- Notes that are only about a thinker's biography, not their ideas
- Notes that are entirely downstream consequences of another note — merge into the parent note instead

---

## Common Failures by Tier

**Tier 1 failure**: Note never gets expanded because "it's just reference." The fix: schedule explicit expansion passes; use `/coverage-audit` to identify Tier 1 notes older than 30 days that haven't been promoted.

**Tier 2 failure**: Opening paragraph defines the concept without naming the problem. The fix: always ask "what failed before this concept existed?"

**Tier 3 failure**: Title names a concept, not an insight — "Homeostasis" instead of "Homeostasis Is Not Equilibrium but Active Resistance to Drift." The fix: if the title could be a dictionary entry, it is not ready.
