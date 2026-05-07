---
description: Hand-mode Pass 2 — Sentences. Voice-tic audit (voice-profile.md 13 tics) + framework §IV three pathologies (gravitas / weak-hedge / performance) + read-aloud prompt. Output is a notes block; never a rewrite.
type: universal-protocol
---

# /hw-pass-2 [essay-path] [--force]

Pass 2 of the three-pass hand-mode revision protocol (framework §VI: "Sentences. Read aloud. Cut every sentence that performs, hedges weakly, or signals more than it says."). Composes the existing voice-profile 13-tic audit (currently in `/article-revise` Pass B) with framework §IV's three pathologies. Operates on operator-written prose. Never edits the essay body — output is `## Pass 2 Notes` appended.

**[essay-path]**: optional. Defaults to most recent `mode: handwrite` essay with status `handwrite-pass-1`.

**[--force]**: bypass the 24h time-gate. Logged in frontmatter.

**Runtime**: Read `vault-config.md`. Extract:
- `reference_docs.essay_framework`
- `reference_docs.framework_integration`
- `reference_docs.voice_profile`
- `reference_docs.hand_mode_protocol`

---

## Step 1 — Pre-conditions

Refuse with specific reason if any fails:
1. Essay exists; `mode: handwrite`.
2. Status is `handwrite-pass-1` or `handwrite-pass-2` (re-run allowed).
3. **Time gate (24h)**: `now - updated >= 24h`, unless `--force`. Framework §VI: "separated in time, don't compress them." Time gate is intentional friction. `--force` proceeds with a logged warning surfaced at the top of Pass 2 Notes.
4. Pass 1 Notes block exists in body (i.e., Pass 1 was actually run).

If time gate trips without `--force`: refuse with the unlock time stated to-the-minute. Suggest the operator step away or revise structurally in the meantime.

---

## Step 2 — Audit: Voice-profile tic scan

Reuse the 13-tic audit logic from `/article-revise` Pass B verbatim. Source: `voice-profile.md` (read its current version — `seeded-v0.2`, `seeded-v0.3`, etc. — and use whatever tics it currently lists). Do not hardcode tic identities here; they evolve.

For each tic listed in voice-profile:
1. Pattern-match across operator's prose body (skip Pass 1 Notes block and any `## Pass N Notes` blocks).
2. Flag every match with: paragraph identifier, the offending sentence, the tic's name, and the voice-profile's prescribed correction (if any).

Voice-profile tics are LLM-essay failure modes — but in hand mode they apply to operator prose too. The operator's prose may have its own voice tics (over-use of em-dashes, signature transitional phrases) that are not LLM tics. Voice-profile is the canonical list; do not invent tics.

If voice-profile is `unfilled` or under v0.2: warn and proceed with a degraded audit ("voice-profile is at <status>; tic detection is incomplete. Consider scheduling voice-profile v0.3 calibration after the current essay ships").

---

## Step 3 — Audit: Framework §IV pathologies

Three pathologies, hunted in order:

### 3.1 — Gravitas voice (§IV.1)
- Signatures: long Latinate clauses; abstract nouns in subject position; sentences whose syntactic head is a nominalization ("the ontological dimensions of …", "the metaphysics of …", "the dialectic between …" used to start a sentence without immediate concrete reference).
- For each sentence whose subject is an abstract nominalization > 4 words long AND the sentence is > 30 words: flag.
- Output: paragraph + sentence + a one-sentence rewrite suggestion that puts a concrete actor in the subject position (e.g., "Strategists working in compute-bounded environments …" instead of "The ontological dimensions of compute-bound strategy …").

### 3.2 — Weak hedge (§IV.2)
- Signatures: "perhaps", "in some sense", "one might argue", "arguably", "to some extent", "in a way", "in many ways". Some warranted; many are decision-avoidance.
- For each occurrence: flag with the surrounding sentence and a question prompt — "Are you genuinely uncertain here, or avoiding commitment?"
- Do not auto-classify. The operator decides per-instance whether the hedge stays. Pass 2's job is to surface every hedge so the operator must make the call consciously.

