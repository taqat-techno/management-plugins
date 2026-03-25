---
name: pm-dashboard-design
description: |
  OKR/KPI dashboard design standards — auto-scoring, inverse metrics, source tabs, modular CSS, zero-dependency static HTML, numbered pipeline scripts, and JSON intermediates. Use when creating dashboards, portals, metrics pages, or data pipeline infrastructure.


  <example>
  Context: User wants a KPI dashboard
  user: "Create a KPI dashboard for the engineering team"
  assistant: "I will use the pm-dashboard-design skill to build a zero-dependency HTML dashboard with auto-calculated progress bars, a Data Source tab, and modular CSS architecture."
  <commentary>Core trigger - KPI dashboard with auto-scoring and source transparency.</commentary>
  </example>

  <example>
  Context: User wants an OKR scorecard
  user: "Build an OKR scorecard for Q2 with key results"
  assistant: "I will use the pm-dashboard-design skill to create separate OKR and KPI sections with editable 'Current' fields that auto-calculate progress percentage, bar color, and status badge."
  <commentary>OKR trigger - auto-scoring with editable current fields.</commentary>
  </example>

  <example>
  Context: User wants a DevOps metrics dashboard
  user: "Create a dashboard showing Azure DevOps sprint progress"
  assistant: "I will use the pm-dashboard-design skill to build a dashboard using real DevOps states, a Data Source tab with exact WIQL queries, and fetch timestamps instead of live clocks."
  <commentary>DevOps dashboard trigger - real states and source transparency.</commentary>
  </example>

  <example>
  Context: User wants a data pipeline for a portal
  user: "Set up the build scripts for the documentation portal"
  assistant: "I will use the pm-dashboard-design skill to create numbered scripts (01-extract, 02-transform, 03-build) with JSON intermediates for stage decoupling."
  <commentary>Pipeline trigger - numbered scripts and JSON intermediates.</commentary>
  </example>
license: "MIT"
metadata:
  version: "1.0.0"
  priority: 75
  filePattern:
    - "**/*dashboard*"
    - "**/*report*.html"
    - "**/*kpi*"
    - "**/*okr*"
    - "**/*metrics*"
    - "**/*portal*"
  bashPattern: []
  promptSignals:
    phrases:
      - "create dashboard"
      - "build report"
      - "KPI dashboard"
      - "OKR scorecard"
      - "metrics page"
      - "portal page"
      - "build scripts"
      - "data pipeline"
      - "sprint dashboard"
    minScore: 6
---

# PM Dashboard Design Standards

## Architecture Rule: Zero-Dependency Static HTML

Every dashboard must be a **self-contained HTML file** that:
- Works offline, on any machine, forever
- Has NO build system, NO bundler, NO server required
- Can be opened by double-clicking the file
- Is suitable for board presentations and long-term archival

## OKR vs KPI: Keep Them Separate

| Type | Purpose | Structure |
|------|---------|-----------|
| **OKR** (Objectives & Key Results) | Quarterly aspirational goals | Separate tab/section with Objectives, each containing Key Results |
| **KPI** (Key Performance Indicators) | Ongoing team metrics | Separate tab/section with metric cards and trend indicators |

NEVER mix OKRs and KPIs in one table. Use separate tabs or clearly demarcated sections.

## Auto-Scoring (Rule 19)

OKR scoring MUST be automatic. Never rely on manual status entry.

### Pattern: Editable Current Fields

```html
<input type="number" class="kr-current" data-target="85" data-direction="higher"
       onchange="updateProgress(this)" value="62">
```

```javascript
function updateProgress(input) {
    const current = parseFloat(input.value);
    const target = parseFloat(input.dataset.target);
    const direction = input.dataset.direction; // "higher" or "lower"

    let progress;
    if (direction === 'lower') {
        // Inverse metric: lower is better (bug rate, carry-over)
        progress = current <= target ? 100 : Math.max(0, (1 - (current - target) / target) * 100);
    } else {
        // Standard metric: higher is better
        progress = Math.min(100, (current / target) * 100);
    }

    // Update bar, color, and badge
    const bar = input.closest('.kr-row').querySelector('.progress-bar');
    bar.style.width = progress + '%';
    bar.className = 'progress-bar ' + getColorClass(progress);
    bar.textContent = Math.round(progress) + '%';
}

function getColorClass(progress) {
    if (progress >= 70) return 'bg-success';
    if (progress >= 40) return 'bg-warning';
    return 'bg-danger';
}
```

### Inverse Metrics (Rule 20)

KPIs where **lower is better** need special handling:

| Metric | Direction | Logic |
|--------|-----------|-------|
| Bug escape rate | Lower is better | If current <= target: 100%. Else: inverse formula |
| Carry-over tasks | Lower is better | If current <= target: 100%. Else: inverse formula |
| Response time (ms) | Lower is better | If current <= target: 100%. Else: inverse formula |
| Sprint velocity | Higher is better | Standard: (current / target) * 100 |
| Test coverage % | Higher is better | Standard: (current / target) * 100 |

