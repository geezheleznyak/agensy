---
type: reference
audience: claude
---
# Inter-Vault Connection Protocol

Rules governing connections between vaults in the synthesis series. Three connection types cover all meaningful relationships between vaults. The rules are enforced by convention — Obsidian does not resolve cross-vault wikilinks — but the semantic structure is real and searchable.

---

## Why This Protocol Exists

Each vault has a different type (accumulation, training, expression) and a different mission (Q1). Cross-vault connections are not wikilinks in the standard Obsidian sense — they do not resolve in the graph view. But they are meaningful references that can be:
- Read and followed manually
- Searched by text (`theoria:`, `politeia:`, `oeconomia:`, `bellum:` prefixes — as configured per vault)
- Used by Claude to locate source material during argument development

**Critical distinction**: Cross-vault references are primarily for **Claude-mediated vault building** — enabling Claude to find relevant source material in sibling vaults when developing maps, notes, or arcs. They are NOT for live Obsidian navigation (links won't resolve). The audience is Claude at build time, not the user at read time.

The protocol prevents two failure modes:
1. **Circular dependency**: Expression vault drives accumulation vault content (gets the direction backwards — knowledge generates expression, not the reverse)
2. **Silent dependency**: Essays or doctrine documents that depend on specific knowledge-base notes without stating the dependency (breaks traceability)

---

## Three Connection Types

### Type 1 — Knowledge-Base → Expression

**Pattern**: synthesis_theoria → synthesis_logos

**Direction**: One-way. Expression vault cites from the knowledge base. Knowledge base does not reference the expression vault.

**When to activate**: A Tier 3 (Evergreen) note in the knowledge base has matured enough to seed an essay or argument. The note's insight is not just theoretical — it has a claim the user wants to make publicly.

**Reference format** (in expression vault note frontmatter):
```yaml
source_refs: ["[[202603161800 - The Chinese Room Shows Syntax Cannot Generate Semantics]]"]
```

**Reference format** (inline in expression vault body):
```
(→ theoria: [[202603161800 - The Chinese Room Shows Syntax Cannot Generate Semantics]])
```

**Rules**:
- Every expression vault note that depends on a knowledge-base note MUST list it in `source_refs`
- Inline references use the `(→ [vault-name]: [[...]])` format at the specific claim they ground
- Knowledge-base notes do NOT get backlinks to expression vault content — direction is preserved
- If an essay requires a knowledge-base note that does not yet exist, it is a signal to run `/arc` in the knowledge base first

---

### Type 2 — Knowledge-Base → Training

**Pattern**: synthesis_theoria → synthesis_bellum

**Direction**: One-way. Training vault extracts principles from the knowledge base as doctrine nodes. Knowledge base does not reference the training vault.

**When to activate**: A systematic map or Tier 3 note in the knowledge base has a "Connection to the Project" section that maps directly onto a training vault domain question. For example: a causation map in theoria maps onto the training vault's intelligence domain (how do commanders reason causally about adversary behavior?).

**Reference format** (in training vault note frontmatter):
```yaml
source_vault: "synthesis_theoria"
source_note: "epistemology/pearl-systematic-map"
```

**Reference format** (inline in training vault body):
```
(→ theoria: pearl-systematic-map § "Counterfactual Reasoning")
```

**Rules**:
- Training vault notes derived from knowledge-base content must cite the source section
- Extraction is selective — a training vault note does not summarize the knowledge-base note; it extracts one operational principle relevant to commander training
- Knowledge-base notes are NOT updated to reference the training vault

---

### Type 3 — Parallel Vaults

**Pattern**: Any two accumulation vaults, or an accumulation vault ↔ training vault where neither depends on the other.

**Active Type 3 bridges**:

| Pair | Bridge domain | Nature |
|---|---|---|
| theoria ↔ politeia | Philosophy, complexity, epistemology | theoria provides metaphysical grounding; politeia applies structurally to power |
| theoria ↔ oeconomia | Complexity, information, causation | theoria's causal/emergence theory illuminates oeconomia economic dynamics |
| politeia ↔ oeconomia | Political economy, institutions, power/markets | Markets as politics; power distributions as economic constraints |
| politeia ↔ bellum | Strategy, state capacity, Clausewitz friction | War as politics by other means; strategic theory spans both |
| oeconomia ↔ bellum | Logistics, economic warfare, resource constraints | Material substrate of military power |

**Direction**: Bidirectional. Either vault can reference the other when a connection is genuinely illuminating.

**When to activate**: During arc building, if the subject falls within a bridge domain listed above, scan the sibling vault for relevant notes. Carry that awareness into the map and notes — do not fabricate links, but let the sibling vault's treatment deepen the analysis. See `cross-vault-bridges.md` for specific bridge domains, search terms, and vault-specific treatments.

**Reference format** (any direction):
```
(→ bellum: theory/maps/clausewitz-systematic-map § "Friction")
(→ politeia: power-strategy/202603180900 - Structural Power)
(→ oeconomia: complexity-economics/202603250800 - Reflexivity and Causation)
```

**Rules**:
- Bidirectional references must be explicitly stated in both vaults (if A → B, then B should also note the connection)
- Parallel connections are logged in `vault-registry.md` in agensy
- Do not create a parallel connection that is really a dependency — if vault A requires vault B's content to make sense, it is Type 1 or Type 2, not Type 3
- Awareness of a bridge does NOT mandate creating a cross-vault reference in every arc note. Quality over quantity — only when the sibling vault's treatment genuinely deepens the note

---

## Cross-Vault Reference Format (Summary)

| Vault | Inline Prefix | Example |
|---|---|---|
| synthesis_theoria | `→ theoria:` | `(→ theoria: [[202603161800 - Consciousness Cannot Be Reduced to Computation]])` |
| synthesis_bellum | `→ bellum:` | `(→ bellum: theory/maps/clausewitz-systematic-map)` |
| synthesis_logos | `→ logos:` | `(→ logos: 20-Essays/202603161000 - On AI and Human Nature)` |
| synthesis_politeia | `→ politeia:` | `(→ politeia: power-strategy/202603180900 - Structural Power Is Invisible)` |
| synthesis_oeconomia | `→ oeconomia:` | `(→ oeconomia: complexity-economics/202603250800 - Reflexivity and Causation)` |
| synthesis_historia | `→ historia:` | `(→ historia: civilizational-dynamics/202603310900 - Imperial Overextension Pattern)` |
| agensy | `→ meta:` | `(→ meta: framework/genesis-protocol)` |

**Never use absolute paths** in vault notes. Use vault-name-relative paths. Absolute paths break when vaults are moved or synced to different machines.

---

## Connection Registry

When a Type 3 (parallel) connection is created, log it in `vault-registry.md` under a `## Cross-Vault Connections` section:

```markdown
## Cross-Vault Connections

| Source Vault | Source Note | Target Vault | Target Note | Connection Type | Created |
|---|---|---|---|---|---|
| bellum | theory/maps/clausewitz-map | logos | 20-Essays/202603... | Type 3 | 2026-03-16 |
```

This registry prevents the parallel connection network from becoming invisible over time.

---

## What NOT to Do

**Do not summarize knowledge-base notes in expression or training vaults.** Extract one principle, one claim, one insight — not the whole note. The knowledge-base note is the full treatment; the derivative vault cites it for one specific purpose.

**Do not create knowledge-base notes whose primary purpose is to serve another vault.** The knowledge-base builds on its own logic (Q1 mission). If a note is only useful as a source for the expression vault, it belongs in the expression vault's `05-Sources/`, not in the knowledge base's `20-Evergreen/`.

**Do not let cross-vault references go stale.** If a knowledge-base note is deleted or restructured, the references in dependent vaults must be updated. A broken reference is worse than no reference — it creates false confidence in the connection.

**Do not skip citing when citing is needed.** Every expression vault note that depends on a specific knowledge-base note for a specific claim must cite it. "Vaguely informed by [vault-name]" is not a citation. Precise dependency tracking is what makes the three-vault system coherent.
