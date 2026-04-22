# Global Lessons — Project Context

**Path:** `D:\Global Lessons\`
**Last Active:** Apr 21, 2026
**Sessions:** 1

## Purpose

Cross-project lessons learned repository — single source of truth for PM best practices, with a Claude plugin (`pm-guidelines-plugin`) that enforces lessons via skills and agents.

## Key Files

- **`global_lessons.md`** — **Single source of truth.** 482 lessons across 97 categories (updated Apr 21, 2026). No HTML copy maintained — plugin syncs from this file; git commits track history.
- `Global_Lessons_Learned.html` — Bilingual EN/AR dashboard (43 lessons displayed)

## Subfolders

- `pm-guidelines-plugin\` — 8 skill SKILL.md files: lesson-sync, pm-bilingual-standards, pm-consolidation, pm-dashboard-design, pm-estimation, pm-report-writing, pm-session-discipline, pm-standalone-updater. 3 agents: lesson-gap-analyzer, pm-bilingual-qa, pm-report-reviewer. README.md.
- `claude-plugin-builder\` — SKILL.md + 4 reference docs: architecture-decision-guide, domain-patterns, hooks-recipes, quality-gates

## Standing Rules

- **Never edit the HTML directly** — `global_lessons.md` is the source; HTML and plugin sync from it
- New lessons added via `/PM-lessons-add` skill
- Lesson coverage verified via `pm-guidelines:lesson-gap-analyzer` agent
- Pre-delivery check via `/PM-lessons-check`

## Counts (Apr 12, 2026)

HTML: 3 | MD: 21 | DOCX: 0 | Total files: 166
