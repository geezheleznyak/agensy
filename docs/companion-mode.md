---
type: documentation
audience: human
---

# Companion Mode — Operator Writes, AI Augments

The expression pipeline (`docs/article-pipeline.md`) delegates prose generation to the AI and audits the output adversarially. That mode is the right tool when you want a complete essay produced against your substrate. It is the **wrong tool** when you want to write the essay yourself and use AI only for the moves AI is best at.

**Companion mode** is the alternative — a parallel mode where **you write the prose** and AI augments via four read-only verbs plus a capture verb. No thesis is locked, no preset is forced, no auto-drafting, no in-place revision. The AI never writes into the essay.

This doc explains when to use companion mode, how the five verbs differ, and how companion-mode work integrates with the rest of the expression-vault workflow.

---

## When to use companion mode

**Use it** when:
- You already know what you want to say and want to write it yourself
- You want the AI to find material across vaults but decide what to cite and when
- The essay is personal / voice-sensitive in a way that delegation blunts
- You're exploring a topic where thesis-locking would prematurely commit you
- You're mid-draft on a specific stuck point and want options, not a rewrite

**Don't use it** when:
- You want a complete draft produced — use the pipeline
- You don't yet know the shape of the argument — use `/article-seed` first, then decide
- You want the preset's narrative-arc enforcement (companion mode treats presets as advisory hints, not constraints)

**Both modes share**: voice-profile, writer-positions, positions-index, article-presets, article-design-principles, source-map-registry. Same substrate; different relationship to AI authorship. Both modes promote through the same `/article-promote` harvest loop.

---

## Starting a companion session

```
/article-companion start <topic-or-source-map> [--from-map <map-path>]
```

This creates an essay file at `20-Essays/` with:
- `mode: companion` (distinguishes from `mode: pipeline`, which is default)
- `status: companion-draft`
- `preset_status: advisory-only` (presets become hints, not gates)
- A workspace dossier report surfacing:
  - Source maps relevant to the topic (or anchor map + cross-vault neighbors)
  - Up to 5 T3 positions from `positions-index.md` matching the topic
  - Voice-profile and writer-positions status checks
  - 1–3 preset candidates as advisory hints

You then write prose directly into the essay file. The five `/co-*` verbs are your augmentation tools.

---

## The four read-only verbs

### `/co-find` — material discovery

```
/co-find <query> [--vault <name>] [--type atomic|t3|map|bridge|all]
```

Search across synthesis vaults for material relevant to a query. Returns a structured dossier — atomic notes, T3 positions, maps, cross-vault bridges — with paths, 1-line excerpts, and classifications. The command does not auto-cite and does not write into the essay.

**Typical uses**:
- "What does vault X say about reflexivity?" — pulls atomics + T3s + maps from that vault on the topic
- "Has any of my prior essays touched this concept?" — pulls matching rows from `positions-index.md`
- "Is there a registered bridge between my current topic and another vault's domain?" — pulls from `cross-vault-bridges.md`

Faster than manually walking another vault's structure. The dossier comes back structured; you pick what to cite.

### `/co-combine` — bridge-surfacing

```
/co-combine <map1> <map2> [<map3> ...]
```

Given 2–5 source maps (cross-vault OK), surfaces conceptual bridges between them: shared concepts, opposing claims, complementary mechanisms, possible synthesis angles. Returns options — not a drafted braid, not an assertion about the "right" composition.

**Typical uses**:
- "I'm considering weaving frameworks F1, F2, F3 on topic T — where are the actual seams?"
- "Do these two maps disagree about something that would make a good pressure section?"
- "Which map should I lead with?" — surfaces the concepts each emphasizes so you decide

Protects against a common failure mode: starting to braid three frameworks and discovering mid-draft that two of them are saying the same thing differently.

### `/co-suggest` — next-move options

```
/co-suggest <selection-or-stuck-point> [--type next-sentence|next-paragraph|counter|pressure|transition]
```

