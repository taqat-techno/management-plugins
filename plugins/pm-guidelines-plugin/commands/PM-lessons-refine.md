---
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, Task
description: Orchestrates a refinement pass on global_lessons.md — pre-flight HEAD snapshot, audit (structural + semantic), decision sheet, mechanical renumber, judgment merges, category absorptions, verify, PR. Skills-side workflow runner that guides Claude through the multi-step pass.
disable-model-invocation: false
---

# /PM-lessons-refine — Orchestrate a Refinement Pass on global_lessons.md

You are running the multi-step refinement workflow on `D:\Global Lessons\global_lessons.md`. This command captures the May 7 manual pass as a reusable orchestration. It dogfoods Rule 38-bis (reflog-aware mid-session verification) throughout — parallel sessions actively edit `global_lessons.md` and you must catch them.

## Workflow

### Phase 0 — Pre-flight

1. **Snapshot HEAD:** run `git -C "D:/Global Lessons" rev-parse HEAD` and remember the SHA. Call it `START_SHA` and reference it in every later phase.
2. **Working tree check:** `git -C "D:/Global Lessons" status --short`. If `global_lessons.md` shows `M` (modified) and not committed, STOP — ask the user to either commit the WIP or stash it. Don't audit a dirty file.
3. **Default branch protection:** verify current branch is NOT `main`. If on `main`, create `feat/lessons-refine-<YYYY-MM-DD>` and switch to it. Per the user's `DEFAULT-BRANCH PUSH RULE`, refinement work goes through a feature branch + PR.
4. **Baseline counts:** record current lesson count and category count from R1's primitives. These become the "expected after delete N, after move M" deltas in Phase 6.

### Phase 1 — Structural Audit

Invoke `/pm-guidelines:PM-lessons-audit`. Capture its full output. The result has:
- Section 1: counts (use as baseline)
- Section 2: collisions → goes into decision sheet's **Section A** (mechanical, pre-accepted)
- Section 3: single-lesson categories → goes into **Section D**
- Section 4: empty categories → flag in sheet (rare, usually a bug elsewhere)
- Section 5: out-of-order date blocks → goes into **Section C**
- Section 6: structural orphans → STOP if any; fix orphans before proceeding

### Phase 2 — Semantic Audit (parallel)

Spawn the `pm-lessons-content-duplicates` agent via the `Task` tool. Run it in parallel with Phase 1 if you didn't already. Capture its top-15 pair list. This becomes the decision sheet's **Section B** (judgment-call merges).

If `--focus=N` was passed in `$ARGUMENTS`, pass `focus_lesson=N` to the agent.

### Phase 3 — Generate Decision Sheet

Write `D:\Global Lessons\Lessons_Refinement_Sheet.md`. Structure (mirrors the May 7 working file):

```markdown
# Global Lessons — Refinement Decision Sheet

**Generated:** YYYY-MM-DD HH:MM
**HEAD SHA at audit:** <START_SHA>
**Source file:** D:\Global Lessons\global_lessons.md
**Lesson count:** N
**Category count:** M

## Section A — Numeric Collisions (mechanical, pre-accepted)

[Table from Phase 1 Section 2 — old number, line numbers, proposed new number = next-free]

## Section B — Semantic Duplicates (judgment required)

[Pairs from Phase 2 — A vs B with shared keywords, suggested action, ☐ Accept ☐ Reject ☐ Modify]

## Section C — Out-of-Order Date Blocks (mechanical)

[List from Phase 1 Section 5 — block to move, current position, target position]

## Section D — Single-Lesson Categories (consolidation candidates)

[List from Phase 1 Section 3 — category, lesson, suggested target category, ☐ Accept ☐ Reject]

## Renumber Map

[Pre-applied table for Section A traceability]
```

**STOP and present the sheet to the user.** Do not proceed past Phase 3 without explicit user marks. The user may say "go with all" (accept all defaults), "accept Section A only" (skip B/C/D), "use these marks" (per-row decisions), or "reject — defer". Wait for explicit instruction.

### Phase 4 — Apply Section A (mechanical renumber)

For each collision pair:
1. Find both occurrences (line numbers from Phase 1)
2. Keep the FIRST occurrence's number unchanged
3. Edit the SECOND occurrence: replace `^OLD\. \*\*Title\*\*` with `^NEW\. \*\*Title\*\*` (one Edit per renumber)
4. After all renumbers: run the collision primitive again (`grep -oE '^[0-9]+\. \*\*' | sort | uniq -d`) — expect empty output

Commit checkpoint: `refine: renumber N collisions in global_lessons.md`. Mid-pass reflog dogfood: confirm HEAD didn't move during the renumber loop.

