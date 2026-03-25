---
name: lesson-sync
description: |
  Synchronizes global_lessons.md with the pm-guidelines plugin components. Detects new/changed lessons, maps them to the correct skill or hook using the category-to-component routing table, and updates the plugin's embedded copy. Use when lessons have been added or changed and the plugin needs to be updated.


  <example>
  Context: User added new lessons to global_lessons.md
  user: "sync lessons"
  assistant: "I will use the lesson-sync skill to compare global_lessons.md with the plugin copy, identify new lessons, and route them to the correct skills/hooks."
  <commentary>Direct sync trigger - user wants to update plugin after adding lessons.</commentary>
  </example>

  <example>
  Context: User wants to see what's not covered
  user: "lesson gap analysis"
  assistant: "I will use the lesson-sync skill to map all lessons against plugin components and produce a coverage report showing which lessons have no enforcement."
  <commentary>Gap analysis trigger - user wants visibility into coverage holes.</commentary>
  </example>

  <example>
  Context: Session-end drift warning fired
  user: "update plugin lessons"
  assistant: "I will use the lesson-sync skill to sync the drifted global_lessons.md into the plugin, routing new lessons to the correct components."
  <commentary>Post-drift-warning trigger - responding to the lesson_drift_detector hook advisory.</commentary>
  </example>

  <example>
  Context: User wants to align lessons with plugin
  user: "align lessons with plugin"
  assistant: "I will use the lesson-sync skill to perform a full alignment — checking every lesson against every plugin component and producing an actionable gap report."
  <commentary>Alignment trigger - comprehensive review of lesson-to-component mapping.</commentary>
  </example>
license: "MIT"
metadata:
  version: "1.0.0"
  priority: 80
  filePattern:
    - "**/global_lessons*"
    - "**/lesson*"
    - "**/*guidelines*"
  bashPattern: []
  promptSignals:
    phrases:
      - "sync lessons"
      - "update plugin lessons"
      - "lesson gap analysis"
      - "align lessons"
      - "lesson coverage"
      - "new lessons"
      - "lesson drift"
    minScore: 6
---

# Lesson Sync System

## Purpose

This skill maintains alignment between `global_lessons.md` (the source of truth) and the pm-guidelines plugin components. It detects new lessons, classifies them, and routes them to the correct plugin component.

## Category-to-Component Routing Table

This is the master routing table. Every lesson category maps to specific plugin components:

| Category | Lessons | Target Skill | Target Hook(s) | Target Agent |
|----------|---------|-------------|-----------------|--------------|
| Report Writing | 1-4 | pm-report-writing | status_label_enforcer | pm-report-reviewer |
| Status Labels & Completion Markers | 5-7 | pm-report-writing | status_label_enforcer | pm-report-reviewer |
| Bilingual Documents (EN/AR) | 8-10 | pm-bilingual-standards | bilingual_parity_check | pm-bilingual-qa |
| Stakeholder Communication & Emails | 11-13 | pm-report-writing | — | pm-report-reviewer |
| HTML Deliverables | 14-15 | — | html_version_naming, html_render_reminder | — |
| Data Validation | 16-18 | pm-estimation | — | — |
| OKR & KPI Dashboards | 19-21 | pm-dashboard-design | dashboard_quality_check | pm-report-reviewer |
| Search Index Maintenance | 22-23 | — | search_index_rebuild | — |
| Project Estimation & Story Points | 24-27 | pm-estimation | — | — |
| DevOps API Integration | 28-35 | pm-dashboard-design | pat_token_guard | — |
| Session Workflow & Git Hygiene | 28b-31b | pm-session-discipline | git_pull_before_analysis | — |
| Data Analysis & Presentation | 32b-35b | pm-estimation | — | — |
| Memory & Lessons Discipline | 36-38 | pm-session-discipline | session_end_lessons | — |
| Consolidation & Multi-Source Architecture | 39-42, 48 | pm-consolidation | source_file_protection | — |
| Portal & Pipeline Architecture | 43-47 | pm-dashboard-design | — | — |
| Dashboard Maintenance & Adoption | 49-52 | pm-dashboard-design | dashboard_quality_check | pm-report-reviewer |
| Enhanced Standalone Auto-Updater Rules | 53-66 | pm-standalone-updater | version_drift_detector | — |
| OKR Dashboard v2 Lessons | 67-71 | pm-dashboard-design | dashboard_quality_check | pm-report-reviewer |
| Auto-Updater & UX Redesign Lessons | 72-77 | pm-standalone-updater | powershell_safety_check | — |

