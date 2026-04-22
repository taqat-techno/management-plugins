---
name: pm-devops-integration
description: |
  Azure DevOps API integration patterns — real work item states, WIQL queries per type, Blocked field usage, project discovery via API, and query-by-assigned-to. Use when building dashboards that fetch from Azure DevOps or when writing WIQL queries.


  <example>
  Context: User wants DevOps metrics in a dashboard
  user: "Add Azure DevOps sprint data to the dashboard"
  assistant: "I will use the pm-devops-integration skill to query real DevOps states via WIQL, separate queries per work item type, and use the Blocked field for blocker counts."
  <commentary>DevOps API trigger - real states and separate WIQL queries.</commentary>
  </example>

  <example>
  Context: User wants team breakdown from DevOps
  user: "Show work items per team from Azure DevOps"
  assistant: "I will use the pm-devops-integration skill to query by [System.AssignedTo] since area paths may not exist, and discover projects via the API."
  <commentary>Team breakdown trigger - query by assigned to pattern.</commentary>
  </example>
license: "MIT"
metadata:
  version: "1.1.0"
  priority: 70
  model: sonnet
  filePattern:
    - "**/*dashboard*"
    - "**/*devops*"
    - "**/*sprint*"
    - "**/*wiql*"
    - "**/roster.json"
    - "**/.team-roster*"
  bashPattern: []
  promptSignals:
    phrases:
      - "DevOps metrics"
      - "WIQL query"
      - "Azure DevOps"
      - "sprint dashboard"
      - "work item types"
      - "blocked items"
      - "DevOps states"
      - "assigned to query"
      - "team roster"
      - "roster file"
      - "add team member"
      - "data readiness"
      - "live API probe"
    minScore: 6
---

# DevOps API Integration Standards

## Use Real DevOps States (Rule 28)

Dashboard metrics must match the exact states in Azure DevOps. Always query actual states first:

```
GET /_apis/wit/workitemtypes/{type}/states

```

Real states: `To Do`, `In Progress`, `Resolved`, `Done`, `Closed`

NEVER use made-up labels like "Active", "Carry-over", or "Backlog" unless they match the actual DevOps configuration.

## Query by Assigned To (Rule 29)

When Area Paths don't exist for team breakdown:

```sql
[System.AssignedTo] CONTAINS 'member name'

```

This works cross-project and is more flexible than area paths.

## Discover Projects via API (Rule 31)

Never hardcode project names. Always discover first:

```
GET /_apis/projects?api-version=7.0

```

Then let the user confirm which projects to include.

## Separate WIQL Queries Per Work Item Type (Rules 110, 126)

Never mix work item types in a single query:

```sql
-- BAD: hides bug counts inside task totals
[System.WorkItemType] IN ('Task', 'Bug')

-- GOOD: separate queries for accurate metrics
-- Query 1: Tasks only
[System.WorkItemType] = 'Task'
-- Query 2: Bugs only
[System.WorkItemType] = 'Bug'
-- Query 3: Enhancements only
[System.WorkItemType] = 'Enhancement'

```

Each type needs its own KPI card, WIQL query, and column in drill-down tables. Without separation, you can't answer "how many bugs are open?" from the dashboard.

## Use the Blocked Field, Not Tags (Rule 128)

Azure DevOps has a dedicated blocked field:

```sql
-- GOOD: built-in field, no manual tagging needed
[Microsoft.VSTS.CMMI.Blocked] = 'Yes'

-- BAD: requires manual tagging, easily forgotten
[System.Tags] CONTAINS 'Blocked'

```

The `Blocked` field is built into the work item form. Tags require discipline that teams rarely maintain.

## Never Expose PAT Tokens (Rule 32)

PAT tokens should only be entered in browser modals and stored in localStorage. Never save them in code, memory files, or conversation. If a user shares one, remind them not to.

## Canonical Roster File Pattern

Team rosters drift when the same list of members is duplicated across dashboards, RACI tables, and WIQL `IN (...)` clauses. When Afthab joins QA-QC, the dashboard is updated but the WIQL query still lists only Mostafa — so Afthab's work items never show up. The fix is a single source of truth per project.

Convention: one `roster.json` (or `.team-roster.yml`) in the project root:

```json
{
  "team": "QA-QC",
  "members": [
    { "name": "Mostafa Ahmed", "email": "mostafa@taqat.qa", "role": "QC Lead" },
    { "name": "Afthab P A", "email": "afthab@taqat.qa", "role": "QC Engineer", "dedicated_to": "KhairGate Wallet" }
  ]
}

```

Every dashboard, RACI table, and WIQL query consumes this file or imports from it. Hand-typing names into HTML is banned.

Consuming in a dashboard:

```javascript
// Fetch once; render many
async function loadRoster() {
    const res = await fetch('./roster.json');
    const roster = await res.json();
    return roster;
}

// Team size comes from .length — honours Rule CT-04
document.querySelector('.team-size').textContent =
    roster.members.length + ' members';

// WIQL IN-clause generated from roster
const assignedToClause = roster.members
    .map(m => `'${m.email}'`)
    .join(', ');
const wiql = `SELECT [System.Id] FROM WorkItems
              WHERE [System.AssignedTo] IN (${assignedToClause})`;

```

Canonical roster checklist:

```
[ ] Dashboard reads roster from roster.json (not inline literals)
[ ] RACI table cells reference names from roster.json
[ ] WIQL IN-clauses are generated from roster.members[*].email
[ ] Adding or removing a team member = one edit (roster.json), never N edits across files
[ ] Roster file path documented in the dashboard's Data Source tab

```

## Live-API Probe Recipe — Data Readiness Gate (Rule DR-1)

Before committing to any estimate, cost claim, user count, or sprint metric that depends on live DevOps data, demand the probe output in-thread. Never reason from assumed counts; verify against a live query.

Probe templates:

```bash
# How many open items in a project?
az boards query --wiql \
    "SELECT [System.Id] FROM WorkItems WHERE [System.State] <> 'Closed'" \
    --project "<project>" \
    --query "length(@)"

# Who is actually assigned in this area path?
az boards query --wiql \
    "SELECT DISTINCT [System.AssignedTo] FROM WorkItems
     WHERE [System.AreaPath] UNDER '<path>'"

# What states does this work item type actually have?
az boards work-item type show --type Task --project "<project>"

```

Rule: if the probe fails (timeout, auth error, empty org) OR returns fewer than expected results, downgrade claim confidence to LOW and state the assumption explicitly in the deliverable. Never report "~40 open items" when the probe timed out — say "probe failed; estimate withheld".

Why skill-only, not hook: network calls in PostToolUse hooks are fragile (timeouts, PAT leakage across subprocess boundaries, retries that double-count). Live probes belong in the authoring loop where Claude can react to a failed probe and the user can supply context.

## DevOps Integration Checklist

Before delivering any DevOps-connected dashboard:

- [ ] Queried actual states via States API (not assumed)
- [ ] Separate WIQL queries per work item type (Task/Bug/Enhancement)
- [ ] Uses `[Microsoft.VSTS.CMMI.Blocked]` field, not tags
- [ ] Projects discovered via API, not hardcoded
- [ ] PAT tokens stored in localStorage only, never in code
- [ ] WIQL returns work item IDs — preserved for drill-down links (Rule 81)
- [ ] Roster consumed from canonical roster.json (no inline name literals)
- [ ] If making estimates or cost claims, ran the Live-API probe (Rule DR-1) and stated confidence