### Phase 5 — Apply Section B (judgment merges)

For each accepted pair (✅ rows in user's marked sheet):

- **MERGE A into B:** Edit B's body to absorb A's distinctive content; provenance tail `(Folded former #A: "Title A")`. Then DELETE A's line entirely (Edit with `old_string="A_full_line\n"`, `new_string=""`).
- **CROSS-REF:** Edit both A and B bodies to append `(See also #B for X)` and `(See also #A for Y)`.
- **KEEP BOTH:** No-op.

After deletes, re-run the empty-categories primitive — Section B deletes can empty a single-lesson category. If so, remove the empty category header (3-line block: `## Header\n\n` → empty) as part of this phase.

### Phase 6 — Apply Section C/D

**Section C** (block move): cut the misplaced block (header + lessons + trailing blank), paste at correct chronological position.

**Section D** (category absorption): for each accepted absorption:
1. Cut the orphan: `## Header + blank + 1 lesson + blank` (4 lines)
2. Append the lesson at the end of the target category's last lesson, with provenance tail `(Relocated from "Source Category" — single-lesson category absorbed.)`

### Phase 7 — Verify and Commit

Run all R1 primitives again:
- Total count: should match `baseline - deletes + parallel_session_adds`. If parallel commits happened, the math gets messy — investigate via reflog.
- Categories: should be `baseline - absorptions - empty-cats-removed`
- Collisions: 0
- Empty categories: 0

Commit: `refine: apply Section B/C/D refinements per decision sheet`. Final reflog dogfood (Rule 38-bis): confirm HEAD movements match the commits you made in Phases 4 and 7.

### Phase 8 — Open PR

Run `gh pr create --base main --head <branch> --title "refine: lessons pass <date>" --body "..."` with body summarizing:
- Counts (before/after)
- Section A renumbers (table)
- Section B decisions (which merged, which kept, which cross-ref'd)
- Section C/D moves
- Reference to the decision sheet file

Share the PR URL with the user. Do NOT push to `main` directly even if a parallel-session auto-push has been observed in this repo before — per `DEFAULT-BRANCH PUSH RULE`, only proceed via PR review unless the user explicitly says "yes push to main".

## Hard rules

- **Rule 38-bis dogfooding:** snapshot HEAD before each phase that takes >5 minutes; check reflog if any verification surprise. Parallel sessions actively edit `global_lessons.md` (saw this twice on May 7).
- **No edits before user marks the sheet.** Phase 3 STOP is mandatory for any non-trivial refinement (anything beyond Section A renumbers).
- **Provenance tails on every merge/relocation:** `(Folded former #N: "Title")` or `(Relocated from "Cat" — single-lesson absorbed.)`. These are how future Claude sessions reconstruct the lineage.
- **Conservative on Section B:** when in doubt, leave a pair as KEEP BOTH and move on. False merges destroy lessons; false KEEPs only delay cleanup.
- **Per-phase commits:** don't bundle Phase 4-7 into one commit. Smaller commits = smaller parallel-collision window (lesson #742).
- **Decision sheet stays in the repo** for audit trail. The May 7 sheet (`Lessons_Refinement_Sheet.md`) is the precedent.

## $ARGUMENTS handling

Optional flags:
- `--dry-run` → run Phases 0-3 only (audit + sheet, no edits, no commits). Useful for checking refinement effort before committing time.
- `--section-a-only` → after Phase 3, apply only Section A renumbers; skip B/C/D entirely. Useful for monthly low-touch maintenance.
- `--focus=N` → restricts Phase 2 semantic audit to pairs involving lesson #N.
- `--no-pr` → skip Phase 8; leave the branch unpushed for the user to review locally before opening the PR.

## Cost story

On 2026-05-07 the user did this exact 7-step workflow manually for the first time. The audit was a general-purpose subagent (~50K tokens, missed 5 collisions, miscounted by 1). The decision sheet was written by hand. The Section A renumbers were 23 individual Edit calls. Section B/C/D edits were another ~20 Edits. The final PR (#1) opened the branch + PR via gh manually. Total session time was well over 2 hours. This command brings the workflow from 2+ hours to ~30 minutes of orchestration plus the user's review time on the decision sheet.

## Companion components

- **`/pm-guidelines:PM-lessons-audit`** — the structural audit (Phase 1)
- **`pm-lessons-content-duplicates`** agent — the semantic audit (Phase 2)
- **`lesson-gap-analyzer`** agent — the plugin-coverage audit (related but different scope)
- **`pm-session-discipline` Rule 38-bis** — reflog-aware verification dogfooded throughout
- **`/PM-lessons-add`** user command — adds lessons; complements this command which restructures them
