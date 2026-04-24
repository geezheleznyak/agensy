---
created: 2026-04-24
updated: 2026-04-24
type: template
stability_tier: foundational
canonicity: canonical
canonical_for: [learner_profile_schema]
audience: both
---

# learner-profile.md Template

This is the bedrock document for the Learner Layer. The user authors it once during Phase A bedrock setup, then revises it as their intellectual life evolves. **Cap: 300 lines** — deeper sections graduate to `learner/learner-topics/`. Every field is optional; leave blank what you can't or don't want to answer.

**Usage**: Copy this template to `synthesis-meta/learner/learner-profile.md`. Work through sections L1–L7 with Claude in interactive Q&A (Claude proposes phrasing from your answers; you accept or edit before Claude writes the file). Mark `last_reviewed` per section so staleness is visible.

**Relationship to neighboring artifacts**:
- For **authoring** commitments and stylistic patterns → cogitationis `writer-positions.md` + `voice-profile.md`
- For **collaboration preferences** with Claude → auto-memory `feedback_*.md`
- For **learning trajectory** (what was opened, what shifted) → `learning-trajectory.md` (Claude-curated, Phase B)
- For **interest declarations** → `interests-register.md` (Claude-curated, Phase B)

This file is the user's self-portrait *as a learner*. Don't duplicate what those neighboring files already capture.

---

## learner-profile.md Template

```markdown
---
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
type: reference
audience: both
---

# Learner Profile

The user as a learner-in-progress. Authored by the user, updated via propose-confirm.

[OPTIONAL: one paragraph framing — who you are intellectually right now, the
broad arc of what you're trying to become. Skip if you'd rather let the
sections speak for themselves.]
```

---

### L1 — Formative Thinkers and Traditions

> The intellectual lineage you've actually wrestled with — not a list of admired names but the thinkers whose categories shape how you see things. Include those who once shaped you and you've since moved past, with a note on why.

```yaml
formative:
  thinkers:
    - name: [Thinker name]
      tradition: [tradition or school]
      role: [what role they play in your thinking — e.g.,
             "default frame for political analysis",
             "rejected after reading X — see Rejected Frames",
             "still unsettled — open question"]
      depth: [skimmed | read deeply | wrestled with | internalized]
  traditions:
    [list the broader traditions or schools you've worked within]
  last_reviewed: [YYYY-MM-DD]
```

---

### L2 — Formal / Mathematical Maturity

> Honest self-assessment of formal-language fluency. Used by Claude to calibrate explanations: if you say "shaky on category theory," Claude leads with intuitions; if "fluent in measure theory," Claude can use that vocabulary directly.

```yaml
formal_maturity:
  mathematics:
    fluent_in: [list — e.g., "linear algebra", "probability"]
    working_knowledge: [list]
    shaky_on: [list]
    avoiding: [list — and why, briefly]
  logic_and_formalism:
    [classical logic, modal logic, type theory, category theory, etc.]
  programming:
    [languages, paradigms, current grasp]
  preferred_explanation_mode:
    - [e.g., "geometric intuitions for analysis"]
    - [e.g., "concrete worked examples before generalization"]
    - [e.g., "always show me the counter-example first"]
  last_reviewed: [YYYY-MM-DD]
```

---

### L3 — Languages

> Languages you read, write, or speak with enough fluency to engage primary sources. Affects which thinkers Claude can recommend in original vs. translation.

```yaml
languages:
  read_in_original:
    - language: [e.g., "Russian"]
      confidence: [native | fluent | working | reading-only-with-effort]
      domains: [list — e.g., "philosophy", "literature", "politics"]
  write:
    [list]
  speak:
    [list]
  translation_notes:
    [e.g., "I prefer Pevear-Volokhonsky for Russian fiction;
            avoid Garnett's translations of Dostoevsky"]
  last_reviewed: [YYYY-MM-DD]
```

---

### L4 — Current Obsessions (3–7 active threads)

> What you're actually wrestling with right now. Not a wish list — the threads that keep returning when you sit down to think. Cap at 7; if more, they're not all obsessions.

