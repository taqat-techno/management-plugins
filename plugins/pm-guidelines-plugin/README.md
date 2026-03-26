# PM Guidelines Plugin for Claude Code

> **Cross-project PM best practices enforcement — automated quality checks for status reports, dashboards, bilingual documents, and stakeholder deliverables.**

**v1.4.0** | 137 guidelines | 8 hooks (7 quality checks in single dispatcher) | 10 skills | 3 agents

---

## What It Does

Encodes 137 real-world PM lessons learned into a 3-layer enforcement system:

| Layer | Purpose | How It Works |
|-------|---------|-------------|
| **Hooks** (8) | Real-time enforcement | Fire automatically on Write/Edit/Bash/Read/Stop events. 7 quality checks consolidated into single dispatcher for performance. |
| **Skills** (10) | Knowledge injection | Loaded into context during document generation |
| **Agents** (3) | Batch quality review | Invoked after completing a deliverable for comprehensive audit |

**Scoped to PM directories only** — hooks only fire on files in `researches/`, `reports/`, `deliverables/`, `dashboards/`, `proposals/`, `presentations/`, and `tasks/`. Zero noise for code files.

---

## Hooks (8)

### Tier 1: Security (Block)

| Hook | Event | Behavior |
|------|-------|----------|
| `pat_token_guard` | PreToolUse (Write/Edit/Bash) | Blocks secrets: GitHub tokens, API keys, Azure PATs with context keywords |
| `source_file_protection` | PreToolUse (Write/Edit) | Blocks edits to files listed in `.pm-protected-paths` config |

### Tier 2: Quality (Advisory)

| Hook | Event | Behavior |
|------|-------|----------|
| `post_write_dispatcher` | PostToolUse (Write/Edit) | **Unified dispatcher** — runs 7 checks in one process: status labels, bilingual parity, dashboard quality, HTML render reminder, title consistency, modal accessibility, print CSS |
| `version_drift_detector` | PostToolUse (Write/Edit) | Detects stale Document Control tables in versioned standalone folders |
| `html_version_naming` | PreToolUse (Write) | Warns when overwriting deliverables without `_v2` suffix |

### Tier 3: Session Lifecycle (Advisory)

| Hook | Event | Behavior |
|------|-------|----------|
| `git_pull_before_analysis` | PreToolUse (Read) | Warns if reading data files before running `git pull` |
| `search_index_rebuild` | PostToolUse (Bash) | Reminds to rebuild search index after `git pull` |
| `session_end_lessons` | Stop | Prompts for lesson capture at session end |

---

## Skills (10)

| Skill | Model | Purpose |
|-------|-------|---------|
| `pm-report-writing` | Sonnet | Report quality: specificity, consistent labels, email 3-version pattern |
| `pm-dashboard-design` | Sonnet | Dashboard core: OKR/KPI scoring, data transparency, drill-down UX, modal accessibility |
| `pm-devops-integration` | Sonnet | Azure DevOps API: WIQL queries, real states, work item types, Blocked field |
| `pm-html-infrastructure` | Sonnet | HTML infrastructure: modular CSS, pipeline scripts, print CSS, content escaping |
| `pm-session-discipline` | Sonnet | Session workflow: memory vs tasks, lesson capture, pull-before-analyze |
| `pm-bilingual-standards` | Sonnet | Bilingual EN/AR: data-i18n, RTL CSS, paired spans, language toggle |
| `pm-estimation` | Opus | Effort estimation: SP scales, person-months, AI multipliers, variance tables |
| `pm-consolidation` | Opus | Multi-source merge: conflict tracking, gap classification, source attribution |
| `pm-standalone-updater` | Sonnet | Version folder management, Document Control, BA review loops, auto-updater |
| `lesson-sync` | Sonnet | Lesson-to-component routing, sync procedure, gap analysis |

---

## Agents (3)

| Agent | Model | Skills Preloaded | Purpose |
|-------|-------|-----------------|---------|
| `pm-report-reviewer` | Opus | pm-report-writing, pm-dashboard-design, pm-devops-integration, pm-html-infrastructure, pm-bilingual-standards | Batch review of completed PM deliverables with quality score and violation list |
| `pm-bilingual-qa` | Opus | pm-bilingual-standards | Deep structural validation of bilingual EN/AR HTML files |
| `lesson-gap-analyzer` | Opus | lesson-sync | Analyzes coverage of global_lessons.md across all plugin components |

All agents are **read-only** (tools: Read, Grep, Glob). They never modify files.

---

## Configuration

### Protected Source Files

Create a `.pm-protected-paths` file in your project root to block edits to source analysis files:

```
# One glob pattern per line
**/S1/*
**/S2/*
**/source-analysis/*
```

The `source_file_protection` hook reads this file and blocks any Write/Edit to matching paths. If no config file exists, the hook is a no-op.

### PM Directories

Hooks only fire on files in these directories:

