---
description: Post-arc validation — mechanical checks + quality assessment on recent notes
type: universal-protocol
audience: claude
---

# /quick-check [scope]

Validate recently created notes for mechanical compliance and synthesis quality. The linter catches structural failures automatically; quick-check catches the failures only Claude can assess — definitional openings, generic tensions, vague threats.

**[scope]** options:
- `last-arc` (default) — all notes from the most recent arc (traced via the latest map's "Atomic Notes" list)
- `last-N` — e.g., `last-5`, notes by most recent `created:` date
- `today` — all notes with `created:` matching today's date
- `[note-path]` — single note, absolute or vault-relative path

**Runtime**: Read `vault-config.md` from the vault root before executing. Extract:
- `domains[]` — slug, label, folder, evergreen_candidate defaults (for note discovery and domain routing)
- `note_template.synthesis.mandatory_sections` — required section headers for synthesis notes
- `note_template.synthesis.additional_frontmatter` — required frontmatter fields for synthesis notes
- `intellectual_style` — engagement_axis (config_key, positions[]) and engagement_field (name); use for M04/M07/M08/Q03/Q04
- **Backward compat**: If `intellectual_style:` absent, read `fault_line.positions[]` directly (config_key = `fault_line`)
- `open_problems[]` — valid open problem IDs (or load from `reference_docs.open_problems` if defined)
- `folder_structure.*` — note discovery paths (output folder, maps folder, MOC folder)
- `vault_type` — `accumulation` | `training` (affects evergreen-candidate logic)

**Cascade context**: If invoked as part of a chain (e.g., from `/arc` Step 5), vault-config.md is already in context — skip the re-read above. Still read the individual target notes — their content must be fresh for M11 (wikilink resolution) and quality checks. If invoked standalone, always read vault-config.md fresh.

---

## Step 0 — Run Linter (Pre-compute Mechanical Results)

Before any Claude-mediated checks, run the vault linter on the target set. This pre-computes M01–M12 so Claude does not redundantly re-inspect every field manually.

**Command**:
```bash
python "[AGENSY_PATH]/tools\vault-linter.py" "<vault-root>" --category note --recent 20
```

Determine `<vault-root>` from vault-config.md location (the directory containing vault-config.md).

**Using linter output**:
- Map each linter failure code to the corresponding M-check in Step 2
- Mark M-checks as FAIL/PASS based on linter output — do not re-inspect fields the linter already verified
- If the linter is unavailable (Python not found, script missing): skip Step 0 and run M01–M12 manually in Step 2

**Do not** reproduce the full linter report verbatim in the quick-check output. Extract only the failures relevant to target notes and carry them forward.

---

## Step 1 — Identify Target Notes

**If scope = `last-arc`**:
1. Find the most recently created map file (by `created:` frontmatter date, or filename timestamp if dated). Check `folder_structure.maps` first; fall back to domain folders.
2. Extract the "Atomic Notes to Generate" or "Atomic Notes" list from the map's Judgment Instrument section.
3. For each listed note title, search the vault for a matching `.md` file (exact stem match or YYYYMMDDHHMM prefix).
4. Collect all resolved notes as the target set. Note any listed titles that did not resolve — these are arc gaps (report in Step 5).

**If scope = `last-N`**:
1. Walk all note-bearing folders (from `domains[].folder` values, deduplicated for flat-folder vaults).
2. Sort by `created:` frontmatter date descending.
3. Take the first N notes.

**If scope = `today`**:
1. Same walk as `last-N`; filter to `created:` == today's date (read from system or use session date).

**If scope = `[note-path]`**:
1. Resolve the path. If relative, prepend vault root.
2. Target set = that single note.

**Training vault handling** (bellum): All Tier 2 notes use synthesis schema regardless of `evergreen-candidate`. Treat every discovered note as synthesis-schema for all checks below.

---

## Step 2 — Mechanical Checks

Run per target note. These replicate the linter's most critical Category A checks — use for fast in-session validation without invoking the linter binary. Mark each **PASS** / **FAIL** / **WARN**.

| Code | Check | Condition |
|---|---|---|
| M01 | Frontmatter well-formed | `---` delimiters present; YAML parseable |
| M02 | Required base fields | `type`, `domain`, `created`, `updated`, `source`, `aliases` all present |
| M03 | Synthesis additional frontmatter | Fields from `note_template.synthesis.additional_frontmatter` all present (synthesis notes only) |
| M04 | Engagement axis value valid | Value of `[engagement_axis.config_key]` frontmatter field is one of `engagement_axis.positions[]` (synthesis notes only) |
| M05 | Open problem IDs valid | All IDs in `open_problems`/`open_challenges` frontmatter exist in `open_problems[]` |
| M06 | Mandatory sections present | All headers from `note_template.synthesis.mandatory_sections` exist in body |
| M07 | Synthesis instrument sub-fields | Correct template fields present — read vault-config.md `note_template.synthesis.instrument_fields`; engagement field label is `intellectual_style.engagement_field.name` (Threatens / Complicates / Transforms / Constrains) |
| M08 | Engagement field entry non-empty | `[engagement_field.name]:` line exists and has content beyond the colon; if escape-valve pattern ("No genuine [field] — [justification]"), flag as "escape valve used" |
| M09 | Open Questions problem reference | Open Questions section contains "Open Problem N" or "Open Challenge N" pattern (synthesis notes only) |
| M10 | See Also wikilink count | 4–8 wikilinks in See Also section |
| M11 | Wikilinks resolve | All `[[wikilink]]` targets exist as `.md` files in the vault — **highest priority**, catches hallucinated links |
| M12 | Schema-structure mismatch | `evergreen-candidate: true` but missing ≥2 mandatory synthesis sections → flag as "synthesis-tagged, reference-format" |

**On any FAIL**: Record the specific field, section, or link that failed. Do not abbreviate — the action item must be actionable without re-reading the note.

---

## Step 3 — Quality Assessment

Claude-only checks. These cannot be mechanized reliably because they require semantic judgment. Run per target note for synthesis notes only. Mark each **PASS** / **WARN** / **FAIL**.

| Code | Check | What PASS looks like | Common failure |
|---|---|---|---|
| Q01 | Opening paragraph: structural problem vs definition | First sentence names a *problem, failure, or historical puzzle* that forced the concept to exist | "X is a concept that..." or "X refers to..." — definitional, not problem-led |
| Q02 | Atomicity: one idea or composite | Note covers a single discrete concept; no sub-concept needs its own section to explain the main one | Note tries to cover a theory + its three phases + critiques — should be 2–3 notes |
| Q03 | Internal Tensions: style-appropriate grounding | Each tension is grounded concretely per the vault's style (adversarial: named exploiter + move; dialectical: boundary condition + demonstration; contemplative: applicability limit + phenomenon; constructive: failure mode + trigger) — read `intellectual_style.internal_tensions.format` | "Some critics argue..." or abstract tension with no concrete grounding |
| Q04 | Synthesis instrument: specific engagement or vague gesture | `[engagement_field.name]` names a specific assumption, prior understanding, perception, or tradeoff the project depends on — one that would need revision if this concept is true | "Challenges conventional thinking" or "complicates the picture" — no specific stake; or escape valve at Tier 3 |
| Q05 | Standalone: comprehensible without vault context | A reader without vault access understands the note; no assumed knowledge of other notes | "As we saw in [[X]]..." or concepts named but not briefly defined for context |
| Q06 | Title: claim vs concept label | Title states an insight or proposition (verb present or implied) | "X's Theory of Y" or "Y Mechanism" — names the concept without making a claim |

**Severity guidance**:
- Q01 FAIL and Q03 FAIL are the most common real failures — treat as mandatory fixes before promotion
- Q04 FAIL signals the note is not yet project-facing — flag for revision
- Q02 WARN is acceptable at Tier 2 if splitting would leave one note near-empty
- Q05/Q06 WARN is acceptable at Tier 2; FAIL blocks Tier 3 promotion

---

## Step 4 — Report

Output one block per note, then a summary line.

**Per-note format**:
```
[NOTE TITLE]
  Mechanical: M01 PASS | M02 PASS | M03 FAIL (missing: [config_key], open_problems) | M11 FAIL ([[broken-link]] not found) | ...
  Quality:    Q01 FAIL (opens with definition: "X is a concept...") | Q03 WARN (no named exploiter) | Q04 PASS | ...
  Action:     [Specific fix 1] / [Specific fix 2]
  Status:     READY | NEEDS REVISION | BLOCKED
```

**Status logic**:
- `READY` — all mechanical PASS + Q01/Q03/Q04 PASS (or WARN only)
- `NEEDS REVISION` — ≥1 mechanical FAIL or Q01/Q03/Q04 FAIL
- `BLOCKED` — M11 FAIL (broken wikilink) or M12 FAIL (schema mismatch) — these block any future use of the note

**Summary line** (always last):
```
N checked | M mechanical failures | K quality issues | P promotion-ready (READY + no Q05/Q06 FAIL)
```

---

## Step 5 — Arc Integrity (scope = last-arc only)

Run after per-note checks. Assesses the arc as a whole — not individual note quality.

**Checks**:

| Code | Check | What to verify |
|---|---|---|
| I01 | Arc coverage | Every title in the map's "Atomic Notes" list → resolved to an actual note. List any unresolved titles as arc gaps. |
| I02 | Source consistency | Every arc note's `source:` frontmatter references the arc map (or the source book/document). No orphaned notes (notes with no source linking back to the arc). |
| I03 | Domain folder placement | Every arc note lives in the correct folder for its `domain:` frontmatter field (from `domains[].folder` in vault-config.md). |
| I04 | MOC update status | Check the MOC for each arc domain: does it have a `updated:` date ≥ the latest arc note's `created:` date? If not, flag as "MOC needs update." |
| I05 | Engagement axis distribution | What is the engagement axis distribution across arc notes (using `engagement_axis.config_key` field)? Flag if all notes share the same position — likely a coverage gap, not vault reality. |

**Arc integrity report format**:
```
Arc integrity: [MAP NAME]
  I01 Coverage:  12/12 titles resolved | 0 arc gaps
  I02 Sources:   All notes source the arc map
  I03 Placement: 2 notes in wrong folder (see below)
  I04 MOCs:      complexity/ MOC stale (last updated 2026-02-10, arc created 2026-03-25)
  I05 Engagement axis: structural x5 | behavioral-ideational x3 | complex-interactive x1 — acceptable distribution
  Arc status: COMPLETE | NEEDS CLEANUP
```
