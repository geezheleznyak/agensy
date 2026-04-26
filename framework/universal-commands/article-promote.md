---
description: Promote a revised essay to 40-Published — backlink source maps, update Writing Dashboard
type: universal-protocol
---

# /article-promote [essay-path]

Move a completed essay from `20-Essays/` to `40-Published/`, backlink to source maps, and update the Writing Dashboard.

**[essay-path]**: absolute or vault-relative path to an essay at status `revision` with all five-questions check passing.

**Runtime**: Read `vault-config.md` from the expression vault root. Extract:
- `reference_docs.source_map_registry`
- `reference_docs.positions_index` — path to positions-index.md (V1.6)
- `reference_docs.writer_positions` — for methodological-promotion target (V1.6)
- `folder_structure.output` — `40-Published/`
- `folder_structure.mocs` — for Writing Dashboard update
- `output_layer.graduation_folder`

---

## Step 1 — Validate Readiness

1. Verify [essay-path] exists and status is `revision`.
2. Read the frontmatter `revision_log`. Verify the most recent entry has `five_questions: [yes, yes, yes, yes, yes]`.
3. Verify non-negotiable violations count is 0 in the most recent revision entry.
4. Verify `audience` and `venue` frontmatter are set (not empty).

If any check fails: refuse with a specific reason. Do not promote incomplete essays.

---

## Step 2 — Pre-Promotion Checks

### 2.1 Final wikilink sweep
Grep the body for `[[` patterns. Any internal vault wikilink remaining → refuse. All references must be in `source_refs` frontmatter (audit trail), not inline.

**Exception**: wikilinks to other published essays in the expression vault (essay → essay cross-references) are allowed.

### 2.2 Word count sanity
- **Type A**: verify the final word count is within range 2,000–4,500 words (generous). Under 1,500 → warn "essay is short; confirm". Over 5,000 → warn "essay is long; confirm".
- **Type D (V1.7)**: verify the final word count is within range 5,000–8,500 words. Under 4,500 → warn "braid is short; three-framework weaves typically need 5k+ to earn equal treatment of each framework. Confirm before proceeding." Over 9,000 → warn "braid is long; verify each framework section earns its space rather than accumulating material. Confirm."

### 2.3 Title check
Verify title is claim-form (not question-form or label-form). Good: "Power Is Relational". Bad: "Some Thoughts on Power" or "Is Power Relational?"

If title is not claim-form: suggest a revised title and ask user.

---

## Step 3 — Move the File

1. Read the essay.
2. Update frontmatter:
   ```yaml
   status: final
   updated: YYYY-MM-DD
   published_date: YYYY-MM-DD  # new field — date of promotion
   ```
3. Write to `40-Published/[original filename].md` (preserve the YYYYMMDDHHMM prefix).
4. Delete the original from `20-Essays/` (or leave as archive if user prefers — configurable in vault-config.md later).

---

## Step 4 — Backlink Source Maps

For each entry in `source_refs` frontmatter (source-vault maps):

