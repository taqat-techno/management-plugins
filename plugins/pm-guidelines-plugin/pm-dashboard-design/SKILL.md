---
name: pm-dashboard-design
description: |
  OKR/KPI dashboard design standards — auto-scoring, inverse metrics, source tabs, data reconciliation, drill-down UX, modal accessibility, health auto-calculation, G/A/R toggles, and collapsible sections. Use when creating dashboards, KPI pages, or OKR scorecards. For DevOps API patterns see pm-devops-integration. For CSS/pipeline infrastructure see pm-html-infrastructure.


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
  version: "1.3.0"
  priority: 75
  model: sonnet
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
      - "sprint dashboard"
      - "health dashboard"
      - "drill-down"
      - "G/A/R toggle"
      - "project health"
      - "audit dashboard"
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

## Numbers Must Reconcile Across Views (Rule 121)

If Executive Summary shows "26 Bugs total", Team Pulse must also total 26. Mismatched totals destroy trust instantly.

**Formula:** `Project total = Sum(all teams) + Unassigned`

Always add an "Unassigned" card to catch work items with no owner. If totals don't match, debug before shipping.

**For multi-tab dashboards:** the `pm-cross-tab-reconciler` skill owns the single-source-of-truth data architecture that makes Rule 121 enforceable — every total rendered from one shared `data` object rather than hardcoded per tab. Activate that skill when adding or editing any tab in a multi-tab dashboard. The audit side (post-authoring semantic review) is handled by the `pm-cross-tab-reconciler` agent.

## Consistent Drill-Down Pattern (Rule 122)

Every clickable number must follow the same flow:

```
Card number → Breakdown table → Work Items popup (with DevOps links) → Back button
```

NEVER skip levels for some metric types while keeping them for others. If To Do has 3-level drill-down, Bugs must too. Inconsistency confuses users.

## Modal Accessibility (Rule 123)

Modals with many items push the Close button off-screen. Always set:

```css
.modal-content {
    max-height: 85vh;
    overflow-y: auto;
}
```

The Close and Back buttons must ALWAYS be reachable without scrolling past content.

## Auto-Calculate Overall Health (Rule 111)

Never let users manually set "Overall" health when it can be computed from dimensions:

```javascript
function calculateOverallHealth(schedule, quality, scope, blockerCount) {
    // Start with worst dimension
    const dimensions = [schedule, quality, scope]; // 'green', 'amber', 'red'
    const worst = getWorst(dimensions);

    let overall = worst;
    // Blocker penalty
    if (blockerCount > 3) overall = 'red';
    else if (blockerCount > 0 && overall !== 'red') overall = downgrade(overall);

    return overall;
}
```

Remove the manual Overall toggle entirely. Manual values drift from reality.

## localStorage Migration Between Versions (Rule 114)

When a dashboard version changes its localStorage key (e.g., `okr-kpi-q2-v2` to `okr-kpi-q2-v3`), auto-migrate on load:

```javascript
function migrateData() {
    const oldKey = 'okr-kpi-q2-2026-v2';
    const newKey = 'okr-kpi-q2-2026-v3';
    const oldData = localStorage.getItem(oldKey);
    if (oldData && !localStorage.getItem(newKey)) {
        const data = JSON.parse(oldData);
        // Transform data shape if needed
        localStorage.setItem(newKey, JSON.stringify(data));
        localStorage.removeItem(oldKey);
    }
}
```

Without migration, users lose all entered data on version upgrades.

### Rule 114-bis: Schema Versioning and Key Consolidation

Rule 114 addresses migration when a key changes. Rule 114-bis prevents the underlying mistake: mixing multiple unrelated localStorage keys in one dashboard, or silently changing a key's shape without a version bump.

**Versioned key pattern.** Every key name must carry a schema version suffix:

```javascript
const STORAGE_KEY = 'pm-dashboard-v2';  // bumped from v1 when schema changed
const MIGRATION = {
    fromV1(data) {
        // new field added in v2; default to null for migrated records
        return { ...data, newField: null };
    }
};

function load() {
    let raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
    // Attempt migration from prior schema
    const v1 = localStorage.getItem('pm-dashboard-v1');
    if (v1) {
        const migrated = MIGRATION.fromV1(JSON.parse(v1));
        localStorage.setItem(STORAGE_KEY, JSON.stringify(migrated));
        localStorage.removeItem('pm-dashboard-v1');
        return migrated;
    }
    return defaultState();
}
```

