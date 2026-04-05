---
type: reference
audience: claude
---
# System Contracts

Invariants, contracts, and design principles of the synthesis vault framework. This document captures what no other framework document contains: the **WHY** behind the 3-layer architecture, the **CONTRACT** between vault-config.md and universal commands, and the **RULES** for evolving the system without breaking existing vaults.

Read this before modifying any universal command protocol, adding a new vault type, or registering a pre-framework vault.

**Reading order**: `architecture-principles.md` (WHY — invariants + change protocol) → `system-contracts.md` (HOW — contract table, breaking change rules) → `system-architecture.md` (WHAT — topology diagrams + YAML manifest)

---

## 1. Why This Architecture

**3-layer loading hierarchy**: Context budget is finite. Global `~/.claude/CLAUDE.md` stays under 100 lines; vault CLAUDE.md stays under 120 lines. Vault CLAUDE.md contains ONLY vault-specific content — universal rules are not repeated. This is a hard budget constraint, not a preference.

**Parameterized runtime**: Universal command protocols are written once and execute in any vault by reading `vault-config.md` at runtime. Protocols never hardcode vault-specific values. Violating this constraint requires duplicating protocols per vault — which defeats the entire architecture.

**Stub pattern**: Vault command files are 11-line pointers to universal protocols. The protocol logic lives once in synthesis-meta. A bug fix or protocol improvement propagates automatically to all vaults.

For the complete system picture (components, relationships, propagation rules, YAML manifest): `architecture-principles.md` and `system-architecture.md`.

---

## 2. The Vault-Config Contract

Every universal command reads `vault-config.md` at runtime. **Required** keys must exist for the command to execute correctly. **Optional** keys have documented fallbacks; a missing optional key never crashes a command.

> **Style notation**: Commands reference `engagement_axis` as the abstract slot for the vault's central tension (Q3). The concrete config key varies by style: `fault_line` (adversarial), `central_dialectic` (dialectical), `central_mystery` (contemplative), `design_problem` (constructive). Read `intellectual_style.engagement_axis.config_key` at runtime to get the actual key.
>
> **Backward compatibility**: Vaults without `intellectual_style:` default to `preset: adversarial`. Their `fault_line:` key is treated as `engagement_axis`. All existing vaults work unchanged.

| Command | Required Keys | Optional Keys |
|---|---|---|
| `/arc` | `domains[]`, `intellectual_style`, `engagement_axis.positions[]`, `note_tiers.tier2`, `note_template.synthesis`, `reference_docs.map_reference`, `folder_structure.mocs` | `folder_structure.maps` (fallback: domain folder from `domains[]`) |
| `/coverage-audit` | `domains[]`, `open_problems[]`, `note_tiers`, `folder_structure.output`, `reference_docs.coverage_plan` | — |
| `/axis-survey` | `domains[]`, `intellectual_style`, `engagement_axis.statement`, `engagement_axis.positions[]`, `open_problems[]` | `folder_structure.maps` (also searched for primers) |
| `/what-next` | `domains[]`, `open_problems[]`, `reference_docs.coverage_plan`, `reference_docs.development_plan` | — |
| `/promote` | `note_tiers.tier2.graduation_rule`, `note_tiers.tier3.output_folder`, `note_tiers.tier3.type_value`, `note_template.synthesis.mandatory_sections`, `intellectual_style.engagement_field`, `folder_structure.mocs` | — |
| `/compare` | `domains[]`, `intellectual_style`, `engagement_axis.positions[]`, `open_problems[]` | — |
| `/engage-problem` | `domains[]`, `open_problems[]`, `intellectual_style`, `engagement_axis.positions[]` | `reference_docs.open_problems` (extends open_problems[]) |
| `/synthesis` | `domains[]`, `driving_questions`, `intellectual_style`, `engagement_axis`, `open_problems[]` | — |
| `/update-moc` | `domains[]`, `folder_structure.mocs` | — |
| `/evergreen-note` | `note_tiers.tier3.output_folder`, `note_tiers.tier3.type_value`, `note_tiers.tier3.graduation_rule`, `note_template.synthesis`, `intellectual_style`, `engagement_axis.positions[]`, `open_problems[]` | — |
| `/engage-deep` | `open_problems[]`, `driving_questions`, `intellectual_style`, `engagement_axis` | — |
| `/domain-audit` | `domains[]`, `note_tiers`, `note_template.synthesis.mandatory_sections`, `intellectual_style.engagement_field`, `folder_structure.output`, `reference_docs.coverage_plan` | — |
| `/quick-check` | `domains[]`, `note_template.synthesis.mandatory_sections`, `note_template.synthesis.additional_frontmatter`, `intellectual_style`, `engagement_axis.positions[]`, `open_problems[]` | `folder_structure.*` (note discovery), `note_template.synthesis.instrument_fields` (JI template), `reference_docs.open_problems` (extended problem list), `vault_type` |
| `/dialogue` | `open_problems[]`, `driving_questions`, `intellectual_style`, `engagement_axis`, `folder_structure.output`, `note_template.synthesis` | `folder_structure.mocs` (MOC update after Route 1) |
| `/positions` | None (reads across vaults by searching for `source: user-dialogue` in frontmatter) | — |
| `/revisit` | `folder_structure.output`, `open_problems[]`, `intellectual_style`, `engagement_axis` | — |
| `/question-bank` | None (reads/writes `synthesis-meta/question-bank.md` directly) | — |

