---
name: pm-cross-tab-reconciler
description: |
  Cross-tab numeric reconciliation for multi-tab dashboards — single source of truth data architecture, reconciliation rules, header-banner sync, team-count array rule, and pre-publish self-check. Use when authoring or editing multi-tab dashboards (OKR, KPI, PMO, sprint, portfolio) so totals that appear in multiple tabs never drift. For general dashboard design see pm-dashboard-design. For WIQL data sources see pm-devops-integration. Post-authoring audit is delegated to the pm-cross-tab-reconciler agent.


  <example>
  Context: User wants to add a new tab to an existing dashboard
  user: "Add a Team Pulse tab to the OKR dashboard"
  assistant: "I will use the pm-cross-tab-reconciler skill. Team Pulse totals must reconcile with the Executive Summary tab — both will render from the same data source array, not hardcoded literals."
  <commentary>Core trigger — adding a tab to a multi-tab dashboard always raises cross-tab reconciliation risk.</commentary>
  </example>

  <example>
  Context: User wants a new multi-tab dashboard
  user: "Build a KPI dashboard with 5 tabs"
  assistant: "I will use the pm-cross-tab-reconciler skill. I will structure a single `const data = {...}` shared by all 5 tabs and end with a reconciliation self-check."
  <commentary>New-dashboard trigger — set the single-source-of-truth pattern from line one.</commentary>
  </example>

  <example>
  Context: User updates a number that appears in multiple tabs
  user: "Change the total open items count from 42 to 38"
  assistant: "I will update `data.openItems` in the shared source object. Because every tab reads from that object, Executive Summary, Team Pulse, and Portfolio will all reflect 38 — no per-tab literal edits needed."
  <commentary>Update trigger — changes propagate through one edit, not N.</commentary>
  </example>

  <example>
  Context: User asks to reconcile an existing dashboard
  user: "Reconcile totals across tabs in the Q2 dashboard"
  assistant: "I will use the pm-cross-tab-reconciler skill to walk the 5 rules and then run the pre-publish self-check. If the dashboard already exists, I will also suggest invoking the pm-cross-tab-reconciler agent for a post-authoring semantic audit."
  <commentary>Audit trigger — skill runs the authoring-time checklist; agent handles semantic alignment judgment.</commentary>
  </example>
license: "MIT"
metadata:
  version: "1.0.0"
  priority: 70
  model: sonnet
  filePattern:
    - "**/dashboards/**/*.html"
    - "**/*dashboard*.html"
    - "**/*kpi*.html"
    - "**/*okr*.html"
    - "**/*portfolio*.html"
    - "**/*scorecard*.html"
    - "**/*sprint*.html"
  bashPattern: []
  promptSignals:
    phrases:
      - "add tab"
      - "add a tab"
      - "multi-tab dashboard"
      - "reconcile totals"
      - "reconcile numbers"
      - "cross-tab"
      - "dashboard with tabs"
      - "KPI dashboard"
      - "OKR dashboard"
      - "sprint dashboard"
      - "portfolio dashboard"
      - "executive summary tab"
      - "team pulse tab"
    minScore: 6
---

# PM Cross-Tab Reconciliation Standards

Multi-tab dashboards fail most often at the seams between tabs — the same number appears on three tabs with three slightly different values, and a board member asks "which one is right?" This skill prevents that class of failure at authoring time by enforcing a single-source-of-truth data architecture and a pre-publish self-check.

Scope: any HTML dashboard with two or more tab regions (`role="tabpanel"`, `.tab-pane`, or equivalent). Not for single-page reports.

Related skills: `pm-dashboard-design` (general dashboard architecture), `pm-devops-integration` (WIQL feeding the shared data object), `pm-html-infrastructure` (CSS and pipeline).

## The Five Rules

### Rule CT-01: Single Source of Truth

Every numeric total that appears in more than one tab MUST be rendered from a single JS data object. Never hard-code a total in a specific tab's HTML.

