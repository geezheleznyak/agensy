---
created: 2026-04-24
updated: 2026-04-24
type: reference
stability_tier: foundational
canonicity: canonical
canonical_for: [expression_vault_substrate_templates]
audience: both
---

# Expression Vault Substrate — Templates

Six substrate files that every expression vault needs beyond the 12 standard genesis documents. The `/article-*` and `/co-*` command pipelines read these at runtime. The templates ship as scaffolds — structure plus guidance — not as finished content. The vault owner fills them in during and after genesis.

## The six files

| Template | Role | Seeded with? |
|---|---|---|
| `voice-profile.md` | **Style layer** — HOW the writer writes (register, rhythm, failure modes). Consumed by `/article-draft`, `/article-revise`, `/co-critique` | Scaffold — user provides corpus + calibration after genesis |
| `writer-positions.md` | **Substance layer (bedrock)** — WHAT the writer's non-negotiable commitments are (founding commitments, recurring dispositions, rejected frames, preferred analytical moves). User-authored, never auto-edited | Scaffold with section skeleton — user fills with personal positions |
| `positions-index.md` | **Harvest-loop index** — cross-essay pointer table to T3 framework claims earned through published essays. Pre-loaded at every `/article-*` invocation; T3 bodies loaded on-demand | Empty table + schema; populated by `/article-promote` Step 7 harvest loop |
| `article-presets.md` | **Narrative-arc blueprint registry** — 4 active presets (`framework-build`, `orthodoxy-counter`, `case-anatomy`, `diagnostic-lens`) + 1 Type-D preset (`synthesis-braid`). Each preset parameterizes opening / body arc / pressure / closing | Near-verbatim — presets transfer across users; vault owner can tune allocations or add new presets |
| `article-design-principles.md` | **Cross-essay craft principles (P1–P10)** — structural rules learned from pilots. Consumed by `/article-outline`, `/article-revise`, `/article-critique` | Near-verbatim — principles transfer across users; vault owner may append their own |
| `source-map-registry.md` | **Source-vault readiness manifest** — per-vault table of maps scored 0–25 on 5 readiness axes (thesis clarity, pressure, atomic support, standalone-ness, stakes) | Empty per-vault tables + schema; populated by `/article-scan` |

## Order of fill

When a new expression vault is bootstrapped via `genesis-protocol.md`, these six files are copied into the vault root. The recommended order to fill them:

1. **`voice-profile.md` first** — a new expression vault cannot produce prose in the user's voice until voice-profile is seeded. Needs at least one corpus sample (long-form writing or ~2,000 characters of aphoristic material). `/article-draft` refuses when voice is `status: unseeded`.
2. **`writer-positions.md` second** — seed with at least `Founding Commitments` (3–7 load-bearing beliefs the user won't compromise) and `Rejected Frames` (what the user will not argue from, even for the sake of argument). Other sections (`Recurring Dispositions`, `Preferred Analytical Moves`) can grow via the harvest loop.
3. **`article-presets.md` and `article-design-principles.md`** — ship near-working out of the box. Review once, tune if a preset doesn't fit the vault's genre, then leave alone until an essay's failure surfaces a new principle.
4. **`source-map-registry.md`** — populated automatically by the first `/article-scan <source-vault>` invocation. No manual seeding needed.
5. **`positions-index.md`** — starts empty; grows one row at a time via `/article-promote` Step 7 harvest. Do not edit by hand unless correcting a harvest classification.

## How `/article-*` and `/co-*` commands use these

- `/article-scan` reads nothing; writes `source-map-registry.md`.
- `/article-seed` reads `source-map-registry.md` (status check), `article-presets.md` (preset inference), `writer-positions.md` (bedrock check), `positions-index.md` (matched-positions lookup).
- `/article-outline` reads `article-presets.md` (arc imposition), `writer-positions.md`, `positions-index.md` (position-slot allocation).
- `/article-draft` reads `voice-profile.md` (style layer), `writer-positions.md`, `positions-index.md`, `article-presets.md`.
- `/article-revise` reads all of the above plus `article-design-principles.md` (Pass E preset-fidelity + frame-pressure sub-pass).
- `/article-critique` reads `voice-profile.md`, `writer-positions.md`, `article-design-principles.md`.
- `/article-promote` reads `source-map-registry.md`, `positions-index.md`, `writer-positions.md`; writes updates to all three.
- `/article-companion start` reads everything above as workspace context but does not lock the essay to them.
- `/co-find`, `/co-combine`, `/co-suggest`, `/co-critique`, `/co-capture` each read a subset per their Runtime section; `/co-capture` writes to `voice-profile.md` sources, `writer-positions.md`, `positions-index.md` only with user confirmation per-item.

## Runtime dependencies

Every expression-vault `vault-config.md` must declare `reference_docs.*` entries pointing to these files:

```yaml
reference_docs:
  voice_profile:             "voice-profile.md"
  writer_positions:          "writer-positions.md"
  positions_index:           "positions-index.md"
  article_presets:           "article-presets.md"
  article_design_principles: "article-design-principles.md"
  source_map_registry:       "source-map-registry.md"
  map_to_article_schema:     "../agensy/framework/templates/map-to-article-extraction.md"
```

(Relative paths are vault-owner's choice. The keys are what `/article-*` protocols look for.)

## See Also

- `framework/universal-commands/article-*.md` — the eight article-pipeline protocols
- `framework/universal-commands/co-*.md` — the five companion-mode protocols
- `framework/templates/map-to-article-extraction.md` — schema for map-section → article-role extraction
- `framework/templates/vault-config-schema.md` — where the `reference_docs.*` block is declared
