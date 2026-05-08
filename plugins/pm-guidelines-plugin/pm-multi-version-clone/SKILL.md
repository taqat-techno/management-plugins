---
name: pm-multi-version-clone
description: |
  Multi-version HTML clone hygiene — three rules for keeping v[N-1] → v[N] HTML clones from leaking past-version state into the new release. Use when cloning a versioned HTML deliverable (Variance Report, Dashboard, Talking Points deck, Kickoff Brief) from one version to the next.

  <example>
  Context: User wants to clone a versioned HTML report
  user: "Clone Variance-Analysis-Report_v12.html to v13"
  assistant: "I will use the pm-multi-version-clone skill to run the 3-rule discipline: post-clone grep audit for past-version chatter, cross-ref nav integration in all sibling files, and reframe stale predecessor badges to HISTORICAL."
  <commentary>Direct trigger for v[N-1] → v[N] clone workflow.</commentary>
  </example>

  <example>
  Context: User wants to bump a dashboard version
  user: "Bump OKR_KPI_Dashboard_v10.html to v11"
  assistant: "I will use the pm-multi-version-clone skill to copy + clean past-version chatter (V10 SSOT, FULLY READY, 9/9 RESOLVED), wire v11 into cross-ref navs, and reframe v10 badges as HISTORICAL."
  <commentary>Same trigger via "bump version" wording.</commentary>
  </example>

  <example>
  Context: User wants to add a (LATEST) successor card to a dashboard
  user: "Add Variance v13 (LATEST) card to health-dashboard.html"
  assistant: "I will use the pm-multi-version-clone skill — specifically rule (c): audit ALL related cards (sibling cards in same row, parent verdict callouts, KPI strips) for stale badges and reframe predecessor as HISTORICAL with neutral grey styling."
  <commentary>Successor-card trigger; engages rule (c) badge reframe.</commentary>
  </example>
license: "MIT"
metadata:
  version: "1.0.0"
  priority: 70
  model: sonnet
  filePattern:
    - "**/*_v[0-9]*.html"
    - "**/*_V[0-9]*.html"
    - "**/Variance*"
    - "**/Dashboard*"
    - "**/Talking_Points*"
  bashPattern:
    - "cp.*_v[0-9].*\\.html.*_v[0-9].*\\.html"
    - "Copy-Item.*_v[0-9]"
  promptSignals:
    phrases:
      - "clone v"
      - "bump version"
      - "v[N-1] to v[N]"
      - "successor card"
      - "(LATEST) card"
      - "version-bump"
      - "bump to v"
      - "promote to v"
    minScore: 5
---

# Multi-Version HTML Clone Hygiene (Lesson #771)

## Core Principle: Cloning Inherits ALL Internal State

A `cp v[N-1] → v[N]` workflow inherits every internal section content, including past-version narratives, frozen verdicts, comparison column headers, and stale predecessor badges. The version-bump subagent only handles tags+dates+PS1 config — section prose is content-domain logic outside its scope.

This skill enforces three rules at clone time.

---

## Rule (a) — Post-Clone Grep Audit for Past-Version Chatter

After cloning v[N-1] → v[N], grep for past-version strings in the new file:

```powershell
grep -nE "(V10|v10|v11|v12 historical|FULLY READY|9/9 RESOLVED|March 23-24|Pre-V12)" path\to\v[N].html
```

Every hit needs section-by-section rewrite with V[N]-current narrative.

### Specific patterns to clean

| Pattern | What to do |
|---|---|
| `V[N-1] SSOT` / `V[N-2] historical` | Update workflow chips (chronology) |
| `9/9 RESOLVED — FULLY READY` | Replace with v[N] verdict (e.g., "4/6 RESOLVED — 2 FLAGGED — READY pending governance") |
| `v11 Value` / `v12 Value` (comparison columns) | Rename to "Pre-V[N] / Post-V[N]" |
| `Sections X-Y are v[N-1] historical` (footer) | Replace with single-version footer |
| `Files Updated` lists referencing prior files | Update to V[N] file roster |
| `Authoritative Numbers` row labels | Update column headers |