```javascript
// CORRECT — one source, every tab reads from it
const data = {
    openItems: 42,
    closedItems: 118,
    teamSize: 18,
    budgetSpent: 12400,
    milestonesComplete: 7,
    milestonesTotal: 12
};

function renderExecutiveTab() {
    document.querySelector('#exec-open').textContent = data.openItems;
    // ... every number comes from `data`
}

function renderTeamPulseTab() {
    document.querySelector('#pulse-open').textContent = data.openItems;
    // same source
}
```

```html
<!-- WRONG — literal in one tab; another tab will drift -->
<div class="exec-kpi"><strong>42</strong> open items</div>
...
<div class="pulse-header">38 open items</div>  <!-- this will rot -->
```

When data comes from an API, still funnel it through ONE promise chain into ONE in-memory object consumed by all tabs:

```javascript
async function loadDashboard() {
    const [workItems, budget, team] = await Promise.all([
        fetchWIQL(query),
        fetchBudget(),
        fetchTeam()
    ]);
    const data = aggregate(workItems, budget, team);
    renderAllTabs(data);  // not renderTab1(data1), renderTab2(data2)
}
```

### Rule CT-02: Summary Equals Sum of Details

Any Executive or Summary widget showing a total MUST equal the sum of its Team or Detail rows. Unassigned items count — add them to an "Unassigned" bucket rather than quietly dropping them.

```
Project open items (Exec)  = 42
  Backend team (Team Pulse) = 15
  Frontend team             = 12
  QA team                   = 8
  Unassigned                = 7
                              ---
                              42  ✓
```

Legitimate filter differences between tabs must be annotated in the HTML so the next author knows the mismatch is intentional:

```html
<div class="exec-summary" data-filter="active-only">
    <!-- NOTE: exec summary excludes 'Blocked' items; detail tab includes all -->
    <strong>38</strong> active open items
</div>
```

Unannotated mismatches are bugs.

### Rule CT-03: Header Banner Sync

Any number in the header banner (`.kpi-value`, `<strong>` in a hero card, `.stat-value`) MUST reconcile with its source row in the detail tab. Header banners are the first thing a board member sees; mismatches are the most embarrassing class of bug.

```javascript
// Header banner is just another consumer of `data`
function renderHeader() {
    document.querySelector('.hero-open').textContent = data.openItems;
    document.querySelector('.hero-closed').textContent = data.closedItems;
    document.querySelector('.hero-completion').textContent =
        Math.round((data.milestonesComplete / data.milestonesTotal) * 100) + '%';
}
```

If the header banner shows a KPI the detail tabs never reproduce (e.g., a single synthetic health score), that's acceptable — just ensure it's computed from `data`, not a literal.

### Rule CT-04: Team-Count Array Rule

"Team size: N" or "N members" text MUST use `.length` of an array, not a numeric literal. Roster arrays drift in real life (people join, people leave); literals don't know when a member was added.

```javascript
// CORRECT
const teamMembers = [
    { name: 'Hala Abdelaziz', role: 'Lead' },
    { name: 'Shehab', role: 'Senior' },
    // ...
];

document.querySelector('.team-size').textContent =
    teamMembers.length + ' members';
```

```html
<!-- WRONG — rotted the moment someone is added -->
<div class="team-size">5 members</div>
```

Same rule for counts of work items, projects, and any other collection visible on the dashboard.

### Rule CT-05: Reconciliation-Friendly Labels

Use the same wording for the same concept across tabs. Synonym drift is a hidden cost — future authors and audit agents both have to judge "is 'Open Items' the same as 'Outstanding Tasks' the same as 'Active'?"

| Tab A label | Tab B label | Verdict |
|---|---|---|
| Open Items | Outstanding Tasks | DRIFT — pick one |
| Budget Spent | Actual Spend | DRIFT — pick one |
| Team Size | Member Count | DRIFT — pick one |
| Milestones Complete | Milestones Complete | aligned |

