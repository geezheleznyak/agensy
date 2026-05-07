---
description: Initialize hand-mode workspace — operator writes the essay by hand on a Loaded Canvas. Three diagnostics locked upfront, anatomy slots prefetched, three-pass discipline enforced after.
type: universal-protocol
---

# /article-handwrite <subcommand> [args]

Hand mode (V2.0) is the third top-level essay mode in expression vaults. It exists to lift the dormant Essayist's Framework (`essay style/essay_framework.md`) from passive scaffolding to active backbone. The operator writes every sentence themselves, but sits down in front of a *Loaded Canvas* — three pre-writing diagnostics already answered, prefetched material in a sidebar, anatomy slots empty and ready, polymath-trap warnings keyed to topic — rather than an empty page that has to be fed mid-thought.

Distinct from the two prior modes:

- **Pipeline mode** does upfront arrangement *but generates the prose for the operator to audit*. Violates "by hand."
- **Companion mode** preserves "operator writes prose by hand" *but is purely reactive* — no upfront arrangement, no thesis lock, no preset forced, by contract.

Hand mode's contract is **contractually opposite** to companion mode's: three diagnostics LOCKED, anatomy slotted, framework as backbone. The two modes coexist; they cannot share an entry point.

**Subcommands** (V2.0):
- `start <topic-or-source-map> [--from-map <map-path>] [--skip-diagnostics]` — run blocking diagnostic Q&A, prefetch material, write the Loaded Canvas.
- `status [essay-path]` — report current frontmatter status, last `updated`, time-gate eligibility for next pass, sidebar freshness.
- `finalize [essay-path]` — set status `handwrite-final`, lock frontmatter, prep for `/article-promote`.

**Runtime**: Read `vault-config.md` from the expression vault root. Extract:
- `reference_docs.voice_profile`
- `reference_docs.writer_positions`
- `reference_docs.positions_index`
- `reference_docs.source_map_registry`
- `reference_docs.article_presets`
- `reference_docs.essay_framework` (V2.0)
- `reference_docs.framework_integration` (V2.0)
- `reference_docs.hand_mode_protocol` (V2.0)
- `folder_structure.essays`
- `folder_structure.templates` (Hand Essay Template lives here)
- `modes.handwrite` (status_chain, frontmatter_field, framework_anchor)

This command never writes prose into the essay body. It writes the Loaded Canvas (frontmatter + section skeleton + prefetched sidebar) and reports.

---

## Subcommand: `start`

### Step 1 — Parse Input

1. Required positional: `<topic-or-source-map>`. If the argument ends in `.md` AND the file exists → treat as source-map anchor. Else → treat as topic string.
2. `--from-map <path>` overrides positional anchoring.
3. `--skip-diagnostics` flag disables the blocking Q&A. The Loaded Canvas is still created, but `diagnostics_locked: false` is set in frontmatter and Pass 3 surfaces a flagged warning at the top of its notes block.

### Step 2 — Load Substrate

Load (read-only):
- `essay style/essay_framework.md` — canon. Used by diagnostic gates (§II), polymath-trap heuristics (§VII), pass composition (§VI).
- `essay style/framework-integration.md` — operational mapping from framework sections to vault commands and substrate. Used to know which existing logic each pass invokes.
- `voice-profile.md` — note current status (`seeded-v0.2`, `seeded-v0.3`, etc.); referenced by Pass 2.
- `writer-positions.md` — note status and section count; referenced by Pass 3.
- `positions-index.md` — for T3 prefetch (Step 3.2).
- `source-map-registry.md` — for source-map prefetch (Step 3.1).
- `article-presets.md` — for advisory preset suggestion (Step 3.4). Presets are advisory in hand mode.
- `hand-mode-protocol.md` — protocol contract (already loaded by command lifecycle, but this command writes its `framework_version` into frontmatter).

If any of the framework-anchor docs (`essay style/essay_framework.md`, `framework-integration.md`, `hand-mode-protocol.md`) is missing: refuse with a specific message instructing the operator to run vault-config check. The framework anchor is mandatory; hand mode without canon is incoherent.

### Step 3 — Discover Material (prefetch for the Loaded Canvas sidebar)

Reuse `/article-companion start` Steps 2.1–2.4 logic verbatim. Do not reimplement.

