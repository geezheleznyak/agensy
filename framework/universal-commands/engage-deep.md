---
description: Deep engagement notebook entry — rigorous intellectual encounter with a thinker, concept, or claim
type: universal-protocol
audience: claude
---

# /engage-deep [thinker/concept/claim]

A deep engagement notebook entry. Different from an arc: the goal is not systematic exposition but rigorous intellectual encounter — finding where a subject creates pressure, what it forces you to revise, and what it demands as a response.

**[thinker/concept/claim]**: The subject to engage with.

**Runtime**: Read `vault-config.md` from the vault root before executing. Extract:
- `open_problems[]` — IDs and names (for vault integration)
- `driving_questions` — q1, q2, q3 (for contextualizing what gets forced)
- `intellectual_style` — engagement_axis (statement and positions), engagement_field (name and prompt)

**Style-dependent framing**: The five phases below use the vault's engagement field:
- **Adversarial** (`engagement_field.name: Threatens`): find what this subject attacks and destabilizes
- **Dialectical** (`engagement_field.name: Complicates`): find what this subject forces revision of
- **Contemplative** (`engagement_field.name: Transforms`): find what this subject changes in how you see
- **Constructive** (`engagement_field.name: Constrains`): find what design tradeoffs this subject introduces

---

## Engagement Protocol

This is a first-person analytical exercise. Write in active voice. Do not hedge. Do not present "multiple perspectives." Take positions and defend them.

---

### Phase 1 — The Challenge

State, as clearly and forcefully as possible, the strongest version of what this subject is claiming.

Not the diplomatic version. Not the "on the other hand." The version that, if true, would force revision of something important in your current analytical framework.

What is this subject saying that is hardest to accept?

---

### Phase 2 — What It [engagement_field.name]

State explicitly what this subject [engagement_field.name — Threatens / Complicates / Transforms / Constrains]:

- Which of your working assumptions does it [destabilize / require revision of / change your perception of / introduce tradeoffs into]?
- Which open problems (from vault-config.md `open_problems[]`) does it shift positions on?
- Which current vault note positions does it put in tension?
- Which driving question (vault-config.md `driving_questions`) does it affect most?

Name specific vault notes that are implicated. This is the most valuable output of a deep engagement.

---

### Phase 3 — The Weakest Points

Where does this subject fail? Not strawman failures — the strongest structural objections.

For each failure mode, use the style-appropriate grounding:
- **Adversarial**: Who exploited this failure, and what was their precise move?
- **Dialectical**: What boundary condition exposes this as limited? What demonstration revealed it?
- **Contemplative**: Where does this subject reach its explanatory limit? What phenomenon shows the limit?
- **Constructive**: Under what conditions does this approach fail? What does the failure produce?

---

### Phase 4 — What It Forces

If this subject is partially right — not fully right, but too right to dismiss — what does it force you to add, qualify, or abandon?

State the minimum revision your analytical framework needs to accommodate what cannot be dismissed.

---

### Phase 5 — Vault Integration

- Which open problems does this engagement advance? State specific movement — not "it's relevant to" but "it shifts my position from X to Y."
- Is there a Tier 3 judgment note that should be written from this engagement?
- Which existing notes need updating to register this challenge?

Engagement entries are working analysis, not vault notes. However:

**Optional Step 6 — Extract and Save (if the engagement produced a genuinely new insight)**

Apply the 4-gate test from the `/dialogue` synthesis check:
1. **Novelty**: Not already captured at ≥70% overlap?
2. **Atomicity**: One claim, not a cluster?
3. **Connection**: Advances at least one OP or driving question?
4. **Consent**: You approve the proposed note title and opening paragraph?

If all four gates pass → run `/evergreen-note` to capture the insight as a standard vault note. The engagement entry remains working analysis; the note captures the distilled insight that emerged from it.

If gates fail → the engagement served its purpose as working analysis. No note needed.
