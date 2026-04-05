---
type: documentation
audience: human
---

# Getting Started with AGENSY

This guide takes you from zero to a working knowledge vault in one session. Plan for 3–4 hours for your first vault. Subsequent vaults take ~1 hour once you understand the pattern.

---

## Before You Start

**What you need:**
- Claude Code installed and authenticated (requires Claude Pro or API access)
- Obsidian installed (free — obsidian.md)
- This repo cloned locally: `git clone https://github.com/geezheleznyak/agensy.git`
- Python 3 (optional — for running validation tools)

**One-time global setup (required):**

Copy the universal rules to your global Claude Code config:
1. Open `docs/global-claude-md.md` in this repo
2. Copy the block between `---BEGIN---` and `---END---`
3. Paste it into `~/.claude/CLAUDE.md` (create the file if it doesn't exist)
4. Replace `[AGENSY_PATH]` with your actual path to the `agensy/` folder

This file loads automatically in every Claude Code session across all your vaults. Without it, Claude won't know the universal framework rules.

> The global CLAUDE.md references optional Claude Code skills for Obsidian integration (`obsidian:obsidian-markdown`, `obsidian:defuddle`, etc.). These aren't required — skip if you don't have them installed; Claude falls back to direct file operations automatically. See `COMPATIBILITY.md` for details.

**What you're building:**
A vault is a domain-specific knowledge system. One vault = one intellectual domain (e.g., economics, military theory, philosophy). You can have multiple vaults; this guide builds your first one.

**The framework lives here (agensy/).** Your vault lives elsewhere — a separate folder you'll create. The two never mix.

---

## Step 1 — Decide Your Domain

Pick a domain you want to understand deeply. It should be:
- Broad enough to sustain 100+ notes (a field, not a topic)
- Something you care about genuinely — the framework creates analytical pressure, which requires real intellectual investment
- Not already a vault (check your registry if you have existing vaults)

Examples from the reference configs: political theory, military strategy, economic systems, philosophy of mind, historical analysis, essay writing.

---

## Step 2 — Open agensy/ in Claude Code

```bash
cd /path/to/agensy
claude
```

Claude Code will load the AGENSY framework instructions automatically from `CLAUDE.md`. If you're using a different agentic system, manually load `agensy/CLAUDE.md` and your vault's `vault-config.md` at session start — the protocol logic is the same.

---

## Step 3 — Run the Genesis Protocol

Type:
```
/new-vault
```

Or just tell Claude: "I want to build a new vault on [domain]." You don't need to memorize any commands — prose works just as well.

**Claude leads the elicitation.** You only need to say what domain you want. Claude asks the questions one by one, proposes options for each, and you refine or accept. The 7 questions are:

1. **What domain?** (name and scope)
2. **What are your 3 driving questions?** (the questions you want the vault to answer — open, researchable, yours)
3. **What is the central fault line?** (the core intellectual tension in this domain — the debate that structures everything else)
4. **What are the open problems?** (8–12 specific questions the field hasn't resolved)
5. **What domains within this field?** (6–10 subdomains — the vault's internal map)
6. **What does output look like?** (what are you building toward — synthesis notes, judgment notes, essays?)
7. **What are the cross-vault connections?** (how this vault connects to others you have or plan to build — Claude will propose likely bridges based on your domain; leave blank if this is your first vault)

After Q7, Claude generates:
- Your vault's folder structure
- `vault-config.md` (your answers, structured)
- `CLAUDE.md` (Claude's operating instructions for your vault)
- All domain subfolders
- Starter MOC files
- Command stubs for all universal commands

**This takes 30–60 minutes.** Claude asks follow-up questions. Be thorough.

---

## Step 4 — Open Your New Vault in Obsidian

Once the genesis protocol completes, open your new vault folder in Obsidian (File → Open vault → select the folder). You'll see the full structure Claude created.

---

## Step 5 — Run Your First Arc

Open your new vault in Claude Code:
```bash
cd /path/to/your-new-vault
claude
```

Then run:
```
/arc [subject]
```

Or say: "Let's do a full arc on [subject]." Either way Claude runs the same protocol.

Pick a subject from one of your open problems or domains. Claude will:
1. Ask you to provide sources or context
2. Generate 8–12 synthesis notes (Tier 2)
3. Update the relevant MOC
4. Run a quick-check validation

This is the core loop: `/arc` → review notes → `/coverage-audit` → `/what-next` → repeat.

---

## Step 6 — Understand the Command Lifecycle

After your first arc, run:
```
/coverage-audit
```

This audits your domain coverage, identifies gaps, and recommends where to build next. It also updates the global state file (`agensy/system-state.md`) with your vault's note count.

From here, the vault is self-directing. Use `/what-next` any time you're not sure where to work.

---

## The Core Loop (Ongoing)

```
/arc [subject]          ← build 8–12 notes on a subject
/coverage-audit         ← diagnose gaps across all domains
/axis-survey            ← see where your notes sit on the engagement axis
/what-next              ← get a prioritized recommendation for next arc
/dialogue [topic]       ← engage the vault as a thinking partner
```

Run `/coverage-audit` after every 3–4 arcs. Run `/axis-survey` monthly. Use `/dialogue` when you want to stress-test a position or explore a question you can't resolve with notes alone.

---

## Where to Go Next

- **[concepts.md](concepts.md)** — understand the key terms (tier, zone, engagement axis, arc, MOC)
- **[commands.md](commands.md)** — full reference for all 16 commands
- **[tools.md](tools.md)** — run the validation scripts to check note quality
- **`framework/genesis-protocol.md`** — the full genesis protocol if you want to understand what Claude is doing in Step 3
