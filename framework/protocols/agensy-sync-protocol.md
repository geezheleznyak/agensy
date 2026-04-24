---
created: 2026-04-24
updated: 2026-04-24
type: reference
---

# Agensy Sync Protocol

Procedure and policy for propagating framework changes from `synthesis-meta/` (the user's working directory — never published) to `agensy/` (the public open-source distribution at `C:\Users\grego\obsidian_repos\agensy\`, GitHub `geezheleznyak/agensy`).

**Direction is one-way: meta → agensy, always.** Never edit agensy directly for framework work.

Sync is **manually triggered with user approval**, not automatic. Claude proactively surfaces sync implications at the end of framework work (see §Triggers). The user confirms, reviews the proposed diff, and approves the write + version bump + CHANGELOG entry.

**Reading order for context**: `architecture-principles.md` (what invariants must survive the sync) → this file (how to sync) → `agensy/CHANGELOG.md` (prior sync records to match entry style).

---

## §1 — What Gets Synced

### Copy 1:1 (framework source)

Every file under these meta paths maps directly to the same relative path under `agensy/`:

| Meta path | Agensy path | Notes |
|---|---|---|
| `framework/principles/architecture-principles.md` | `framework/principles/architecture-principles.md` | |
| `framework/principles/system-contracts.md` | `framework/principles/system-contracts.md` | |
| `framework/principles/system-architecture.md` | `framework/principles/system-architecture.md` | |
| `framework/principles/framework-meta-architecture.md` | `framework/principles/framework-meta-architecture.md` | |
| `framework/principles/learner-layer-architecture.md` | `framework/principles/learner-layer-architecture.md` | Added v2.1.0 |
| `framework/slash-command-suite.md` | `framework/slash-command-suite.md` | |
| `framework/protocols/command-lifecycle.md` | `framework/protocols/command-lifecycle.md` | |
| `framework/protocols/genesis-protocol.md` | `framework/protocols/genesis-protocol.md` | |
| `framework/protocols/inter-vault-protocol.md` | `framework/protocols/inter-vault-protocol.md` | |
| `framework/protocols/agensy-sync-protocol.md` | `framework/protocols/agensy-sync-protocol.md` | **this file** — included so agensy users can see the sync policy |
| `framework/templates/vault-config-schema.md` | `framework/templates/vault-config-schema.md` | |
| `framework/templates/claude-md-template.md` | `framework/templates/claude-md-template.md` | |
| `framework/templates/note-tier-template.md` | `framework/templates/note-tier-template.md` | |
| `framework/templates/map-type-template.md` | `framework/templates/map-type-template.md` | |
| `framework/templates/learner-profile-template.md` | `framework/templates/learner-profile-template.md` | Added v2.1.0 |
| `framework/system-model/primitives.md` | `framework/system-model/primitives.md` | |
| `framework/system-model/system-model-schema.yaml` | `framework/system-model/system-model-schema.yaml` | |
| `framework/system-model/system-model-architecture.md` | `framework/system-model/system-model-architecture.md` | |
| `framework/templates/map-to-article-extraction.md` | `framework/templates/map-to-article-extraction.md` | |
| `framework/universal-commands/*.md` | `framework/universal-commands/*.md` | All 34 protocol files + 2 alias files, 1:1 |
| `tools/framework-verify.py` | `tools/framework-verify.py` | Apply path-sub + portability transform (§3) |
| `tools/vault-linter.py` | `tools/vault-linter.py` | Apply path-sub + portability transform (§3) |
| `tools/baselines/*` | `tools/baselines/*` | Anonymize any identifying data first |

### Copy with transformation (sanitize before sync)

| Meta path | Agensy path | Transformation |
|---|---|---|
| `vault-registry.md` | `vault-registry.md` | Replace real vault names (omega, kratos, oikos, belli, cogitationis, clio) with Latin equivalents (theoria, politeia, oeconomia, bellum, logos, historia); replace `C:\Users\grego\obsidian_repos\...` paths with `/path/to/...`; preserve table structure |
| `system-state.md` | `system-state.md` | Zero out user-specific note counts + audit dates + dirt levels; keep the table schema and column semantics as an empty template |
| `cross-vault-bridges.md` | `cross-vault-bridges.md` | Anonymize vault names (same Latin mapping); keep bridge schema + examples; remove any user-specific T3 references |
| `vaults/[vault]-config.md` (×6) | `vaults/[latin-name]-config.md` (×6) | Rename files (belli→bellum, clio→historia, cogitationis→logos, kratos→politeia, oikos→oeconomia, omega→theoria); rewrite absolute paths to `/path/to/...` placeholders; generalize Q1 mission wording to remove identifying specifics |
| `question-bank.md` | `question-bank.md` | Replace user's actual questions with template header + format example; keep the schema |

### Never synced (meta-only; not shipped in agensy)

| Path | Reason |
|---|---|
| `memory/` | Private working memory; gitignored in agensy per `.gitignore` |
| `learner/` | Private user-as-learner data — profile, trajectory, interests-register, archives. User-specific intellectual self-portrait; structurally parallel to `memory/`. The framework documents that DECLARE this layer (`learner-layer-architecture.md`, `learner-profile-template.md`) DO sync; the user's actual learner data does NOT. Added v2.1.0 |
| `framework/system-model/primitives-experiment.md` | User's Phase 0 experimental record — specific to user's vaults. *Optional*: ship a redacted version in `docs/examples/` as a worked methodology example (current agensy does not include it) |
| `framework/closures/phase-2-closure-kratos.md` | User's phase closure record — specific to user's rollout. Keep meta-only, or ship to `docs/examples/` as decision-record template |
| `framework/closures/phase-4-closure.md` | Same |
| `framework/closures/phase-5-closure.md` | Same |
| `.obsidian/` | Obsidian app config; per-machine |
| `.claude/` | Local Claude settings |
| Any file under `tools/baselines/` that references real vault paths or user notes | Sanitize before sync or exclude |

### Agensy-only (exists in agensy, NOT in meta)

These files live only in agensy and are never imported from meta:

| Agensy path | Role |
|---|---|
| `README.md` | Public project intro; written for agensy |
| `LICENSE` | Open-source license |
| `CHANGELOG.md` | Semantic-versioning release log; updated on each sync |
| `CONTRIBUTING.md` | Contribution guidelines |
| `COMPATIBILITY.md` | Compatibility matrix |
| `docs/` | Public documentation, quickstart, examples |
| `CLAUDE.md` | Agensy-specific; mentions agensy name + public framing (distinct from meta's CLAUDE.md which references user's own working practices). **Do not overwrite from meta.** Per feedback record `feedback_synthesis-meta-vs-agensy.md`, path differences are intentional |

---

## §2 — Triggers: When to Sync

Claude surfaces a sync proposal at the end of framework work when **any** of these trigger conditions holds. The user approves, reviews the diff, and authorizes the write.

### Trigger A — New universal command added

A new protocol file appears under `framework/universal-commands/` in meta. Sync implications: copy protocol file; update `slash-command-suite.md` count header; update `system-contracts.md §2` contract table; update `system-architecture.md` YAML manifest; update `framework-verify.py COMMAND_REQUIRED_KEYS` dict. Version bump: MINOR.

### Trigger B — Framework doc substantively updated

Material change to any of the architectural-spine docs (`architecture-principles.md`, `system-contracts.md`, `system-architecture.md`), orchestration docs (`slash-command-suite.md`, `command-lifecycle.md`, `genesis-protocol.md`, `inter-vault-protocol.md`), or any template. Version bump: MINOR if additive; MAJOR if breaking.

### Trigger C — Schema version bump

`framework/system-model/system-model-schema.yaml` version changes (e.g., v0.1 → v0.2). Sync both the schema and `primitives.md` + `system-model-architecture.md` together — they travel as a set. Version bump: MINOR (additive schema) or MAJOR (breaking).

### Trigger D — Protocol bugfix users would need

Correctness fix to any command protocol that agensy users would encounter. Version bump: PATCH.

### Trigger E — Tool fix or new check

New or modified check in `framework-verify.py` or `vault-linter.py`. Version bump: PATCH (adds check) or MINOR (new category).

### Trigger F — Vault-registry structural shift

Meta `vault-registry.md` changes in a way that affects the agensy template (new framework-doc row, new connection type, etc.). Sync the structural change; do NOT sync vault-identity changes (those are user-specific). Version bump: PATCH.

### NOT a trigger

- User adds/edits their own vault content — the framework didn't change; no sync needed.
- `memory/` changes — gitignored.
- `system-state.md` operational updates (note counts, audit dates) — user-specific dynamic state.
- Closure records (phase-*-closure.md), experiment records — decision-records specific to user's rollout.
- `vaults/[vault]-config.md` edits that are about the user's particular vault (rather than testing a framework change).

---

## §3 — How to Sync (Execution)

### Step 1 — Diff meta vs. agensy

Claude lists every file that would change under §1 "Copy 1:1" and "Copy with transformation". For each: show full-file or hunk-level diff. Do not execute writes yet.

### Step 2 — Apply path substitutions

For every file being copied, run these substitutions before writing to agensy:

| Pattern | Replacement |
|---|---|
| `C:\Users\grego\obsidian_repos\synthesis-meta` | `agensy` (path-root) — or relative/templated form if that's the convention on that line |
| `C:\Users\grego\obsidian_repos\sythesis_omega` | `/path/to/synthesis_theoria` |
| `C:\Users\grego\obsidian_repos\synthesis_kratos` | `/path/to/synthesis_politeia` |
| `C:\Users\grego\obsidian_repos\synthesis_oikos` | `/path/to/synthesis_oeconomia` |
| `C:\Users\grego\obsidian_repos\synthesis_belli` | `/path/to/synthesis_bellum` |
| `C:\Users\grego\obsidian_repos\synthesis_clio` | `/path/to/synthesis_historia` |
| `C:\Users\grego\obsidian_repos\synthesis_cogitationis` | `/path/to/synthesis_logos` |
| Vault name `synthesis_omega` / `omega` | `synthesis_theoria` / `theoria` |
| Vault name `synthesis_kratos` / `kratos` | `synthesis_politeia` / `politeia` |
| Vault name `synthesis_oikos` / `oikos` | `synthesis_oeconomia` / `oeconomia` |
| Vault name `synthesis_belli` / `belli` | `synthesis_bellum` / `bellum` |
| Vault name `synthesis_clio` / `clio` | `synthesis_historia` / `historia` |
| Vault name `synthesis_cogitationis` / `cogitationis` | `synthesis_logos` / `logos` |
| Meta-name `synthesis-meta` (when referring to the framework repo) | `agensy` |

The user's email, git author name, and absolute machine paths should never land in agensy. A grep on the agensy diff for `grego` is a final sanity check before commit.

### Step 3 — Write

Apply edits file-by-file under `agensy/`. For file-renames (`vaults/omega-config.md` → `vaults/theoria-config.md`), delete the old agensy file before writing the new one. For new files (e.g., this sync-protocol doc on first sync), create directly.

### Step 4 — Version bump + CHANGELOG entry

Update `agensy/` version per SemVer:
- **MAJOR** — breaking change to any universal protocol contract, schema backward incompatibility, required-key addition that existing vaults lack.
- **MINOR** — additive change (new command, new schema field, new template block, new framework doc).
- **PATCH** — bugfix, docs polish, tooling-only change.

Compose the CHANGELOG entry matching the existing style in `agensy/CHANGELOG.md`:
- Heading `## [X.Y.Z] — YYYY-MM-DD`
- Subsections as appropriate: `Added`, `Changed`, `Fixed`, `Removed`, `Notes`
- Each entry names the specific file changed (not just "updated framework") so `git log` is traceable
- Backward-compatibility note at the bottom when relevant

Per memory (`feedback_agensy-version-bump.md`): **propose the version bump + CHANGELOG entry and await user approval BEFORE committing agensy changes.** Don't commit a sync without the CHANGELOG line.

### Step 5 — Update agensy-side metadata

If §1 touches files referenced in `agensy/CLAUDE.md` or `agensy/README.md` (count lines, file listings in the Vault Structure block), update those too. The agensy CLAUDE.md currently lists `21 universal` — this becomes stale on every trigger-A sync. Fix it.

### Step 6 — Verify on the agensy side

From the agensy directory, run `python tools/framework-verify.py` to confirm architectural integrity. Any new FAIL or WARN introduced by the sync is a regression — fix before commit.

### Step 7 — Commit and push (user-approved)

Commit message format:
```
release vX.Y.Z — [one-line summary of what changed]

- [file 1]: [change]
- [file 2]: [change]
- ...
```

Never add Co-Authored-By trailers (per user's global CLAUDE.md). Push to origin only after the user explicitly approves.

---

## §4 — Why This Exists

Three failure modes this protocol prevents:

1. **Silent drift** — framework evolves in meta; agensy lags without anyone noticing; public users get stale documentation or broken verify runs.
2. **Personal-information leakage** — user's machine paths, email, vault names, or private notes accidentally land in a public git history. Path substitutions in §3 block this; the `grep grego` final check catches misses.
3. **Version-history rot** — unsynced framework changes mean CHANGELOG stops reflecting what's actually in the code. Users who follow release notes end up with a broken mental model.

The three failure modes compound. The protocol keeps them isolated: meta is the single source of truth; agensy is the sanitized public mirror; CHANGELOG is the ledger of what crossed the boundary.

---

## §5 — Invariants

These hold across every sync (never broken, even for "just a small fix"):

1. **Meta → agensy is one-way.** No sync ever runs in the reverse direction.
2. **Path substitutions always apply.** A sync that omits them is a leak — refuse to write.
3. **CHANGELOG entry precedes commit.** No silent releases.
4. **User approves the diff.** This is a public directory; writes are gated.
5. **agensy CLAUDE.md and README.md are not overwritten from meta.** They are independent documents with their own audience.
6. **Agensy must remain runnable.** After sync, `framework-verify.py` from agensy root must succeed with 0 FAIL.

---

## §6 — Known Drift Points (check at each sync)

These are places where meta and agensy diverge and require attention:

- `agensy/CLAUDE.md` command count (currently says "21 universal") — stale after any Trigger-A sync. Manual update required.
- `agensy/framework/slash-command-suite.md` command count — same. Meta's count is now "34 protocol files + 2 backward-compat aliases".
- `agensy/tools/framework-verify.py COMMAND_REQUIRED_KEYS` dict — must match the version in meta (just updated 2026-04-24).
- Vault-specific naming in `agensy/vault-registry.md`, `agensy/vaults/*-config.md`, `agensy/cross-vault-bridges.md` — must stay anonymized (Latin names) even if meta adds a new vault.
- `agensy/system-state.md` — should remain a blank template; never import user's live counts.

---

## See Also

- `agensy/CHANGELOG.md` — release history; match its entry style.
- `agensy/COMPATIBILITY.md` — matrix of what works with what.
- Memory: `agensy_distribution.md` · `feedback_synthesis-meta-vs-agensy.md` · `feedback_agensy-version-bump.md`.
- `architecture-principles.md §4 How Changes Propagate` — the internal propagation table that governs changes within meta (and by extension, what will need to sync).
