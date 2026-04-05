---
type: config-extract
vault: synthesis_oeconomia
audience: claude
---
# Config Extract — synthesis_oeconomia

Q1–Q7 answers extracted from `synthesis_oeconomia/vault-config.md`. Full runtime config lives in vault root.

---

## Q1 — Mission

Build a rigorous analytical framework for understanding economic systems as complex adaptive systems — mapping the structural forces, behavioral patterns, and emergent dynamics that generate orders, cycles, crises, and regime transitions. Output: calibrated analytical lenses for reading any economic situation accurately and navigating it with cold-blooded precision.

---

## Q2 — Driving Questions

1. **Structural**: What are the generative mechanisms of economic systems — the structural forces (debt dynamics, technological paradigms, institutional path dependency, power distributions) that produce orders, cycles, crises, and regime transitions regardless of individual actors?
2. **Behavioral**: How do individuals, firms, and states actually make economic decisions — and how do cognitive limits, incentive structures, narrative contagion, and power asymmetries create outcomes that rational models systematically miss?
3. **Navigational**: How does an agent read an economic situation accurately and position to survive, exploit, or endure different regimes, cycles, and disruptions without requiring accurate prediction of specific outcomes?

---

## Q3 — Fault Line

**Statement**: Are economic outcomes primarily determined by structural forces — debt cycles, technological paradigms, institutional path dependency, power distributions — that individual actors cannot meaningfully resist? Or are they primarily shaped by ideas, narratives, and behavioral patterns — where expectations, herding, and narrative contagion become the very structural forces they appear to reflect?

**Positions**: `structuralist` | `behavioral-ideational` | `complex-interactive` | `regime-dependent`

---

## Q4 — Open Problems (12)

1. **The Business Cycle Problem**: What actually drives economic cycles — exogenous shocks, endogenous credit dynamics, technological paradigm shifts, or policy errors?
2. **The Debt Supercycle Problem**: Are long-run debt accumulation dynamics structurally deterministic, or contingent on policy and political choices?
3. **The Expectations Problem**: How much do agent expectations shape economic reality vs. reflect underlying fundamentals?
4. **The Crisis Anatomy Problem**: What structural features make financial systems crisis-prone — and when does systemic risk become unavoidable?
5. **The Institutions Problem**: How do institutional configurations determine growth trajectories — and how do institutions change?
6. **The Reflexivity Problem**: How does economic analysis alter the systems it analyzes — making standard causal inference circular?
7. **The Knowledge Problem**: Can any central mechanism aggregate the dispersed knowledge that markets process — and what follows if not?
8. **The Paradigm Shift Problem**: How do technological paradigms restructure economic systems — and how do we know if AI represents genuine discontinuity?
9. **The Narrative Problem**: How much causal weight do economic narratives carry — do they merely reflect economic reality or help constitute it?
10. **The Power Problem**: How do power asymmetries shape economic outcomes that market models treat as determined by efficiency?
11. **The Financialization Problem**: Has the growing dominance of financial sector logic over production altered the deep structure of capitalism?
12. **The Navigation Problem**: What decision frameworks are robust across different economic regimes when prediction of specific outcomes is impossible?

---

## Q5 — Note Tier Structure

- **Tier 1 (Source)**: Raw captures from economic texts, research, debates — lives in `10-Sources/`
- **Tier 2 (Analysis)**: Atomic notes on mechanisms, thinkers, frameworks — lives in domain subfolders
- **Tier 3 (Judgment)**: Permanent claim-titled notes on economic mechanisms and regime patterns — lives in `20-Judgment/`
- **Graduation rule**: T2 → T3 when atomic, standalone, claim-titled, and fault_line position set

---

## Q6 — Domain Taxonomy

| Domain | Folder | Priority | evergreen_candidate |
|---|---|---|---|
| macro-dynamics | `macro-dynamics/` | core | true |
| financial-systems | `financial-systems/` | core | true |
| behavioral-economics | `behavioral-economics/` | core | true |
| institutional-economics | `institutional-economics/` | tier1 | true |
| political-economy | `political-economy/` | tier1 | true |
| complexity-economics | `complexity-economics/` | tier1 | true |
| navigation | `navigation/` | tier2 | mixed |

---

## Q7 — Output Layer

**Type**: judgment notes + navigation lenses
**Artifact**: Tier 3 claim-titled notes on economic mechanisms; navigation notes on regime-reading
**Audience**: Practitioner navigating economic uncertainty without requiring point prediction
**Connection**: Type 3 bidirectional with politeia (political economy), bellum (logistics, resource constraints), theoria (complexity as ontology), historia (economic history patterns)

---

## Intellectual Style Config

```yaml
intellectual_style:
  preset: dialectical
  engagement_axis:
    config_key: central_dialectic
    label: "Structure vs. Behavioral-Ideational Dynamics"
    positions:
      - structuralist: "Structural forces (debt, technology, institutions, power) determine economic outcomes regardless of actor cognition"
      - behavioral-ideational: "Cognitive limits, narratives, and expectations are not noise but the mechanism — they constitute the structural forces"
      - complex-interactive: "Neither is prior — the system is reflexive; structure and belief mutually constitute each other"
      - regime-dependent: "Which lens applies depends on the economic configuration — different regimes privilege different causal channels"
  engagement_field:
    name: Complicates
    prompt: "What prior understanding does this force revision of — what had to be qualified, refined, or abandoned?"
  pressure_points:
    format: boundary_condition
```
