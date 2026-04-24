---
created: 2026-04-24
updated: 2026-04-24
type: reference
stability_tier: foundational
canonicity: canonical
canonical_for: [vault_type_substrate_templates]
audience: both
---

# Vault-Type Templates

Scaffolds for the **vault-type-specific substrate files** that genesis does not cover with its 12 standard documents. The 12 docs build a universal skeleton (CLAUDE.md, vault-config.md, folder structure, tier schema, map reference, MOCs, coverage plan, development plan, open problems, stubs, memory/). But expression vaults and training vaults need additional files whose *structure* is universal even though the *content* is vault-specific.

This directory holds those additional templates, organized by vault type:

- **`expression/`** — six substrate files consumed by the `/article-*` and `/co-*` pipelines. Includes voice profile (style), writer positions (substance bedrock), positions index (harvest-loop cache), article presets (narrative-arc blueprints), article design principles (craft rules), source-map registry (readiness scores).
- **`training/`** — three scaffolds for training-vault substrate. Phased curriculum, load-bearing postulates, and sources master list.
- **`accumulation/`** — intentionally empty. The 12 standard genesis documents cover everything an accumulation vault needs.

## When these are used

During `genesis-protocol.md` Phase 1, after Doc 11 (the extended `vault-config.md`) is written, the vault-type chosen in Q0.5 / Q7 determines which sub-folder to copy into the vault root:

- Expression vault → copy `expression/*` into vault root.
- Training vault → copy `training/*` into vault root.
- Accumulation vault → no copy needed.

Each copied file is a starting scaffold. The user fills in the specifics during the first session(s) after genesis completes. The `/article-*` and `/co-*` commands (for expression vaults) and any future training-vault commands check that these files exist at expected locations and respond gracefully when they are unseeded.

## Why they live here, not in per-vault genesis

**Canonicity** — the structure of these files is framework-level. If the structure changes (new sections added, new format adopted), that change should propagate to every future vault of that type. Keeping the templates here, under the framework directory, ensures genesis always uses the latest structure.

**Symmetric with templates/schemas** — `claude-md-template.md`, `note-tier-template.md`, `map-type-template.md`, `vault-config-schema.md` all live in `framework/` as universally-consumed scaffolds. These vault-type-templates are the same pattern, just gated by vault type.

## How to extend

If a new vault type emerges (e.g., *curation*, *dialogue*, *archive*), add a new sub-folder here with its scaffold set and a README explaining the vault type. Update `genesis-protocol.md` Phase 1 to recognize it.

If a new substrate file is added to an existing vault type (e.g., a new `/article-*` command needs a new substrate file), add the template here, update the corresponding README, and update the consumer protocol's Runtime section to reference the new file.

## See Also

- `framework/protocols/genesis-protocol.md` — when these get copied into a new vault
- `framework/templates/vault-config-schema.md` — Q0.5 (vault type) and Q7 (output layer) answers determine which sub-folder applies
- `framework/principles/framework-meta-architecture.md §2` — document taxonomy (these files are `template`-type, `operational`-tier)
