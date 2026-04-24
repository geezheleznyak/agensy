---
created: 2026-04-24
updated: 2026-04-24
type: reference
stability_tier: foundational
canonicity: canonical
canonical_for: [learner_layer_architecture, user_engagement_states, learner_artifacts_loading_rules, learner_curation_discipline]
audience: both
---

# Learner Layer — Architecture

The Learner Layer is a horizontal layer in the synthesis framework that captures the user as a **learner-in-progress** — what they're acquiring, struggling with, curious about, ready for — distinct from the user as **author** (cogitationis writer-positions/voice-profile) or **position-holder** (cross-vault positions index). It sits parallel to the System Model layer: where System Model describes the structural shape of each vault's domain, Learner Layer describes the user's traversal of those domains over time.

Plan: `~/.claude/plans/so-i-was-thinking-elegant-wind.md` (designed 2026-04-24, scope: Phase 0 + Phases A + B).

---

## Why This Layer Exists

The existing framework captures the user along three axes:

| Existing primitive | Captures the user as |
|---|---|
| `/dialogue`, `/positions`, cross-vault positions index | Position-holder — what stances they hold |
| cogitationis `writer-positions.md` + `voice-profile.md` | Author — what bedrock commitments and stylistic patterns shape their writing |
| Auto-memory (`MEMORY.md` + topic files) | Collaborator — preferences, feedback, work style with Claude |

None of these answers: *what is the user acquiring? where are they stuck? what disciplines have they shown curiosity about? given a goal, what should they study next?* The framework knows what the user has **produced** (T3 notes, positions, essays). It does not know what the user has **acquired**, **struggles with**, or is **drawn toward**.

Without a learner model, the system can only respond to what the user explicitly raises. It cannot:

- Notice that the same question keeps recurring across sessions (struggle signal)
- Recommend a study sequence calibrated to current grasp
- Tailor explanations to the user's preferred mode (e.g., geometric intuitions for math)
- Surface engagement signals (what got the user excited; what they declared they wanted to understand)
- Calibrate `/what-next` recommendations to user readiness (prerequisites grasped vs. unseen)

The Learner Layer fills this gap with **structured, user-authored bedrock plus Claude-curated trajectory** — same shape as the cogitationis writer-positions pattern, applied to learning rather than authoring.

---

## What It Solves

Five capabilities that the framework cannot deliver without this layer:

1. **Continuity of learning** — sessions stop starting cold. Recent trajectory entries surface what was opened, what shifted, what stayed stuck.
2. **Adaptive explanation** — `/dialogue`, `/teach` (Phase C) and `/curriculum` (Phase C) read the profile to calibrate style and prior assumptions to the user's actual grasp.
3. **Readiness-aware recommendation** — `/what-next` checks `user_engagement` annotations on system-model nodes; deprioritizes recommendations whose prerequisites are `unseen`.
4. **Curriculum proposals** — `/curriculum` (Phase C) traverses the system-model dependency graph against the user's profile + engagement state to propose study sequences (vault navigation + external sources).
5. **Interest signal capture** — when the user says "I want to understand X better" or "this fascinates me," the proposal lands in `interests-register.md` and informs future recommendations.

Phase A delivers the bedrock and the schema extension. Phase B wires up trajectory capture and readiness checks. Phase C delivers the active commands. Phase D adds reflexive audit. Phase C and D are deferred per `roadmap.md`.

---

## Three Artifacts

The layer comprises three files in `synthesis-meta/learner/`:

### `learner-profile.md` — user-authored bedrock
- Formative thinkers and traditions
- Mathematical / formal maturity
- Languages read in original
- Current obsessions (3–7 active threads)
- Taboo areas (deliberate non-engagement, with why)
- Learning style (e.g., "geometric intuitions for math first")
- Goals at 6mo / 2yr / 10yr horizons

This is the analogue of `writer-positions.md` for learning rather than authoring. **The user edits it.** Claude only proposes appends; the user accepts or edits before the file is written. Cap: 300 lines; deeper sections graduate to `learner/learner-topics/` (mirrors `memory/` overflow pattern).

### `learning-trajectory.md` — Claude-curated trajectory log
- Per session / per arc: what was opened, what shifted, what stayed stuck
- Confidence deltas on positions (when `/dialogue` produces them)
- Arc completions and abandonments with reason
- Question recurrences (the same question coming back across sessions = signal)
- Surprise log — moments where the user said "huh, I didn't know that"

Cap: 200 lines / ~3 months active. Older entries archived to `learner/trajectory-archive/YYYY-MM.md`. **Archive is grep-only, never auto-read** — once archived, an entry is cold storage.