**One versioned key per dashboard.** Do not scatter unrelated keys across one file (e.g., `kg-action-progress` alongside `kg-adr-state` alongside `kg-filters`). Consolidate into one object under one versioned key. When the schema needs new fields, bump the version and write a migration function — never silently change the shape.

**Anti-patterns to avoid:**

```javascript
// BAD — three unrelated keys, none versioned
localStorage.setItem('actionProgress', progress);
localStorage.setItem('adrState', adr);
localStorage.setItem('filters', filters);

// BAD — key stayed 'pm-dashboard' but schema changed (users lose state)
localStorage.setItem('pm-dashboard', { progress, adr, filters });  // was just { progress }

// GOOD — one versioned key, one consolidated object, migration on version bump
localStorage.setItem('pm-dashboard-v2', { progress, adr, filters });
```

Rule 114-bis checklist:

```
[ ] One versioned localStorage key per dashboard (no mixed unrelated keys)
[ ] Schema version in the key name (pm-dashboard-v2, not pm-dashboard)
[ ] Migration function (fromV1, fromV2, ...) for every prior schema version
[ ] Migration runs once on load, preserves user data, removes the old key
```

## Collapsible Sections for Board HTML (Rule 74)

Board members navigate 15+ sections. Use collapsible containers:

```html
<details class="section" open>
    <summary>Sprint Progress</summary>
    <!-- section content -->
</details>

<details class="section">
    <summary>Resolved Items (12)</summary>
    <!-- collapsed by default for resolved/closed items -->
</details>
```

**Rule:** Resolved/Closed sections should be collapsed by default (`<details>` without `open`). Focus attention on pending items.

Add Expand All / Collapse All buttons for quick navigation.

## Modal Popups Beat Inline Results (Rule 117)

For audit output, validation results, or drill-down data:

```javascript
// BAD: inline div pushes content down, gets lost on scroll
document.getElementById('results').innerHTML = output;

// GOOD: modal overlay with backdrop, dismissible, no layout shift
showModal({
    title: 'Audit Results',
    summary: { pass: 14, fail: 3, warn: 2 },
    details: checkResults
});
```

Include a summary bar (pass/fail counts) at the top of every modal.

## G/A/R Toggles Need Deselect (Rule 125)

Status toggle buttons must support clearing:

```javascript
function toggleGAR(el, value) {
    if (el.classList.contains('selected')) {
        el.classList.remove('selected'); // Deselect on second click
        saveStatus(el, 'none');
    } else {
        // Clear siblings, select this one
        el.parentNode.querySelectorAll('.gar-btn').forEach(b => b.classList.remove('selected'));
        el.classList.add('selected');
        saveStatus(el, value);
    }
}
```

Without deselect, once you set a value you can never clear it.

## Design Checklist

Before delivering any dashboard:

**Architecture**
- [ ] OKR and KPI sections are separate (not mixed)
- [ ] Works offline (zero external dependencies)
- [ ] See `pm-html-infrastructure` for CSS, pipeline, and print rules
- [ ] See `pm-devops-integration` for WIQL, states, and Blocked field rules

**Auto-Scoring & Data**
- [ ] All scoring is automatic from editable "Current" fields
- [ ] Inverse metrics use correct formula (lower-is-better)
- [ ] Overall health auto-calculated from dimensions (no manual toggle)

**Transparency**
- [ ] "Data Source" tab exists with exact queries and verification links
- [ ] Timestamps show fetch time, not live clock
- [ ] Full project names used (no unexplained abbreviations)
- [ ] Numbers reconcile across all views (total = sum of parts + unassigned)

**UX & Accessibility**
- [ ] Consistent drill-down pattern: Card -> Breakdown -> Items -> Back
- [ ] Modals have `max-height: 85vh; overflow: auto`
- [ ] G/A/R toggles support deselect (click again to clear)
- [ ] Collapsible sections for board HTML; resolved items collapsed by default
- [ ] Audit/validation results shown in modal popup, not inline div
- [ ] localStorage migration logic handles version key changes