1. Traverse to the source map file in its source vault.
2. Check if the source map has an "Essays citing this" or "Published derivatives" section. If no: add one at the bottom (before any trailing horizontal rule).
3. Append a line: `- [YYYY-MM-DD] [[<vault path to expression-vault essay>]] — <one-sentence description>`
4. **Type D only**: the description should state the framework's role in the braid, not just the essay title. Example: `- [2026-04-21] [[logos/40-Published/... - The Pole Is Obsolete]] — Mearsheimer's multipolar-instability claim, in braid with Strange + Arthur to argue the pole is an unstable unit of analysis under AGI.` This makes it clear to a future reader of the source map how the framework participated in the composition, not just that it was cited.

This creates the reverse link: source maps know which essays have been derived from them. For Type D, each of the N source maps gets its own backlink with a framework-role-specific description.

---

## Step 5 — Update Source-Map Registry

Update source-map-registry.md:
- Essay status → `published`
- Essay path → the new `40-Published/` path (not `20-Essays/`)

Increment any per-source-vault essay count if tracked.

---

## Step 6 — Update Writing Dashboard

Read `50-MOCs/Writing Dashboard.md`. If it has a "Published" section with a Dataview query: verify the query will catch the new file (should auto-refresh in Obsidian).

If there's no Published section or no Dataview: add a manual entry — `- [YYYY-MM-DD] [[<essay wikilink>]] — <theme>` under a "Recently Published" section.

---

## Step 7 — Harvest Loop (V1.6)

Essay-writing is a **producer** of substantive claims, not only a consumer. This step diffs the published essay's claims against the source-map atomics (and any `matched_positions` T3s it drew on) to surface novel analytical claims that should be promoted into the knowledge layer.

**Blocking**: if any accepted promotion fails to write (target folder missing, file-write error), the promote halts and surfaces the error. Do not leave positions-index in a half-updated state.

### 7.1 — Extract claims from the essay

Parse the essay body. For each paragraph:
- Identify **structural-assertion sentences**: sentences that make a general claim about how things work (mechanism, scope, failure condition, KPI critique). Skip narrative description, case exposition, and direct quotation.
- Collect into a claim candidate set.

### 7.2 — Diff against prior material

For each claim candidate:
1. Check the source map's atomic notes (read `source_refs` frontmatter) — is this claim already present in an atomic?
2. Check the `matched_positions` T3s — is this claim already in a referenced T3?
3. Check existing positions-index rows for claim overlap (grep by the claim's key nouns).

If match: mark as **already grounded**, skip.
If no match: mark as **novel claim candidate**.

### 7.3 — Classify each novel candidate

For each novel candidate, propose one of four classifications (fourth added V1.7 for Type D):

- **Substantive framework claim** — generalizable, domain-bound, has mechanism + scope. Promotes to a new T3 in the relevant source vault + new row in positions-index.
  - Heuristic: the claim has a clear target (what it describes), a mechanism (why it holds), and at least one pressure point (when it fails). And: the claim could be cited in a future essay on an adjacent topic.
- **Methodological claim** — about how to analyze, not about what's true in the domain. Appends to `writer-positions.md` §"Preferred Analytical Moves" (or §"Recurring Dispositions" if better fit). Does not get a T3.
  - Heuristic: the claim takes the form "before X, always Y" or "the way to read X is Z" — it is a move, not a finding.
- **Cross-vault emergent claim** (V1.7, Type D only) — a substantive claim that none of the N source vaults alone is the natural home for, because the claim is itself about how phenomena in those vaults compose. Promotes to `agensy/cross-vault-bridges.md` as a new bridge entry (or extension of an existing bridge) AND to positions-index as a new row with `source vaults` listing all N. May also get a T3 in each source vault summarizing the braid's contribution to that vault's domain, but the primary artifact is the cross-vault bridge entry.
  - Heuristic: the claim mentions phenomena or concepts native to two or more of the N source vaults in the same sentence, and the claim would lose meaning if reduced to any single vault's domain vocabulary.
  - Braid emergent claims (`C` itself, the essay's thesis) are almost always this classification, not the plain substantive-framework classification.
- **Essay-specific** — contingent on the specific case, not generalizing. Remains in essay only. No promotion.
  - Default for unclear cases. Conservative bias.

**Expected volume per essay**:
- Type A: typically 0–2 substantive promotions + 0–1 methodological. Hirschman pilot produced 1 substantive (P001) + 1 methodological.
- Type D: typically 2–4 substantive and/or cross-vault promotions + 0–1 methodological. The emergent claim (C) itself is almost always the signature artifact; additional substantive claims often emerge from the per-framework sections where the essay extended a single-framework T3 into braid territory.

### 7.4 — User confirmation

Emit a confirmation block listing every novel claim with proposed classification and one-sentence rationale:

```
Harvest candidates for [essay title]:

1. [SUBSTANTIVE] "<claim>"
   Rationale: <why substantive>
   Proposed target: synthesis_<vault>/20-Judgment/... + positions-index row P###

2. [METHODOLOGICAL] "<claim>"
   Rationale: <why methodological>
   Proposed target: writer-positions.md §"Preferred Analytical Moves"

3. [ESSAY-SPECIFIC] "<claim>"
   Rationale: contingent on this case.
   Proposed target: none.

Accept each? (Y to accept as proposed, R to reclassify, N to reject.)
```

Reclassifications are free-form — user can override any of the three classifications. Rejections do not block promote; they are logged in essay frontmatter `harvest_rejections`.

### 7.5 — Execute accepted promotions

For each accepted **substantive promotion**:
1. Determine the target source vault (typically the source-map's vault, but the user may redirect — e.g., a claim about narratives may belong in oeconomia rather than politeia).
2. Draft the T3 note using that vault's synthesis-note template: title as claim-sentence, body with mechanism + cases + pressure, backlinks to essay + source map, frontmatter fields per vault schema (`fault_line`, `open_problems`, `evergreen-candidate: true`, `source`, `originating_essay`).
3. Write the T3 to `synthesis_<vault>/20-Judgment/YYYYMMDDHHMM - <Claim>.md` (or vault's equivalent T3 folder).
4. Append a row to `positions-index.md`:
   - ID: next `P###` (scan for highest existing ID, increment).
   - Claim: the claim sentence (compressed if necessary).
   - Source T3: wikilink to the new T3.
   - Topics: derived from T3 frontmatter + essay tags + claim key nouns.
   - Originating Essay: wikilink to the newly published essay.
   - Status: `active`.
   - Registered: today's date.