### `interests-register.md` — interest declarations log
- Every time the user says "I want to understand X better" or "this fascinates me" or "remind me to read Y"
- With date, vault context, and follow-through status (acted-on / dormant / closed)

Cap: 150 lines active. Closed/dormant interests moved to `learner/interests-archive.md`; only the active section is read by commands.

---

## Curation Discipline — Propose-Confirm Pattern

All three artifacts follow the **cogitationis writer-positions pattern**:

1. Claude detects a candidate addition (from dialogue, session activity, article harvest)
2. Claude proposes the addition explicitly: *"I noticed X — should I append this to your interests-register? (y/n/edit)"*
3. Only on user confirmation does the file get written
4. No silent updates. No background curation. Even append-only logs are gated.

This is slower than Hermes-style auto-curated profiles. It is intentional: a vault user is by construction someone with strong intellectual identity; letting an agent define them is the wrong direction of fit. Propose-confirm gives the user a continuous opportunity to correct misreads — Claude proposing "you seem to have shifted on X" lets the user push back before any artifact records it.

---

## Token-Budget Discipline (load-bearing)

The framework already auto-loads `MEMORY.md` (capped at 200 lines), the active vault's `CLAUDE.md`, and any vault-config. Adding three Learner Layer files plus per-node system-model annotations could double session-start cost if loaded carelessly. Constraints below are non-negotiable:

### Loading rules — none of the new artifacts auto-load at session start

The correct model is `writer-positions.md` / `voice-profile.md` in cogitationis: loaded **only** by commands that explicitly need them. Apply the same to Learner Layer:

| Artifact | Loaded by | NOT loaded by |
|---|---|---|
| `learner-profile.md` | `/dialogue`, `/what-next`, `/positions`, `/curriculum` (Phase C), `/teach` (Phase C) | session start, `/coverage-audit`, `/article-*`, default reads |
| `learning-trajectory.md` | `/dialogue` (only most recent ≤10 entries via tail-read), `/positions` (when computing mastery deltas) | session start, anything else |
| `interests-register.md` | `/article-promote` harvest, `/what-next` interest weighting, `/curriculum` | session start, anything else |

`MEMORY.md` index gets exactly three new one-line pointers (one per new artifact). No content duplication. Net cost to auto-loaded context: 3 lines.

### Size caps and rotation

| Artifact | Hard cap | Rotation |
|---|---|---|
| `learner-profile.md` | 300 lines | Deeper sections graduate to `learner/learner-topics/` |
| `learning-trajectory.md` | 200 lines / ~3 months active | Older entries archived to `learner/trajectory-archive/YYYY-MM.md`; archive never auto-read |
| `interests-register.md` | 150 lines active | Closed/dormant moved to `learner/interests-archive.md`; only active section read |

### Lazy loading within commands

- `learning-trajectory.md`: `/dialogue` reads only the **last 10 entries** via tail-style read. Never whole file.
- `interests-register.md`: `/what-next` greps for entries matching current vault's domains. Don't load whole file.
- `learner-profile.md`: read whole file (capped at 300 lines, comparable to a CLAUDE.md). One full read per command invocation, not per turn.

### Acceptance threshold

If a Learner-Layer-aware command's load exceeds its pre-Layer load by >25%, the design needs reconsideration before that command ships. Verify during Phase B rollout on the pilot vault.

---

## Integration with System Model — `user_engagement` annotation (schema v0.3)

Each system-model node gets two optional fields:

```yaml
- id: bounded_rationality
  type: pattern
  user_engagement: applied   # one of: unseen | surfaced | applied | mastered
  last_engaged: 2026-03-21
  evidence: [202603210900-...]
```

State semantics:
- `unseen` — node exists in domain model, user hasn't touched it
- `surfaced` — user encountered in dialogue or note; no working understanding yet
- `applied` — user has used the concept in their own writing or argument
- `mastered` — user can teach it, contest it, extend it

This is the **only** quantitative-feeling addition. Four states, qualitative, marked manually or via `/recall` audit (Phase C). No numbers, no scores.

### Cost containment

- Fields are **optional, sparse by default**. Default state for unannotated nodes is implicitly `unseen` — do **not** pre-fill the YAML with `unseen` markers.
- Annotate **only** nodes the user has actually engaged with. Expected steady state: 10–30% of nodes annotated, not 100%.
- Schema validation in `framework-verify.py` treats fields as optional — old vaults still on schema v0.2 unaffected.
- Each annotated node grows by ~2 lines YAML.

### Used by
- `/what-next` — readiness check: deprioritize recommendations whose prerequisites are `unseen`
- `/positions` — annotate each position with mastery state (mastered / contested / exploratory)
- `/curriculum` (Phase C) — traverse dependency graph, identify the boundary between mastered and unmastered

