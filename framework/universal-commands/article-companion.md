---
description: Initialize a companion-mode workspace — operator writes the essay, AI augments with /co-find, /co-combine, /co-suggest, /co-critique. No full-write delegation.
type: universal-protocol
audience: claude
---

# /article-companion start <topic-or-source-map> [--from-map <map-path>]

Create a companion-mode essay workspace where the operator writes the prose themselves and AI serves as research-aide + pressure-source. Distinct from `/article-seed` because no thesis is locked, no preset is forced, no auto-generation pipeline is entered. The operator owns the essay file; AI never writes into it via this command or the four `/co-*` verbs.

**Why this exists**: the pipeline (`/article-seed` → `/article-outline` → `/article-draft` → `/article-revise` → `/article-promote`) delegates prose generation to the AI and audits the output adversarially. That mode is the right tool when the operator wants a complete essay produced against the substrate. It is the wrong tool when the operator wants to write themselves and use the AI for the four moves AI is best at: finding material across vaults, combining concepts across frameworks, suggesting next-move options at stuck points, and applying critic-style pressure to selected passages. Companion mode separates those concerns.

**<topic-or-source-map>**: one of:
- A free-form topic (e.g., "reflexivity in oikos", "deterrence under autonomous systems") — the command will infer relevant source maps and T3s by keyword search.
- A specific source-map path (e.g., `synthesis_politeia/theory/IR/mearsheimer-systematic-map.md`) — used as the anchoring map; other relevant material is discovered around it.

**[--from-map <map-path>]**: explicit anchor. Required only if the topic string is ambiguous across vaults.

**Runtime**: Read `vault-config.md` from cogitationis vault root. Extract:
- `reference_docs.voice_profile`
- `reference_docs.writer_positions`
- `reference_docs.positions_index`
- `reference_docs.source_map_registry`
- `reference_docs.article_presets`
- `folder_structure.essays` (for the essay file location)

This command only creates the essay file and reports the workspace summary. It does not write into the essay body and does not lock a thesis.

---

## Step 1 — Parse Input

1. Determine `start` subcommand. Currently only `start` is supported; reserve other subcommands (`resume`, `status`) for V2.
2. Parse topic or source-map path:
   - If the argument ends in `.md` AND exists as a file → treat as source-map anchor.
   - Otherwise → treat as a topic string.
3. If `--from-map` passed, use as explicit anchor regardless of topic parsing.

---

## Step 2 — Discover Material

Build a workspace context the operator will use while writing.