**Pre-publish audit:** re-grep for ALL prior version numbers; any hit means cleanup incomplete.

---

## Rule (b) — Wire New File into Cross-Ref Nav (Not Optional Polish)

Creating a new HTML file in a multi-file portal without adding it to the cross-ref nav makes it an **orphan** — reviewers cannot reach it from any other file. Nav-integration is part of "done", not optional polish.

### Required cross-ref updates

When creating `<file>_v[N].html`:

1. **Edit cross-ref nav in ALL sibling files** to include the new entry. Decide which category (ACTION / REFERENCE / AUDIT / OVERVIEW) and place it consistently across siblings.
2. **Update link count** if the nav has a count display ("18 Links" → "19 Links").
3. **Verify by opening any sibling file in browser** and clicking the new nav entry — should resolve to v[N], not 404.
4. **For dual-repo setups** (e.g., melshahedpearl/Hub V2 sister copy + project-local primary), ensure BOTH copies (if synced) get the nav update.

### Anti-pattern to avoid

Creating `READINESS_ONE_PAGER.html` without adding nav links in any sibling file. Reviewers later ask "how do I reach this from the index?" — the file effectively doesn't exist from a navigational perspective. (Companion to lesson #770: if you skipped the coverage matrix and created the file, at minimum wire it into nav so it's not orphaned.)

---

## Rule (c) — Reframe Stale Predecessor Badges

When adding a `(LATEST)` tag or successor card, audit ALL related cards (sibling cards in same row, parent verdict callouts, KPI strips) for stale badges that reflect the predecessor's state when it WAS the latest.

### Reframe checklist

| Old (stale) | New (historical) |
|---|---|
| `✓ CLEAR` / `FULLY READY` green badge | `✓ HISTORICAL` / `Superseded by v[N+1]` (neutral grey styling) |
| `9/9 items resolved` | `9/9 items resolved AS OF March 23` (past tense) |
| (no cross-link) | Add `Superseded by v[N+1] above` cross-link |
| Bright green `bg-success` / `bg-green-500` | Neutral `bg-gray-200` / `bg-slate-300` |

The historical card SHOULD still link to the underlying file (it remains a valid artifact for traceability) — only the visual framing changes.

### Workflow

1. Before adding the new (LATEST) card, list every card on the same dashboard that references the predecessor.
2. For each, apply the reframe checklist.
3. Add the new (LATEST) card with bright green badge + verdict callout.
4. Visual diff: predecessor card should look "historical" at-a-glance vs the new card.

---

## End-to-End Workflow When Cloning

1. **Decide scope.** What's the clone — single HTML, sibling pair (HTML + MD), full portal? Cross-ref scope follows.
2. **Copy.** `Copy-Item v[N-1].html v[N].html` (or `cp` on bash).
3. **Run version-bump subagent** (existing pm-standalone-updater workflow) — handles tags+dates+PS1.
4. **Apply rule (a)** — grep + rewrite past-version chatter section-by-section.
5. **Apply rule (b)** — edit cross-ref nav in all sibling files; update link count.
6. **Apply rule (c)** — reframe predecessor badges to HISTORICAL across all related cards.
7. **Pre-publish audit** — re-grep for ALL prior version numbers; visual browser check; toggle EN ↔ AR if bilingual.
8. **Commit per rule** if in a tracked repo, so reviewers can see the discipline applied.

---

## Companion to pm-standalone-updater

`pm-standalone-updater` handles the **mechanical** version-bump (file naming, Document Control tables, PS1 auto-updater scripts). This skill (`pm-multi-version-clone`) handles the **content-domain cleanup** that the mechanical bump cannot do — past-version narratives, cross-ref nav, predecessor badge reframing.

Run them together: pm-standalone-updater FIRST, then pm-multi-version-clone for the section-prose work.

---

## Reference

- Lesson #771 in `D:\Global Lessons\global_lessons.md` — full body with sub-incident citations from the Apr 28 V16 Drift Fix session
- Companion lessons: #770 (coverage-matrix BEFORE creating new files), #758 (living-doc fork-vs-edit + multi-PR audit doc), #772 (bilingual + audit-check drift catchers post-clone)