**Step 3.1 — Source maps**:
- If anchor map provided: that map + cross-vault neighbors (from map's `see also` / `related`).
- If topic only: grep `source-map-registry.md` for topic keywords; collect top matches by keyword-overlap (cap 5).

**Step 3.2 — T3 positions**:
- Grep `positions-index.md` for topic keywords (or anchor map's core concepts if anchor-based). Cap 5.
- Surface ID + claim sentence + T3 path. Do NOT classify — there is no thesis yet.

**Step 3.3 — Voice + substrate load notes**:
- Voice-profile status. Writer-positions status + commitments / non-negotiables count.

**Step 3.4 — Preset suggestions (advisory only)**:
- Based on topic keywords and any anchor map's `problem_type`, suggest 1–3 presets from `article-presets.md`. Mark explicitly as advisory; the operator is not bound. `preset_status: advisory-only` in frontmatter.

### Step 4 — Polymath-Trap Scan (V2.0, framework §VII)

Scan the topic string + anchor-map titles + anchor-map summaries (if any) for **§VII trigger keywords**:

| Trap | Trigger keywords (topic-string heuristic) |
|---|---|
| Civilizational frame | "civilization", "the West", "humanity", "decline of …", "future of humanity", "civilizational", "empire", "imperial", "late-cycle", "the modern condition" |
| Strategist romance | "strategist", "the strategist", "art of war", "Greene-style", "warrior", "warlord", "chieftain", "conqueror", "the prince" (without explicit Machiavelli grounding), "philosophy of war/conflict/power" without specific person/case |
| Futurist register (esp. AI) | "in twenty years", "20 years", "by 2045", "by 2040", "long-term AI", "AGI in N years" |
| Premature synthesis | two or more of: "entropy", "complexity", "self-organization", "emergence", "evolution" applied across domains in a single topic-string |
| Gravitas voice | latinate-heavy topic-string ("ontological dimensions of strategic agency", "metaphysics of …") |

Each fired trigger becomes a `polymath_traps_active` entry in frontmatter and surfaces in the sidebar as a warning. Triggers are **nudges, not blocks** — false positives are acceptable. The operator can dismiss a trigger by removing it from the frontmatter list manually; Pass 1 re-checks against the surviving list.

### Step 5 — Three Diagnostics (BLOCKING — unless `--skip-diagnostics`)

Framework §II. Run interactively, in order. Each diagnostic blocks until answered to the test condition; the operator iterates.

**Diagnostic 1 — Question, not topic.**
- Prompt: "What is your question? (A topic is a noun. A question is a sentence with stakes — and the question must be one whose answer could surprise you.)"
- Test: parse the answer.
  - Refuse if the answer is a single noun phrase (e.g., "consciousness", "Clausewitz", "AI alignment") or any phrase without an interrogative form or stakes verb.
  - Refuse if the answer has the form "I want to write about X" — that is a topic, not a question.
  - Pass test: answer ends in `?` OR contains an interrogative head ("why", "when", "under what conditions", "how does", "why does"). And: the answer admits a falsifiable / surprisable form (Claude rephrases the answer back to the operator: "If [trivial-counter-answer] turned out to be right, would that surprise you?" — operator must say yes).
- Iterate until the question passes both halves of the test. Save to `question:` frontmatter (visible in the canvas at top, per §V.1).

**Diagnostic 2 — Steelmanned opposition.**
- Prompt: "Where is the disagreement? Steelman the opposing view in the smartest opponent's own language. Not a strawman."
- Test: parse the answer for evidence of steelmanning.
  - Refuse if the answer dismisses, ridicules, or characterizes the opposing view in pejorative terms ("they think X, but obviously…", "the naive view holds…").
  - Refuse if the answer is shorter than a sentence or mentions no concrete claim from the opposing camp.
  - Pass test: answer contains at least one claim that, if true, would falsify or weaken the operator's question's emerging answer; and that claim is stated in the language an advocate would accept (no scare quotes, no irony).
- Iterate. Save to `steelmanned_objection:` frontmatter.

**Diagnostic 3 — Hostile-but-fair reader.**
- Prompt: "Who is your hostile-but-fair reader? Name them — real and named if possible."
- Test: pass if the answer names a specific person (real or precisely-typed archetype: "an economist trained in price theory who reads Schelling" beats "an economist"). Refuse generic "a skeptic" or "the reader."
- Save to `hostile_reader:` frontmatter.

If `--skip-diagnostics`: skip Step 5 entirely. Set `diagnostics_locked: false` in frontmatter. Pass 3 will surface this as a flagged warning.

### Step 6 — Write the Loaded Canvas

Load `60-Templates/Hand Essay Template.md`. Substitute the template variables with the answers and prefetched material. Write to `[essays-folder]/YYYYMMDDHHMM - <Topic>.md`.

**Filename**: current timestamp (UTC OK; vault timezone if vault-config specifies) + sanitized topic slug ≤60 chars.

**Frontmatter additions over the template defaults**:

```yaml
title: ""                      # operator fills when title settles
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [type/essay, type/handwrite-arranged, theme/<inferred>]
status: handwrite-arranged
mode: handwrite
framework_version: 1.0          # version of essay_framework.md the canvas was loaded against
diagnostics_locked: true|false  # false only with --skip-diagnostics
question: "<answer to D1>"
steelmanned_objection: "<answer to D2>"
hostile_reader: "<answer to D3>"
polymath_traps_active: [list of triggers fired in Step 4]
loaded_at: YYYY-MM-DDTHH:MM
preset_status: advisory-only
preset_suggestions:
  - id: <preset-id>
    rationale: <one-line>
article_type: ""             # operator may set "A" or "D" if they're doing a braid; default empty → Type A report at promote
audience: general
venue: ""
word_count: 0
source_vault_anchors: [<vaults discovered in Step 3.1>]
source_map_anchors:           # sidebar/companion-verb lookup field
  - "[[<map 1 path>]]"
  - "[[<map 2 path>]]"
source_refs:                  # /article-promote Step 4/Step 7 read THIS field; populate from the same Step 3.1 result so backlinks land at promote time
  - "[[<map 1 path>]]"
  - "[[<map 2 path>]]"
positions_available:
  - id: P00X
    claim: "<claim>"
    t3: "[[<T3 path>]]"
handwrite_session_log:
  - date: YYYY-MM-DD
    event: canvas-loaded
    diagnostics_locked: true|false
    material_loaded:
      source_maps: <count>
      t3_positions: <count>
      preset_suggestions: <list of ids>
      polymath_traps: <list>
```

**Body**: see `60-Templates/Hand Essay Template.md`. The template lays out: Question (top-of-page, kept visible), Provisional Answer (2–3 sentence placeholder, expected to be abandoned), Steelmanned Objection, Hostile-but-Fair Reader, Anatomy Slots (Provocation / Movement / Turn / Resting Point — empty placeholders the operator fills), Body, Pass Notes (empty until passes run), Sidebar — Loaded Material (prefetched material).

### Step 7 — Report Workspace Ready

```
## /article-handwrite start <topic> — YYYY-MM-DD

Hand-mode canvas loaded.

Essay file: [absolute path]
Mode: handwrite (operator writes every sentence; framework backbone enforced)

Diagnostics:
  Q1 (question): "<question>" — locked
  Q2 (steelman): "<objection>" — locked
  Q3 (reader):   "<hostile reader>" — locked
[OR if --skip-diagnostics:]
  Diagnostics: SKIPPED. diagnostics_locked: false. Pass 3 will flag.

Polymath-trap warnings active: <list or "none">
  (These are nudges keyed to §VII triggers. False positives are OK; remove from frontmatter to dismiss.)

Sidebar loaded:
- Source maps: <count>
- T3 positions available: <count>
- Voice profile: loaded (status: <status>)
- Writer positions: loaded (status: <status>; N commitments / M non-negotiables)
- Preset suggestions (advisory): <list of ids>

Anatomy slots to fill:
  Provocation     — <empty>
  Movement        — <empty>
  Turn            — <empty>
  Resting Point   — <empty>

Companion verbs are still callable while you write:
  /co-find <query>           — discover material across vaults
  /co-suggest <stuck point>  — 3 next-move options (not prose)
  /co-critique <selection>   — surgical pressure
  /co-capture [mode]         — harvest substrate from dialogue

Three-pass discipline (after you draft):
  /hw-pass-1   — Structure (movement, anatomy slot fill, polymath-trap re-scan)
  /hw-pass-2   — Sentences (voice tics + §IV pathologies + read-aloud) — refuses within 24h of last update unless --force
  /hw-pass-3   — Honesty (C1–C8 + non-negotiables + §VI honesty audit)  — refuses within 24h of last update unless --force

When done: /article-handwrite finalize, then /article-promote.

Status: handwrite-arranged. Begin writing into the anatomy slots and Body.
```

---

## Subcommand: `status`

Default to most recent `mode: handwrite` essay if no path given.

Report:
```
Essay: [path]
Status: <handwrite-arranged | handwrite-drafting | handwrite-pass-1 | handwrite-pass-2 | handwrite-pass-3 | handwrite-final>
Updated: YYYY-MM-DD HH:MM   (Δ since now: <N>h <M>m)
Diagnostics locked: true|false
Loaded at: YYYY-MM-DDTHH:MM   (sidebar age: <N>d)
Polymath traps active: <list>
Word count: <integer>

Time-gate (24h):
  /hw-pass-2: <eligible | blocked until YYYY-MM-DD HH:MM>
  /hw-pass-3: <eligible | blocked until YYYY-MM-DD HH:MM>

Pass status:
  Pass 1: <run YYYY-MM-DD | not run>
  Pass 2: <run YYYY-MM-DD | not run>
  Pass 3: <run YYYY-MM-DD | not run>
```

The operator can manually flip status to `handwrite-drafting` when they begin writing into the body. `status` confirms the manual edit landed.

---

## Subcommand: `finalize`

Default to most recent `mode: handwrite` essay if no path given.

Pre-conditions (refuse if any fail; report which):
1. Status is `handwrite-pass-3`.
2. Pass 3 notes block exists in body.
3. `audience` and `venue` frontmatter set.
4. `title` frontmatter is non-empty and is in claim-form (not question-form, not topic-noun). If question-form, prompt operator to revise.
5. No remaining anatomy slot is empty (Provocation, Movement, Turn, Resting Point — at least each must reference a paragraph or section in the Body, even if the slot section itself is short).
6. `source_refs` is consciously curated. Compare `source_refs` against the canvas-load `source_map_anchors`: if `source_refs` is empty AND `source_map_anchors` is non-empty, prompt the operator: "source_refs is empty but the canvas was loaded with N source maps. Either (a) confirm zero maps actually fed this essay, or (b) populate source_refs from source_map_anchors before finalize. /article-promote Step 4 will silently skip backlinking if source_refs is empty."

If pre-conditions pass:
1. Set `status: handwrite-final`.
2. Update `updated: YYYY-MM-DD`.
3. Append to `handwrite_session_log`:
   ```yaml
   - date: YYYY-MM-DD
     event: finalized
     passes_completed: [pass-1, pass-2, pass-3]
     diagnostics_locked: <true|false>
   ```
4. Report: "Status set to `handwrite-final`. Run `/article-promote [path]` for the harvest loop. The promote protocol's status whitelist accepts `handwrite-final` identically to `final` and `companion-final`."

---

## Error modes

- Missing framework anchor (`essay style/essay_framework.md`, `framework-integration.md`, or `hand-mode-protocol.md` not found): refuse `start`. Hand mode's contract is "framework as active backbone"; without canon, the contract is broken.
- Diagnostic-loop infinite (operator cannot pass D1 after, say, 5 iterations): suggest the operator stop and read more — framework §II says "reading is not procrastination at this stage; it is the work." Save what was written so far; do NOT create a canvas. Operator can re-run `start` later.
- File collision on same-minute timestamp: append `-2` suffix.
- `--skip-diagnostics` AND missing framework anchor: refuse. Skip-diagnostics only escapes the operator-blocking interview, not the framework load.
- Operator passes a topic that triggers all five §VII traps simultaneously: still proceed, but include a single composite warning in the canvas sidebar: "this topic activates every polymath-trap heuristic; consider whether it should be split into smaller essays per framework §VII guidance."

---

## Non-goals (V2.0)

- **No prose generation, ever.** Hand mode has no equivalent to `/article-draft`. All prose is operator-written. The four `/co-*` verbs remain callable but they too generate no prose into the essay file.
- **No mode conversion.** A companion-mode essay cannot be re-entered as hand mode and vice versa. Acknowledged Open Tension; revisit V2.1 after one hand-mode pilot ships.
- **No sidebar refresh.** `loaded_at` makes staleness visible. A `/article-handwrite refresh-sidebar` subcommand can ship in V2.1 if pilot reveals it is needed.
- **No preset enforcement.** Presets are advisory in hand mode (mirroring companion mode). `preset_status: advisory-only` is the only valid value.
- **No automatic `handwrite-drafting` transition.** Operator flips manually. Status reporting confirms.

---

## Interaction with existing pipeline

- `/article-promote` works on `handwrite-final` essays the same way it works on `final` and `companion-final` essays. The harvest loop (Step 7) does not care whether the prose was AI-drafted, companion-written, or hand-written. Same Step 7 logic applies.
- `/article-critique` is composed into `/hw-pass-3`. Running it standalone on a hand-mode essay is also valid (e.g., as a checkpoint between passes), though `/hw-pass-3` is the canonical invocation.
- `/article-revise` is **not** the right tool on a hand-mode essay. Pass B / Pass C / Pass E logic is composed into `/hw-pass-2` and `/hw-pass-3` instead. Operators who run `/article-revise` on a hand-mode essay should expect a warning and a redirect to the appropriate `/hw-pass-N`.