Given a passage or a stuck-point description, proposes **three distinct next-move options** with rationale and risk per option. Each option is a one-sentence direction, not generated prose.

Types:
- `next-sentence` — options for the single sentence that follows
- `next-paragraph` — options for the move the next paragraph makes (not its prose)
- `counter` — options for counters/objections to the current claim
- `pressure` — options for the pressure section
- `transition` — options for moving between named moves

**Typical uses**:
- You've finished a paragraph and don't know which way to turn next — three options frame the choice
- You know you need a counter-argument but don't know which is strongest — three counters, ranked by bite
- Pressure section is coming up and you want to see three different ways to structure it before committing

You pick an option and then write the prose yourself. AI gave you structure; you supply execution.

### `/co-critique` — passage-level critique

```
/co-critique <selection> [--mode light|adversarial]
```

Critic-style pressure on a **selected passage** (paste inline or reference `[[essay-path]]:42-58`). Shares the C1–C8 pass library with `/article-critique` but scoped to the selection. Returns bulleted flags with location pointers. Does not rewrite.

Modes:
- `light` (default) — clarity / redundancy / voice-match / minor-logic. Fast.
- `adversarial` — full C1–C8 library scoped to the selection, plus writing-tells. Heavier.

**Typical uses**:
- Mid-draft, a paragraph feels off and you want to know why
- You're about to send the essay to a reader and want one more pass on the opening
- A concession you just wrote might be load-bearing — adversarial critique will flag it (C6)

`/co-critique` is what lets you write without full-pipeline overhead but still get the adversarial pressure that a delegated essay would receive.

---

## The capture verb — `/co-capture`

```
/co-capture [flag|sweep|close] [--target voice|positions|methodological|framework|all]
```

**Why it exists**: pipeline mode harvests novel claims at `/article-promote` Step 7. Companion mode generates the same kind of substrate material — voice samples from prose-register thinking-out-loud, framework claims articulated mid-dialogue, methodological moves surfaced through pressure-testing — but there's no equivalent end-of-pipeline harvest. Without capture, this material evaporates when the session ends.

`/co-capture` is the companion-mode harvest. Every substrate write is **user-confirmed per item**.

Modes:
- **`flag`** — mark a specific current-turn articulation as a candidate. Cheap; used in the moment when you recognize you just said something worth saving.
- **`sweep`** — scan the whole session-so-far for candidates across target types. Heavier; use at major pause points.
- **`close`** — sweep + save full dialogue archive + offer commit on all gated items + finalize. Use at end of session.

Targets:
- **`voice`** — appends dialogue samples to `voice-profile.md`'s source inventory; may update register notes
- **`positions`** — promotes claims to `positions-index.md` with status `under-review` (demoted to `retired` if next essay contradicts; promoted to `active` if next essay validates)
- **`methodological`** — appends to `writer-positions.md` §"Preferred Analytical Moves"
- **`framework`** — rare; appends to `writer-positions.md` §"Founding Commitments" or §"Recurring Dispositions". Requires explicit user commitment, not inference.

The `user-authored-ness` of `writer-positions.md` is inviolable. Every substrate write gets a per-item confirmation gate. You can always reject; nothing writes silently.

---

## A companion session, end-to-end

*Abstracted from companion-mode usage; specific names generic.*

1. **Start**: `/article-companion start "reflexivity across policy and markets" --from-map <source>/theory/<framework>.md`
   - Creates essay file at `20-Essays/202604241500 - Reflexivity Across Policy and Markets.md` (`mode: companion`)
   - Workspace dossier reports: 4 source maps relevant, 3 positions-index matches, voice-profile `seeded-v0.3`, writer-positions seeded through §5, suggested presets: `framework-build` | `diagnostic-lens`

2. **Material scan**: `/co-find "reflexivity" --type t3`
   - Returns 7 T3 positions from the knowledge vaults. Three are directly relevant; you note them in the essay's scratch section for citation later.

3. **Write opening**: you draft paragraphs 1–3 yourself.

