# AGENSY — Agentic Generative Synthesis Framework

> **Synthesize what you learn. Build understanding that compounds.**

AGENSY is a framework for building knowledge vaults that force synthesis. Most tools help you capture and recall. This one makes you learn — requiring you to connect ideas, take positions, and follow implications across domains. Notes build on notes. Vaults build on vaults. Over time, you're not accumulating facts; you're building understanding that actually grows.

Knowledge compounds the same way the universe does — each insight opening onto others, each connection reframing what you thought you knew. Understanding isn't a collection; it's a structure. AGENSY gives you the infrastructure to build that structure deliberately: connections made explicit, positions tracked, synthesis that accumulates rather than decays.

**Built for**: anyone learning seriously across multiple domains — not to collect more, but to understand more deeply.

---

## The Problem It Solves

- **"I read a lot but nothing sticks or connects"** — the synthesis schema forces active processing; the engagement axis forces position-taking on every note
- **"My notes graveyard — hundreds of files, no synthesis"** — the tier structure + MOCs + coverage audits surface what's there and what's missing
- **"AI gives me summaries, not synthesis"** — `/dialogue` and the engagement field mandate a position, not a description
- **"I work across domains but the connections don't stick"** — cross-vault bridges make domain overlaps explicit and searchable
- **"I keep rebuilding the same structure for every project"** — the genesis protocol gives any new domain a complete vault in one session

---

## Who This Is For

**Will get full value:**
- Anyone building serious domain expertise across multiple fields — not to remember more, but to think better
- Writers and thinkers who want AI as a genuine thinking partner, not a search engine
- People who find Obsidian vaults turn into graveyards without something forcing synthesis

**Will get partial value:**
- Students or researchers doing structured domain coverage
- Anyone working cross-discipline where connecting ideas is the main challenge

**Will get the least value:**
- People looking for a productivity system (PARA, GTD) or simple quick-capture
- Anyone who wants a basic Zettelkasten without synthesis pressure

---

## Prerequisites

| Requirement | Details |
|---|---|
| **Claude Code** | Reference implementation — designed and tested for Claude Code. The protocol logic is model-agnostic; any capable agentic system on a state-of-the-art reasoning model can run it with manual file loading. See COMPATIBILITY.md. |
| **Obsidian** | Required — free. Download at obsidian.md |
| **Python 3** | Optional — needed to run `tools/vault-linter.py` and `tools/framework-verify.py` |
| **Time** | The genesis protocol takes one focused session (~3 hours) — most of it is a 7-question conversation with Claude about your domain, which is itself a useful thinking exercise. Each subsequent vault: ~1 hour. |

> This framework is designed for **Claude Sonnet or above** — or any equivalent state-of-the-art reasoning model. Weaker models are not tested and may produce insufficient synthesis depth.

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/geezheleznyak/agensy.git

# 2. Open agensy/ as an Obsidian vault

# 3. Open agensy/ in Claude Code and run:
# /new-vault
# (Or in any capable agentic system: load CLAUDE.md manually and describe what you want)
```

Then read **[docs/getting-started.md](docs/getting-started.md)** for the full first-vault walkthrough.

---

## Key Features

### 1. Genesis Protocol
Answer 7 questions. Claude builds your entire vault structure in one session — folders, templates, MOCs, coverage plans, command stubs, opening notes. No setup paralysis. A domain you know nothing about becomes a structured knowledge system ready for your first arc.

### 2. Engagement Axis
Every vault has a central intellectual tension. Every synthesis note must take a position on it. This makes passive summarizing structurally impossible — the schema enforces analytical pressure on every single note. Comfortable confirmation is not analysis.

### 3. Self-Regulating Command Lifecycle
20 canonical commands that chain: `/arc` accumulates notes → `/coverage-audit` diagnoses gaps → `/axis-survey` tracks intellectual distribution → `/what-next` recommends next action. The vault tells you what to build next. You never have to decide where to start.

Slash commands are shorthand — you never have to memorize them. Describe any operation in plain English and Claude runs the protocol. `/arc Keynes` and "let's build an arc on Keynes" are equivalent.

### 4. Cross-Vault Architecture
Multiple vaults (economics, politics, history, philosophy, military theory) operate simultaneously with defined bridge domains. Insights from one vault inform others. The `/dialogue` command runs in `Bridge` mode across vault boundaries, and user positions are tracked in a shared state file.

### 5. Living Dialogue
`/dialogue` turns the vault into a thinking partner. Your positions are tracked, challenged against existing notes, and can generate new synthesis notes directly from the conversation. Not retrieval — genuine intellectual friction.

### 6. Optional System Model Layer
Each vault can opt in to a machine-readable structural ontology (`system-model.yaml`) declaring its actors, states, flows, constraints, and the dynamical patterns — feedback, threshold, reflexivity, path-dependence — they instantiate. Four commands operate on it: `/system-query` (read), `/system-audit` (drift), `/system-build` (write), `/system-bridge` (cross-vault binding reconciliation). This is what lets an agent reason about a vault's domain *shape* without reading every note, and lets cross-vault queries find structurally matching patterns across domains.

---

## Architecture Overview

```
Your vault (e.g., synthesis_economics/)
│
├── vault-config.md          ← your answers to the 7 founding questions
├── CLAUDE.md                ← Claude's operating instructions (vault-specific)
├── 00-Inbox/                ← raw captures
├── 20-Evergreen/            ← synthesis notes (T2 and T3)
│   ├── domain-name/         ← one folder per domain
│   └── ...
├── 30-MOCs/                 ← maps of content (orientation layer)
└── memory/                  ← cross-session memory (MEMORY.md + topic files)

