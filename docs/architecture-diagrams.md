---
type: reference
stability_tier: foundational
canonicity: derived
derives_from: [framework/principles/system-architecture.md]
audience: human
---

# System Diagrams

Visual companion to `system-architecture.md`. The canonical form of the framework's topology is the YAML manifest in `system-architecture.md`; the diagrams here render the same structure for human orientation. Claude does not need to read this file to reason about the framework — the YAML manifest carries the same information in structured form.

**Reading order for framework-change work**: `architecture-principles.md` (WHY — invariants) → `system-contracts.md` (HOW — contract table) → `system-architecture.md` (WHAT — YAML manifest) → `framework-meta-architecture.md` (META — doc system). This file is *not* in the reading chain; open it when you want to see the system visually.

**View in Obsidian** for rendered Mermaid.

---

## Diagram 1 — Complete System Map

Every major component and the relationships between them. Subgraphs group by functional layer. Constraints are annotated at the relevant edges and nodes.

```mermaid
graph TD
    subgraph META["agensy — Framework Source"]
        SPINE["Architectural Spine ×4<br/>architecture-principles (WHY)<br/>system-contracts (HOW)<br/>system-architecture (WHAT)<br/>framework-meta-architecture (META)"]
        FD["Other Framework Docs ×11<br/>genesis-protocol · vault-config-schema<br/>claude-md-template · note-tier-template<br/>map-type-template · command-lifecycle<br/>inter-vault-protocol · slash-command-suite<br/>system-model-schema · system-model-architecture<br/>primitives · map-to-article-extraction"]
        VTT["vault-type-templates/<br/>expression/ — 6 substrate scaffolds<br/>training/ — 3 scaffolds<br/>accumulation/ — intentionally empty"]
        UP["Universal Protocols ×34 + 2 aliases<br/>core (17): arc · coverage-audit · axis-survey<br/>what-next · promote · compare · engage-problem<br/>synthesis · update-moc · evergreen-note · engage-deep<br/>domain-audit · dialogue · positions · revisit<br/>question-bank · quick-check<br/>system-model (4): query · audit · build · bridge<br/>article-pipeline (8): scan/seed/outline/draft/revise<br/>promote/critique/companion<br/>companion-co (5): find · combine · suggest<br/>critique · capture"]
    end

    subgraph CONF["Configuration — loaded into context"]
        GC["Global CLAUDE.md<br/>universal rules · every session<br/>CONSTRAINT: max 100 lines"]
        VC["Vault CLAUDE.md<br/>vault identity · per vault every session<br/>CONSTRAINT: max 120 lines"]
        VCF["vault-config.md<br/>~260 lines · on-demand per command<br/>blocks: intellectual_style · driving_questions<br/>engagement_axis · open_problems · domains<br/>note_tiers · folder_structure<br/>note_template · reference_docs"]
    end

    subgraph EXEC["Execution — command dispatch chain"]
        STUBS[".claude/commands/ stubs<br/>~11 lines · logic-free pointers<br/>CONSTRAINT: one stub per universal command"]
        PROTO["Protocol read from<br/>[AGENSY_PATH]/framework/universal-commands/"]
        PARAM["Parameterized execution<br/>vault-config values injected"]
    end

    subgraph CONTENT["Content — vault output"]
        T1["Tier 1 — Capture<br/>00-Inbox/ · 10-Sources/"]
        T2R["Tier 2-Ref<br/>Reference schema<br/>evergreen-candidate: false"]
        T2S["Tier 2-Syn<br/>Synthesis schema<br/>evergreen-candidate: true"]
        T3["Tier 3 — Output<br/>20-Output/<br/>claim-titled · standalone · never demoted"]
        MAPS["Maps ×4 types<br/>_maps/ · person · concept · domain · framework"]
        MOCS["MOCs<br/>30-MOCs/"]
        SM["system-model.yaml<br/>(opt-in per vault)<br/>nodes · edges · patterns<br/>v0.2: timescale · subtype · secondary_types"]
    end

    subgraph EXPR["Expression Vault Substrate (expression vaults only)"]
        VP["voice-profile.md<br/>style layer"]
        WP["writer-positions.md<br/>substance bedrock"]
        PI["positions-index.md<br/>harvest-loop T3 pointers"]
        AP["article-presets.md<br/>5 narrative-arc blueprints"]
        ADP["article-design-principles.md<br/>P1-P10 craft principles"]
        SMR["source-map-registry.md<br/>per-vault readiness scores"]
    end

    subgraph STATE["State — memory/ + system-state.md"]
        MEM["MEMORY.md<br/>persistent decisions · dialogue log<br/>CONSTRAINT: max 150 lines"]
        SS["session-state.md<br/>notes_since_last_audit · last_coverage_audit<br/>last_axis_survey · open_actions · recent_arcs<br/>last_system_audit_summary (v1.2.0)<br/>replaces vault-wide globbing"]
        NI["note-index.md<br/>bulk metadata cache<br/>CONSTRAINT: stale after 30 days → fallback"]
        SYS["system-state.md (cross-vault)<br/>Vault Registry · System Model Freshness<br/>User Positions · Active Tensions"]
    end

    subgraph VAULTS["Vault Instances"]
        VACC["Accumulation vaults<br/>2-zone · 3-tier · 4 styles<br/>standard genesis (Docs 1-12)"]
        VTRA["Training vaults<br/>all-synthesis · doctrine tier<br/>+ Doc 13: training substrate"]
        VEXP["Expression vaults<br/>draft → publish lifecycle<br/>+ Doc 13: expression substrate"]
    end

    %% Framework generates configuration layer via genesis
    SPINE -->|"governs change rules"| FD
    FD -->|"genesis-protocol<br/>Phase 0-1"| CONF
    VTT -->|"Doc 13 copy<br/>conditional by vault type"| EXPR
    VTT -->|"Doc 13 copy<br/>conditional"| VTRA
    FD -->|"slash-command-suite<br/>stub format"| STUBS
    UP -->|"referenced by stubs"| STUBS

    %% Dispatch chain: stub → protocol → vault-config → execution
    STUBS -->|"Step 1: read protocol path"| PROTO
    STUBS -->|"Step 2: read vault-config"| VCF
    PROTO -->|"instructions"| PARAM
    VCF -->|"parameterizes"| PARAM
    GC -->|"always loaded"| PARAM
    VC -->|"always loaded"| PARAM

    %% Expression pipeline reads its substrate
    EXPR -->|"/article-* and /co-*<br/>consume substrate"| PARAM

    %% Execution creates content and updates state
    PARAM -->|"creates"| T1
    PARAM -->|"creates"| MAPS
    PARAM -->|"updates"| MOCS
    T1 -->|"promote"| T2R
    T1 -->|"promote"| T2S
    T2R -->|"upgrade schema"| T2S
    T2S -->|"5-gate graduation check"| T3
    PARAM -.->|"opt-in:<br/>/system-build bootstrap"| SM

    %% State read/write
    PARAM -->|"updates"| SS
    PARAM -->|"appends/rebuilds"| NI
    PARAM -->|"updates<br/>(coverage-audit · dialogue Bridge)"| SYS
    SS -->|"Type C session check<br/>thresholds: 15 notes · 60 days"| EXEC
    NI -->|"bulk reads: coverage-audit<br/>axis-survey · domain-audit · positions"| EXEC
    SS -.->|"fallback if absent"| MEM
    NI -.->|"fallback: glob + rebuild"| CONTENT

    %% Harvest loop populates positions-index from published essays
    T3 -.->|"/article-promote harvest<br/>classify novel claims"| PI

    %% Cross-vault connections
    VACC -->|"Type 1<br/>knowledge → expression"| VEXP
    VACC -->|"Type 2<br/>knowledge → training"| VTRA
    VACC <-->|"Type 3 peer<br/>bidirectional"| VACC
```

