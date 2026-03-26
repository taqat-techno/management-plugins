---
name: pm-html-infrastructure
description: |
  HTML infrastructure standards — modular CSS architecture, numbered pipeline scripts, JSON intermediates, folder objective maps, print CSS, embedded content escaping, and Chart.js patterns. Use when building portal infrastructure, CSS architecture, or data pipelines for dashboards.


  <example>
  Context: User wants to set up build scripts
  user: "Set up the build scripts for the documentation portal"
  assistant: "I will use the pm-html-infrastructure skill to create numbered scripts (01-extract, 02-transform, 03-build) with JSON intermediates for stage decoupling."
  <commentary>Pipeline trigger - numbered scripts and JSON intermediates.</commentary>
  </example>

  <example>
  Context: User wants CSS architecture
  user: "Set up the CSS structure for the new dashboard"
  assistant: "I will use the pm-html-infrastructure skill to create modular CSS files (variables, base, layout, nav, components, rtl, print) for maintainable styling."
  <commentary>CSS architecture trigger - modular file separation.</commentary>
  </example>
license: "MIT"
metadata:
  version: "1.0.0"
  priority: 65
  model: sonnet
  filePattern:
    - "**/*portal*"
    - "**/*pipeline*"
    - "**/static/css/**"
    - "**/scripts/**"
  bashPattern: []
  promptSignals:
    phrases:
      - "build scripts"
      - "data pipeline"
      - "portal page"
      - "modular CSS"
      - "print CSS"
      - "pipeline scripts"
      - "CSS architecture"
      - "folder map"
    minScore: 6
---

# HTML Infrastructure Standards

## Zero-Dependency Static HTML (Rule 51)

Every dashboard must be a **self-contained HTML file** that:
- Works offline, on any machine, forever
- Has NO build system, NO bundler, NO server required
- Can be opened by double-clicking the file
- Is suitable for board presentations and long-term archival

## Modular CSS Architecture (Rule 52)

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

## Pipeline Scripts (Rules 53-54)

### Numbered Execution Order

```
scripts/
├── 01_extract_devops.py       # Pull data from APIs
├── 02_extract_timesheets.py   # Pull timesheet data
├── 03_transform_sprint.py     # Clean and normalize
├── 04_calculate_metrics.py    # Compute KPIs
├── 05_generate_charts.py      # Build chart data
├── 06_build_dashboard.py      # Assemble HTML
└── run_all.sh                 # Execute 01-06 in sequence
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

## Folder Objective Map (Rule 55)

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

## Print CSS Protection (Rule 77)

Dashboard print output breaks mid-card without these rules:

```css
@media print {
    .card, .table, .metric-card { break-inside: avoid; }
    h2, h3, h4 { break-after: avoid; }
    .tab-content { display: block !important; } /* Show all tabs */
    .tab-content + .tab-content { break-before: always; }
}
```

Always test `Ctrl+P` after adding print styles. Hidden tabs produce blank pages.

## Embedded Content Escaping

Self-contained HTML with embedded JSON or script data must escape:

| Raw | Escaped |
|-----|---------|
| `</script>` | `<\/script>` |
| Template literal backticks | `\`` |
| `${}` template expressions | `\${}` |

Failure to escape causes the browser to close the `<script>` tag prematurely, breaking the entire page.

## Chart.js Requires `.update()`

When modifying Chart.js chart data programmatically:

```javascript
// BAD: DOM manipulation doesn't work on canvas elements
document.querySelector('canvas').style.display = 'block';

// GOOD: use Chart.js API
myChart.data.datasets[0].data = newData;
myChart.update(); // Required - re-renders the canvas
```

Canvas-based charts are not DOM elements. Always use the chart library's API for updates.

## Infrastructure Checklist

Before delivering any portal or pipeline:

- [ ] CSS is modular (separate files, not one monolith)
- [ ] Pipeline scripts are numbered (01, 02, 03...)
- [ ] JSON intermediates decouple pipeline stages
- [ ] FOLDER_OBJECTIVE_MAP.html exists for projects with 10+ folders
- [ ] Print CSS has `break-inside: avoid` on cards/tables
- [ ] Print CSS shows all tabs with `display: block !important`
- [ ] Embedded content properly escaped (`</script>` to `<\/script>`)
- [ ] Chart.js updates use `.update()` API, not DOM manipulation