**Universal required keys** (needed by ≥6 commands): `domains[]`, `open_problems[]`, `intellectual_style` (with `engagement_axis`), `note_tiers`. Every vault must define all four.

**Deprecated key**: `fault_line` (top-level) is deprecated in favor of `intellectual_style.engagement_axis`. Still supported for backward compatibility — commands detect its presence and construct an adversarial-style `intellectual_style` block from it. Migrate at your convenience.

**Verification**: When registering a new vault, confirm every required key for every command you intend to use. A missing required key fails at the step that reads it, not at invocation — making the failure harder to diagnose.

---

## 3. Design Principles for Protocol Authors

When writing a new universal command or modifying an existing one:

1. **Never hardcode vault-specific values.** Every path, slug, folder, or domain name must come from vault-config.md at runtime. A literal path string in a protocol is a bug.

2. **Check `folder_structure.*` keys before falling back to domain folder.** If `folder_structure.maps` is defined, use it. Do not assume maps live in the domain note folder.

3. **Detect flat-folder structure before walking domains.** Check if multiple domains share the same `folder` value. If yes, glob that folder once and classify notes by `domain:` frontmatter field — never walk the same folder multiple times.

4. **Verify `reference_docs.*` paths before reading.** A vault may be pre-framework or have a missing stub. If a path does not resolve, note the gap and continue — do not crash the command.

5. **Add new required keys to the contract table in this document.** The contract is only useful if it stays accurate.

6. **Test every protocol modification against all active vault types** (accumulation, training). Structural variants exist — see Section 4.

7. **Read the analysis protocol before proposing structural changes.** See `architecture-principles.md` — §7 Change Analysis Protocol gives a 7-step process for evaluating any framework modification.

8. **Run `framework-verify.py` after any structural change** to validate architectural integrity across all vaults. Run it before registering any new vault.

---

## 4. Structural Variants

Known vault structures that universal protocols must handle:

**Per-folder domains** (theoria, politeia): Each domain has a unique folder path. Walk by folder — note counts map 1:1 to domain.

**Flat-folder domains** (bellum): Multiple domains share one folder (`20-Evergreen/`). Glob once; classify by `domain:` frontmatter field. Never count the same note against multiple domains.

**Dedicated map folder** (all active vaults define `folder_structure.maps`): Maps go there, not to the domain note folder. The arc and axis-survey protocols check this key first.

**Training vault** (bellum): No reference/synthesis split — all Tier 2 notes use synthesis schema. Protocols that branch on `evergreen-candidate` should treat training vaults as all-synthesis (`evergreen_candidate: true` always).

**Pre-framework vaults**: May be missing `reference_docs` files (coverage plan, development plan). Create stubs before running commands that require them — see Section 6.

---

## 5. Breaking Change Criteria

| Change | Breaking? | Required action |
|---|---|---|
| Add a REQUIRED key to vault-config.md | Yes | Add key to all active vault-configs; update contract table |
| Add an OPTIONAL key with fallback | No | Document fallback in the protocol |
| Change a protocol's vault-config.md reads | Depends | Update contract table; verify all active vaults have the key |
| Change mandatory note frontmatter fields | Yes | Update `note_template` blocks in all active vault-configs |
| Add a new universal command | No | Add stub to all vault `.claude/commands/` directories; update contract table. **Note**: if a vault has custom commands that share names with new universals, rename the vault-specific ones (e.g., `/dialogue` → `/[vault]-dialogue`) |
| Rename a universal command | Yes | Update stubs in all vaults; update contract table |
| Use `intellectual_style.engagement_axis` instead of `fault_line` | No (backward compat shim exists) | Commands read both; construct adversarial style from `fault_line` if `intellectual_style` absent |

**2026-03-29 renames** (backward-compat aliases maintained in adversarial vaults):
- `/confront` → `/engage-deep` (universal command; adversarial vaults may keep `/confront` as a vault-specific alias)
- `/fault-line-survey` → `/axis-survey` (universal command; adversarial vaults may keep `/fault-line-survey` as alias)

---

## 6. Pre-Framework Vault Integration Checklist

When registering a vault built before the framework (before 2026-03-21 migration):

- [ ] `vault-config.md` has all 3 runtime blocks: `folder_structure`, `note_template`, `reference_docs`
- [ ] All paths in `reference_docs.*` resolve to existing files (create stubs if any are missing)
- [ ] `domains[].folder` values are accurate (flat vs per-folder structure documented)
- [ ] `folder_structure.maps` points to the correct dedicated map folder
- [ ] Run `/coverage-audit` as baseline — if it completes without error, the contract is satisfied
- [ ] Add vault to `synthesis-meta/vault-registry.md`