---

## Integration with Auto-Memory

Auto-memory (`MEMORY.md` + topic files) captures **feedback** (corrections, validated approaches) and **user preferences** (collaboration style with Claude). The Learner Layer doesn't replace this — it's the **structured, vault-facing** counterpart:

| Concern | Lives in |
|---|---|
| How the user prefers to collaborate with Claude | Auto-memory `feedback_*.md` |
| What the user has acquired in a domain | `learner/` (this layer) |
| User's stylistic / methodological commitments as an author | cogitationis `writer-positions.md` + `voice-profile.md` |
| User's positions on substantive claims | cross-vault positions index (output of `/positions`) |

`MEMORY.md` index gets one-line pointers to learner files; no content duplication.

---

## Integration with Cogitationis (writer-positions / voice-profile)

The Learner Layer mirrors the cogitationis pattern explicitly:

| Cogitationis (authoring) | Learner Layer (learning) |
|---|---|
| `writer-positions.md` — user-authored bedrock (founding commitments, rejected frames, recurring dispositions) | `learner-profile.md` — user-authored bedrock (formative thinkers, learning style, current obsessions) |
| `voice-profile.md` — stylistic bedrock | (no learner-layer equivalent — handled by `learner-profile.md` "learning style" section) |
| `/article-promote` Step 7 harvest loop — proposes appends to writer-positions when essays surface new dispositions | Phase B harvest in `/dialogue` and `/article-promote` — proposes appends to learning-trajectory and interests-register |

The pattern is reused wholesale because it is already proven (Hirschman pilot) and because the underlying principle is the same: **the user is the authority on themselves**; Claude proposes; the user confirms.

---

## What the Learner Layer Is NOT

| Boundary | Rule |
|---|---|
| Not a position-holder index | Cross-vault positions are output by `/positions` from source-tagged notes; this layer is upstream (acquisition trajectory), not downstream (settled stances) |
| Not auto-memory | Auto-memory captures collaboration feedback; this layer captures intellectual trajectory |
| Not Hermes-style auto-curation | Claude does not silently update profiles based on inferred preferences. All writes are propose-confirm. |
| Not a quiz / grading system | Mastery states are qualitative (4-state ladder). No scores, no quizzes, no Bloom's Taxonomy machinery |
| Not a domain ontology | The system model carries domain structure; the Learner Layer carries user-relative annotation on top of it |
| Not external-source recommendation by default | `/curriculum` (Phase C) will recommend external sources; until then, only vault-internal navigation |

---

## Self-Maintenance

The Learner Layer needs periodic maintenance to avoid stale-by-default failure:

- **Quarterly audit prompt** (Phase D `/learner-audit`): Claude prompts the user to review `learner-profile.md` and confirm which sections still hold. Stale sections move to learner-topics archive or get rewritten.
- **Last-reviewed date** on each profile section. Visible signal of staleness.
- **Trajectory archival**: when `learning-trajectory.md` exceeds 200 lines or 3 months, oldest entries move to `learner/trajectory-archive/YYYY-MM.md`. Never re-loaded.
- **Interest closure**: when an interest has been acted on (essay published, arc run) or dormant for >6 months, move from `interests-register.md` active section to `learner/interests-archive.md`.

Phase A and B do not implement the audit command — it lives in `roadmap.md` as item LL-D (deferred). Until Phase D ships, the user runs the audit manually.

---

## Reading Order

For framework-change work that touches the Learner Layer:
1. `architecture-principles.md` — what invariants must survive
2. This file — what the layer is and how it integrates
3. `framework/system-model/system-model-architecture.md` — for the `user_engagement` annotation context
4. `framework/templates/learner-profile-template.md` — for the user-authored bedrock structure

For the user authoring or revising their profile:
1. `framework/templates/learner-profile-template.md` first
2. Existing `synthesis-meta/learner/learner-profile.md` second (if revising)

For Claude reading the user's learner state during a command:
1. `synthesis-meta/learner/learner-profile.md` — the bedrock
2. Tail of `synthesis-meta/learner/learning-trajectory.md` — recent activity
3. Targeted grep of `synthesis-meta/learner/interests-register.md` — relevant interests for the current vault/domain

---

## Status

Phase A (this commit): bedrock — architecture doc, template, schema v0.3, profile authored interactively.
Phase B: trajectory capture — `/dialogue` + `/what-next` + `/positions` extensions, `/article-promote` harvest, pilot backfill on omega.
Phase C (deferred per `roadmap.md` LL-C): `/curriculum`, `/recall`, `/teach` active commands.
Phase D (deferred per `roadmap.md` LL-D): `/learner-audit` reflexive audit.
