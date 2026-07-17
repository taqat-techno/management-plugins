---
name: pm-source-provenance
description: |
  Source-provenance gate for ANY load-bearing fact about to enter a deliverable — a number, name, date, count, status, version, owner, or repo-visibility flag. Requires every such fact to carry a NAMED source consulted in the current turn (live API result, source-file read this turn, screenshot, or the user's own words) and flags any fact whose real source is memory/assumption or the WRONG typed source. Complements pm-data-readiness (which owns the freshness of LIVE counts/costs/velocity) by covering the broader right-source-for-any-fact discipline plus the recurring wrong-source anti-patterns. Use before finalizing any report, dashboard, email, proposal, or status that asserts facts a reader will act on. This is the activatable layer of Operating Discipline (2) in the global CLAUDE.md.

  <example>
  Context: A status line about to be written from memory.
  user: "Add a line saying the Wallet sprint has 40 open items."
  assistant: "I'll apply pm-source-provenance: 40 is a load-bearing count. Its canonical source is live DevOps (via pm-data-readiness), not memory — I'll probe before writing it, or mark it LOW CONFIDENCE."
  <commentary>Memory-sourced number → must be SOURCED, blocked, or downgraded.</commentary>
  </example>

  <example>
  Context: Course stats copied from a saved-page sidebar.
  user: "The course has 91 lectures — put that in the dashboard."
  assistant: "pm-source-provenance flags a wrong-source risk: saved-page sidebars and downloaded HTML often show a different/stale value than the live render. I'll re-read the live page (Playwright) before committing the count."
  <commentary>WRONG typed source → escalate to the canonical source before publishing.</commentary>
  </example>

  <example>
  Context: An owner name inferred from a CC list.
  user: "Who owns this? Put their name on the action item."
  assistant: "pm-source-provenance: owners come from the team directory + git identity, never a CC list or an AI placeholder name. I'll resolve against the directory before publishing the name."
  <commentary>Identity fact → authoritative directory, not inference.</commentary>
  </example>

  <example>
  Context: Reusing a figure from a self-dated snapshot.
  user: "Use last week's utilization number in the board pack."
  assistant: "pm-source-provenance: that snapshot carries its own as-of date older than tolerance for a board figure — I'll escalate to a live fetch (or label it explicitly 'as of <date>') rather than silently presenting a stale number as current."
  <commentary>Stale-self-dated source → escalate to live or disclose the as-of date.</commentary>
  </example>
license: "MIT"
metadata:
  version: "1.0.0"
  priority: 72
  model: opus
  filePattern:
    - "**/reports/**"
    - "**/deliverables/**"
    - "**/dashboards/**"
    - "**/proposals/**"
    - "**/*status*"
    - "**/*report*"
    - "**/*dashboard*"
    - "**/*board*"
  promptSignals:
    phrases:
      - "put that in"
      - "add a line saying"
      - "the count is"
      - "how many"
      - "the number is"
      - "who owns"
      - "the status is"
      - "the version is"
      - "according to my notes"
      - "is it current"
      - "from memory"
      - "i think it was"
    minScore: 6
---

# PM Source-Provenance Gate

Every load-bearing fact that enters a stakeholder-visible artifact must be traceable to a **named source consulted in the current turn**. The single most-repeated failure in the cross-project corpus is a number/name/date/status that ships as fact while it was actually recalled from memory, copied from a stale or wrong-typed source, or invented. Once published, it propagates across versions and into board reports, and the error surfaces only when a director challenges it.

This skill is the authoring-time gate. For the **freshness of live data specifically** (sprint counts, costs, utilization, velocity) defer to `pm-data-readiness`; this skill is the broader discipline that covers **any** load-bearing fact and the wrong-source anti-patterns.

## The rule

Before writing any load-bearing fact, classify its provenance into exactly one of:

- **SOURCED** — backed by a named source touched this turn: a live API/tool result, a file read this turn, a screenshot, or the user's own words. Cite it inline where the reader benefits.
- **MEMORY-ONLY** — the only basis is recall/assumption. **Do not publish.** Either fetch the real source, or write the honest placeholder (`NO DATA` / `TBD` / `PLANNED` / "as of <date>") — never a confident number.
- **WRONG-SOURCE** — a source exists but it is the wrong *type* for this fact. Escalate to the canonical source before publishing.

## Fact-Source Provenance Map (canonical source per fact-type)

| Fact type | Canonical source (use this) | Wrong source to avoid |
|---|---|---|
| Course / page stats | the **live** page render (Playwright) | a saved/downloaded HTML, the sidebar of a saved page |
| Video / media duration | the platform's own duration field | reading-time treated as video-time |
| Project status / open-item counts | OKR / live DevOps (via pm-data-readiness) | memory, a prior report |
| Sprint dates / iterations | DevOps `_settings/work` or live iterations API | a remembered cadence |
| Closure month / reporting date | `Custom.ClosureDate` | `System.ChangedDate`, a guess |
| "Dev did the work" | the work item's revision history | the current assignee |
| Entity identity (project/team/person) | project GUIDs / area paths / team directory | display names, a CC list, AI placeholder names |
| Repo visibility | `gh repo view --json visibility` | memory of how it was set up |
| App version | `app.getVersion()` / the manifest | a hardcoded string |
| Owner / role / title | team directory + git identity | a CC list, a signature block, an invented name |

## Wrong-source anti-patterns (the recurring traps)

- A **saved/downloaded page** shows a different or stale value than the live render — re-fetch live.
- **Reading-time vs video-duration** confusion in course/media stats.
- A **CC list, signature, or AI placeholder name** treated as the owner — resolve against the directory.
- A **self-dated snapshot** reused past its freshness budget — escalate to live, or disclose the as-of date.
- A **WIQL/page-capped count** reported as the true count — reconcile against a second method (e.g. an OData aggregate) for any "how many".

## Procedure

1. Scan the draft for load-bearing facts (numbers, names, dates, statuses, versions, owners, visibility).
2. For each, name its source. If the source is memory → fetch or downgrade. If it is the wrong type → escalate per the map.
3. Where the reader benefits (board/exec/external), cite the source and, for any live figure, the fetch timestamp.
4. If a probe is impossible this turn, mark the figure LOW CONFIDENCE and state the assumption — never fabricate.

## Related surfaces (no duplication)

- `pm-data-readiness` — owns probe-before-quote and honest-LOW-CONFIDENCE for **live** counts/costs/velocity. This skill calls it for those fact-types and covers everything else.
- `pm-devops-integration` — owns the WIQL/CLI probe recipes and identity/GUID resolution.
- `pm-report-writing` / `pm-dashboard-design` — own how the cited figure and its timestamp are rendered.

## Source lessons

#16, #24, #142, #145, #148, #149, #150, #161, #266, #286, #292, #293, #326, #345, #355, #910 (and the global-CLAUDE.md Operating Discipline (2)).