**Step 2.1 — Source maps**:
- If anchor map provided: that map + its cross-vault neighbors (from map's `see also` or `related` sections if present).
- If topic only: grep source-map-registry.md for topic keywords; collect top matches by keyword-overlap score (cap 5).

**Step 2.2 — T3 positions**:
- Grep `positions-index.md` for topic keywords (or anchor map's core concepts if anchor-based).
- Return up to 5 matching positions with classification (reuse `/article-seed` Step 2.6 classification logic: supports / extends / tensions-with / orthogonal — but do NOT classify yet; the operator has no thesis yet to classify against. Classification is deferred; just surface the position IDs + claim sentences).

**Step 2.3 — Voice + substrate load**:
- Verify `voice-profile.md` is readable. Note status (`seeded-v0.2`, `seeded-v0.3`, etc.).
- Verify `writer-positions.md` is readable. Note status and section count.

**Step 2.4 — Preset suggestions (advisory only)**:
- Based on topic keywords and anchor map's problem_type, suggest 1–3 presets from `article-presets.md` that the essay *might* fit. Mark clearly as suggestions — the operator is not bound.

---

## Step 3 — Create the Essay File

Write a minimal essay file at `[vault]/20-Essays/YYYYMMDDHHMM - <Topic>.md`.

**Filename**: use current timestamp + sanitized topic slug (≤60 chars).

**Frontmatter**:
```yaml
---
title: ""  # operator fills when the title settles
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [type/essay, type/companion-draft, theme/<inferred from anchor / topic>]
status: companion-draft
mode: companion   # V1.9 — distinguishes from default `mode: pipeline`
article_type: ""  # operator fills if they decide (not required)
preset: ""        # empty means "no preset enforced"; operator may set later
preset_status: advisory-only   # V1.9 — presets are hints, not gates, in companion mode
audience: general
venue: ""
word_count: 0
source_vault_anchors: [<list of vault names discovered in Step 2.1>]
source_map_anchors:
  - "[[<path to map 1>]]"
  - "[[<path to map 2>]]"
positions_available:  # surfaced at workspace-setup time; operator uses /co-find and /co-suggest to engage them
  - id: P00X
    claim: "<T3 claim sentence>"
    t3: "[[<T3 path>]]"
thesis: ""              # empty initially — operator writes when committed
companion_session_log:
  - date: YYYY-MM-DD
    event: workspace-initialized
    material_loaded:
      source_maps: <count>
      t3_positions: <count>
      preset_suggestions: <list of preset ids>
---
```

**Body**:
```markdown
# <Topic or placeholder title>

<!-- Operator writes the essay body here. Use /co-find <query>, /co-combine <map1> <map2>, /co-suggest <stuck point>, /co-critique <selection> while writing. The AI does not write into this file. -->
```

The empty body is deliberate. The operator starts from scratch. The placeholder comment is a reminder of the four verbs; it can be deleted or kept.

---

## Step 4 — Report Workspace Ready

```
## /article-companion start <topic> — YYYY-MM-DD

Companion workspace ready.

Essay file: [absolute path to new essay file]
Mode: companion (operator writes; AI augments via /co-* verbs)

Material loaded (use /co-find to search further):
- Source maps: <count>
  - <map 1 label> — <vault> — <one-line purpose>
  - <map 2 label> — <vault> — <one-line purpose>
  ...
- T3 positions available: <count>
  - P00X: <claim sentence> — [[T3 path]]
  - P00Y: <claim sentence> — [[T3 path]]
  ...
- Voice profile: loaded (status: <voice-profile status>)
- Writer positions: loaded (status: <writer-positions status>; N commitments / M non-negotiables)

Preset suggestions (advisory):
- <preset id 1>: <one-line fit rationale>
- <preset id 2>: <one-line fit rationale>
(You are not bound to any preset in companion mode. Consider these only if they help.)

Five verbs available while you write:
  /co-find <query>           — find material across vaults (atomic notes, T3s, source maps, bridges)
  /co-combine <map> <map> …  — surface bridges between N source maps (cross-vault OK)
  /co-suggest <stuck point>  — propose 3 distinct next-move options (not prose)
  /co-critique <selection>   — surgical critique of selected text (C1-C8 passes, not rewrite)
  /co-capture [mode]         — harvest substrate from dialogue: voice samples, positions candidates, methodological moves (user-confirmed per item)

When done:
  /co-capture close          — save dialogue archive, commit confirmed substrate, close session.
  Set status: companion-final in frontmatter.
  /article-promote [essay-path] runs the harvest loop (same as pipeline mode; upgrades under-review positions to active on validation).

Next step: open [essay path] and start writing. Invoke any /co-* verb at any time.
```

---

## Error modes

- If no source maps found for the topic: report "No source maps matched — the topic may be too novel or the search terms too specific. You can still create the workspace and use /co-find with different queries as you write." Create the file with empty `source_map_anchors` and an advisory message.
- If `--from-map` path is invalid: abort with "Map not found: [path]".
- If the essay file path already exists (collision on same-minute timestamp): append a `-2` suffix to filename. Do not overwrite.
- If `voice-profile.md` or `writer-positions.md` is missing or unfilled: proceed with a warning — "[file] is [missing / unfilled]; companion verbs will still work but voice/position checks in /co-critique will be limited".

---

## Non-goals (for V1)

- **No automatic body generation.** The operator writes every sentence of the essay. The AI never writes into the essay file via this command or the four `/co-*` verbs. (The operator can always pull text from `/co-suggest` or `/co-find` output into their essay manually.)
- **No thesis locking.** The `thesis:` frontmatter field is empty by default and the operator fills it when committed. `/article-companion` does not extract or infer one.
- **No preset enforcement.** `preset_status: advisory-only` is the V1 default. `/article-outline` Step 6.5 seam-audit gates do NOT run for companion-mode essays. `/article-revise` Pass E preset-fidelity checks are softened (flagged but not mandatory) when `mode: companion`.
- **No subcommands beyond `start` in V1.** `resume`, `status`, and `end` are deferred to V2 once the companion-mode pattern has a pilot behind it.

---

## Interaction with existing pipeline

- `/article-promote` works on `companion-final` essays the same way it works on `final` essays. The harvest loop (Step 7) does not care whether the prose was AI-drafted or operator-written. User-confirmation gate on classifications still applies.
- `/article-critique` can be run on a companion-mode essay at any status. Useful before transitioning to `companion-final`.
- `/article-revise` can be run on a companion-mode essay *if the operator wants the adversarial passes applied to their own prose*. Not recommended — the operator is their own first reviser in companion mode. But not blocked.
- Converting between modes: not supported in V1. An essay is either pipeline or companion for its lifetime. (V2 may support conversion — defer until pattern is validated.)