## Sync Procedure

### Step 1: Parse Source File

Read `global_lessons.md` and extract:
- Each `## Heading` = category name
- Each `N. **Bold title** — description` = lesson
- Build a list: `[{number, title, category, full_text}]`

### Step 2: Compare with Plugin Copy

Read `plugins/pm-guidelines-plugin/global_lessons.md` (the plugin's embedded copy).

Detect:
- **New lessons**: present in source, absent in plugin copy
- **Modified lessons**: same number but different text
- **Removed lessons**: present in plugin copy, absent in source
- **New categories**: `##` headings in source not in plugin copy

### Step 3: Classify New Lessons

For each new or modified lesson:

1. **Match category** against the routing table above
2. If category matches an existing row → route to that skill/hook
3. If category is NEW (no match) → apply the decision tree:

#### Decision Tree for New Categories

```
Is the lesson a rule that can be detected by regex in file content?
  YES → Create a new Hook (PostToolUse advisory)
  NO  → Is it a design principle to follow during content generation?
    YES → Create a new Skill (or extend closest existing skill)
    NO  → Does it require multi-file analysis?
      YES → Extend an existing Agent's checklist
      NO  → Add to pm-session-discipline skill (catch-all for workflow rules)
```

### Step 4: Route to Components

For each classified lesson:

**If routed to a Skill:**
1. Open the target SKILL.md
2. Find the appropriate section (by rule number range)
3. Add the new rule as a subsection with: heading, explanation, code example if applicable, checklist item

**If routed to a Hook:**
1. Check if existing hook can be extended (add a new check function)
2. If not, create a new hook .py file following the pattern:
   - Import pm_utils
   - Read stdin JSON
   - Extract file_path or command
   - Apply regex/content check
   - Output JSON with description
3. Register in hooks.json

**If routed to an Agent:**
1. Open the agent .md file
2. Add new check IDs to the appropriate check category table
3. Update the scoring rubric if needed

### Step 5: Sync Plugin Copy

After routing all new lessons:
1. Copy root `global_lessons.md` → `plugins/pm-guidelines-plugin/global_lessons.md`
2. Update plugin.json version (bump patch: 1.1.0 → 1.1.1)
3. Update README.md Guidelines Covered table

### Step 6: Report

Produce a sync report:

```
## Lesson Sync Report

**Source:** global_lessons.md (N lessons, M categories)
**Plugin:** pm-guidelines v1.x.x

### Changes Detected
- X new lessons added
- Y lessons modified
- Z new categories

### Routing Summary
| Lesson | Category | Routed To | Action |
|--------|----------|-----------|--------|
| 78 | New Category | pm-report-writing skill | Added as new section |
| 79 | New Category | NEW hook: xyz_check | Created new hook |

### Updated Files
- [list of files modified]

### Coverage: N/N lessons (100%)
```

## Handling Edge Cases

### Duplicate Lesson Numbers
`global_lessons.md` has duplicate numbers 28-35 (DevOps Integration and Session Workflow). The unique key for a lesson is `{category}:{number}`, NOT just the number.

### Lessons Without Clear Category Match
If a lesson's category doesn't match any row in the routing table AND the decision tree doesn't clearly suggest a component type, flag it in the report as "Manual classification needed" rather than guessing wrong.

### Rapid Succession of Changes
If multiple lessons are added at once across different categories, process them in category order (top to bottom in global_lessons.md) to maintain consistency.

## Sync Frequency

- **Automatic:** The `lesson_drift_detector` hook checks at session end
- **On-demand:** User says "sync lessons" or "lesson gap analysis"
- **Scheduled:** Daily cron job compares both files
