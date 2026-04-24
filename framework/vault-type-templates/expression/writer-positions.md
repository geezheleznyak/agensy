---
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: positions-card
status: awaiting-user-fill
---

# Writer Positions

**Substance layer** — WHAT the writer believes. Consumed by `/article-seed`, `/article-draft`, and `/article-revise` on every run. Pairs with `voice-profile.md` (style layer).

**This file is authored by you, not extracted from vault content.** A position is what you'd defend at a dinner party when the vault isn't on screen. The vault informs your writing but does not substitute for your commitments.

**Status progression**: `awaiting-user-fill` → `seeded-v0.1` (sections 1, 2, 5 minimally filled — enough for `/article-draft` to check alignment) → `seeded-v1.0` (all seven sections filled). `/article-draft` will warn when this file is unfilled but proceed; `/article-revise` Pass C will skip position-alignment checks until at least §1 and §2 are filled.

---

## How this file is used

- `/article-seed`: when extracting a thesis candidate from a map, the seed is flagged if the implicit thesis conflicts with any non-negotiable in this file. Conflict is surfaced, not silently resolved.
- `/article-draft`: every generated claim is checked against positions. Alignment is good. Conflict triggers one of three responses: (a) suppress the claim, (b) argue against the map's claim from your position, (c) revise the position here. Choice is yours.
- `/article-revise`: adversarial pass includes a "vault-voice bleed" check — does the draft argue something you don't actually hold? This file is the reference.
- `/article-critique` and `/co-critique`: cited theorists are cross-checked against `Rejected Frames` to catch misuse.
- `/co-capture` in companion mode: user-confirmed substantive commitments can be appended here.

---

## 1. Founding Commitments

*The core ideas you build from — the things you take as given, not because they are trivially true but because they are the starting premises of your thinking.*

Fill in 3–7 commitments. Each is a claim you hold as premise, not conclusion. State each as a sentence or two, not a paragraph.

**Your entries**:

1. *[Commitment 1 — e.g., "Complexity is not a decoration on simple systems; it is a distinct ontological mode."]*
2. *[Commitment 2]*
3. *[Commitment 3]*
4. *...*

---

## 2. Rejected Frames

*Frames, methods, or vocabularies you deliberately refuse. What you won't argue from, and why. This is where your essays diverge from the mainstream that might otherwise surround the topic.*

Fill in 3–7 rejected frames. Each is a vocabulary or conceptual move you explicitly will not use. State each with a one-sentence reason.

**Your entries**:

1. *[Rejected frame 1 — e.g., "'Rules-based order' as an analytical category. It is a coalition label, not a structural description."]*
2. *[Rejected frame 2]*
3. *...*

---

## 3. Recurring Dispositions

*Intellectual habits that show up across your writing. Not as rigid as commitments, but reliable tendencies — how you approach a new problem.*

Fill in 5–10 dispositions. Each is a pattern of intellectual orientation, stated as a one-sentence tendency.

**Your entries**:

1. *[Disposition 1 — e.g., "Start with the structural forces; treat stated intentions as signals to be decoded, not as primary causes."]*
2. *[Disposition 2]*
3. *...*

---

## 4. Open Tensions I'm Willing to Inhabit

*Places where you hold two commitments that don't fully reconcile, and where you've decided not to force a resolution. Naming them prevents future essays from pretending the tension doesn't exist.*

Fill in 2–5 open tensions. Each is a genuine pairing of beliefs whose synthesis is unclear.

**Your entries**:

1. *[Tension 1 — e.g., "Structural determinism vs. heroic will: structure explains most of what happens, but genuine agency is the residual that matters most."]*
2. *[Tension 2]*
3. *...*

---

## 5. Non-Negotiables

*Positions where a draft that argues against you — even for the sake of exploring a counterargument — is wrong. These are the places where `/article-draft` must refuse to generate against you, not merely flag.*

Fill in 2–5 non-negotiables. Be strict here — only include what you genuinely will not argue against. If you include too many, the pipeline loses expressive range; too few, and drafts risk contradicting you silently.

**Your entries**:

1. *[Non-negotiable 1]*
2. *[Non-negotiable 2]*
3. *...*

---

## 6. Preferred Analytical Moves

*Methodological commitments — not what you believe, but how you prefer to argue. The moves you reach for first.*

Fill in 5–10 analytical moves. Each is a stated methodological preference. This section grows through the harvest loop at `/article-promote` Step 7 when a published essay surfaces a new methodological commitment.

**Your entries**:

1. *[Move 1 — e.g., "Reach for mechanism first. If you can describe the mechanism, the claim is analytically serious; if you can't, it's still at the claim level."]*
2. *[Move 2]*
3. *...*

---

## 7. Audience Contract

*What you commit to your reader. What level of background you assume; what you will and will not do to ease comprehension; what kind of reading experience the reader is signing up for.*

Fill in 4–8 audience-contract bullets. Each is a commitment about the reader relationship.

**Your entries**:

1. *[Contract bullet 1 — e.g., "Technical concepts arrive doing work, not as prerequisite material. A reader who does not know the term will learn it through its use in the argument, not through a dictionary definition."]*
2. *[Contract bullet 2]*
3. *...*

---

## Maintenance

- **Appends, not rewrites.** Existing entries should rarely be deleted. If a position has evolved, update it in place with a note (e.g., "updated 2026-XX-XX after Essay N"). If a position is abandoned, move it to a dated §Retired section rather than deleting it.
- **Harvest sources**: the harvest loop at `/article-promote` Step 7 proposes appends to §3 (Dispositions) and §6 (Preferred Analytical Moves) when a published essay surfaces a new methodological commitment. User confirms each.
- **Conflicts between sections**: if §1 (Founding Commitment) and §5 (Non-Negotiable) disagree, the non-negotiable wins — it is the stricter contract.
- **Cross-reference with `voice-profile.md`**: style changes rarely require position changes; position changes often require voice updates. Check both when revising either.

---

## See Also

- `voice-profile.md` — style layer (HOW, not WHAT)
- `positions-index.md` — substantive framework claims earned in essays (complementary: writer-positions is bedrock; positions-index is accumulation)
- `article-design-principles.md` — craft principles (structural rules for essays, not substantive commitments)
