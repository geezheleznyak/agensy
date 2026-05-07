---
description: Hand-mode Pass 1 — Structure. Audits movement, anatomy slot fill, and polymath-trap re-scan against the operator's prose. Output is a notes block appended to the essay; never a rewrite.
type: universal-protocol
---

# /hw-pass-1 [essay-path]

Pass 1 of the three-pass hand-mode revision protocol (framework §VI). Composes structural audits drawn from `essay_framework.md` §III (Anatomy) + §VII (Traps) + §VI ("Does the essay move? Where does it stall?"). Operates on operator-written prose. Never edits the essay body — output is a `## Pass 1 Notes` block appended at the end.

**[essay-path]**: optional. Defaults to the most recent essay with `mode: handwrite` AND status in `[handwrite-arranged, handwrite-drafting]`.

**Runtime**: Read `vault-config.md`. Extract:
- `reference_docs.essay_framework`
- `reference_docs.framework_integration`
- `reference_docs.hand_mode_protocol`
- `modes.handwrite.status_chain`

---

## Step 1 — Pre-conditions

Refuse with a specific reason if any fails:
1. Essay exists.
2. `mode: handwrite` in frontmatter.
3. Status is `handwrite-arranged`, `handwrite-drafting`, or `handwrite-pass-1` (re-run is allowed).
4. Body is non-trivial (≥500 words written into Body or anatomy slots — running Pass 1 on an empty canvas is a no-op).

No 24h time-gate on Pass 1. Pass 1 can be run as soon as the structural skeleton exists. The 24h time gate kicks in for Pass 2 and Pass 3, mirroring framework §VI: "separated in time, don't compress them."

---

## Step 2 — Audit: Movement

Framework §III: "Movement — the essay travels. Each paragraph changes the situation. Test: if the middle paragraphs can be reordered without damage, you have a list, not an argument."

For each paragraph in Body (skip the anatomy-slot scaffolding sections — those are slots, not prose):
1. Identify the paragraph's **state-change**: what is true in the argument's situation that wasn't true at the start of this paragraph?
2. Mark paragraphs whose state-change is one of:
   - **Restating the same point** the prior paragraph already made (movement-zero).
   - **Pure exposition** that doesn't advance the argument toward the question (decorative).
   - **Reversible with a neighbor** without damage to the argument (list-not-argument).

Output for each: paragraph identifier (first 8 words), reason flagged, and one sentence of guidance ("the prior paragraph already established X; this one repeats it. Cut, or sharpen the new claim").

If zero paragraphs are flagged: report "Movement: clean — every paragraph changes the situation." Do not invent flags.

---

## Step 3 — Audit: Anatomy slot fill

Framework §III: four functions — Provocation / Movement / Turn / Resting Point — that "interleave; they don't appear in order."

The Hand Essay Template lays out four anatomy-slot sections. Each slot must reference at least one paragraph or section in Body. Pass 1 audits:

1. **Provocation** — first paragraph (or whatever the operator pointed the slot to). Test (§III): "If the first paragraph could be deleted without loss, it should be." Audit: read the slot-targeted paragraph; ask whether the rest of the essay survives if it is removed. Flag if yes — provocation absent.
2. **Movement** — at minimum two paragraphs in the middle that change situation (validated against Step 2). Flag if Step 2 found ≥50% of middle paragraphs to be list-not-argument.
3. **Turn** — at least one paragraph (or named section) where one of: the question shifts, the obvious answer fails, or the two sides share a hidden premise. Audit: parse the operator's Turn-slot pointer; read the targeted prose; test for one of these three signatures. Flag if absent — "Without a turn, you have not thought; you have arranged."
4. **Resting Point** — final paragraph. Test (§III): is it a sharper version of the opening question, or a clean acknowledgment of what's still unknown? Or is it a forced resolution? Flag if forced-resolution — "Resolutions are usually lies."

Output: a `## Anatomy slots` subsection of Pass 1 Notes listing each slot's status (filled / partial / empty / forced) and the prose pointer.

---

## Step 4 — Audit: Polymath-trap re-scan

