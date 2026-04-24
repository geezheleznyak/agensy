---
description: Multi-turn engagement between the user's thinking and vault frameworks
type: universal-protocol
---

# /dialogue [topic or opening thought]

Engage the user's own thinking against the vault's frameworks in a multi-turn conversation. Every other command is Claude reading the vault and producing a document. `/dialogue` is Claude engaging the user's thinking — their developing positions, disagreements, and uncertainties — as a thinking partner.

**Runtime**: Read `vault-config.md` from the vault root before executing. Extract:
- `open_problems[]` — IDs and names (for routing output and checking novelty)
- `driving_questions` — q1, q2, q3 (for checking whether what emerged is project-facing)
- `intellectual_style` — engagement_axis (statement, positions) and dialogue_philosophy (convergence_rule) for identifying where the user's position sits and when convergence is legitimate
- `folder_structure.output` — where Route 1 notes are placed
- `note_template.synthesis` — schema for any note produced

---

## Four Modes (auto-detected from user input)

| Mode | User Signal | Claude's Role | Typical Route |
|---|---|---|---|
| **Interrogate** | "What does the vault say about X?" | Synthesizer — present vault's position, let user steer | Route 4 (already captured) or Route 1 (synthesis reveals gap) |
| **Reflect** | "I've been thinking about X..." | Midwife — surface tensions, deepen the thought | Route 1 (knowledge claim) or Route 2 (personal position) |
| **Challenge** | "I disagree with [note/position]..." | Steelman — defend the vault's strongest version | Route 1 (if challenge holds → new note) or Route 4 (if vault position holds) |
| **Bridge** | "What would [vault A] say about this [vault B] problem?" | Translator — read both vaults, synthesize across | Route 1 (cross-vault bridge note) or Route 3 (cross-vault question) |

---

## Step 1 — Listen and Surface

Read the user's input carefully. Identify the mode (Interrogate / Reflect / Challenge / Bridge).

Search the vault for 3–7 most relevant notes. For each:
- Read the synthesis instrument (Connection to the Project / Judgment Instrument)
- Note the engagement axis position
- Note which open problems it addresses

If Bridge mode: read from both referenced vaults before proceeding.

---

## Step 2 — First Engagement

Present what the vault says, with specific note citations. Do not summarize — state positions.

Identify 1–2 tensions between the user's input and vault positions. Name them precisely:
- "Your claim assumes X, but [Note Title] argues Y because Z."
- "The vault is split on this: [Note A] says X while [Note B] says not-X."

Ask **one focused question** that pushes the user deeper. Not a clarifying question — a deepening question that forces the user to defend or refine their position.

**Follow `intellectual_style.dialogue_philosophy.convergence_rule`** (read from vault-config.md). Default styles: adversarial → "Do not resolve. Deepen." | dialectical → "Do not flatten. Synthesize upward." | contemplative → "Do not summarize. Inhabit." | constructive → "Do not assert. Test." — Convergence gate in Step 4 overrides this only when all 4 gates pass AND the user has produced a specific, falsifiable claim with supporting evidence.

---

## Step 3 — Iterative Exchange (2–4 turns)

Each turn:
1. Acknowledge the user's response in one sentence.
2. Surface the next tension or implication — not the same one again.
3. Relate to a specific vault framework by name.
4. Ask the next deepening question.

**Rules for the exchange**:
- Neither you nor the user wins prematurely.
- Each turn must introduce something new — a new framework, a new tension, a forced concession.
- Do NOT converge before Step 4.
- If the user asks for your view, give it briefly, then return the question.

---

## Step 4 — Synthesis Check

State what emerged from the dialogue in 2–3 sentences. Then apply the 4-gate test:

| Gate | Test | Failure Action |
|---|---|---|
| **Novelty** | Search vault output folder for ≥70% content overlap with proposed claim | Point to existing note; if dialogue added nuance, suggest editing existing note |
| **Atomicity** | Is this one claim or a cluster? | If cluster: decompose into candidates, test each separately |
| **Connection** | Does it advance at least one OP or address a driving question? | If no: log to question bank or cogitationis, not the knowledge vault |
| **User consent** | Propose the note title and opening paragraph. User approves? | If declined: respect. Log insight to dialogue log for potential future revisit |

Route the output:

```
Knowledge claim → Route 1 (standard note in vault)
Personal position → Route 2 (cogitationis Thought)
Unresolved question → Route 3 (question bank)
Already captured → Route 4 (cite existing notes)
```

---

## Step 5 — Write (if Route 1 or Route 2)

**Route 1** — Knowledge claim that passes all 4 gates:
- Run the standard `/evergreen-note` protocol.
- Frontmatter must include: `source: user-dialogue`
- Full synthesis instrument (Connection to the Project / Judgment Instrument), See Also, Open Questions.
- Update relevant MOC.
- Append one row to `memory/note-index.md`: `| [path] | T2 | [domain] | true | [axis] | [ops] | user-dialogue | [date] |`

**Route 2** — Personal position or developing argument:
- Write a cogitationis Thought note using the Thought template.
- Frontmatter: `status: raw`, `omega_refs: [relevant note titles]`
- First-person voice. Claim-titled.
- Optionally also produce a Reflection in `30-Reflections/` if the dialogue had a significant personal dimension.

**Route 3** — Unresolved question:
- Run `/question-bank add "[question]" --vault [name] --op [N]`
- No new knowledge note.