For each accepted **cross-vault emergent promotion** (V1.7, Type D):
1. Determine whether an existing bridge in `agensy/cross-vault-bridges.md` covers the claim's domain. If yes → extend that bridge with a new sub-entry; if no → add a new bridge entry at the end of the file with a new bridge number.
2. The bridge entry records: (a) the emergent claim, (b) the N vaults and what each contributes, (c) the braid hinge mechanism in one sentence, (d) a backlink to the originating essay.
3. Append a row to `positions-index.md`:
   - ID: next `P###`.
   - Claim: the emergent claim.
   - Source T3: the bridge entry path (not a single-vault T3).
   - Source vaults: list of all N source vaults.
   - Topics: derived from T3 frontmatter + essay tags + claim key nouns; also add `cross-vault`.
   - Originating Essay: wikilink.
   - Status: `active`.
   - Registered: today's date.
4. **Optional companion T3s**: if the braid's contribution to any *single* source vault is also a standalone substantive claim (e.g., the braid argued Strange's structural-power architecture collapses under compute mediation — that's a politeia-native claim even though it emerged from a braid), draft a T3 in that vault's `20-Judgment/` with a backlink to the cross-vault bridge entry. Mark the T3 frontmatter `derived_from_braid: true` and `originating_essay: <wikilink>`. These companion T3s are *additional* to the cross-vault bridge entry, not replacements.

For each accepted **methodological promotion**:
1. Identify the best section in `writer-positions.md` (usually §"Preferred Analytical Moves", sometimes §"Recurring Dispositions").
2. Append a numbered entry with the move + one-sentence rationale + backlink to the originating essay.
3. Do not create a T3 and do not add to positions-index.

**Essay-specific** candidates: no action.

### 7.6a — Interests-register harvest (Learner Layer)

Skip this sub-step entirely if `agensy/learner/interests-register.md` does not exist (vault user has not adopted the Learner Layer).

A published essay frequently surfaces *new* lines of inquiry the user wants to pursue but isn't ready to write about — phrases like "this opens questions about X I want to develop later," "the relationship between Y and Z deserves its own essay," "I should look more deeply into W." These are interest declarations distinct from the substantive/methodological/cross-vault claims handled in 7.3–7.5.

Scan the essay body once more for **interest signals**:
- Explicit deferrals: "deserves separate treatment," "I'll return to this," "another essay's territory"
- Curiosity declarations: "I want to understand X better," "this fascinates me"
- Reading intentions: "I should read more of [thinker]," "the literature on Y warrants engagement"

For each detected signal, propose ONE entry to `learner/interests-register.md`'s Active Interests section, format per that file:
```
### [INTEREST-####] <short topic>

- **Surfaced**: YYYY-MM-DD (vault: logos — context: published essay [essay title])
- **What**: <one-sentence>
- **Why now**: <the trigger sentence from the essay, optionally>
- **Status**: active
- **Follow-through**: [[<essay path>]]
- **Last touched**: YYYY-MM-DD
```

Generate next ID by reading current highest INTEREST-#### and incrementing.

Confirmation block (separate from the 7.4 claim block):
```
Interest harvest candidates from [essay title]:

1. [INTEREST] "<one-sentence interest>"
   Surfaced from: "<quoted essay phrase>"
   Proposed status: active

Accept each? (Y / edit / N to reject)
```

Append accepted entries to interests-register.md Active Interests. No T3 created. No positions-index touch.

**Token-budget**: do NOT load the whole interests-register; tail-read for the highest existing ID, append.

### 7.6 — Record harvest outcome in essay frontmatter

Append to the promoted essay:
```yaml
harvest:
  run_date: YYYY-MM-DD
  substantive_promotions:
    - t3: "[[synthesis_<vault>/20-Judgment/...]]"
      positions_index_id: P###
  methodological_promotions:
    - section: "Preferred Analytical Moves"
      entry: "<one-line summary>"
  interest_harvests:
    - register_id: INTEREST-####
      what: "<short topic>"
  essay_specific: <count>
  rejections: <count>
```

**For Type D, also include:**
```yaml
harvest:
  run_date: YYYY-MM-DD
  cross_vault_promotions:
    - bridge_entry: "[[agensy/cross-vault-bridges.md#Bridge N]]"
      positions_index_id: P###
      source_vaults: [politeia, oeconomia, ...]
      companion_t3s:
        - "[[synthesis_<vault>/20-Judgment/...]]"  # optional
  substantive_promotions: [...]  # per-framework extensions, if any
  methodological_promotions: [...]
  essay_specific: <count>
  rejections: <count>
```

