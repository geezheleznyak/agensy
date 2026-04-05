---
description: Deep dive on one open problem using current vault material
type: universal-protocol
audience: claude
---
# /engage-problem [N or name]

Deep structural engagement with one of the vault's open problems. Surveys what the vault currently knows, maps competing positions, names the fault line tension, and identifies what would advance the problem.

**[N or name]**: Problem number or partial name.

**Runtime**: Read `vault-config.md` from the vault root before executing. Extract:
- `open_problems[]` — full list with IDs, names, and questions
- `reference_docs.open_problems` — path to detailed open problems file (may contain richer context than vault-config.md)
- `intellectual_style` — engagement_axis (positions[]) and engagement_field (name) for mapping vault stances
- `domains[]` — folder structure for vault survey

---

## Step 1 — Problem Retrieval

Find the specified problem in vault-config.md `open_problems[]`. If `reference_docs.open_problems` exists with a richer definition, read it.

Extract:
- Full problem statement and question
- Why it matters for the vault's mission
- Core tension as currently stated
- Engagement axis relevance
- Which driving questions it bears on (if specified in vault-config.md)
- Current vault position (if any)

---

## Step 2 — Vault Survey

Search all domain folders (vault-config.md `domains[]`) for notes with this problem's ID in `open_problems` frontmatter.

For each relevant note: read the synthesis instrument section (Judgment Instrument / vault-equivalent).
Record: What position does each note take on the problem? What does it confirm? What does it `[engagement_field.name]`?

---

## Step 3 — Position Mapping

Map current vault positions using engagement axis positions from vault-config.md `intellectual_style.engagement_axis.positions[]`:

For each engagement axis position: list notes with wikilinks that take this stance.

**Currently unaddressed aspects**:
- What dimensions of this problem has the vault not yet addressed?
- What evidence would resolve or advance the problem that the vault currently lacks?

---

## Step 4 — Synthesis

State the vault's current best position on this problem:
- What can the vault currently argue, based on existing material?
- What is the key tension in that position?
- What would the strongest counter-argument look like from within the vault?

---

## Step 5 — Advancement Plan

Identify 2–3 specific actions that would advance this problem most:
- Which thinker or concept map would contribute most? → `/arc [subject]`
- Which historical case would calibrate the problem best? → `/arc [case] concept`
- Which domain currently has the most relevant unbuilt material?

Output: specific actionable recommendations, not general suggestions.
