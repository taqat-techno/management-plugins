---
name: pm-coverage-matrix
description: |
  Coverage-matrix discipline BEFORE creating new files OR offering AskUserQuestion options OR deleting orphans. Three rules: (a) before creating a new consolidated file, run a coverage matrix vs existing files (≥80% redundancy → enhance canonical instead); (b) before AskUserQuestion offers "create new file" as an option, run the matrix check first — present "don't create" as Option 1 if redundant; (c) before deleting orphan/redundant files, identify and migrate genuinely-net-new content to canonical files FIRST. Use whenever the user describes creating a "new consolidated", "executive summary", "one-pager", "readiness page", or planning to delete a file.

  <example>
  Context: User wants to create a consolidated executive summary
  user: "Create a consolidated executive summary one-pager for the kickoff"
  assistant: "I'll use the pm-coverage-matrix skill — first, build a coverage matrix vs existing files. If ≥80% of the planned content already exists in canonical files, enhance those instead of creating an orphan."
  <commentary>Direct trigger for rule (a).</commentary>
  </example>

  <example>
  Context: User asks where a new file should live (mid-AskUserQuestion drafting)
  user: "Where should the new readiness page live — V16 folder or Hub V2?"
  assistant: "I'll use the pm-coverage-matrix skill before answering. The question implies a new file; rule (b) requires the matrix check first. If ≥80% redundant, the right Option 1 is 'don't create — content already covered by file X'."
  <commentary>Trigger for rule (b) — preventing the create-it assumption from sneaking past via location-question framing.</commentary>
  </example>

  <example>
  Context: User wants to delete redundant files
  user: "Delete READINESS_ONE_PAGER and PROJECT_ONE_PAGER — they duplicate other files"
  assistant: "I'll use the pm-coverage-matrix skill — rule (c): section-by-section uniqueness audit first. Migrate genuinely-net-new content (e.g., new risks) to the right canonical file BEFORE running Remove-Item."
  <commentary>Trigger for rule (c) — preventing accidental deletion of net-new content.</commentary>
  </example>

  <example>
  Context: User wants to add a new dashboard tab as a "summary view"
  user: "Add a new Summary tab that consolidates the other 4 tabs"
  assistant: "I'll use the pm-coverage-matrix skill — same principle applies to tabs as files. Build the matrix; if ≥80% redundant, enhance an existing tab instead of adding a fifth."
  <commentary>Trigger generalizes beyond files to any 'new consolidated thing' creation.</commentary>
  </example>
license: "MIT"
metadata:
  version: "1.0.0"
  priority: 80
  model: sonnet
  filePattern: []
  bashPattern:
    - "Remove-Item.*\\.html"
    - "rm.*\\.html"
  promptSignals:
    phrases:
      - "consolidated"
      - "executive summary"
      - "one-pager"
      - "readiness page"
      - "create new file"
      - "create new HTML"
      - "delete orphan"
      - "delete redundant"
      - "where should"
      - "summary view"
      - "consolidated readiness"
    minScore: 5
---

# Coverage-Matrix Discipline (Lesson #770)

## Core Principle: New Files Are an Anti-Pattern Until Proven Net-New

When tempted to create a new "executive summary", "consolidated readiness page", "one-pager", or "summary view", the default assumption is wrong: most of the planned content already exists somewhere in the canonical file set. Building the new file silently triples maintenance burden, creates orphan navigation, and lets numbers drift across copies.

This skill enforces three rules: matrix-before-create, matrix-before-AskUserQuestion-options, and uniqueness-audit-before-delete.

---

## Rule (a) — Coverage matrix BEFORE creating new file

### Step 1: Build the matrix

Rows = sections you plan to include in the new file.
Columns = existing canonical files in the workspace.
Cells = `✓ fully covered` / `~ partially covered` / `— missing`.

Example (READINESS_ONE_PAGER for KhairGate kickoff):

| Section | KICKOFF_PREREQUISITES.html | KICKOFF_READINESS_GUIDE.html | PM_RISK_REGISTER.html | health-dashboard.html |
|---|---|---|---|---|
| Open prerequisites count | ✓ | ✓ | — | ~ |
| Risk landscape | — | ~ | ✓ | — |
| BRD status | ~ | ✓ | — | ~ |
| Team readiness | — | ✓ | — | — |
| Sprint 0.1 entry criteria | ✓ | ✓ | — | — |

### Step 2: Decision gate