```yaml
current_obsessions:
  - topic: [short name, e.g. "reflexivity in social science"]
      vault: [which vault this lives in — omega | belli | kratos | oikos | clio | cogitationis | cross-vault]
      why: [why this matters to you right now — what's at stake]
      open_question: [the specific unresolved question driving the obsession]
      surfaced: [YYYY-MM-DD when this became active]
  - topic: ...
  last_reviewed: [YYYY-MM-DD]
```

---

### L5 — Taboo Areas (deliberate non-engagement)

> Things you are deliberately NOT engaging with right now, with the reason. Distinct from "don't know" — these are conscious exclusions. Useful so Claude doesn't keep suggesting reading you've decided not to do.

```yaml
taboo_areas:
  - area: [topic / discipline / thinker / framing]
    why_not: [reason — e.g., "ideologically poisoned domain that wastes my attention",
              "out of scope for my current 5-year arc",
              "previously got too absorbed; need distance",
              "intentionally protecting time for L4 obsessions"]
    duration: [permanent | for the next [N months/years] | until [milestone]]
  last_reviewed: [YYYY-MM-DD]
```

---

### L6 — Learning Style

> How you actually absorb new material. Used by Claude when explaining or proposing reading sequences. Be specific — "I learn best from examples" is too generic; "I need 3 worked examples before I'll trust a generalization" is useful.

```yaml
learning_style:
  intake_modes:
    [list — e.g., "long primary sources over secondary syntheses",
            "Mermaid diagrams help when concepts have ≥4 components",
            "I trace arguments through paraphrase, not annotation"]
  mastery_signals:
    [how you know you've understood something — e.g.,
     "I can teach it to a smart non-specialist",
     "I can construct a counter-example to a related claim",
     "I can predict what the thinker would say about X"]
  difficulty_signals:
    [what tells you you're struggling — e.g.,
     "I keep paraphrasing but can't generate new examples",
     "I can't recall the dependency chain a week later",
     "I find myself avoiding the topic"]
  scaffolding_preferences:
    [e.g., "always cite the page number / section reference",
           "give me the historical conditions that produced the claim",
           "prefer pre-1950 primary sources for philosophy"]
  last_reviewed: [YYYY-MM-DD]
```

---

### L7 — Goals (6mo / 2yr / 10yr horizons)

> What mastery looks like at three time horizons. Three different time scales force different levels of specificity. The 10-year goals are usually directional ("become someone who can…"); the 6-month goals are concrete deliverables.

```yaml
goals:
  six_month:
    - goal: [concrete, deliverable]
      vault: [which vault drives this]
      indicator_of_progress: [how you'll know you're moving toward it]
  two_year:
    - goal: [scope: a discipline mastered, a position defended publicly, a project shipped]
      indicator_of_progress: [larger structural milestone]
  ten_year:
    - goal: [directional — "become someone who…"]
      why_this_horizon: [why this is the long-term vector, not a fad]
  last_reviewed: [YYYY-MM-DD]
```

---

## Maintenance

- **Per-section `last_reviewed`** dates make staleness visible. When `last_reviewed` is >6 months old AND that section has had relevant activity in `learning-trajectory.md`, Claude proposes a review.
- **Quarterly audit** (Phase D `/learner-audit`, deferred per `roadmap.md` LL-D): Claude prompts a full review of the profile against trajectory evidence.
- **Overflow**: when a section grows past ~30 lines or becomes dense enough to deserve its own page, graduate to `learner/learner-topics/[topic-name].md` and leave a one-line pointer in the main profile.
- **Deletion is allowed**: any section can be deleted at any time. The profile is not load-bearing in the framework — its absence just means Claude has less information to calibrate against.

## Relationship to System Model `user_engagement` annotations

The profile captures user-relative attributes that **don't fit per-node** (formative thinkers, learning style, goals). The system-model `user_engagement` field captures **per-concept** mastery state. Both inform `/what-next`, `/curriculum`, and `/teach`, but they live in different artifacts because their structure is different:

| Artifact | Granularity |
|---|---|
| `learner-profile.md` | User-level (whole-person attributes) |
| Per-vault `system-model.yaml` `user_engagement` | Per-node (concept-level mastery) |

Don't duplicate. If something is per-concept, it goes in the system model; if it's about who you are as a learner, it goes here.
