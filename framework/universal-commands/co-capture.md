---
description: Companion-mode substrate harvest. Captures voice-profile samples, writer-positions candidates, positions-index T3 candidates, and methodological moves from an active companion dialogue. Mirrors /article-promote Step 7 harvest-loop pattern, pre-essay.
type: universal-protocol
audience: claude
---

# /co-capture [mode] [--target voice|positions|methodological|framework|all]

Harvest substrate material from the current companion-mode dialogue — before an essay ships. Mirrors the pattern of `/article-promote` Step 7 harvest loop but operates during or at the close of a companion session rather than after essay promotion.

**Why this exists**: Pipeline mode harvests positions post-essay via `/article-promote` Step 7. Companion dialogues also generate substrate material — voice-profile calibration samples (prose-register thinking-out-loud), bedrock-position candidates (commitments articulated in user's own voice), positions-index T3 candidates (framework claims emerging through pressure-testing), methodological moves (analytical patterns surfaced through the Fork-commit process). Without a capture mechanism, this material evaporates when the session ends. `/co-capture` preserves it with a user-confirmation gate at every substrate write — the user-authored-ness of `writer-positions.md` is inviolable.

**[mode]**:
- `flag` — mark a specific current-turn articulation as a candidate. Cheap; used in the moment when the operator recognizes they just said something worth saving.
- `sweep` — scan the whole session-so-far for candidates across all target types. Heavier; use at major pause points or mid-session checkpoints.
- `close` — `sweep` + save full dialogue archive + offer commit on all gated items + finalize session. Used at end of session before the dialogue context clears.

Default: `sweep`.

**[--target]**:
- `voice` — only harvest voice-profile source material (dialogue archive + register notes).
- `positions` — only harvest positions-index T3 candidates (framework claims pre-essay, status `under-review`).
- `methodological` — only harvest writer-positions.md §Preferred Analytical Moves candidates.
- `framework` — only harvest bedrock-candidate material for writer-positions.md §Founding Commitments or §Recurring Dispositions (rare; requires clear user commitment).
- `all` (default) — all four.

**Runtime**: Read `vault-config.md` (cogitationis) for:
- `reference_docs.voice_profile` — voice-profile.md path
- `reference_docs.writer_positions` — writer-positions.md path
- `reference_docs.positions_index` — positions-index.md path
- `folder_structure.essays` — to locate the active companion essay file
- Active companion-mode essay file (from last `/article-companion start` session, or the essay file explicitly referenced in the current context)

This command reads the current dialogue from the conversation context. It writes to substrate files only after user confirmation on each item.

---

## Step 1 — Locate Active Session

1. Identify the current companion-mode essay file (via last `/article-companion start`, explicit reference, or most recent `mode: companion` essay updated today).
2. Read the essay's `companion_session_log` to understand what has happened in the session.
3. Confirm mode — reject if essay is `mode: pipeline` (this command is companion-only; pipeline mode uses `/article-promote` Step 7 for harvest).

---

## Step 2 — Scan Dialogue for Candidates

Read the conversation context. Classify substantive articulations into four candidate types:

### Voice candidates

The dialogue itself is prose-register thinking-out-loud material. Rarer than essay prose in the vault; more natural than aphoristic corpus samples. Voice-profile v0.2 explicitly flags long-form samples as the v0.3 calibration trigger.

Patterns to note when extracting:
- Sentence-length distribution in user's prose turns
- Paragraph structure (if any — dialogues are often single-paragraph)
- Hedge density
- Vocabulary register (vernacular vs. technical; structural vs. moral)
- Argumentative cadence (chains, cascades, declaratives)
- Register markers distinct from the aphoristic corpus and from essay-register

### Positions-index T3 candidates

Framework-level claims the user has articulated and committed to during the session — not essay thesis claims (those stay essay-internal until `/article-promote`), but structural moves that would apply across multiple essays.

Patterns to spot:
- User makes a claim about *how a class of phenomena works* (not just this essay's subject).
- User commits to a typology or distinction that has analytical reach beyond the current argument.
- User rejects a frame or accepts one in a way that reshapes how future analysis would approach the domain.

Status for pre-essay promotion: `under-review`. Candidates promoted here are held as pending until the source essay lands and validates them. If the essay retracts or significantly revises the claim, the `under-review` status can be demoted to `retired` without downstream breakage.

### Methodological-move candidates

Analytical patterns surfaced through the session's pressure-testing — moves the user now holds about *how to analyze*, not just *what's true*.

Patterns to spot:
- User articulates a rule for handling a class of evidence ("don't generalize from ceiling cases to mean cases").
- User commits to a principle about operationalization ("aggregate power is a composite, not GDP alone").
- User commits to a frame-audit habit that transfers to other essays.

Destination: `writer-positions.md` §Preferred Analytical Moves.

### Bedrock candidates (rare)

Changes to the user's Founding Commitments or Rejected Frames — deep-substrate shifts. Very rare from a single session. Typically only flagged when the user explicitly says "this is something I actually hold across my thinking, not just for this essay."

Destination: `writer-positions.md` §Founding Commitments, §Rejected Frames, §Recurring Dispositions, or §Open Tensions.

---

## Step 3 — Classify and Draft

For each candidate, produce a classification entry:

```yaml
candidate:
  type: <voice | positions | methodological | bedrock>
  content: "<the articulation, verbatim or closely paraphrased>"
  source_turn: "<which dialogue turn, summarized>"
  destination: "<file path + section>"
  draft_entry: |
    <the proposed text to write — one paragraph for positions, one bullet for methodological, one annotation-block for voice, one section-addition for bedrock>
  status: proposed  # will be `confirmed` after user review
  notes: "<any caveat about premature-commitment risk>"
```

For voice candidates specifically: produce a filename for the archive and an annotation block describing the sample's register.

---

## Step 4 — User Review Block

Emit a single review block covering all candidates, grouped by type:

```
## /co-capture — YYYY-MM-DD [mode]
Session: [[<active essay path>]]

### Voice candidates (<count>)
- [V1] <one-line description of the sample + register>
  Proposed: save full dialogue to `voice-profile-source/companion-dialogue-<YYYY-MM-DD>-<slug>.md` with register annotation.
  Confirm? [Y / skip / edit]

### Positions-index candidates (<count>)
- [P1] <claim summary>
  Proposed entry:
  | ID | Claim | Source T3 | Topics | Originating Essay | Status | Registered |
  |---|---|---|---|---|---|---|
  | P00X | <full claim sentence> | pending-essay | <topics> | [[<essay path, in-flight>]] | under-review | <YYYY-MM-DD> |
  Note: status is `under-review` because the source essay has not yet landed. Will be promoted to `active` by `/article-promote` Step 7 or demoted to `retired` if the essay retracts.
  Confirm? [Y / skip / edit]

### Methodological-move candidates (<count>)
- [M1] <move summary>
  Proposed entry for `writer-positions.md` §Preferred Analytical Moves:
  > "<full move text with rationale>"
  Source: <one-line citation to the dialogue moment>
  Confirm? [Y / skip / edit]

### Bedrock candidates (<count>)
- [B1] <proposed shift summary>
  Proposed section: <§Founding Commitments | §Rejected Frames | etc.>
  Proposed addition:
  > "<full text>"
  Note: bedrock additions are rare. Confirm only if you hold this across your work, not just for this essay.
  Confirm? [Y / skip / edit]
```

Each candidate must have a confirm / skip / edit decision. `skip` logs the flag in the essay's frontmatter without writing to substrate. `edit` opens a revision loop (user provides corrected text; `/co-capture` re-drafts).

---

## Step 5 — Write on Confirmation

For each `confirm`ed candidate:

### Voice writes

1. Create file at `voice-profile-source/companion-dialogue-<YYYY-MM-DD>-<slug>.md`.
2. File contents:
   ```markdown
   ---
   source: companion-dialogue
   date: YYYY-MM-DD
   essay_in_flight: "[[<essay path>]]"
   session_topic: "<topic>"
   register: "prose-register-thinking-out-loud"
   sample_type: "dialogue"
   notes: "<any additional calibration notes>"
   ---

   # Companion Dialogue — <date> — <topic>

   <full dialogue prose, user turns extracted; AI turns included only as minimal context>
   ```
3. Do NOT modify `voice-profile.md` directly. The source file feeds the next voice-profile calibration round (v0.3 trigger).

### Positions-index writes

1. Append the candidate's row to `positions-index.md` §Active Positions table with:
   - Status: `under-review`
   - Source T3: `pending-essay` placeholder until essay ships
   - Topics: extracted from candidate
   - Originating Essay: wikilink to the in-flight essay file
2. On essay promotion via `/article-promote`, Step 7 will:
   - Upgrade `under-review` → `active`
   - Replace `pending-essay` placeholder with actual T3 path
   - Create the T3 in the source vault if not already present
3. If the essay is abandoned, the `under-review` row stays until a subsequent `/co-capture close` demotes it or the user retires it manually.

### Methodological-move writes

1. Append to `writer-positions.md` §Preferred Analytical Moves as a numbered item.
2. Format:
   ```markdown
   N. <Move text.> <Why it matters, one sentence.> (Source: companion dialogue <YYYY-MM-DD>, essay [[<essay path>]].)
   ```
3. Update `writer-positions.md` frontmatter `updated:` date.

### Bedrock writes

1. Append to the named section of `writer-positions.md`.
2. Update frontmatter `updated:` date and `revision_log` (if present) with a one-line note.
3. Hard gate: if the bedrock write conflicts with an existing Founding Commitment or Rejected Frame, refuse with a diff showing the conflict; user must resolve the conflict before the write proceeds.

### Skip handling

For any `skip`, append to the essay's `companion_session_log`:
```yaml
- date: YYYY-MM-DD
  event: co-capture-skipped
  candidate_type: <type>
  content: "<one-line summary>"
  reason: "<user-provided reason, if any>"
```

This preserves the audit trail — the user can revisit flagged-but-skipped candidates in later sessions.

---

## Step 6 — Update the Essay's Frontmatter

Append to `companion_session_log`:
```yaml
- date: YYYY-MM-DD
  event: co-capture
  mode: <flag | sweep | close>
  candidates_flagged: <count>
  candidates_confirmed: <count>
  candidates_skipped: <count>
  candidates_edited: <count>
  writes:
    voice: <count of voice-source files created>
    positions: <count of positions-index rows added under-review>
    methodological: <count of writer-positions moves appended>
    bedrock: <count of writer-positions section additions>
```

---

## Step 7 — Report

```
## /co-capture [mode] — YYYY-MM-DD

Session: [[<essay path>]]
Mode: <flag | sweep | close>

Candidates proposed: <count>
  Voice: <count> — <confirmed / skipped>
  Positions-index: <count> — <confirmed / skipped>
  Methodological: <count> — <confirmed / skipped>
  Bedrock: <count> — <confirmed / skipped>

Substrate writes:
  voice-profile-source/: <list of files created>
  positions-index.md: <count of rows added under-review>
  writer-positions.md: <sections modified>

<If mode=close:>
Dialogue archive: [[voice-profile-source/companion-dialogue-<date>-<slug>]]
Session ended.

Next recommended action:
- /article-outline [essay-path] — if ready to leave companion mode and sketch structure
- /co-find, /co-suggest, /co-critique — to continue companion session
- Return later; session state persists in essay frontmatter
```

---

## Mode-specific behavior

### `flag` mode

Use when the operator just said something worth saving and doesn't want to lose it. Fast; captures one articulation at a time.

1. Scan only the most recent user turn (or turn range the operator specifies).
2. Produce 1–3 candidates max.
3. Review block as per Step 4.
4. Writes on confirm.

### `sweep` mode

Use mid-session when the dialogue has accumulated substantial material.

1. Scan the whole session.
2. Produce all candidates without artificial cap (but stop if >20 — session is too rich for one sweep; suggest splitting).
3. Review block grouped by type.
4. Writes on confirm.

### `close` mode

Use at end of session. Combines sweep with dialogue archival and session finalization.

1. Run sweep (above).
2. Unconditionally propose voice-source save (archival is the base case at close).
3. User can edit the archived dialogue slug and topic before save.
4. After writes: update essay `status` if user wants to move from `companion-draft` to a different state (e.g., paused, ready-for-outline). The essay doesn't auto-close.

---

## Error modes

- If no companion-mode essay is active: refuse with "No active companion session. Run /article-companion start <topic> or reference the essay explicitly with /co-capture --essay <path>."
- If the dialogue in context is too short to produce meaningful candidates (e.g., 1–2 turns): emit "Dialogue is too brief for capture. Continue the session; invoke /co-capture when substantive material has accumulated."
- If a candidate conflicts with existing substrate (e.g., proposed methodological move already exists in writer-positions.md): flag the duplicate in the review block; user decides whether to refine, replace, or skip.
- If `voice-profile-source/` does not exist: create it.
- If the user confirms a bedrock candidate but the addition conflicts with an existing Founding Commitment: hard refusal; diff shown; user resolves before proceeding.

---

## Relationship to existing harvest loop

`/article-promote` Step 7 is the post-essay harvest loop. It runs when an essay moves from `revision` → `final` → `published`. It handles:
- Essay-validated framework claims → new T3s + positions-index `active` rows.
- Essay-validated methodological moves → writer-positions.md appends.
- Cross-vault emergent claims (Type D) → cross-vault-bridges.md entries.

`/co-capture` is the pre-essay harvest loop. It runs during companion-mode sessions. It handles:
- Pre-validation framework claims → positions-index `under-review` rows.
- Pre-validation methodological moves → writer-positions.md appends (same destination, same format — the move either holds across further dialogue and essays, or gets refined/retired).
- Dialogue material → voice-profile-source files.
- Bedrock shifts → writer-positions.md deeper-section additions.

The two commands share classification taxonomy. On essay promotion, `/article-promote` Step 7 reconciles: any `under-review` rows tied to the promoting essay are upgraded to `active` if the essay's claims validate them; demoted to `retired` if the essay retracts; left `under-review` if the essay is orthogonal.

This means `/co-capture` doesn't bypass the validation loop — it just defers essay-validation while letting substrate accumulation happen in real time rather than being lost.

---

## Non-goals

- **No automatic writing without user confirmation.** Every substrate write is gated. Writer-positions.md remains user-authored per the framework's core principle.
- **No over-eager promotion.** Framework claims go to `under-review`, not `active`, pre-essay. Methodological moves go straight to writer-positions.md because they're lighter-weight; but they can be revised/retired any time.
- **No auto-sweep on every turn.** The operator invokes the command explicitly. Automatic capture would produce noise and violate the "user chooses what's promoted" principle.
- **No capture of in-flight thesis claims.** Essay-specific thesis content stays essay-internal. `/co-capture` looks for *framework-level* and *stylistic* material that has reach beyond the current essay.