- `researches/`
- `reports/`
- `deliverables/`
- `dashboards/`
- `proposals/`
- `presentations/`
- `tasks/`

Files outside these directories are never checked.

---

## Plugin Structure

```
pm-guidelines-plugin/
├── .claude-plugin/
│   └── plugin.json
├── .gitignore
├── README.md
├── agents/
│   ├── pm-report-reviewer.md
│   ├── pm-bilingual-qa.md
│   └── lesson-gap-analyzer.md
├── hooks/
│   ├── hooks.json
│   ├── pm_utils.py
│   ├── post_write_dispatcher.py      ← consolidated (7 checks in 1 process)
│   ├── pat_token_guard.py
│   ├── source_file_protection.py
│   ├── html_version_naming.py
│   ├── version_drift_detector.py
│   ├── git_pull_before_analysis.py
│   ├── search_index_rebuild.py
│   ├── session_end_lessons.py
│   └── health_check.py             ← plugin integrity validator
├── pm-report-writing/
│   └── SKILL.md
├── pm-dashboard-design/
│   └── SKILL.md
├── pm-session-discipline/
│   └── SKILL.md
├── pm-bilingual-standards/
│   └── SKILL.md
├── pm-estimation/
│   └── SKILL.md
├── pm-consolidation/
│   └── SKILL.md
├── pm-devops-integration/
│   └── SKILL.md
├── pm-html-infrastructure/
│   └── SKILL.md
├── pm-standalone-updater/
│   └── SKILL.md
├── lesson-sync/
│   └── SKILL.md
└── tests/
    ├── conftest.py
    ├── test_pm_utils.py
    ├── test_pat_token_guard.py
    ├── test_post_write_dispatcher.py
    └── fixtures/
```

> **Note:** 7 legacy hook files (`status_label_enforcer.py`, `bilingual_parity_check.py`, etc.) remain in `hooks/` as reference but are not registered in hooks.json. Their logic is consolidated into `post_write_dispatcher.py`.

---

## Guidelines Covered

The 137 guidelines are organized into domains:

| Domain | Guidelines | Components |
|--------|-----------|------------|
| Report Writing | 1-4 | pm-report-writing skill, post_write_dispatcher hook |
| Status Labels | 5-7 | pm-report-writing skill, post_write_dispatcher hook |
| Bilingual EN/AR | 8-10, 33 | pm-bilingual-standards skill, post_write_dispatcher hook |
| Email Drafting | 11-13 | pm-report-writing skill |
| HTML Deliverables | 14-15 | html_version_naming hook, post_write_dispatcher hook |
| Data Validation | 16-18 | pm-estimation skill |
| OKR/KPI Dashboards | 19-21 | pm-dashboard-design skill, post_write_dispatcher hook |
| Search Index | 22-23 | search_index_rebuild hook |
| Project Estimation | 24-27 | pm-estimation skill |
| DevOps Integration | 28-35 | pm-devops-integration skill, pat_token_guard hook |
| Session Workflow & Git | 36-39 | pm-session-discipline skill, git_pull_before_analysis hook |
| Data Analysis | 40-43 | pm-estimation skill |
| Memory & Lessons | 44-46 | pm-session-discipline skill, session_end_lessons hook |
| Consolidation | 47-50 | pm-consolidation skill, source_file_protection hook |
| Portal Architecture | 51-56 | pm-html-infrastructure skill |
| Dashboard Maintenance | 57-60 | pm-dashboard-design skill |
| Standalone Updater | 61-74 | pm-standalone-updater skill, version_drift_detector hook |
| OKR Dashboard v2 | 75-83 | pm-dashboard-design skill |
| Auto-Updater & UX | 84-89 | pm-standalone-updater skill |
| Cross-File Consistency | 90-99 | pm-session-discipline skill |
| Git & Deployment | 100-109 | pm-session-discipline skill |
| Dashboard & KPI Design | 110-114 | pm-dashboard-design skill |
| Document Consolidation | 115-116 | pm-consolidation skill |
| Modal, Audit & i18n | 117-120 | pm-dashboard-design skill |
| OKR Dashboard v3 | 121-133 | pm-dashboard-design skill |
| Email Analysis | 134-137 | pm-report-writing skill |

---

## Health Check

Validate plugin integrity with a single command:

```bash
py hooks/health_check.py
```

Checks: hooks.json file references, agent skill references, orphaned files, lesson count vs plugin.json, skill directories, plugin metadata, model declarations.

---

## Testing

73 tests covering the 3 highest-risk modules:

```bash
py -m pytest tests/ -v
```

| Test File | Tests | Coverage |
|-----------|-------|----------|
| `test_pm_utils.py` | 16 | Path matching, file type detection, safe reading |
| `test_pat_token_guard.py` | 17 | Secret detection (GitHub, AWS, Azure, npm, Bearer) |
| `test_post_write_dispatcher.py` | 40 | All 7 consolidated checks + graceful degradation |

---

## License

MIT - TaqaTechno
