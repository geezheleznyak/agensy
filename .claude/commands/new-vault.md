You are running the `/new-vault` command. Your job is to elicit the seven founding questions from the user, write a completed `vault-config.md`, and then run Phase 1 of the Genesis Protocol to generate all structural documents.

Follow this procedure exactly. Do not skip steps or reorder them.

---

## Step 0 — Orient the User

Before asking anything, say this (adapt to the conversation — don't read it verbatim):

> We're going to build your new vault from scratch. I'll ask you eight questions — one about intellectual style, then seven about the vault itself. Each one determines a specific part of the vault's structure — nothing is arbitrary. Some questions have right and wrong answers; I'll tell you when an answer needs revision. Once all eight are answered, I'll generate everything: folders, CLAUDE.md, note schema, map reference, domain primers, MOCs, slash commands, coverage plan, and open problems file.
>
> This will take 10–20 minutes. The more precise your answers, the better the vault.

Then ask Q0.5.

---

## Step 0.5 — Q0.5: Intellectual Style

Ask:
> **Q0.5 — Intellectual Style**: How does your domain primarily advance knowledge? Choose the framing that best fits the kind of thinking you want this vault to do:
>
> | | Style | Best for |
> |---|---|---|
> | A | **Adversarial** | Contested domains: politics, philosophy, law, strategy |
> | B | **Dialectical** | Systems domains: economics, complexity, biology, science studies |
> | C | **Contemplative** | Deep traditions: phenomenology, mathematics, art, theology |
> | D | **Constructive** | Building domains: engineering, policy, design, product |
>
> This determines how Q3 is framed, what your engagement field is called (Threatens / Complicates / Transforms / Constrains), and how pressure points and internal tensions are structured.

Wait for the answer.

**Validate**:
- If the user is unsure, ask: "When you encounter a concept that challenges your project, do you want to know what it *attacks*, what it *complicates*, what it *reveals*, or what it *constrains*?" The answer usually points to the style.
- All four styles demand equal analytical rigor — they differ in framing, not depth.
- A contested domain (philosophy, strategy) that is NOT adversarial is fine — if the user's goal is building a system or understanding emergence, dialectical may be right even for traditionally adversarial subjects.

Confirm the style choice back before moving on.

Record as:
```yaml
intellectual_style:
  preset: [adversarial | dialectical | contemplative | constructive]
```

Then ask Q1.

---

## Step 1 — Q1: Mission

Ask:
> **Q1 — Mission**: What is this vault for? One or two sentences maximum. Who is the intended reader in 10 years — you, a student, a specific kind of practitioner? What kind of thinking does it produce?

Wait for the answer.

**Validate**:
- Must be 1–2 sentences. If it's a paragraph, say: "That's the right territory — now compress it to two sentences. The mission statement has to be tight enough to rule things out."
- Must name an output type (notes, essays, training materials, a framework, etc.)
- Must name either a domain or a purpose (not both is fine; neither is not fine)

If it passes: confirm it back — "So your mission is: [restate in your own compression]. Is that right?" — and wait for confirmation before proceeding.

Record as: `mission: "[confirmed text]"`

Then ask Q2.

---

## Step 2 — Q2: Three Driving Questions

Ask:
> **Q2 — Three Driving Questions**: What are the three questions that orient every note in this vault? They should sit at three different levels. A useful pattern (not mandatory):
> - Level 1 — foundational/theoretical: the deep "what is" question
> - Level 2 — applied/operational: the "how does it work in practice" question
> - Level 3 — normative/output: the "so what, what follows" question
>
> Give me three questions. They should be genuinely hard — the kind where a note that doesn't address at least one of them doesn't belong in the vault.

Wait for the answer.

**Validate**:
- Must be exactly 3. If fewer: "What's missing? Every vault has a theoretical question, a practical question, and a 'so what' question — which one don't you have yet?" If more than 3: "Pick the three that a note MUST address. The others are downstream of these."
- The three must be at different levels — not three versions of the same question at different zoom levels.
- Each must be a genuine question (ends with "?"), not a topic ("the nature of consciousness" is not a question).

Confirm each one back before moving on.

Record as:
```yaml
driving_questions:
  q1:
    label: [user's label or your best inference, e.g. "metaphysical", "strategic", "conceptual"]
    text: "[question text]"
  q2:
    label: [...]
    text: "[...]"
  q3:
    label: [...]
    text: "[...]"
```

Then ask Q3.

---

## Step 3 — Q3: Central Engagement Axis

The prompt depends on the style chosen in Q0.5. Use the matching version:

**If Adversarial**:
> **Q3 — Central Fault Line**: What is the deepest unresolved tension in this domain? State it as a genuine opposition — not a preference or a question you expect to answer, but a real dispute where both sides have strong arguments and the vault cannot settle it by fiat.
>
> Format: "Is [X] doing A — or is it doing B?" where both A and B are defensible positions that serious thinkers hold.
>
> Examples: theoria: "Is the universe's tendency toward complexity ontologically real — or an epistemic imposition?" | bellum: "Is the AI/drone revolution creating genuine discontinuity — or do eternal principles hold?"

**If Dialectical**:
> **Q3 — Central Dialectic**: What is the generative tension that drives conceptual development in this domain — the opposition that produces new insight rather than just disagreement? Name the two poles and what synthesizing them would look like.

**If Contemplative**:
> **Q3 — Central Mystery**: What is the core question or mystery this domain progressively illuminates — never fully answering, always deepening? It should be a question where each good answer reveals new layers of the question.

**If Constructive**:
> **Q3 — Central Design Problem**: What is the core constraint-satisfaction problem your domain keeps returning to? Name the competing values or constraints that cannot all be maximized simultaneously.

Wait for the answer.

**Validate (all styles)**:
- Must be statable in one sentence.
- Must have at least 3 named positions (stances notes can take toward the tension/mystery/problem).
- Style-specific failure modes:
  - Adversarial: "I think X is clearly true" → push back: "State it so a serious thinker on the other side has a case."
  - Dialectical: user gives a list of topics → "Name the single animating tension that makes the others make sense."
  - Contemplative: user gives a solvable puzzle → "This sounds answerable. What's the question that stays open even after you answer it?"
  - Constructive: user gives a technical spec → "Name the competing values — what does optimizing for X cost you in Y?"

Confirm back and collect the named positions.

Record using the style-appropriate key:
- Adversarial → `fault_line:` | Dialectical → `central_dialectic:` | Contemplative → `central_mystery:` | Constructive → `design_problem:`

```yaml
# Replace [config_key] with the style-appropriate key above
[config_key]:
  statement: "[one sentence]"
  positions:
    - [name]: "[one sentence description]"
    - [name]: "[one sentence description]"
    - [name]: "[one sentence description]"
```

Then ask Q4.

---

## Step 4 — Q4: Open Problems

Ask:
> **Q4 — Open Problems**: List 8–15 genuinely open problems in this domain. These are the questions the vault exists to work on — not to answer definitively, but to accumulate evidence and arguments about over time.
>
> For each problem: give it a short name (used in note frontmatter) and a one-sentence question.
>
> Aim for problems that span all three of your driving questions. If all your problems are at one level (all theoretical, or all practical), that's a sign the vault's scope is uneven.

Wait for the answer. The user may give a rough list — that's fine.

**Validate**:
- Minimum 8. If fewer: "What else would you want this vault to eventually be able to say something about? Push into territory that feels premature — that's where the open problems live."
- Maximum 15. If more: "Pick the 15 that are most load-bearing. The others are probably downstream of these."
- Each must have a short name (for frontmatter: `open_problems: [1, 3]`) and a question.
- Check distribution across Q2's three driving questions — at least 2 problems per level.

If the list is rough, clean it up and confirm the final list before moving on.

Record as:
```yaml
open_problems:
  - id: 1
    name: "[Short Name]"
    question: "[One sentence question]"
    bears_on: [q1 | q2 | q3 | q1+q2 | all]
  - id: 2
    ...
```

Then ask Q5.

---

## Step 5 — Q5: Note Tier Structure

Ask:
> **Q5 — Note Tier Structure**: Every vault has three tiers of note. What are yours?
>
> - **Tier 1** — the minimal form: raw captures, lookup tables, image stubs. What do you call it, and what triggers promotion to Tier 2?
> - **Tier 2** — the working form: mechanistic explanations, the main note type. What do you call it, and what triggers graduation to Tier 3?
> - **Tier 3** — the final form: permanent output. What do you call it, and where does it live?
>
> Examples:
> - theoria: Reference → Concept → Evergreen (in `20-Evergreen/`)
> - bellum: Source → Evergreen (operational) → Doctrine (in `50-Curriculum/`)
> - logos: Thought → Essay → Published (in `40-Published/`)
>
> The graduation rule for Tier 2 → Tier 3 is the most important one — be specific.

Wait for the answer.

**Validate**:
- Graduation rules must be decision criteria, not descriptions. "When the note is good enough" is not a rule. "When the insight is atomic, the title states a claim, and Connection to the Project is complete" is a rule.
- Tier 3 must have a named output folder.
- Tier 1 can be minimal — even just "raw captures; promote when one operational principle is extractable."

Record as:
```yaml
note_tiers:
  tier1:
    name: "[name]"
    type_value: "[frontmatter type: value]"
    description: "[what qualifies]"
    graduation_rule: "[specific criteria]"
  tier2:
    name: "[name]"
    type_value: "[frontmatter type: value]"
    description: "[what qualifies]"
    graduation_rule: "[specific criteria]"
  tier3:
    name: "[name]"
    type_value: "[frontmatter type: value]"
    description: "[what qualifies]"
    graduation_rule: "[never | specific condition]"
    output_folder: "[relative path]"
```

Then ask Q6.

---

## Step 6 — Q6: Domain Taxonomy

Ask:
> **Q6 — Domain Taxonomy**: What are the major sub-domains in this vault? For each:
> - A label (display name)
> - A folder path (relative to vault root)
> - A priority: `core` (built first, most important), `tier1` (important, build second), `tier2` (valuable but lower priority), `reference` (lookup only)
> - Whether notes in this domain can graduate to Tier 3 (`true`) or are purely reference (`false`)
>
> Aim for 3–12 domains. Too few means the vault won't organize well. Too many means the taxonomy is too fine-grained and will feel fragmented.

Wait for the answer.

**Validate**:
- At least 3 domains, maximum 12.
- At least one domain at `core` priority.
- Domains must not overlap significantly — if two domains share >50% of their notes, merge them.
- Technical/lookup domains (formulas, procedures, definitions) should have `evergreen_candidate: false`.
- Check folder paths: each domain needs a unique path. Suggest standard structure if the user hasn't thought about it.

Clean up and assign slugs (lowercase-hyphenated, e.g. `philosophy-of-mind`). The slug is permanent — warn the user that changing it later requires updating all note frontmatter.

Record as:
```yaml
domains:
  - slug: "[lowercase-hyphenated]"
    label: "[Display Name]"
    folder: "[relative/path/]"
    priority: [core | tier1 | tier2 | reference]
    evergreen_candidate: [true | false]
```

Then ask Q7.

---

## Step 7 — Q7: Output Layer

Ask:
> **Q7 — Output Layer**: What does the final-form output of this vault look like? Be concrete — describe the artifact.
>
> - What is it? (atomic notes, published essays, training modules, doctrine documents, a book manuscript, a system of arguments...)
> - Who reads it? (future you, students, an audience, a specific practitioner...)
> - What does it do? (serves as reference, makes a public argument, trains a skill, preserves thinking...)
>
> This determines where Tier 3 lives, what it looks like, and which slash commands are generated.

Wait for the answer.

**Validate**:
- Must match the vault type implied by Q1 (accumulation → evergreen notes; training → curriculum/doctrine; expression → essays/published).
- Must name a folder (the Tier 3 output folder from Q5 should match this).
- If the user names a publication target (a blog, a journal, a specific audience), record it.

Record as:
```yaml
output_layer:
  type: [evergreen-notes | training-curriculum | published-essays | doctrine-notes | hybrid]
  description: "[concrete description of the artifact]"
  graduation_folder: "[same as Q5 tier3.output_folder]"
  graduation_command: "[the slash command that produces this output]"
  publication_target: "[venue/audience or N/A]"
```

---

## Step 8 — Final Checklist

Before writing any files, run the checklist aloud with the user:

> Before I generate everything, let me confirm the eight answers:
>
> - **Q0.5 Style**: [preset name]
> - **Q1 Mission**: [restate]
> - **Q2 Driving Questions**: [list all three]
> - **Q3 [engagement axis label]**: [restate + named positions]
> - **Q4 Open Problems**: [count] problems spanning [distribution across Q2 levels]
> - **Q5 Tiers**: [Tier 1 name] → [Tier 2 name] → [Tier 3 name], output in [folder]
> - **Q6 Domains**: [count] domains — [list slugs and priorities]
> - **Q7 Output**: [type], [graduation folder]
>
> Checklist:
> - [ ] Q0.5 intellectual style chosen and confirmed
> - [ ] Q1 is 1–2 sentences and rules things out
> - [ ] Q2 has exactly 3 questions at 3 different levels
> - [ ] Q3 uses the style-appropriate config key and framing, with at least 3 named positions
> - [ ] Q4 has 8–15 problems spanning all three driving questions
> - [ ] Q5 graduation rules are specific enough to decide without judgment
> - [ ] Q6 has 3–12 domains; slugs are final
> - [ ] Q7 output type matches vault type from Q1

Ask: "Does this look right? Any corrections before I build?"

Wait for confirmation. Make any corrections. Do not proceed until the user explicitly confirms.

---

## Step 9 — Write vault-config.md

Ask: "What is the vault's root path?" — get the absolute path.

Write `vault-config.md` to `[vault-root]/vault-config.md` using the full YAML structure from `framework/vault-config-schema.md`, populated with all confirmed Q0.5–Q7 answers. The `intellectual_style:` block (from Q0.5) must be included in full — including the derived `engagement_axis`, `engagement_field`, `pressure_points`, `internal_tensions`, `dialogue_philosophy`, and `graduated_depth` sub-blocks for the chosen preset. See `vault-config-schema.md` § Q0.5 for the complete block to populate.

Also write `vault-config.md` as `[vault-name]-config.md` to `synthesis-meta/vaults/` for the registry.

---

## Step 10 — Run Phase 1 (Document Generation)

Tell the user:
> Config is written. Now generating the 12 structural documents. This will take a few minutes — I'll tell you what I'm writing as I go.

Generate all 12 documents in order, announcing each one:
1. Folder structure
2. CLAUDE.md (from `framework/claude-md-template.md` + vault-config answers)
3. `[vault-name]-note-taxonomy.md`
4. `[vault-name]-development-plan.md`
5. `[vault-name]-coverage-plan.md`
6. `[vault-name]-map-reference.md` or map reference document for this vault type
7. Domain primers (one per core/tier1 domain in `_maps/` or `maps/`)
8. MOCs (one per domain + master index in `30-MOCs/`)
9. `.claude/commands/` files (all universal + generated commands)
10. `open-problems-[domain].md`
11. Confirm `vault-config.md` is in vault root
12. `memory/MEMORY.md` (initial state)

After each document: state what was written and its path. If a document has a structural decision embedded in it, note why: "The CLAUDE.md generated `/wargame` because this is a training vault (Q7)."

---

## Step 11 — Self-Audit

After all 12 documents:

Tell the user:
> Structure complete. Running self-audit to verify everything is coherent.

Run `/coverage-audit` equivalent manually:
- List all domain folders created (from Q6)
- Confirm all primers exist (one per core/tier1 domain)
- Confirm all MOCs exist
- Confirm all slash command files exist
- Report: "N folders, N primers, N MOCs, N slash commands. Coverage plan baseline: all [count] planned notes show as gaps — expected at this stage."

If anything is missing, fix it before reporting done.

---

## Step 12 — Handoff

Tell the user:

> Your vault is ready. Here's how to use it:
>
> **To start building content**: Run `/arc [subject] [type]` on your highest-priority domain. This produces a map + 8–12 atomic notes — the structural test that everything is working.
>
> **To know what to build next**: Run `/what-next` at the start of any session.
>
> **To maintain coverage**: Run `/coverage-audit` after every 10–15 new notes.
>
> **Your open problems** are in `open-problems-[name].md`. Every Tier 2 note should reference at least one by number.
>
> **Your [engagement axis label]** is: [Q3 statement]. Every synthesis-schema note must state its position on this using the `[config_key]:` frontmatter field.
>
> **Your engagement field** is: **[engagement_field.name]** — every Connection to the Project section must fill it. [Style reminder: Threatens = what assumption it attacks | Complicates = what prior understanding it revises | Transforms = what perception it changes | Constrains = what design tradeoff it introduces.]

Update `synthesis-meta/vault-registry.md` with the new vault entry.
