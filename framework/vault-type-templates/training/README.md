---
created: 2026-04-24
updated: 2026-04-24
type: reference
stability_tier: foundational
canonicity: canonical
canonical_for: [training_vault_substrate_templates]
audience: both
---

# Training Vault Substrate — Templates

Scaffolds for substrate files unique to training vaults — vaults whose Q1 mission is to *develop competence* (train a reader, shape judgment, produce doctrine) rather than accumulate atomic knowledge. Training vaults share the universal genesis skeleton but need three additional artifacts:

| Template | Role |
|---|---|
| `curriculum-template.md` | Phased development arc — from foundations to terminal competence. Structure: sequential phases with prerequisites, core competencies, essential readings, and a culminating exercise per phase |
| `principles-and-postulates-template.md` | Load-bearing priors the vault commits to before inquiry begins — the postulates every note, map, and curriculum phase must be consistent with |
| `sources-master-list-template.md` | Master bibliography of texts the vault treats as canonical — with each entry scored for weight, recency, and which curriculum phase it anchors |

## Scope honesty

These scaffolds are derived from a single training-vault reference implementation. They capture the structural pattern — phased curriculum, load-bearing postulates, curated sources — but a second training vault in a different domain (medicine, law, trade skill, athletic coaching) may surface structural needs the scaffolds don't yet cover. Treat these as **starting scaffolds, not authoritative forms**. If your training vault needs additional substrate (scenario libraries, assessment rubrics, practicum protocols, spacing schedules), add it and propose the template upstream.

## When copied

Per `genesis-protocol.md` Phase 1, when Q0.5 selects training as vault type, these three templates are copied into the vault root alongside the standard genesis artifacts. The vault owner fills each during the first 2–3 sessions after genesis completes.

## Order of fill

1. **`principles-and-postulates.md` first** — the postulates define what the curriculum teaches toward. Without them, curriculum phases drift into topic-coverage rather than competence development.
2. **`curriculum-template.md` next** — structure the phased arc once postulates are clear. Each phase maps to a subset of postulates: Phase N covers the competencies needed to internalize Postulates X, Y, Z.
3. **`sources-master-list.md` last** — after postulates and curriculum exist, the source-list is what anchors each curriculum phase's required readings.

## What's NOT in scope for training templates

- Scenario / wargame / case-study file formats — these are vault-specific content generation commands (`/wargame`, `/red-team`, `/stress-test` for military-strategy training vaults; different commands for other domains). Each training vault builds its own scenario library in a 50-Scenarios/ or equivalent folder.
- Assessment / certification schemas — depends on what the vault certifies. Not all training vaults certify.
- Spacing / retrieval schedules — only relevant if the training vault implements spaced-repetition mechanics.

## See Also

- `framework/vault-type-templates/expression/` — substrate for expression vaults (voice, positions, article pipeline)
- `framework/vault-type-templates/accumulation/` — no substrate needed; standard genesis covers it
- `framework/genesis-protocol.md` — when these get copied into a new vault
