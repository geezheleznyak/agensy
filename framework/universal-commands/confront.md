---
description: Confrontation notebook entry — adversarial engagement with a thinker, concept, or claim
type: universal-protocol
audience: claude
---

# /confront [thinker/concept/claim]

A confrontation notebook entry. Different from an arc: the goal is not systematic exposition but adversarial engagement — finding where a subject fails, where it threatens comfortable assumptions, and where it demands a response.

**[thinker/concept/claim]**: The subject to confront.

**Runtime**: Read `vault-config.md` from the vault root before executing. Extract:
- `open_problems[]` — IDs and names (for vault integration)
- `driving_questions` — q1, q2, q3 (for contextualizing what gets threatened)
- `fault_line` — statement and positions (for positioning the confrontation)

---

## Confrontation Protocol

This is a first-person analytical exercise. Write in active voice. Do not hedge. Do not present "multiple perspectives." Take positions and defend them.

---

### Phase 1 — The Challenge

State, as clearly and forcefully as possible, the strongest version of what this subject is claiming.

Not the diplomatic version. Not the "on the other hand." The version that, if true, would force revision of something important in your current analytical framework.

What is this subject saying that is hardest to accept?

---

### Phase 2 — What It Threatens

State explicitly what this subject threatens:
- Which of your working assumptions does it destabilize?
- Which open problems (from vault-config.md `open_problems[]`) does it shift positions on?
- Which current vault note positions does it put in tension?
- Which driving question (vault-config.md `driving_questions`) does it complicate most?

Name specific vault notes that are threatened. This is the most valuable output of a confrontation.

---

### Phase 3 — The Weakest Points

Where does this subject fail? Not strawman failures — the strongest structural objections.

For each failure mode:
- What is the specific mechanism that fails?
- Is the failure empirical (the claim doesn't match the cases) or logical (internally inconsistent)?
- Who has exploited this failure most effectively, and what was their precise move?

---

### Phase 4 — What It Forces

If this subject is partially right — not fully right, but too right to dismiss — what does it force you to add, qualify, or abandon?

State the minimum revision your analytical framework needs to accommodate what cannot be dismissed.

---

### Phase 5 — Vault Integration

- Which open problems does this confrontation advance? State specific movement — not "it's relevant to" but "it shifts my position from X to Y."
- Is there a Tier 3 judgment note that should be written from this confrontation?
- Which existing notes need updating to register this challenge?

Confrontation entries are working analysis, not vault notes. However:

**Optional Step 6 — Extract and Save (if the confrontation produced a genuinely new insight)**

Apply the 4-gate test from the `/dialogue` synthesis check:
1. **Novelty**: Not already captured at ≥70% overlap?
2. **Atomicity**: One claim, not a cluster?
3. **Connection**: Advances at least one OP or driving question?
4. **Consent**: You approve the proposed note title and opening paragraph?

If all four gates pass → run `/evergreen-note` to capture the insight as a standard vault note. The confrontation entry remains working analysis; the note captures the distilled insight that emerged from it.

If gates fail → the confrontation served its purpose as working analysis. No note needed.