| Coverage Result | Action |
|---|---|
| ≥80% rows have at least one ✓ cell | **Enhance canonical files instead.** New file would duplicate content. The unique-value justification ("single-screen consolidation" / "print handout" / "exec audience") rarely overcomes the maintenance burden. |
| 50-80% coverage | **Borderline — discuss with user.** If "single-screen for one specific stakeholder" is the only unique value, the existing nav sidebar may already serve that. |
| <50% coverage | **Net-new file justified.** Proceed to creation, but mandate Rule (b) of pm-multi-version-clone (wire into cross-ref nav of all sibling files in the same step). |

### Step 3: If creating, integrate immediately

Per pm-multi-version-clone Rule (b): edit the cross-ref nav in ALL sibling files in the same step. Update link counts. Verify by opening any sibling and clicking the new entry.

---

## Rule (b) — Matrix-check BEFORE AskUserQuestion offers "create" options

When you're about to call `AskUserQuestion` with options like:
- "Create new file in folder X"
- "Create new file in folder Y"
- "Create new file in both folders"

→ STOP. The question implicitly assumes the new file is needed. The user inherits that assumption when they choose AMONG the create-it options.

### Required pre-question step

Run the Rule (a) matrix BEFORE drafting the AskUserQuestion. If the matrix shows ≥80% redundancy:

1. **Option 1 (Recommended):** "Don't create — content already covered by file X. Enhance X instead with the missing pieces."
2. **Options 2/3:** the original create-here / create-there options, but only as fallbacks if the user has a unique-value justification.

### Anti-pattern caught by this rule

Apr 28 V16 example: AskUserQuestion offered V16 / Hub V2 / both as 3 options for a new readiness one-pager. User picked Option 1 (V16). Hours later, a coverage-matrix audit revealed ~95% redundancy — the file was deleted with 3 net-new risks migrated to PM_RISK_REGISTER. The AskUserQuestion should have included "Don't create — content covered by KICKOFF_PREREQUISITES + PM_RISK_REGISTER" as Option 1 (Recommended).

### When user pushes back ("why are we adding them?")

That's the late signal you should have done the matrix BEFORE the question. Don't argue — re-run the matrix, present the redundancy finding, and propose deletion or merge.

---

## Rule (c) — Uniqueness audit BEFORE delete

When deleting a file that has some unique content, run a section-by-section uniqueness audit FIRST. Don't blindly delete.

### Section-by-section workflow

For each section in the file-to-delete:

1. **Search canonical files** for verbatim or near-verbatim matches.
2. **Classify the section:**
   - `Fully covered` — section content exists in a canonical file. Safe to skip; deletion confirms.
   - `Partially covered` — section content exists in modified form. Decide whether the missing piece warrants enhancing the canonical file or is redundant detail.
   - `Net-new` — section content does NOT exist anywhere else. Migrate to the right canonical file with proper format/structure BEFORE deletion.
3. **Migrate net-new sections** to canonical files. Use the existing format conventions (KPI strip, risk register row, BRD index entry).
4. **Then** `Remove-Item` / `rm` the orphan file.
5. **Post-deletion verification:** zero broken cross-references via grep:
   ```
   grep -lE "(deleted_filename1|deleted_filename2)" *.html
   ```
   Any hit means a parent file links to the deleted file — fix the parent.

### Apr 28 example

`READINESS_ONE_PAGER.html` + `PROJECT_ONE_PAGER.html` (1700+ lines combined) — section-by-section audit found ~95% redundancy + 3 net-new items: Senior Django hiring delay risk, BRD Index review pending risk, Mid-Level Django assessment outcome risk. Migrated to `PM_RISK_REGISTER.html` as R-20/R-21/R-22 with bilingual rows + KPI strip 19→22 + Trend paragraph update, THEN deleted. Post-deletion grep confirmed zero broken cross-references.

---

## Three-Rule Summary Card

| Rule | When | Required action |
|---|---|---|
| (a) | Before creating new consolidated/executive/one-pager file | Build coverage matrix; if ≥80% covered, enhance canonical instead |
| (b) | Before AskUserQuestion offers "create new file" options | Run matrix FIRST; if redundant, "Don't create" is Option 1 (Recommended) |
| (c) | Before deleting orphan/redundant files | Section-by-section uniqueness audit; migrate net-new BEFORE delete; grep for broken cross-refs after |

---

## Reference

- Lesson #770 in `D:\Global Lessons\global_lessons.md` — full body with Apr 28 V16 incident references.
- Companion: pm-multi-version-clone (Rule b — cross-ref nav integration when you DO create a new file).
- Companion: pm-consolidation (multi-source merge with numbered conflicts — different operation; this skill prevents the merge from happening if redundancy makes it unnecessary).