### 3.3 — Performance (§IV.3)
- Signatures: aphorism without argumentative function; allusion that does not earn its weight; inverted-syntax sentences whose primary effect is rhythmic; sentences repeating an earlier point in more elegant language.
- This is the hardest to detect mechanically. Heuristics:
  - Sentence is the only sentence in its paragraph AND the paragraph is positioned between two other paragraphs that already make the same argument the sentence restates.
  - Sentence contains an unreferenced cultural-literary allusion not connected to the essay's argument.
  - Sentence's load-bearing claim is presented in inverted syntax ("Not the answer, but the question, was what …") without further development.
- Flag suspected performance with a low-confidence flag — operator decides. Test prompt for the operator (per §IV.3): "Does this sentence advance the thought? If not, cut."

---

## Step 4 — Read-aloud prompt

Framework §IV: "Read every draft aloud. The ear catches what the eye misses. This is the single most underrated revision technique that exists."

Append to the Pass 2 Notes a directive (not an audit):

```
### Read-aloud directive

Pass 2's audits run on the eye. The ear catches what the eye misses.

Read the essay aloud — actually aloud, in your voice, at your normal speaking pace. Mark every sentence that:
- you stumbled on
- you ran out of breath in
- felt embarrassing to say
- you naturally rephrased mid-sentence

These are problems even if Pass 2's mechanical audits did not catch them.

Pass 2 is not complete until the read-aloud has happened. The mechanical audits are a floor, not a ceiling.
```

This is the only place the protocol cannot mechanize. Frame it as a non-skippable manual step the operator owns.

---

## Step 5 — Append Pass 2 Notes to Essay

```markdown
---

## Pass 2 Notes — YYYY-MM-DD [--force was used: <yes|no>]

### Voice-profile tics
- Voice-profile status: <status>
- Tics flagged: <count>
  - <paragraph "first 8 words…"> — <tic name> — "<sentence>" — <correction>
  - …

### §IV.1 Gravitas voice
- Flagged: <count>
  - <paragraph "first 8 words…"> — "<sentence>" — <rewrite suggestion>
  - …

### §IV.2 Weak hedges
- Hedge instances: <count>
  - <paragraph "first 8 words…"> — "<sentence>" — decide: genuine uncertainty or avoidance?
  - …

### §IV.3 Performance (low-confidence)
- Suspected: <count>
  - <paragraph "first 8 words…"> — "<sentence>" — does this advance the thought?
  - …

### Read-aloud directive
[non-skippable manual step — see body]

### Pass 2 verdict
<one sentence — clean / needs sentence-level revision before Pass 3>
```

Update frontmatter:
- `status: handwrite-pass-2`
- `updated: YYYY-MM-DD`
- Append to `handwrite_session_log`:
  ```yaml
  - date: YYYY-MM-DD
    event: pass-2-run
    voice_tics_flagged: <count>
    gravitas_flagged: <count>
    hedges_flagged: <count>
    performance_suspected: <count>
    force_used: <true|false>
  ```

---

## Step 6 — Report

```
## /hw-pass-2 [path] — YYYY-MM-DD

Pass 2 (Sentences) complete.[--force used: yes]

Voice tics: <count> flagged (voice-profile <status>)
§IV.1 Gravitas: <count> flagged
§IV.2 Weak hedges: <count> flagged
§IV.3 Performance (low-confidence): <count> suspected

Read-aloud directive issued — this manual step is non-skippable per framework §IV.

Pass 2 Notes appended to essay body.
Status: handwrite-pass-2.

Time gate: /hw-pass-3 unlocked in <N>h (24h after this run, unless --force).
Recommended next: revise sentences flagged, run the read-aloud, leave essay overnight, then run /hw-pass-3.
```

---

## Error modes

- Time gate trips without `--force`: refuse with the unlock time. State the framework rationale ("§VI: separated in time, don't compress them"). Do not allow override flags other than `--force`.
- `--force` used but Pass 1 was within the last 12h: warn ("you have used --force AND Pass 1 was run very recently. Hand mode's three passes are designed to operate on a settled draft. Consider waiting"). Proceed if user accepts.
- Pass 1 Notes missing from body: refuse. Pass 2 audits a structurally-clean draft; without Pass 1 there is no signal that structure is settled.
- Voice-profile missing: refuse, redirect to seed voice-profile first. The voice-tic audit is half of Pass 2.
- Re-run on `handwrite-pass-2`: replace prior Pass 2 Notes block. Re-set time gate from new run timestamp.
