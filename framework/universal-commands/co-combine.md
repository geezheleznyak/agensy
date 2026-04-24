---
description: Companion-mode bridge-surfacing. Given N source maps, return conceptual bridges — shared concepts, opposing claims, complementary mechanisms, possible synthesis angles — as options, not drafts.
type: universal-protocol
audience: claude
---

# /co-combine <map1> <map2> [<map3> ...]

Given 2–5 source maps (cross-vault OK), surface conceptual bridges between them. Return a structured report the operator reads to decide whether and how to weave the maps into their own writing. Does not write prose, does not draft a braid, does not assert the "right" composition.

**<map1> <map2> ...**: 2 to 5 source-map paths (absolute or vault-relative). 1 map is rejected (no pair to combine); 6+ maps rejected as diffuse (suggest splitting into two combines).

**Runtime**: Read each map file fully. Read `vault-config.md` of each map's source vault for context on map conventions. Read `cross-vault-bridges.md` from agensy to see if any of the pairwise combinations are already registered as formal bridges.

---

## Step 1 — Validate Input

1. Parse paths. Split on whitespace.
2. Enforce 2 ≤ N ≤ 5. If N=1: "Use /co-find to explore a single map, or provide a second map to combine." If N>5: "Too many maps for one combine — cap is 5. Split into two /co-combine calls."
3. Verify each map exists. If any missing, list all missing before aborting.
4. Read each map. Parse into sections (founding problem, first principles, core concepts with Depends/Enables/Constrains clauses, pressure points, connection-to-project).

---

## Step 2 — Extract Bridge Candidates

For each pair of maps (M_i, M_j) where i<j (so (N choose 2) pairs), look for:

**2.1 — Shared concepts**:
- Core-concept nouns that appear (by lemma match or close synonym) in both M_i and M_j.
- Founding-problem overlap — same phenomenon analyzed from different angles.

**2.2 — Opposing claims**:
- First-principles in M_i that contradict first-principles in M_j.
- Pressure points in M_i that name M_j's framework (or a recognizable proxy).

**2.3 — Complementary mechanisms**:
- Enables/Constrains clauses in M_i that connect to core concepts in M_j (M_i's output becomes M_j's input, or vice versa).
- Sequential explanation: M_i explains the condition, M_j explains what happens under it.

**2.4 — Shared pressure, different resolution**:
- Pressure points in both maps targeting the same phenomenon but proposing different failure modes. The maps may agree on what's hard but disagree on why.

**2.5 — Unit-of-analysis difference**:
- Note when M_i operates at state-level and M_j at firm-level (or individual / collective / platform). This is a structural incompatibility that must be engaged if the maps are composed — it is NOT a bridge; it is a seam-stress candidate.

---

## Step 3 — Score and Surface

Rank bridges by how much of each map's core they involve:

- **Strong**: touches ≥2 core concepts in both M_i and M_j AND the maps' founding problems overlap.
- **Moderate**: touches ≥1 core concept in each, with a clear mechanism linking them.
- **Weak**: surface keyword match only, no mechanism connection.

Report strong + moderate; drop weak unless N=2 (then include weak to give the operator anything).

---

## Step 4 — Identify Possible Synthesis Angles

For each pair with ≥ moderate strength, name 1–3 possible synthesis angles:
- "M_i's X becomes M_j's Y under condition K" (sequential composition)
- "M_i and M_j make competing predictions about Z — reconciliation requires naming which is primary" (competing-framework composition)
- "M_i explains why M_j's mechanism fails in case K" (limitation-finding)
- "M_i's pressure point names M_j; M_j's treatment of that pressure differs from M_i's canonical reading" (tension-surfacing)

Synthesis angles are **options the operator reads, not theses the operator must adopt**. The operator decides whether any angle is worth writing.

---

## Step 5 — Cross-Vault Bridge Registry Check

If any pair (M_i, M_j) is in `cross-vault-bridges.md` already, surface the existing bridge entry — the work of connecting these has been done before; the operator can reuse or extend.

---

## Step 6 — Report

```
## /co-combine <N maps> — YYYY-MM-DD

Maps combined (N=<count>):
  M1 [[<path>]] — "<title>" (vault: <vault>)
  M2 [[<path>]] — "<title>" (vault: <vault>)
  ...

### Bridges by pair

**M1 ↔ M2** (strength: <strong|moderate>)
- Shared concept: <concept name> — appears in M1 §<section> and M2 §<section>.
- Opposing claim: M1 says "<claim>"; M2 says "<claim>". Tension source: <one-line>.
- Complementary mechanism: M1's <concept X> Enables M2's <concept Y> via <mechanism>.
- Unit-of-analysis note: M1 operates on <unit>, M2 on <unit>. Composition across scales requires explicit argument.

**M1 ↔ M3** (strength: <...>)
- ...

(one subsection per pair with ≥ moderate strength)

### Possible synthesis angles (options, not drafts)
1. **<angle name>**: <one-to-two sentence description of a composition the operator could write>. Seam candidate: "<named tension>". Load-bearing frameworks: M1, M2.
2. ...
3. ...

### Existing cross-vault bridges
- Bridge <N> [<pair>]: "<title>" — [[cross-vault-bridges.md#Bridge N]]. Note: <relevance to current combine>.

### Unit/timescale cautions
- M1 operates at <unit>/<timescale>; M2 at <unit>/<timescale>. If composing, name the shift explicitly or restrict scope.

---

Next moves:
- Pick an angle and start writing — the essay is yours.
- /co-find <concept> to deepen any specific bridge with T3 material or atomic notes.
- /co-suggest <stuck point> if a composition idea is unclear.
- /co-critique <selection> once you've drafted a passage that engages the bridge.
```

---

## Non-goals

- **Does not write a braid.** A braid is a Type D pipeline artifact (`/article-seed` with `type=D`, `preset: synthesis-braid`). `/co-combine` surfaces the same bridge material but leaves composition to the operator.
- **Does not assert the right composition.** The report lists options; the operator picks or rejects.
- **Does not score for thesis-fit.** The companion-mode essay may not have a thesis yet. Ranking is by bridge strength, not by how well the bridge serves a claim the operator hasn't committed to.
- **Does not run seam-audit gates.** The V1.7 seam-stress / synthesis-validity audits in `/article-outline` Step 6.5 and `/article-revise` Pass E are pipeline artifacts. In companion mode, the operator engages the seam themselves (or invokes `/co-critique` on a drafted braid section for similar pressure).

---

## Error modes

- If a pair has no bridges (zero shared concepts, no opposing claims, no mechanism links): report the pair with strength=none and a one-line reason ("these maps do not appear to share conceptual surface on inspection — consider whether they belong in the same essay").
- If all pairs are weak: emit a warning — "All pairwise bridges are weak. These maps may not be the right set to combine. Consider /co-find for material closer to a shared concept."
- If a map file cannot be parsed (unusual structure): fall back to keyword-level bridge extraction and note the degradation in the report.