**Key constraints visible in the diagram**:
- Global CLAUDE.md is capped at 100 lines — every line is paid in every session everywhere.
- vault-config.md is read fresh per command (cascade exception: chained sub-commands skip re-read).
- Tier promotion is one-way; T3 notes are never moved back.
- Protocol logic lives once in agensy; vault stubs are pure pointers.
- The expression-vault substrate is a separate layer that only expression vaults consume.
- `system-model.yaml` is opt-in per vault; `/coverage-audit` auto-fires `/system-audit` when it exists.

---

## Diagram 2 — Command Dispatch & Lifecycle

How a command goes from user invocation to completion, and how the four trigger types chain together.

```mermaid
sequenceDiagram
    participant U as User
    participant S as Stub<br/>.claude/commands/
    participant P as Protocol<br/>universal-commands/
    participant V as vault-config.md
    participant C as Content
    participant St as State

    Note over U,St: Every command invocation follows this chain
    U->>S: /command [args]
    S->>P: Read full protocol
    S->>V: Read vault-config.md
    Note over P,V: Cascade rule — tight chains<br/>(arc → update-moc → quick-check)<br/>skip the vault-config re-read
    P->>C: Execute steps → write notes/maps/reports
    P->>St: Update session-state.md
    P->>St: Append/rebuild note-index.md
    P-->>U: Output

    Note over P,C: Type A auto-chain example
    P->>P: /arc completes
    P->>P: → /quick-check (built-in Step 5)
    P->>P: → /update-moc (built-in Step 4)

    Note over P,St: Type A auto-chain v1.2.0 addition
    P->>P: /coverage-audit completes
    P->>P: → /system-audit (Step 9, if system-model.yaml exists)
```

