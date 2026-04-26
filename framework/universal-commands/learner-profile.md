---
description: Bootstrap or revise the cross-vault learner profile (Learner Layer bedrock)
type: universal-protocol
---

# /learner-profile [init | revise | status]

Bootstrap or revise `agensy/learner/learner-profile.md` — the cross-vault bedrock of the Learner Layer. This command exists to remove the First-Use Gate that blocks hard-gate Learner-Layer-aware commands (`/teach`, `/curriculum`, future `/recall`) from running against an empty profile.

**Runtime**: this command does NOT read any `vault-config.md`. It operates on `agensy/learner/` directly. Same pattern as `/question-bank` and `/positions` (cross-vault commands that work on framework-level artifacts in `agensy/`).

**Read order before running**:
1. `framework/principles/learner-layer-architecture.md` — layer overview + First-Use Gate
2. `framework/templates/learner-profile-template.md` — schema and sections L1–L7

---

## Modes

| Mode | When | Result |
|---|---|---|
| `init` | No profile exists, or profile is at `status: unseeded`/empty | Interactive authoring of L1–L7 bedrock sections; writes `learner-profile.md` at `status: seeded-v0.1` |
| `revise` | Profile exists at `seeded-v0.1` or higher; user wants to update sections | Section-by-section revision pass; writes updated profile, increments status (v0.1 → v0.2 → v1.0) |
| `status` (default if no arg) | — | Report: profile status, last_reviewed per section, size in lines, staleness flags |

---

## Step 0 — Locate and classify

1. Check for `agensy/learner/learner-profile.md`.
2. If file exists, parse frontmatter for `status` field and count substantive sections (those containing content beyond template placeholders).
3. Classify into one of:
   - **Absent**: file does not exist
   - **Unseeded**: file exists, `status: unseeded` or all sections are placeholder-only
   - **Seeded-v0.1**: file exists with `status: seeded-v0.1` and ≥3 substantive sections
   - **Seeded-v1.0**: file exists with `status: seeded-v1.0` (stable — most sections substantive, reviewed within last 6mo)

If no mode arg was provided: default to `status` for seeded profiles; default to `init` for absent/unseeded profiles.

---

## Step 1 — `init` mode (interactive authoring)

**When to enter**: profile is Absent or Unseeded, user invoked `/learner-profile` with no arg or `init`.

1. If file doesn't exist, copy the template scaffold from `framework/templates/learner-profile-template.md` (sections L1–L7 with frontmatter).

2. Walk L1 → L7 in order. For each section:
   - Read the section's prompt from the template
   - Present the prompt to the user
   - Accept user's free-text answer
   - **Propose-confirm**: Claude re-renders the answer in markdown with appropriate structure (bullets, subheadings); user accepts, edits, or skips
   - On accept: stage the section content (do not write yet)
   - On skip: mark section `[optional — user declined in this pass]`

3. **Compression pass**: if a section is >40 lines, propose compression to the user with the longer version preserved in `learner/learner-topics/[section-slug].md`. User decides.

4. **Atomic write**: once all sections are staged, show the full proposed file to the user for a final read. User confirms with a single `accept`. Then write the file with:
   - `status: seeded-v0.1`
   - `created: [today]`
   - `updated: [today]`
   - Per-section `last_reviewed: [today]` markers

5. **Announce**: print the file path and a one-sentence summary of which hard-gate commands are now unblocked (e.g., `"Profile seeded. /teach and /curriculum are now unblocked in {active-vault}."`)

6. **MEMORY.md index update**: if the `MEMORY.md` pointer to `learner-profile.md` does not exist, add it (one line).

### Failure modes in init

- **User writes a paragraph instead of a structured answer** — Claude extracts structure and proposes the markdown version. User adjusts or accepts.
- **User skips most sections** — Minimum: require L1 or L2 or L4 to be substantive. A profile with all sections skipped is not useful and cannot exit init.
- **User wants to resume later** — Save progress to `agensy/learner/learner-profile.draft.md` with `status: unseeded`. Next `/learner-profile init` run detects the draft and offers to resume.

---

## Step 2 — `revise` mode (section-by-section update)

**When to enter**: profile is Seeded-v0.1 or Seeded-v1.0, user invoked `/learner-profile revise` with optional section-filter arg (e.g., `/learner-profile revise L4`).

1. Load current profile.

2. Determine scope:
   - No section arg: propose the 3 sections with oldest `last_reviewed` dates
   - Section arg (e.g., `L4`): limit to that section
   - `all`: walk every section

3. For each section in scope:
   - Show current content
   - Ask: *"What has changed? What needs adding or removing?"*
   - Propose-confirm: Claude renders the proposed new version; user accepts, edits, or leaves section unchanged
   - On accept: update section in memory; refresh `last_reviewed: [today]`

4. **Graduation checkpoint**: after revision, check if profile meets `seeded-v1.0` criteria (all 7 sections substantive, all `last_reviewed` within last 6mo). If yes, offer status upgrade to v1.0.

5. **Atomic write**: show full diff to user; single `accept` confirmation; write file.

### Failure modes in revise

- **User says "everything is current"** without engaging the sections — note this and flag for the next `/learner-audit` (Phase D).
- **Section grew >40 lines post-revision** — propose graduation to `learner/learner-topics/`.

---

## Step 3 — `status` mode (report)

Report to the user:

- Profile status (absent / unseeded / seeded-v0.1 / seeded-v1.0)
- File path
- Line count (and whether approaching the 300-line cap)
- Per-section `last_reviewed` dates
- Sections with stale reviews (>6 months old)
- Which Learner-Layer-aware commands are currently unblocked (hard gate status)
- Suggested next action (init / revise / no action needed)

Do not write anything in status mode.

---

## Contract

- **Writes**: `agensy/learner/learner-profile.md` (on user confirmation in `init` or `revise`); optional overflow in `agensy/learner/learner-topics/[section-slug].md`; optional draft in `agensy/learner/learner-profile.draft.md`
- **Reads**: `framework/templates/learner-profile-template.md`, existing `learner-profile.md` if present, `learner-topics/` overflow files if present
- **Does not read**: vault-config.md of any vault (cross-vault command, framework-level artifact)
- **Propose-confirm discipline**: no silent writes; every section change is user-gated; final file write is a separate confirmation step

---

## See Also

- `framework/principles/learner-layer-architecture.md` — layer architecture, First-Use Gate section, propose-confirm discipline
- `framework/templates/learner-profile-template.md` — schema for sections L1–L7
- `/dialogue`, `/what-next`, `/positions` — soft-gate consumers (degrade-and-warn)
- Training-vault `/teach`, `/curriculum` — hard-gate consumers (refuse without profile)
