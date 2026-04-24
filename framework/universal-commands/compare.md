---
description: Structural comparison of two thinkers, concepts, or frameworks on a specific question
type: universal-protocol
audience: claude
---

# /compare [s1] and [s2] on [question]

Generate a systematic structural comparison of two subjects on a specific analytical question.

**[s1], [s2]**: Thinkers, concepts, or frameworks to compare.
**[question]**: The specific question or problem domain for the comparison.

**Runtime**: Read `vault-config.md` from the vault root before executing. Extract:
- `intellectual_style` — engagement_axis (positions[]) and engagement_field (name)
- `open_problems[]` — IDs and names for vault integration
- `domains[]` — folder structure for locating existing maps

---

## Step 1 — Subject Mapping

For each subject ([s1] and [s2]):
- Glob domain folders from vault-config.md `domains[]` for `[name]-systematic-map.md`, `[name]-concept-map.md`, `[name]-framework-map.md`
- If a map exists: extract engagement axis position, core mechanism, and synthesis instrument entries
- If no map exists: draw from available notes and prior knowledge; flag that a map would strengthen the comparison

---

## Step 2 — Comparison Matrix

Build a structured comparison on the specified [question]:

| Dimension | [S1] | [S2] |
|---|---|---|
| Core claim | | |
| Analytical mechanism | | |
| Engagement axis position | | |
| Evidence base | | |
| Diagnostic power (what it reads correctly) | | |
| Blind spots (what it systematically misreads) | | |
| Position on [question] | | |

---

## Step 3 — Key Agreements

Where do [S1] and [S2] converge? Does the convergence strengthen or weaken the combined position?

Two frameworks agreeing for very different internal reasons should prompt suspicion — agreement on the surface may mask incompatible underlying logic.

---

## Step 4 — Key Disagreements

For each point of divergence on [question]:
- Name the specific disagreement
- State what each position predicts or implies
- Identify which vault evidence (historical cases, existing notes) favors which position

---

## Step 5 — Conditional Judgment

Do not hedge with "it depends" without specifying: under what conditions does each position hold?

**When [S1] is the stronger framework**: [conditions]
**When [S2] is the stronger framework**: [conditions]
**The unresolved core**: What question does neither framework resolve, and what would it take to resolve it?

---

## Step 6 — Vault Integration

- Which open problems (vault-config.md `open_problems[]`) does this comparison advance? State specific movement.
- Which engagement axis tension (vault-config.md `intellectual_style.engagement_axis`) does this comparison illuminate most clearly?
- Recommendation: Should a synthesis note or Tier 3 judgment note be generated from this comparison? If yes, state the claim it would make and which `/evergreen-note` call would produce it.