agensy/ (this repo — framework vault)
│
├── framework/               ← Claude-facing protocol files
│   ├── genesis-protocol.md  ← the 7-question vault bootstrapping procedure
│   ├── universal-commands/  ← 20 command protocols (read by Claude at runtime)
│   └── ...
├── vaults/                  ← config extracts for each registered vault
├── tools/                   ← Python validation scripts
└── docs/                    ← human-readable documentation (start here)
```

---

## Repository Structure

```
agensy/
  README.md                  ← you are here
  LICENSE                    ← MIT
  CONTRIBUTING.md            ← how to contribute
  COMPATIBILITY.md           ← tested versions and dependencies
  CLAUDE.md                  ← Claude's instructions (if you're human, read README instead)
  vault-registry.md          ← registry of all active vaults
  system-state.md            ← dynamic cross-vault state
  cross-vault-bridges.md     ← cross-vault connection rules and bridge domains
  question-bank.md           ← persistent cross-vault question tracking
  docs/
    getting-started.md       ← first vault walkthrough (start here)
    concepts.md              ← glossary of key terms
    commands.md              ← all 20 commands explained
    tools.md                 ← validation scripts reference
  framework/
    genesis-protocol.md      ← 5-phase vault bootstrapping procedure
    vault-config-schema.md   ← vault configuration template
    claude-md-template.md    ← CLAUDE.md template
    slash-command-suite.md   ← command index
    architecture-principles.md ← WHY — design rationale and invariants
    system-contracts.md      ← HOW — architectural contracts and design principles
    system-architecture.md   ← WHAT — system diagrams and YAML manifest
    framework-meta-architecture.md ← META — framework-as-system-of-documents
    inter-vault-protocol.md  ← cross-vault connection rules
    command-lifecycle.md     ← when to fire each command
    map-to-article-extraction.md ← schema for /article-* expression pipeline
    system-model-schema.yaml ← v0.2 schema for per-vault system-model.yaml
    system-model-architecture.md ← design rationale for the System Model Layer
    primitives.md            ← three-layer primitive vocabulary (nodes/edges/patterns)
    universal-commands/      ← 34 command protocol files + 2 backward-compat aliases
  vaults/
    theoria-config.md        ← example: philosophy + metaphysics vault config
    politeia-config.md       ← example: political theory vault config
    oeconomia-config.md      ← example: economic systems vault config
    bellum-config.md         ← example: military theory vault config
    historia-config.md       ← example: historical dynamics vault config
    logos-config.md          ← example: expression (essay) vault config
  tools/
    vault-linter.py          ← note schema validation
    framework-verify.py      ← framework integrity checks
```

---

## The Vault Configs Are Illustrative

The configs in `vaults/` are based on production vault configurations built using the genesis protocol across six domains: philosophy + metaphysics, political theory, economic systems, military theory, historical dynamics, and essay writing. They show what the framework produces across real domains. Use them as reference when building your own.

---

## Built With (and For) Claude

Every file in this repository — framework protocols, command suites, template documents, this README — was generated through synthesis sessions with Claude. AGENSY is a meta-example of its own method: the framework was built by running synthesis on the problem of building synthesis frameworks.

This matters for two reasons: (1) it demonstrates the methodology works — the framework itself was built by the same process it teaches; (2) it's honest. If you use this, you are building on AI-generated infrastructure. The ideas are ours; the articulation was collaborative.

---

## License

MIT — see [LICENSE](LICENSE).
