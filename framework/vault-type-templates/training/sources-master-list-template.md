---
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [meta/sources]
status: awaiting-user-fill
---

# Sources Master List — [Domain]

*Rename this file to the domain-specific form, e.g., `sources-master-list.md` (generic) or domain-prefixed.*

Canonical bibliography for the vault's training project. Every curriculum phase cites sources from this master list; every Tier 3 judgment note grounds its claims in sources that appear here. The list is curated — not a reading catalog of everything relevant, but the anchor set the vault treats as authoritative.

**Status progression**: `awaiting-user-fill` → `seeded-v0.1` (20–50 foundational entries across all curriculum phases) → `maintained` (continuous additions as sources prove load-bearing; rare retirements).

**Criterion for inclusion**: a source belongs on this list if it meets at least two of the following — (1) it is cited across multiple curriculum phases, (2) its framework structures how the vault reads other sources, (3) removing it would require rewriting at least one postulate or one curriculum phase.

---

## Schema

Each entry carries:

- **Author + Title + Date** — standard bibliographic header
- **Phase anchor** — which curriculum phase(s) cite this source as essential
- **Role** — what this source does for the vault (foundational theory, operational doctrine, historical case, reference resource, counter-position)
- **Weight** — `core` / `supporting` / `counter` / `reference`
  - `core` — required reading at its anchor phase
  - `supporting` — cited for specific claims; not required but recurring
  - `counter` — treated as the serious opposition whose view must be engaged
  - `reference` — consulted for specific facts; not load-bearing
- **Recency** — when this source's analytical frame was most relevant; flag if the source predates significant regime-shift in the domain
- **Vault note** — backlink to the map or T3 note where this source is most fully engaged

---

## [Thematic Section 1 — e.g., "Foundational Theory"]

*[Group the list by thematic section. Common groupings for training vaults: Foundational Theory / Operational Doctrine / Historical Cases / Counter-Positions / Reference Sources. Domain-specific groupings are expected.]*

### [Author], *[Title]* ([Year])

- **Phase anchor**: *[e.g., Phase 0, Phase 2]*
- **Role**: *[one sentence]*
- **Weight**: `core` | `supporting` | `counter` | `reference`
- **Recency**: *[e.g., "foundational — remains analytically current despite predating drone era"]*
- **Vault note**: [[vault-note-path]]

### [Author], *[Title]* ([Year])

- *[entry]*

---

## [Thematic Section 2]

*[entries]*

---

## Counter-Positions

*Sources the vault treats as serious opposition. Students are expected to engage these — not as strawmen to dismiss, but as positions that pressure the vault's postulates and force sharper articulation.*

### [Author], *[Title]* ([Year])

- **Phase anchor**: *[typically later phases — Phase 3+ — after students have enough vault material to engage serious opposition]*
- **Role**: *[what this source claims that the vault resists]*
- **Weight**: `counter`
- **Which postulate it pressures**: *[e.g., Postulate 3]*
- **Vault note**: [[vault-note-path]]

---

## Reference Sources

*Consulted for specific facts or definitions. Not load-bearing; not required reading; but cited enough to warrant a stable entry.*

### [Reference 1]

*[entry — abbreviated schema is fine for reference sources]*

---

## Maintenance

- **Additions**: whenever a source is cited in three or more vault notes, consider adding it to the list. Not every cited source belongs here — only those that have become anchor points.
- **Retirements**: if a source stops being cited for a full year, demote from `core` to `supporting`, or remove entirely. Moved entries stay in a §Retired section with a note explaining the move.
- **Recency audits**: once per year, audit entries flagged with old recency notes. A source that was load-bearing 20 years ago may have been superseded or may need a contemporary companion entry.
- **Domain regime shifts**: when the domain experiences a regime shift (new technology changes the analytical picture; institutional structure transforms; foundational assumptions break), run a full list audit. Sources whose framing assumed the prior regime may now be counter-positions or purely historical.

---

## Retired Sources

*(Empty at start. Populated when a previously canonical source is demoted or removed, with dated note explaining the retirement.)*

| Source | Was | Retired on | Why |
|---|---|---|---|

---

## See Also

- `[domain]-curriculum.md` — phases cite sources from this list as essential readings
- `principles-and-postulates.md` — postulates must be consistent with (or explicitly engage conflict with) canonical sources here
- `vault-config.md` — Q6 domains shape how this list is thematically organized