4. **Stuck at paragraph 4**: `/co-suggest <paragraph-3-pasted-in> --type next-paragraph`
   - Returns three options: (a) introduce the second framework now, (b) defer the second framework and deepen paragraph 3's case, (c) transition directly to pressure. You pick (b). Write paragraph 4 yourself.

5. **Mid-draft pressure check**: `/co-critique <paragraphs-5-6-selected> adversarial`
   - Flags: C7 — you shifted unit of analysis between paragraphs 5 and 6. Fix and continue.

6. **Bridge sanity check**: `/co-combine <map1> <map2>`
   - Surfaces that the two frameworks share a pressure point you hadn't noticed. You add a sentence acknowledging the shared pressure in the current draft.

7. **End of session, before closing**: `/co-capture close --target all`
   - Sweep finds:
     - Voice candidate: 3 turns of prose-register articulation of your analytical position. You confirm — they get appended to voice-profile's source-dialogue archive.
     - Positions candidate: one framework claim you articulated and committed to during the session. You confirm with status `under-review`. It lands in positions-index.
     - Methodological candidate: one rule you stated about how to handle cross-scale evidence. You confirm — appended to writer-positions §"Preferred Analytical Moves".
   - Dialogue archive saved. Session closes.

8. **Later** — when you come back to the essay, the captured positions-index entry is available for future `/article-seed` matched-position lookup even before this essay lands. If a subsequent essay pressures the claim, its status can demote; if it validates, it promotes to `active`.

9. **Eventually** — when the essay is done, you can either stay companion-mode all the way through or promote via `/article-promote`, which runs the full harvest loop against the final essay as usual.

---

## Companion vs. pipeline — at a glance

| Concern | Pipeline mode | Companion mode |
|---|---|---|
| Who writes the prose | AI generates; you revise | You write; AI augments |
| Thesis locking | `/article-seed` locks it | Never locked |
| Preset enforcement | `/article-outline` enforces | Advisory only |
| Voice application | `/article-draft` applies | You apply; `/co-critique` flags drift |
| Position alignment | Hard constraints via `/article-revise` Pass C | Constraint via `/co-suggest` (no suggestions that violate non-negotiables); flagging via `/co-critique` |
| Adversarial pressure | `/article-revise` passes + `/article-critique` | Per-passage `/co-critique` |
| Harvest | `/article-promote` Step 7 | `/co-capture close` |
| Output file location | `20-Essays/` → `40-Published/` | `20-Essays/` → `40-Published/` (same structure) |
| When to use | Complete draft, delegated | Operator-driven, piecewise |

**They share substrate and promotion path.** You can start in companion mode and promote via `/article-promote` when you're done — the harvest loop runs the same way. You cannot, however, flip a pipeline-mode essay to companion mode mid-flight; the thesis-lock and preset-enforcement state doesn't reverse cleanly.

---

## When companion mode fights you

**`/co-suggest` returns options you'd never pick**: either your stuck-point description is too narrow, or one of the options is actually right and you're resisting it. Try describing the stuck-point differently, or pressure-test the option you're resisting with `/co-critique`.

**`/co-critique` adversarial returns nothing interesting**: either the passage is good, or the passage is boring. Boring passages are sometimes the real problem — `/co-critique light` might catch clarity/redundancy that adversarial skipped.

**`/co-capture` keeps proposing captures you reject**: either the session is exploratory and nothing is converging yet (fine — `close` without committing anything), or the capture threshold is too loose. Be strict; capturing weak candidates dilutes positions-index value.

**No voice candidates surface**: companion sessions that are heavy on AI-speaking and light on user-prose don't generate voice material. That's honest. Voice-profile needs your prose, not the AI's.

---

## See Also

- `docs/article-pipeline.md` — the delegated alternative
- `docs/commands.md §Companion Mode Commands` — one-paragraph reference per verb
- `framework/vault-type-templates/expression/voice-profile.md` — what voice-profile looks like (template form)
- `framework/vault-type-templates/expression/writer-positions.md` — what writer-positions looks like (template form)