Pick the label once, put it in the CSS class or data attribute, and use it everywhere. A future `pm-cross-tab-reconciler` agent audit will thank you.

## Authoring Procedure

When this skill activates, walk these five steps:

1. **Inventory tabs.** Scan the dashboard for tab regions (`role="tabpanel"`, `.tab-pane`, `<section id="...">` with a matching nav above). List them.
2. **Inventory numeric totals per tab.** For each tab, list every numeric total it displays and where each one comes from: shared `data` object, API call, computed aggregate, or — red flag — hardcoded literal.
3. **Enforce single source.** For each numeric total that appears in ≥2 tabs, verify it comes from the same source. If not, refactor to a shared source BEFORE proceeding with the user's requested change.
4. **Trace header banner.** For every number in the header banner, trace it to its source row. Either both come from `data`, or the banner KPI is a synthesized computation with no detail equivalent (acceptable).
5. **Check team counts.** Every "N members" / "N tasks" / "N items" text must use `.length` of an array. Flag any literal.

## Pre-Publish Self-Check

Before handing the dashboard back to the user, run this checklist and report the result:

```
Cross-Tab Reconciliation Self-Check

[ ] All cross-tab totals render from shared `const data = {...}` or equivalent (CT-01)
[ ] No hardcoded numeric literals appear in >1 tab (CT-01)
[ ] Executive Summary totals = sum of detail rows, or annotated filter difference (CT-02)
[ ] Header banner numbers trace to source rows or are computed from `data` (CT-03)
[ ] "N members" / "N tasks" text uses .length of an array, not a literal (CT-04)
[ ] Same label used for same concept across all tabs (CT-05)
[ ] If the dashboard already existed before this session, suggest running the
    pm-cross-tab-reconciler agent for a semantic post-authoring audit
```

If any box fails, explain the specific mismatch with tab names and suggest the fix before closing the turn.

## When Not To Activate

This skill is for multi-tab dashboards. Do NOT activate for:

- Single-page reports (no tabs = no cross-tab risk).
- Pure presentation decks (HTML slideshows where each slide is independent).
- Dashboards where all tabs are legitimately different-scope (e.g., "This Week" vs "Last Quarter") — those numbers shouldn't reconcile. Use the Rule CT-02 annotated-filter pattern instead.
- Bilingual dashboards where the "duplicate" number is just the EN and AR version of the same thing — count that as one logical number, not two.

## Delegation to the Audit Agent

The `pm-cross-tab-reconciler` agent (in `agents/`) handles post-authoring semantic audit: it reads the finished HTML and aligns labels via Opus judgment (identifying "Open Items" ≈ "Outstanding Tasks" cases the skill can't catch statically). Invoke the agent when:

- Auditing a dashboard you didn't author.
- The user suggests the dashboard "might have drift" and you're unsure.
- `pm-report-reviewer` is reviewing a dashboard — it will auto-delegate.

Don't invoke the agent for every change you make during authoring — the skill's pre-publish self-check is enough for normal editing flow.

## Mistakes This Skill Prevents

| Lesson | Mistake | How this skill prevents it |
|---|---|---|
| 19–21 | Exec summary showed 42 open; Team Pulse showed 38; Portfolio showed 45 | CT-01: all three would render from `data.openItems` |
| 57–60 | KPI score drift across tabs from rounding/filter differences | CT-01 + CT-02 annotated filters |
| 111 | Team size "12" on Exec vs roster count "11" on Team Pulse | CT-04: both from `teamMembers.length` |
| 121–133 | Milestone completion % differs across summary widgets | CT-01 + CT-03 header-banner sync |
| 183, 436–439, 467 | Team count header vs actual array length mismatch | CT-04 |
| 447 | Budget utilization shown twice with different denominators | CT-02 annotated filter or reconcile |
