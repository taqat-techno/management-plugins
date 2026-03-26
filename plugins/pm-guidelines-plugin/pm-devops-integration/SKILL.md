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
  version: "1.0.0"
  priority: 70
  model: sonnet
  filePattern:
    - "**/*dashboard*"
    - "**/*devops*"
    - "**/*sprint*"
    - "**/*wiql*"
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

## DevOps Integration Checklist

Before delivering any DevOps-connected dashboard:

- [ ] Queried actual states via States API (not assumed)
- [ ] Separate WIQL queries per work item type (Task/Bug/Enhancement)
- [ ] Uses `[Microsoft.VSTS.CMMI.Blocked]` field, not tags
- [ ] Projects discovered via API, not hardcoded
- [ ] PAT tokens stored in localStorage only, never in code
- [ ] WIQL returns work item IDs — preserved for drill-down links (Rule 81)
