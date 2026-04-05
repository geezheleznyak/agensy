# Contributing to AGENSY

AGENSY is a markdown-based framework — all protocols, templates, and schemas are `.md` files. There is no compiled code. This means a bad change can silently break vault behavior without any type error or test failure. Please read this before submitting a PR.

---

## What Can Be Contributed

| Category | Examples | Risk |
|---|---|---|
| **Documentation** | Improving docs/, fixing typos, adding examples | Low — won't affect vault behavior |
| **New vault configs** | Adding a new `vaults/[domain]-config.md` as an example | Low |
| **Bug fixes** | Correcting protocol logic, fixing broken cross-references | Medium — test thoroughly |
| **Protocol changes** | Modifying command behavior, schema fields, tier logic | High — read the contract system first |
| **New commands** | Adding a new universal command | High — requires full contract review |

---

## Before You Change a Protocol File

Protocol files in `framework/` and `framework/universal-commands/` are Claude's operating instructions. They are not documentation — they are executable. Changes here change how Claude behaves in every vault.

Before any protocol change:
1. Read `framework/system-contracts.md` — this lists the invariants the framework cannot break. If your change violates a contract, it will be rejected.
2. Read `framework/architecture-principles.md` §7 — this gives the 7-step analysis protocol for evaluating whether a change is safe.
3. Ask: does this change break any existing vault that was built with the current protocol? If yes, is the migration path documented?

---

## Submitting a Pull Request

### Required for all PRs:
- [ ] Run `python tools/framework-verify.py --verbose` and include the output in your PR description
- [ ] Describe what the change does and why it is needed
- [ ] Note which files were changed and how they affect Claude's behavior

### Required for protocol changes (framework/ or universal-commands/):
- [ ] Test the change against a real vault through the full genesis protocol (at minimum: Phase 0 + Phase 1 + `/arc` once)
- [ ] If the change affects `system-contracts.md` invariants, update that file explicitly and explain why the contract changed
- [ ] Note whether existing vaults need migration and how

### Required for new commands:
- [ ] Add the command to `framework/slash-command-suite.md`
- [ ] Add a stub file to `.claude/commands/` following the existing pattern
- [ ] Add the command to `docs/commands.md`
- [ ] Update `framework/command-lifecycle.md` with the appropriate trigger type

---

## What Will Be Rejected

- Changes that introduce absolute paths or platform-specific syntax into framework files
- Protocol changes without test evidence
- New features that duplicate existing command behavior
- Changes to vault configs that make them less useful as examples (they demonstrate production-quality vaults)
- Speculative abstractions or "improvements" that no existing vault requires

---

## Questions

Open an issue before starting any significant protocol change. It's faster to align on direction first than to review a large PR that goes the wrong way.