Re-read `polymath_traps_active` from frontmatter. For each trap still listed (operator hasn't dismissed it), scan the essay body for **realized-trap evidence**:

| Trap | Realized-evidence signature |
|---|---|
| Civilizational frame | Body contains "the West", "civilization", "humanity", "empire", "imperial", "late-cycle" deployed as load-bearing actors of arguments (not as objects of argument). Flag the specific sentences. |
| Strategist romance | Body uses "the strategist", "the warlord", "the warrior", "the chieftain", "the conqueror", or "the prince" in subject position without naming a specific person or case. Flag the abstract usage. |
| Futurist register | Body makes confident predictions about AI / technology beyond ~5 years out without evidential anchor. Flag the prediction sentences. |
| Premature synthesis | Body bridges two domains via shared abstract noun (entropy, complexity, emergence, evolution) without articulating each in its own terms first. Flag the bridge sentence and identify the two domains. |
| Gravitas voice | Body has paragraphs whose subject positions are nominalized abstractions ("the ontological dimensions of …", "the metaphysics of …"). Flag the worst offenders. |

Also: scan for traps NOT in `polymath_traps_active` but newly visible in prose. Add to `## Anatomy slots` notes (do not auto-add to frontmatter; operator decides).

If a trap was triggered at canvas-load but no realized evidence appears in prose: report "Trap [X] was flagged at canvas-load but does not appear realized in prose. You may dismiss the warning by removing it from `polymath_traps_active` frontmatter."

---

## Step 5 — Append Pass 1 Notes to Essay

Append the following block at the end of the essay body (before any trailing horizontal rule):

```markdown
---

## Pass 1 Notes — YYYY-MM-DD

### Movement
- Flagged paragraphs: <count>
  - "<first 8 words>…" — <reason> — <guidance>
  - …
- Verdict: <clean | needs-tightening | list-not-argument>

### Anatomy slots
- Provocation:    <filled | partial | empty | should-be-cut> — <pointer or note>
- Movement:       <filled | partial | empty | list-not-argument> — <pointer or note>
- Turn:           <filled | partial | empty | absent> — <pointer or note>
- Resting Point:  <filled | partial | forced-resolution | empty> — <pointer or note>

### Polymath-trap re-scan
- Active at load: [list]
- Realized in prose: [list with sentences]
- Newly visible: [list]
- Recommended: <dismiss X | retain Y | add Z>

### Pass 1 verdict
<one sentence — pass / needs structural revision / re-arrange before Pass 2>
```

Update frontmatter:
- `status: handwrite-pass-1`
- `updated: YYYY-MM-DD`
- Append to `handwrite_session_log`:
  ```yaml
  - date: YYYY-MM-DD
    event: pass-1-run
    movement_flagged: <count>
    anatomy_complete: <true | false>
    traps_realized: <count>
  ```

---

## Step 6 — Report

```
## /hw-pass-1 [path] — YYYY-MM-DD

Pass 1 (Structure) complete.

Movement: <verdict> (<count> paragraphs flagged)
Anatomy slots: <X/4 filled cleanly>
Polymath-trap realization: <count realized> (of <count active>)

Pass 1 Notes appended to essay body.
Status: handwrite-pass-1.

Time gate: /hw-pass-2 unlocked in <N>h (24h after this run, unless --force).
Recommended next: address Pass 1 flags structurally, leave essay overnight, then run /hw-pass-2.
```

---

## Error modes

- Body too short (<500 words): refuse. "Pass 1 expects a structural draft, not a stub. Continue writing first."
- Anatomy slots all empty (operator wrote into Body but never pointed slots at paragraphs): warn and proceed; the audit reports all four slots as `empty` and recommends slot assignment before Pass 2.
- Operator already at status `handwrite-pass-2` or beyond: refuse. "Pass 1 cannot be run after Pass 2 has appended its notes — the audit would be auditing already-revised prose. Revert status manually if you want to re-run." (No automatic state-rollback.)
- Re-run on `handwrite-pass-1`: replace prior Pass 1 Notes block (delete previous, append new). Audit again from current body.