## Data Source Tab (Rule 30)

Every dashboard MUST include a "Data Source" or "Source" tab showing:

1. **Exact queries used** (WIQL for DevOps, SQL for databases, API endpoints)
2. **Results returned** (row counts, date ranges)
3. **Verification links** (direct URLs to the source system)
4. **Last fetched timestamp** (when data was retrieved, NOT current time)

```html
<div id="source-tab">
    <h3>Data Source</h3>
    <p><strong>Last fetched:</strong> <span id="fetch-time">2026-03-24 14:30:00 UTC</span></p>

    <h4>Query 1: Sprint Work Items</h4>
    <pre>SELECT [System.Id], [System.Title], [System.State]
FROM WorkItems
WHERE [System.IterationPath] = 'Project\Sprint 5'
AND [System.AssignedTo] CONTAINS 'Team Member'</pre>
    <p>Results: 22 items returned</p>
    <a href="https://dev.azure.com/org/project/_queries" target="_blank">Verify in DevOps</a>
</div>
```

## Timestamps: Fetch Time, Not Live Clock (Rule 34)

```javascript
// BAD - live clock gives false confidence
setInterval(() => {
    document.getElementById('time').textContent = new Date().toLocaleString();
}, 1000);

// GOOD - shows when data was actually retrieved
document.getElementById('fetch-time').textContent = fetchTimestamp;
// Where fetchTimestamp was captured at the moment of API call
```

## Full Project Names (Rule 35)

In dashboards for CEO/Board audiences, use full names:

| Bad | Good |
|-----|------|
| BMS | KhairGate (BMS) |
| RC | Relief Center |
| TP | TAQAT Property Management |

Abbreviations are internal shorthand that external stakeholders won't recognize.

## DevOps Query Patterns (Rule 28-29)

### Use Real DevOps States (Rule 28)

Always query actual states first:
```
GET /_apis/wit/workitemtypes/{type}/states
```

Real states: `To Do`, `In Progress`, `Resolved`, `Done`, `Closed`

NEVER use made-up labels like "Active", "Carry-over", or "Backlog" unless they match the actual DevOps configuration.

### Query by Assigned To (Rule 29)

When Area Paths don't exist for team breakdown:
```sql
[System.AssignedTo] CONTAINS 'member name'
```

This works cross-project and is more flexible than area paths.

### Discover Projects via API (Rule 31)

Never hardcode project names. Always discover first:
```
GET /_apis/projects?api-version=7.0
```

Then let the user confirm which projects to include.

## Modular CSS Architecture (Rule 44)

Separate CSS into focused files from day one:

```
static/css/
├── variables.css        # Color tokens, spacing, typography
├── base.css            # Reset, body, global styles
├── layout.css          # Grid, containers, sections
├── nav.css             # Navigation, tabs, sidebar
├── components.css      # Cards, tables, badges, progress bars
├── rtl.css             # Arabic/RTL overrides
└── print.css           # Print-specific styles
```

This allows targeted changes without breaking unrelated pages.

## Pipeline Scripts (Rule 45-46)

### Numbered Execution Order

```
scripts/
├── 01_extract_devops.py       # Pull data from APIs
├── 02_extract_timesheets.py   # Pull timesheet data
├── 03_transform_sprint.py     # Clean and normalize
├── 04_calculate_metrics.py    # Compute KPIs
├── 05_generate_charts.py      # Build chart data
├── 06_build_dashboard.py      # Assemble HTML
└── run_all.sh                 # Execute 01→06 in sequence
```

### JSON Intermediates

Each script reads from and writes to JSON files:
```
data/
├── raw_workitems.json         # Output of 01
├── raw_timesheets.json        # Output of 02
├── normalized_sprint.json     # Output of 03
├── metrics.json               # Output of 04
├── charts.json                # Output of 05
└── dashboard.html             # Output of 06
```

Large JSON intermediates (even 20MB) are worth the storage cost — they decouple pipeline stages so any downstream script can run independently.

## Folder Objective Map (Rule 47)

For projects exceeding 10 subfolders, create `FOLDER_OBJECTIVE_MAP.html`:

```html
<table>
    <tr><th>Folder</th><th>Purpose</th><th>Key Files</th></tr>
    <tr><td>scripts/</td><td>Data pipeline (01-06)</td><td>run_all.sh</td></tr>
    <tr><td>data/</td><td>JSON intermediates</td><td>metrics.json</td></tr>
    <tr><td>templates/</td><td>HTML templates</td><td>dashboard_base.html</td></tr>
</table>
```

New team members can orient themselves immediately.

## Dashboard Maintenance & Adoption (Rules 49-52)

### Maintenance Burden Threshold (Rule 49)

If a dashboard requires **> 30 manual inputs per week** for one person, it won't be used. Design rule: **if an API can provide it, never ask the PM to type it.**

| Version | Manual Inputs | Outcome |
|---------|--------------|---------|
| v1 | ~113 | Never populated |
| v2 | ~24 | Actively used |

Always count manual inputs during design. Auto-fetch everything possible from DevOps APIs, databases, or localStorage history.