The `cross_vault_promotions` block is distinct from `substantive_promotions` because the primary artifact is the bridge entry, not a single-vault T3. Companion T3s (if any) are listed nested under their parent cross-vault promotion so the origin braid is always recoverable.

---

## Step 8 — Record in Memory (Optional)

If this is a pilot essay or a milestone (first essay, tenth essay, first Type B pair, etc.): append a brief line to `memory/MEMORY.md` or a topic file. Ephemeral details (date, word count) do not belong in memory; only the fact of the milestone + anything surprising about the process.

---

## Step 9 — Report

**Type A report:**
```
## /article-promote [essay-path] — YYYY-MM-DD

Essay published: [absolute path to new file in 40-Published/]
Status: final
Published: YYYY-MM-DD
Type: A
Word count: <final>
Audience: <audience from frontmatter>
Venue: <venue from frontmatter>

Source maps backlinked: <count>
Registry updated.
Writing Dashboard updated.

Harvest loop (V1.6):
- Claim candidates extracted: <N>
- Substantive promotions: <N> (P### IDs: <list>)
- Methodological promotions: <N> (to <section>)
- Essay-specific: <N>
- Rejections: <N>

[If milestone] Milestone recorded in memory: <which>.

Essay URL ready for:
- Export to <venue> format (use `obsidian:defuddle` or manual export)
- Sharing with at least one external audience (per Tier 3 graduation rule)
```

**Type D report (V1.7):**
```
## /article-promote [essay-path] — YYYY-MM-DD

Essay published: [absolute path to new file in 40-Published/]
Status: final
Published: YYYY-MM-DD
Type: D (synthesis-braid)
Frameworks: <F1 name> × <F2 name> × <F3 name> [× ...]
Seam: <seam sentence>
Emergent claim: <C, one sentence>
Word count: <final> (target band: 5,000–8,500)
Audience: <audience>
Venue: <venue>

Source maps backlinked: <count of N> — each with framework-role description.
Registry updated: all N source maps marked published (<essay>).
Writing Dashboard updated.

Harvest loop (V1.7, Type D):
- Claim candidates extracted: <N>
- Cross-vault emergent promotions: <N> (P### IDs: <list>, bridge entries: <list>)
- Companion T3s: <N> (one per source vault where the braid's contribution stands alone)
- Substantive per-framework promotions: <N> (P### IDs: <list>)
- Methodological promotions: <N>
- Essay-specific: <N>
- Rejections: <N>

Cross-vault bridges touched: <Bridge-N name(s)> (extended / added)

[If milestone] Milestone recorded in memory: <which>.
  (V1.7 first Type D pilot = milestone.)

Essay URL ready for:
- Export to <venue> format
- Sharing with at least one external audience (per Tier 3 graduation rule)
```

---

## Error modes

- Incomplete revision (five-questions not all yes): refuse, return to `/article-revise`.
- Remaining wikilinks inline: refuse, return to revision with specific wikilinks flagged.
- Venue/audience empty: prompt the user to set before promotion.
- Source map missing from its vault: warn, still promote, note as "source-map-missing-at-promotion" in frontmatter for future review.
- **Harvest promotion fails** (T3 write error, positions-index append error, writer-positions append error): halt at Step 7.5, report the failure, leave any successfully-written artifacts in place but mark the promote as `partial`. Next invocation can re-run Step 7 idempotently (skip already-promoted candidates by checking essay frontmatter `harvest.substantive_promotions`).
- **Type D seam mismatch at promotion** (V1.7): if final essay body no longer instantiates the seam named in frontmatter (e.g., revise-step drift collapsed the braid to a solo-with-footnotes), refuse and return to `/article-revise` Pass E seam-stress audit. Promote is not the place to discover a degenerated braid.
- **Type D cross-vault bridge write fails**: halt at Step 7.5, report the failure. Do not create companion T3s referencing a non-existent bridge entry — the bridge entry is the primary artifact and must land first. Next invocation skips already-written artifacts by checking essay frontmatter `harvest.cross_vault_promotions[].bridge_entry`.
- **Type D: no cross-vault emergent promotion accepted** but essay frontmatter declares `article_type: D`: warn that a braid producing zero cross-vault claims is anomalous — either the essay under-earned its emergent claim (revise issue) or the user deliberately rejected the promotion. Proceed but record `harvest.braid_produced_no_emergent_claim: true` for future pattern-mining.