**Route 4** — Already captured:
- Cite the 2–3 most relevant existing notes.
- Optionally suggest editing one to incorporate any nuance that emerged.

---

## Step 6 — Log

Add an entry to the vault's `memory/MEMORY.md` Dialogue Log:

```
- YYYY-MM-DD | [topic] | [mode] | [user's position in one sentence, or — if no clear position emerged] | Route [N]: [note path / question-bank entry N / no output]
```

**Bridge mode addition**: If mode = `Bridge` and a clear position emerged (not `—`), also append one line to `C:\Users\grego\obsidian_repos\synthesis-meta\system-state.md` under `## User Positions (Cross-Vault)`:

```
- YYYY-MM-DD | [user's position in one sentence] | [vaults implicated]
```

Do not append if the dialogue produced only Route 3 (question bank) or Route 4 (already captured) without a new cross-vault stance.

---

## Step 7 — Trajectory & Interest Capture (Learner Layer)

After logging the dialogue, surface candidate Learner Layer entries via **propose-confirm**. Skip this step entirely if `synthesis-meta/learner/` does not exist (vault user has not adopted the Learner Layer).

### 7.1 — Trajectory delta detection

Read the **tail** of `synthesis-meta/learner/learning-trajectory.md` (the most recent ~10 entries via `Read` with `offset` near end-of-file; do NOT read the whole file). This gives recent-trajectory context for shift detection.

Detect whether THIS session produced a trajectory-significant event:
- **Confidence shift**: the user reversed or substantially refined a position they previously held (cross-reference Step 4 output against tail)
- **Recurring question landed**: a question that has appeared in prior trajectory entries finally got resolved (or got reframed, which counts)
- **Stuck signal**: the same tension came up again unresolved — note as a "stuck" entry so future sessions see the recurrence

If none: skip to 7.2 (do NOT propose a trajectory entry just because a session happened — only when something shifted).

If yes: propose ONE trajectory entry in the format declared in `learning-trajectory.md`:
```
### YYYY-MM-DD — [vault] — [topic short tag]

- **Opened**: <what was engaged>
- **Shifted**: <delta — terse>
- **Stuck**: <if applicable>
- **Source**: /dialogue
- **Refs**: <note paths or position IDs>
```

Ask: "Trajectory entry for `learning-trajectory.md`? (Y / edit / skip)" — only on Y or edit-then-Y, append to the **Active Entries** section of the file.

### 7.2 — Interest signal detection

Detect interest declarations in the user's turns: phrases like "I want to understand X better," "this fascinates me," "remind me to read Y," "I should look into Z," "this opens up questions about W I want to pursue."

For each detected signal, propose ONE interests-register entry in the format declared in `interests-register.md`:
```
### [INTEREST-####] [Short topic name]

- **Surfaced**: YYYY-MM-DD (vault: [vault] — context: dialogue on [topic])
- **What**: <one-sentence>
- **Why now**: <the trigger>
- **Status**: active
- **Last touched**: YYYY-MM-DD
```

Generate next ID by reading the current highest INTEREST-#### in the file's Active Interests section and incrementing.

Ask: "Interest entry for `interests-register.md`? (Y / edit / skip)"

### 7.3 — Token-budget discipline

- Tail-read trajectory only (≤30 lines).
- Grep interests-register only if the user said something interest-y (don't read the whole file by default).
- If neither 7.1 nor 7.2 surfaces a candidate, the cost of Step 7 is zero file writes and ≤30 lines of context.

---

## The Synthesis Test in Detail

The 4-gate test prevents note inflation. Gate failures do not mean the dialogue failed — they mean the insight belongs elsewhere or needs more development.

**Novelty failure** → Point to the existing note. If dialogue added a new angle, suggest a targeted edit rather than a new note. One well-developed note beats two thin ones.

**Atomicity failure** → Decompose the cluster. Test each candidate separately through all 4 gates. Some candidates will pass; others won't. Write only those that pass.

**Connection failure** → This insight may be genuinely valuable but not project-facing. Route 2 (personal position in cogitationis) or Route 3 (question bank) are legitimate homes. Not every insight needs to be a vault note.

**Consent failure** → The user may feel the insight is not ready, not quite right, or too personal. Respect this. Log the topic in the dialogue log so it can surface in a future session.

---

## Integration With Other Commands

| Command | Integration |
|---|---|
| `/coverage-audit` | Counts `source: user-dialogue` notes in domain totals and OP coverage. Reports "user positions" as a separate line: "Domain X: 15 thinker-derived, 3 user-originated." |
| `/axis-survey` | Includes user-dialogue notes in engagement axis distribution. User's positions appear alongside thinker positions. |
| `/what-next` | Checks question bank for open questions. If a question aligns with the next recommended arc, surfaces the connection. |
| `/synthesis` | User-dialogue notes are first-class vault knowledge — included as evidence alongside thinker-derived notes. |
| `/engage-deep` | Natural follow-up: "You just formulated a claim in dialogue. Now engage it deeply — find where it fails, what it forces, what it cannot resolve." Lifecycle protocol should suggest this. |
| `/arc` | After arc completes in a domain where the user has existing positions, flag: "You have N dialogue-derived positions in this domain — does the new material challenge any?" |
| `/revisit` | After 30 days, re-engage the note with new vault context. Has the user's position held? |
