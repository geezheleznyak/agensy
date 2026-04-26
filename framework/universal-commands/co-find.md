---
description: Companion-mode material discovery. Cross-vault search that returns a structured dossier — no prose, no auto-citation, no edits to the essay.
type: universal-protocol
audience: claude
---

# /co-find <query> [--vault <vault-name>] [--type <atomic|t3|map|bridge|all>]

Search across synthesis vaults for material relevant to a query. Returns a structured dossier the operator reads and pulls from manually while writing. Read-only: does not write into the essay, does not auto-cite.

**<query>**: free-form search phrase. The query is split into keywords; keyword overlap drives ranking.

**[--vault]**: limit search to a single vault (politeia, oeconomia, bellum, theoria, historia, logos, meta). Default: search all non-logos vaults (the writer's own positions live in logos and are surfaced via `positions-index.md` regardless).

**[--type]**: limit result type. `atomic` = evergreen atomic notes in source vaults; `t3` = judgment notes (politeia 20-Judgment, oeconomia 20-Judgment); `map` = systematic maps; `bridge` = cross-vault bridge entries in `[AGENSY_PATH]/cross-vault-bridges.md`. Default: `all`.

**Runtime**: Read `vault-registry.md` from `[AGENSY_PATH]/` to know which vaults exist and their paths. Read `positions-index.md` from logos. Read `cross-vault-bridges.md` from agensy if `--type=bridge` or `--type=all`.

---

## Step 1 — Query Prep

1. Tokenize query into keywords. Strip punctuation, lowercase, singularize.
2. If query is very short (1 keyword), expand by loading the vault registry and looking for synonyms in recent maps/T3s — but cap expansion at 3 extra terms.
3. If `--vault` specified, restrict search paths accordingly.

---

## Step 2 — Search

Run ripgrep-equivalent searches across the relevant vaults. Parallel search by type:

**Atomic notes** (`--type=atomic` or `all`):
- Paths: `synthesis_<vault>/20-Evergreen/` (bellum, theoria), `synthesis_<vault>/<domain>/` (politeia, oeconomia).
- Match in: title, first paragraph, tags.
- Return: path, title, 1-line excerpt (first substantive sentence), tags.

**T3 positions** (`--type=t3` or `all`):
- Primary source: `synthesis_logos/positions-index.md` — grep topic column + claim column.
- Secondary: `synthesis_<vault>/20-Judgment/` directly for T3s not yet harvested into the index.
- Return: position ID (if in index), claim sentence, T3 path, source vault, fault-line classification.

**Maps** (`--type=map` or `all`):
- Paths: `synthesis_<vault>/theory/**/*-map.md`, `synthesis_<vault>/<domain>/*-map.md`.
- Match in: title, founding problem section, first-principles section, core concepts.
- Return: map path, title, 1-line founding problem, list of core concepts (≤5).

**Bridges** (`--type=bridge` or `all`):
- Source: `[AGENSY_PATH]/cross-vault-bridges.md`.
- Match in: bridge title, linked vault pair, description.
- Return: bridge ID, title, vault pair, 1-line description.

---

## Step 3 — Rank and Cap

- Score each hit by keyword-overlap count (weighted: title matches > excerpt matches > tag matches).
- Tie-break by document recency (newer wins).
- Cap totals: atomic ≤ 10, t3 ≤ 8, maps ≤ 5, bridges ≤ 3. Totals chosen so the dossier fits on one screen and doesn't swamp the operator.

---

## Step 4 — Report Dossier

```
## /co-find <query> — YYYY-MM-DD

Search: "<query>" (keywords: <k1, k2, ...>)
Scope: <all vaults | <vault>> / types: <all | <type>>

### Atomic notes (<count> of <total found>)
- [[<vault>/<path>]] — "<title>"
  "<1-line excerpt>"
  tags: <tags>

- ...

### T3 positions (<count>)
- **P00X** [<relation to anything? not classified here — operator decides>]
  "<claim sentence>"
  source: [[<T3 path>]] (vault: <vault>, fault-line: <classification>)

- ...

### Source maps (<count>)
- [[<map path>]] — "<title>"
  founding problem: <one line>
  core concepts: <c1, c2, c3, ...>

- ...

### Cross-vault bridges (<count>)
- **Bridge <N>** [<vault A> ↔ <vault B>] — "<title>"
  "<description>"

---

Refine: /co-find <narrower query>  |  /co-find <query> --type=t3  |  /co-find <query> --vault=<vault>
Compose: /co-combine <map1> <map2> ...   (to surface bridges between any two of the maps above)
Pressure: /co-critique <selection>       (on any prose you've written)
```

---

## Non-goals

- **No prose.** The dossier is structured listings, not essay-ready sentences. The operator reads the notes/T3s themselves before deciding to cite.
- **No auto-citation.** `/co-find` does not append to the essay's source_refs or body. The operator manually pulls any wikilink they want.
- **No classification of T3s against a thesis.** `/co-find` returns T3s with their canonical claim; it does not determine whether they support / extend / tension with the operator's argument. That classification is a writing decision the operator makes (or defers to `/co-critique` on a drafted passage).
- **No ranking by "relevance to your thesis".** The essay's thesis may not exist yet (companion mode). Ranking is by keyword overlap and recency; relevance judgment stays with the operator.

---

## Error modes

- If no hits: report "No material found for '<query>'. Try: broader keywords, a different --vault, or /co-find <related-concept>." Do not fail silently.
- If a vault is unreachable or path is missing: skip that vault with a note in the report.
- If the result set is pathologically large (>50 raw hits before capping): emit a capping notice so the operator knows to narrow the query.