```mermaid
graph TD
    START(["Session Start"])
    TC["Type C — read session-state.md<br/>notes_since_last_audit ≥ 15 → suggest coverage-audit<br/>last_axis_survey > 60 days → suggest axis-survey<br/>open_actions not empty → surface top item<br/>DO NOT auto-run — surface only"]

    START --> TC
    TC --> REQ["User request"]

    REQ --> ARC["/arc"]
    ARC -->|"Type A auto"| QC["/quick-check"]
    ARC -->|"Type A auto"| UM["/update-moc"]
    ARC -->|"Type B: 15+ notes accumulated"| CA["/coverage-audit"]

    CA -->|"Type A auto<br/>(if system-model.yaml)"| SA["/system-audit"]
    CA -->|"Type B: gaps found"| WN["/what-next"]
    CA -->|"Type B: gaps found"| EP["/engage-problem"]

    ARC -->|"Type B: arc complete"| DA["/domain-audit"]
    DA -->|"Type B: candidates found"| PR["/promote"]

    ARC -->|"Type B: 3+ T3 notes"| AS["/axis-survey"]
    AS -->|"Type B: underrepresented position"| ARC

    DI["/dialogue"] -->|"Type B: 30+ days old"| REV["/revisit"]

    REQ -->|"Type D: user-initiated<br/>with proactive suggestion"| TD["engage-deep · compare · synthesis<br/>dialogue · positions · question-bank<br/>system-query · system-build · system-bridge"]

    REQ -->|"Expression pipeline<br/>(sequential, per essay)"| PIPE["article-scan → article-seed<br/>→ article-outline → article-draft<br/>→ article-revise → article-critique<br/>→ article-promote"]
    REQ -->|"Companion mode<br/>(operator-initiated)"| COMP["article-companion start<br/>+ co-find · co-combine · co-suggest<br/>co-critique · co-capture"]
```

---

## Diagram 3 — State Management & Feedback Loops

Every read and write relationship between commands and the state files. Dashed edges are fallback paths. New in v1.2.0: `/coverage-audit` Step 9 auto-fires `/system-audit`; expression-vault substrate writes via `/article-promote` harvest loop and `/co-capture`.

```mermaid
flowchart LR
    subgraph WRITES["Commands — Write to State"]
        ARC_W["arc"]
        CA_W["coverage-audit"]
        AS_W["axis-survey"]
        WN_W["what-next"]
        EV_W["evergreen-note"]
        DI_W["dialogue Route 1"]
        PR_W["promote"]
        SA_W["system-audit<br/>(new v1.2.0)"]
        AP_W["article-promote<br/>harvest loop"]
        CC_W["co-capture<br/>(user-confirmed)"]
    end

    subgraph FILES["State Files"]
        SS["memory/session-state.md<br/>notes_since_last_audit<br/>last_coverage_audit · last_axis_survey<br/>last_what_next · open_actions<br/>recent_arcs · last_system_audit_summary"]
        NI["memory/note-index.md<br/>Path · Tier · Domain<br/>EC · Axis · OPs · Source · Created"]
        MEM["memory/MEMORY.md<br/>persistent knowledge<br/>dialogue log"]
        SYS["system-state.md (cross-vault)<br/>Vault Registry<br/>System Model Freshness (v1.2.0)<br/>User Positions · Active Tensions"]
        PI["positions-index.md<br/>(expression vaults only)<br/>harvest-loop T3 pointers"]
        WP["writer-positions.md<br/>(expression vaults only)<br/>user-authored bedrock"]
        VP["voice-profile.md<br/>(expression vaults only)<br/>style corpus + register notes"]
    end

    subgraph READS["Commands — Read from State"]
        TC["Type C Session Check"]
        CA_R["coverage-audit"]
        DA_R["domain-audit"]
        AS_R["axis-survey"]
        POS_R["positions"]
        SA_R["system-audit"]
        AS_SEED["article-seed Step 2.6"]
        AD_R["article-draft"]
        AR_R["article-revise Pass C"]
    end

    ARC_W -->|"increment notes_since_last_audit"| SS
    CA_W -->|"reset → 0 · update last_coverage_audit<br/>write open_actions from gap list"| SS
    CA_W -->|"update System Model Freshness<br/>write last_system_audit_summary"| SYS
    AS_W -->|"update last_axis_survey"| SS
    WN_W -->|"update last_what_next · open_actions"| SS
    SA_W -->|"update dirt level<br/>(green/yellow/red)"| SYS

    ARC_W -->|"append 8-12 rows"| NI
    CA_W -->|"full rebuild"| NI
    EV_W -->|"append 1 row"| NI
    DI_W -->|"append 1 row"| NI
    PR_W -->|"T2 → T3 tier update"| NI

    AP_W -->|"new substantive claim →<br/>new T3 + new row"| PI
    AP_W -->|"methodological claim →<br/>append section"| WP
    CC_W -->|"positions candidate"| PI
    CC_W -->|"methodological move"| WP
    CC_W -->|"voice sample"| VP

    SS -->|"read every session start"| TC
    SS -.->|"fallback: session-state absent"| MEM
    NI -->|"filter by domain"| DA_R
    NI -->|"filter by Axis"| AS_R
    NI -->|"filter by Source<br/>cross-vault"| POS_R
    NI -->|"analyze after rebuild"| CA_R
    SYS -->|"read for dirt level +<br/>cross-vault positions"| SA_R
    PI -->|"grep by topic"| AS_SEED
    WP -->|"bedrock check"| AD_R
    VP -->|"style calibration"| AD_R
    WP -->|"two-layer position check"| AR_R
    PI -->|"matched-position check"| AR_R
    NI -.->|"if absent or >30 days old<br/>fall back to glob-and-read"| WRITES
```

