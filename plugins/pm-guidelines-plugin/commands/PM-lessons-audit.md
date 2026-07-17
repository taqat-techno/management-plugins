---
allowed-tools: Read, Grep, Bash(grep:*), Bash(awk:*), Bash(wc:*), Bash(sort:*), Bash(uniq:*)
description: Read-only structural audit of global_lessons.md — collisions, single-lesson categories, empty categories, out-of-order date blocks, max number, total counts. Produces the Section A / Section D inputs that feed /pm-guidelines:PM-lessons-refine.
disable-model-invocation: false
---

# /PM-lessons-audit — Read-Only Structural Audit of global_lessons.md

You are running a precision audit of `D:\Global Lessons\global_lessons.md`. This command is **READ-ONLY** — never edit the file. Output a structured markdown report the user can review, and which `/pm-guidelines:PM-lessons-refine` can ingest as Section A and Section D of the decision sheet.

## When to invoke

- Before any refinement pass on `global_lessons.md`
- As the standalone first step when the user types `/pm-guidelines:PM-lessons-audit`
- As phase 2 of `/pm-guidelines:PM-lessons-refine`
- Quarterly or whenever the file has grown by >50 lessons since the last audit

## Hard rules

- **READ-ONLY.** Never edit `global_lessons.md`.
- **Use the deterministic primitives below.** Never eyeball-enumerate from a content-mode grep — `head_limit` truncates silently and miscounts.
- **No estimates.** Every number in the output report comes from a primitive listed below, run via Bash.
- **Cross-reference with `lesson-gap-analyzer` agent** for plugin-coverage view; this command is the **structural** view (collisions, orphans, out-of-order). Both audits have distinct purposes — don't conflate.

## Audit Primitives (MANDATORY — copy-paste these exact commands)

| Metric | Required Bash primitive |
|---|---|
| Total lesson count | `grep -cE '^[0-9]+\. \*\*' "D:/Global Lessons/global_lessons.md"` |
| Total category count | `grep -cE '^## ' "D:/Global Lessons/global_lessons.md"` |
| Numeric collisions | `grep -oE '^[0-9]+\. \*\*' "D:/Global Lessons/global_lessons.md" \| sort \| uniq -d` |
| Max lesson number | `grep -oE '^[0-9]+' "D:/Global Lessons/global_lessons.md" \| sort -nu \| tail -1` |
| Empty categories | `grep -n '^## \|^[0-9]\+\. \*\*' "D:/Global Lessons/global_lessons.md" \| awk -F: '/^[0-9]+:## / {if (h) print pl": EMPTY: "pt; h=1; pl=$1; pt=$0; next} /^[0-9]+:[0-9]/ {h=0} END {if (h) print pl": EMPTY: "pt}'` |
| Single-lesson categories | `awk '/^## /{if (current && lesson_count==1) print prev_line": ["lesson_count"] "current; current=$0; prev_line=NR; lesson_count=0; next} /^[0-9]+\. \*\*/{lesson_count++} END {if (current && lesson_count==1) print prev_line": ["lesson_count"] "current}' "D:/Global Lessons/global_lessons.md"` |
| Category line numbers (for date-order check) | `grep -nE '^## ' "D:/Global Lessons/global_lessons.md"` |

## Workflow

### Step 1 — Run the 7 primitives in parallel

Run all 7 Bash commands above. Capture each output. Do NOT manually enumerate or sample.

### Step 2 — Detect out-of-order date blocks

From the category-line-numbers primitive output, parse each `## ... (Mon DD, YYYY)` heading. Two failure modes to flag:

- **Date-out-of-order:** a `(Mar 31)` block appearing between `(Mar 25)` and `(Mar 26)` blocks (real example: HR & Recruitment was misplaced this morning before the May 7 refinement)
- **Undated category in a dated cluster:** a category without a date tag (`(YYYY-MM-DD)`) sitting between two dated categories — usually a recategorization in progress

Walk the heading list, parse the trailing `(Mon DD, YYYY)` from each, and flag any non-monotonic transition.

### Step 3 — Detect structural orphans

A "structural orphan" is a numbered lesson that doesn't follow the canonical format `^N\. \*\*Title\*\* — body`. Run:

```
grep -nE '^[0-9]+\. ' "D:/Global Lessons/global_lessons.md" | grep -vE '^\d+:\d+\. \*\*[^*]+\*\* — '
```

Any line returned is an orphan needing manual review.

### Step 4 — Compose the report

Emit the report in this exact structure (mirrors the input shape `/pm-guidelines:PM-lessons-refine` expects):

```markdown
# Structural Audit — global_lessons.md

**Generated:** YYYY-MM-DD HH:MM
**Source:** D:\Global Lessons\global_lessons.md
**HEAD SHA at audit:** <run `git rev-parse HEAD` and quote it here>

## 1. Counts (deterministic)

- Total lessons: N (primitive: grep -c)
- Total categories: M
- Max lesson number: K
- Next free number: K+1

## 2. Numeric Collisions (Section A material)

[Empty if none. Otherwise: list every duplicate number with both occurrences (line number + truncated lesson title), suggest renumber target = max+1, max+2, ...]

## 3. Single-Lesson Categories (Section D material)

[List, with line number + category name + the single lesson it contains, plus a suggested target category for absorption based on topic match.]

## 4. Empty Categories

[List of category headers with no lessons under them. Should be EMPTY in healthy state.]

## 5. Out-of-Order Date Blocks (Section C material)

[List any `## ... (date)` heading whose date is non-monotonic vs. its neighbors. Suggest the correct insertion position.]

## 6. Structural Orphans

[List any numbered lesson not matching the canonical format. Should be EMPTY in healthy state.]

## 7. Verdict

- Refinement effort: **None** / **Light** (only Section A) / **Medium** (Section A + B + C/D) / **Heavy** (full re-categorize)
- Recommended next action: <one sentence>
- If `/pm-guidelines:PM-lessons-refine` should be invoked, say so explicitly here.
```

### Step 5 — Save the report (optional)

If the user passed `$ARGUMENTS` containing `--save`, save the report to `D:\Global Lessons\Lessons_Audit_<YYYY-MM-DD-HHMM>.md`. Otherwise just emit it inline.

## Cost story (why this command exists)

On 2026-05-07 the user did a manual 7-step refinement pass on `global_lessons.md`. Step 1 (audit) took about 10 minutes via a general-purpose subagent that miscounted by 1 and missed 5 of 23 numeric collisions (later caught by deterministic verification grep). This command formalizes the audit as deterministic primitives so future refinement passes can't false-clean. Pair with `pm-lessons-content-duplicates` agent for full audit coverage (structural + semantic). Reference: lesson #742 (parallel-commit reflog), lesson-gap-analyzer agent (post-PR #1 deterministic primitives).

## Companion components

- **`pm-lessons-content-duplicates`** agent — semantic dupe detector (covers what this command does NOT: same-topic lessons under different numbers)
- **`/pm-guidelines:PM-lessons-refine`** orchestrator — invokes this command as its phase-2 audit, then proceeds with decision sheet + edits + verify + PR
- **`lesson-gap-analyzer`** agent — plugin-coverage audit (different scope: which lessons are enforced by which plugin component)
