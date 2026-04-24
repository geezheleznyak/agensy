---
description: Position statement — what can this vault currently argue on a question?
type: universal-protocol
audience: claude
---

# /synthesis [question]

Generate a position statement from vault material: what can the vault currently argue, with what confidence, and where does the argument break down?

**[question]**: A driving question, an open problem, or a specific claim to evaluate.

**Runtime**: Read `vault-config.md` from the vault root before executing. Extract:
- `driving_questions` — q1, q2, q3 labels and text (for question classification)
- `intellectual_style` — engagement_axis (statement, positions[]) and engagement_field (name)
- `open_problems[]` — IDs and names (for relevance tagging)
- `domains[]` — folder structure for evidence survey

---

## Step 1 — Question Classification

Classify the question by type (using vault-config.md `driving_questions` as reference framework):
- **Structural**: How do political/intellectual forces work systematically?
- **Diagnostic**: How to read a specific type of situation correctly?
- **Decisional**: What is the optimal move in a given configuration?

Engagement axis relevance: Does answering this question require taking a position on the vault's central engagement axis (Q3)? State the expected engagement axis position of the answer.

---

## Step 2 — Vault Evidence Survey

Search domain folders (vault-config.md `domains[]`) for notes that bear on this question:
- Search by topic in domain folders
- Search `open_problems` frontmatter for relevant problem IDs
- Read synthesis instrument sections (Judgment Instrument / vault-equivalent) — specifically the primary insight entries and `[engagement_field.name]` entries

For each relevant note: What position does it support? What does it complicate?

---

## Step 3 — Position Construction

**Main claim** (1–2 sentences): What does the vault currently argue about this question?

**Supporting evidence** (from vault notes with wikilinks):
- [Claim 1]: *(→ [[note wikilink]])*
- [Claim 2]: *(→ [[note wikilink]])*
- [Claim 3]: *(→ [[note wikilink]])*

**Engagement axis position**: Which position from vault-config.md `engagement_axis.positions[]` does the vault's argument occupy on this question? One sentence justifying it.

---

## Step 4 — Stress Test

**Internal tensions**: Places where vault notes pull in opposite directions on this question.

**Empirical challenges**: Historical cases or evidence that complicate the main claim.

**What the vault cannot yet argue**: What would strengthen or falsify the main claim that the vault currently lacks the material to address?

---

## Step 5 — Confidence Assessment

Rate the argument's confidence:
- **High**: Multiple converging vault notes, confirmed by historical cases, no major internal tensions
- **Medium**: Some vault support, but key evidence missing or contested
- **Low**: Vault material exists but points in different directions; significant gaps

State explicitly: which `/arc` sessions would most increase confidence?

---

## Step 6 — Output

Structured position paper:
- Main claim
- Supporting structure (3–5 points with wikilinks)
- Key complications
- Confidence level + upgrade path
- Which open problems (vault-config.md `open_problems[]`) this question advances