---

## Diagram 4 — Genesis Protocol

How a new vault is bootstrapped from scratch. Each phase depends on the prior phase's complete output. **v1.2.0 adds Doc 13** — a conditional vault-type substrate step.

```mermaid
graph TD
    P0["Phase 0 — Config Elicitation<br/>Claude asks Q0.5→Q7 in sequence<br/>Q0.5: Intellectual style preset<br/>Q1: Mission · Q2: Driving questions<br/>Q3: Engagement axis · Q4: Open problems 8-15<br/>Q5: Note tier structure · Q6: Domains 3-12<br/>Q7: Output layer (vault type determined)<br/>▶ Output: vault-config.md"]

    P1["Phase 1 — Document Generation<br/>Claude generates in dependency order:<br/>Doc 1: Folder structure<br/>Doc 2: CLAUDE.md<br/>Doc 3: note-taxonomy.md<br/>Doc 4: development-plan.md<br/>Doc 5: coverage-plan.md<br/>Doc 6: map-reference.md<br/>Doc 7: Domain primers → _maps/<br/>Doc 8: Initial MOCs → 30-MOCs/<br/>Doc 9: Stubs → .claude/commands/<br/>Doc 10: open-problems.md<br/>Doc 11: vault-config.md extensions<br/>Doc 12: memory/ initialization<br/>▶ Output: 12 universal documents"]

    P1B["Phase 1 Doc 13 (conditional, v1.2.0)<br/>Vault-Type Substrate Copy<br/>IF expression → copy vault-type-templates/expression/*<br/>(voice-profile · writer-positions · positions-index<br/>article-presets · article-design-principles<br/>source-map-registry)<br/>IF training → copy vault-type-templates/training/*<br/>(curriculum · postulates · sources-master-list)<br/>IF accumulation → skip<br/>▶ Output: vault-type substrate in vault root"]

    P2["Phase 2 — Self-Audit Initialization<br/>Run /coverage-audit as baseline test<br/>Verify: 0 notes · all primers present<br/>all MOCs present · no structural gaps<br/>▶ Output: baseline coverage-plan.md"]

    P3["Phase 3 — First Content Arc<br/>Run /arc on core-priority domain<br/>Target: most central to engagement axis<br/>Success criteria: 1 map + 8-12 T2 notes<br/>≥2 open problems referenced<br/>engagement axis field in every synthesis note<br/>≥3 cross-domain links<br/>▶ Output: calibrated framework"]

    P4["Phase 4 — Ongoing Self-Regulation<br/>Standing mechanisms replace project management:<br/>/coverage-audit every 10-15 new notes<br/>→ auto-fires /system-audit (if system-model.yaml)<br/>/what-next at session start when intent unclear<br/>/axis-survey every 2-3 months<br/>▶ Output: maintained growing vault"]

    P0 -->|"vault-config.md complete<br/>all questions answered"| P1
    P1 -->|"12 universal docs complete"| P1B
    P1B -->|"substrate copied<br/>(or skipped for accumulation)"| P2
    P2 -->|"structure validated"| P3
    P3 -->|"calibration successful"| P4

    P2 -.->|"structural errors<br/>fix before Phase 3"| P1
    P3 -.->|"schema problems<br/>fix vault-config + CLAUDE.md"| P1
```

---

## See Also

- `framework/principles/system-architecture.md` — canonical YAML manifest (source of truth for topology)
- `framework/principles/architecture-principles.md` — invariants and change-analysis protocol
- `framework/principles/system-contracts.md` — contract table (command → required vault-config keys)
- `framework/principles/framework-meta-architecture.md` — document taxonomy, stability tiers, canonicity, supersession