### KRs Must Be Outcomes, Not Activities (Rule 50)

Before finalizing OKRs, test each KR: **"Could someone else observe and verify this was achieved?"** If not, rewrite it.

| Bad (Activity) | Good (Outcome) |
|----------------|----------------|
| "Weekly agendas with DevOps metrics pre-populated" | "Decision turnaround time < 3 days" |
| "Hold weekly meetings" | "100% meeting compliance for 4 consecutive weeks" |
| "Create sprint reports" | "Sprint carry-over rate < 15%" |

### PM Scorecard for CEO Visibility (Rule 51)

Team KPIs measure the team, not the PM. Add a dedicated **PM Scorecard** tab with metrics the CEO evaluates the PM on:

- Decision turnaround time
- Scope change control (% approved vs rejected)
- Meeting compliance rate
- Stakeholder satisfaction pulse
- Risk escalation timeliness

Without this, the PM is invisible in their own dashboard.

### localStorage Snapshots for Trend Tracking (Rule 52)

Save a weekly snapshot object into a history array on every "Save" click:

```javascript
function saveSnapshot() {
    const history = JSON.parse(localStorage.getItem('okr-history') || '[]');
    history.push({
        date: new Date().toISOString().slice(0, 10),
        data: getCurrentState()
    });
    // Cap at 13 weeks (~500KB)
    if (history.length > 13) history.shift();
    localStorage.setItem('okr-history', JSON.stringify(history));
}
```

Use inline SVG sparklines (no Chart.js dependency) for week-over-week progress. Add Export/Import JSON for backup. Zero infrastructure needed.

## OKR Dashboard v2 Lessons (Rules 67-71)

### Tab vs Sidebar Navigation (Rule 67)

**Under 10 views = tabs. 10+ views = sidebar.**

| Views | Navigation | Reason |
|-------|-----------|--------|
| < 10 | Horizontal tabs | Fewer choices = faster cognitive load for executives |
| 10+ | Sidebar | Persistent visibility of all options |

v1 had 12 sidebar items; v2 consolidated to 7 tabs. Always consolidate before adding navigation complexity.

### Auto-Fetch Coverage Determines Adoption (Rule 68)

The practical threshold: **< 30 manual inputs/week** for PM dashboard adoption.

Track your coverage ratio:
```
Auto-fetch ratio = auto-fetched data points / total data points
Target: > 60% auto-fetch
```

v2 auto-fetches ~44 data points via WIQL, leaving only ~24 manual inputs.

### Bilingual i18n via Data Attributes (Rule 69)

Use `data-i18n` keys with a JS translation map — **never duplicate HTML for EN/AR**.

```html
<h3 data-i18n="team_pulse_title">Team Pulse</h3>
```

```javascript
const translations = {
    en: { team_pulse_title: "Team Pulse" },
    ar: { team_pulse_title: "نبض الفريق" }
};
```

Duplicating pages for languages doubles maintenance and guarantees drift.

### Print CSS Must Show All Tabs (Rule 70)

Dashboard print styles that hide inactive tabs produce blank pages:

```css
@media print {
    .tab-content { display: block !important; }
    .tab-content + .tab-content { page-break-before: always; }
    .tab-content::before {
        content: attr(data-tab-title);
        font-size: 1.5em;
        font-weight: bold;
    }
}
```

Always test `Ctrl+P` after adding print styles.

### Clickable Drill-Down Metric Cards (Rule 71)

Every aggregate metric card should open a per-member or per-project breakdown modal on click:

```javascript
function showTeamDetailModal(teamId, state) {
    // Show breakdown: who owns what within "To Do: 12"
    const members = getTeamMembers(teamId);
    const items = members.map(m => getItemsByState(m, state));
    renderModal(items);
}
```

Showing "To Do: 12" is useless without knowing who owns what. All aggregate numbers must drill down.

## Design Checklist

Before delivering any dashboard:

- [ ] OKR and KPI sections are separate (not mixed)
- [ ] All scoring is automatic from editable "Current" fields
- [ ] Inverse metrics use correct formula (lower-is-better)
- [ ] "Data Source" tab exists with exact queries and verification links
- [ ] Timestamps show fetch time, not live clock
- [ ] Full project names used (no unexplained abbreviations)
- [ ] CSS is modular (separate files, not one monolith)
- [ ] Works offline (zero external dependencies)
- [ ] Pipeline scripts are numbered (01, 02, 03...)
- [ ] JSON intermediates decouple pipeline stages
- [ ] Manual inputs < 30/week (auto-fetch everything possible)
- [ ] KRs are outcomes, not activities ("Could someone verify this?")
- [ ] PM Scorecard tab exists for CEO visibility
- [ ] localStorage snapshots with Export/Import JSON
- [ ] Tab navigation if < 10 views, sidebar if 10+
- [ ] `data-i18n` attributes on all text (no duplicate HTML for languages)
- [ ] Print CSS shows all tabs with page breaks
- [ ] All metric cards have clickable drill-downs
