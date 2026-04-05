# Compatibility

## Framework Version

**v1.0.1** — released 2026-04-04.

Version scheme:
- **Major** (v2.x.x) — breaking protocol changes (existing vaults require migration)
- **Minor** (v1.x.x) — new commands or non-breaking protocol additions
- **Patch** (v1.0.x) — documentation fixes, path corrections, typo fixes

---

## Tested Environment

| Component | Version | Notes |
|---|---|---|
| **Claude Code** | Latest (April 2026) | Reference implementation — CLAUDE.md loading, slash command resolution, and context persistence tested here |
| **Claude Model** | Sonnet 4+ recommended | Or any equivalent state-of-the-art reasoning model. Haiku-tier / weaker models not tested; synthesis depth degrades significantly. |
| **Obsidian** | v1.7+ | Wikilink resolution and frontmatter display tested on v1.7. Core Obsidian features only — no community plugins required. |
| **Python** | 3.8+ | For `tools/vault-linter.py` and `tools/framework-verify.py`. Optional. |
| **OS** | Windows 11, macOS (untested), Linux (untested) | Framework itself is OS-agnostic (markdown files). Path syntax in docs uses forward slashes. |

---

## Claude Code Behaviors This Framework Depends On

The tooling layer relies on specific Claude Code behaviors. If these change, the framework may break silently:

1. **CLAUDE.md auto-loading**: Claude Code reads `CLAUDE.md` from the working directory at session start. The framework depends on this to load vault-specific instructions.

2. **Slash command resolution**: Commands in `.claude/commands/` are resolved by Claude Code when prefixed with `/`. The framework uses stub files that point Claude to `[AGENSY_PATH]/framework/universal-commands/[command-name].md`.

3. **Context persistence**: The framework chains commands (e.g., `/arc` invokes `/update-moc` which invokes `/quick-check`). This requires Claude Code to maintain context across these invocations within a session.

4. **File read/write access**: The framework writes notes, MOCs, and updates `system-state.md` directly. Claude Code requires appropriate file permissions.

**If the framework stops working after a Claude Code update**, check whether any of these behaviors changed. Open an issue with the Claude Code version where the breakage began.

---

## Other Agentic Systems

The **protocol logic** — arc structure, synthesis schema, command protocols in `framework/universal-commands/` — is model-agnostic. Any capable agentic system on a state-of-the-art reasoning model can run the framework with manual file loading:

1. **Skip the CLAUDE.md setup** — instead, paste the contents of `agensy/CLAUDE.md` into your system prompt or session context
2. **Skip slash commands** — describe operations in plain English ("run an arc on Keynes") and manually load the relevant protocol file from `framework/universal-commands/[cmd].md`
3. **Load `vault-config.md` at session start** — this gives the system vault-specific parameters (domains, open problems, engagement axis)

The `.claude/` directory (command stubs, CLAUDE.md auto-loading) is Claude Code-specific infrastructure. The `framework/` directory is universal — it contains complete protocol logic that any system can follow.

**Minimum model requirement**: The synthesis commands require multi-step reasoning, position-taking, and cross-document synthesis. Models significantly below frontier-class capability will produce degraded output regardless of which platform they run on.

---

## Optional Claude Code Skills

The global CLAUDE.md references five Claude Code skills:

| Skill | Function |
|---|---|
| `obsidian:obsidian-markdown` | Validates Obsidian-flavored markdown syntax when writing vault files |
| `obsidian:obsidian-cli` | Enables live interaction with the Obsidian app (plugin reload, JavaScript execution, screenshots) |
| `obsidian:defuddle` | Cleaner web extraction when reading URLs — less noise than raw HTML |
| `obsidian:json-canvas` | Validates Canvas file syntax |
| `obsidian:obsidian-bases` | Validates Bases file syntax |

These are **optional**. If not installed, Claude falls back to direct file operations (Read/Write/Edit). The core framework works without any skills installed.

**What you lose without them**: `defuddle` gives noticeably cleaner web page extraction. `obsidian-cli` enables live vault interaction that is otherwise unavailable. The other three validate syntax that Claude can also check manually.

**Where to find skills**: Claude Code skills are `.md` files placed in `~/.claude/skills/`. The author's skill setup is not bundled with this repo. Search the Claude Code community or GitHub for `claude-code-skills obsidian` to find community-distributed skill packages. The framework is designed to work without them.

---

## Known Limitations

- **Model capacity**: The `/engage-deep` and `/dialogue` commands require multi-step reasoning and position-tracking. With weaker models, output quality degrades significantly.
- **Long sessions**: Very long sessions (10+ arc runs) may encounter context window limits. If this happens, start a new session — vault state is persisted in files, not in Claude's context.
- **Windows path separators**: Framework files use `[AGENSY_PATH]` placeholders with forward slashes. On Windows, Claude Code handles both separators correctly, but terminal commands may need adjustment.
- **Concurrent vault access**: Do not run Claude Code in two vaults simultaneously with the same `system-state.md`. Updates will conflict.
