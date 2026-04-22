---
name: pm-data-readiness
description: |
  Data-Readiness-Gate workflow for deliverables that quote live project data — sprint counts, open-task totals, user counts, cost figures, license utilization. Forces in-thread verification via Azure DevOps MCP / CLI (or equivalent live source) before any estimate, claim, or KPI is finalized. Degrades gracefully when MCP/CLI is unavailable: in that case, the claim must be marked LOW CONFIDENCE with the assumption stated explicitly. Use when drafting estimates, status reports, or dashboards that quote counts/costs from a live system. For estimation math see pm-estimation. For WIQL/CLI recipes see pm-devops-integration. For the underlying data-quality lessons see Rule DR-1.


  <example>
  Context: User asks for an estimate based on live DevOps data
  user: "Estimate Phase 2 effort based on the open work items in the Wallet project"
  assistant: "I will use the pm-data-readiness skill. First I run the Azure DevOps probe to fetch the actual open-item count, record the timestamp, and only then produce the estimate. If the probe fails, I'll mark confidence LOW."
  <commentary>Core trigger — estimate depends on live counts.</commentary>
  </example>

  <example>
  Context: User drafts a cost report
  user: "What was our Udemy license utilization last quarter?"
  assistant: "I will use the pm-data-readiness skill — utilization is live data. I'll fetch from the Udemy Business admin portal (or cite the last exported CSV with its timestamp), then report with explicit source + freshness."
  <commentary>Cost / licence trigger — same rule applies to non-DevOps live sources.</commentary>
  </example>

  <example>
  Context: MCP unavailable
  user: "Estimate Q3 backlog based on current sprint velocity"
  assistant: "I will use the pm-data-readiness skill. Azure DevOps MCP is not currently reachable; I'll mark any velocity number as LOW CONFIDENCE and state the assumption. I will NOT fabricate a number."
  <commentary>Degraded-mode trigger — skill enforces honesty when probes fail.</commentary>
  </example>

  <example>
  Context: User asks why a number seems off
  user: "The 40 open items figure in this report — is that current?"
  assistant: "I will use the pm-data-readiness skill to re-probe live and compare against the reported figure; if stale, I flag the drift and recommend re-running the estimate."
  <commentary>Freshness-audit trigger.</commentary>
  </example>
license: "MIT"
metadata:
  version: "1.0.0"
  priority: 70
  model: opus
  filePattern:
    - "**/*estimation*"
    - "**/*proposal*"
    - "**/*status*"
    - "**/*dashboard*"
    - "**/*forecast*"
    - "**/*capacity*"
  bashPattern:
    - "az boards"
    - "az devops"
  promptSignals:
    phrases:
      - "estimate based on"
      - "open work items"
      - "sprint velocity"
      - "utilization"
      - "cost figure"
      - "live count"
      - "data readiness"
      - "probe the source"
      - "verify the number"
      - "before I commit to"
      - "based on current"
      - "based on actual"
    minScore: 6
---

# PM Data-Readiness Gate

Any estimate, status claim, or dashboard KPI that quotes live project data must be gated on an in-thread probe of that live source. Numbers invented from memory (even recent memory) become stale silently and destroy the reliability of every downstream artifact. This skill enforces probe-before-publish as a hard rule, and it enforces honest downgrade-to-LOW-CONFIDENCE when probes fail.

The underlying rule (DR-1) was added in v1.5.0 as a cross-cutting rule in `pm-estimation` and `pm-devops-integration`. This skill is the activatable workflow layer: when Claude notices a live-data claim in a draft, this skill walks the probe → verify → annotate procedure.

Related surfaces:

- `pm-estimation` owns the estimation math and SP/PM/velocity calculations. This skill ensures the inputs to that math are live.
- `pm-devops-integration` owns WIQL query syntax and the probe recipes. This skill calls them.
- `pm-dashboard-design` owns the "fetch timestamp, not live clock" rule for the rendered artifact (Rule 34). This skill ensures the underlying fetch actually happened recently.

## The Five Rules

### Rule DR-A: Probe Before Quote

Never quote a count, utilization, cost, or velocity number without running the live probe in the same thread. "~40 open items" without a probe is a guess.

Probe priorities (highest to lowest confidence):

1. **Live MCP call** (e.g., `mcp__plugin_devops_azure-devops__wit_query_by_wiql`) — preferred when available.
2. **CLI call** (`az boards query --wiql "..."`) — good fallback.
3. **Recent exported CSV** with timestamp ≤ 7 days old — acceptable for slow-moving data (e.g., budget allocations).
4. **Last known figure from a recent deliverable** with explicit date — LOW CONFIDENCE only; cite the deliverable.

If none of the above is available, go to Rule DR-D (Honest Downgrade).

### Rule DR-B: Record Provenance

Every live-data claim in a deliverable must include:

- The probe query (or export source).
- The timestamp the probe ran.
- The raw result count or figure.
- The confidence level (HIGH / MEDIUM / LOW).

Example, in a Data Source tab:

```
Open Work Items — KhairGate Wallet
  Query: SELECT [System.Id] FROM WorkItems WHERE [System.State] <> 'Closed' AND [System.AreaPath] UNDER 'KhairGate\Wallet'
  Probe: 2026-04-21 15:30 UTC (live MCP via wit_query_by_wiql)
  Result: 42 items
  Confidence: HIGH

```

### Rule DR-C: Freshness Budget

Different data types tolerate different staleness:

| Data type | Freshness budget | Notes |
|---|---|---|
| Open work items, sprint counts | 24 hours | Changes daily |
| Team velocity | 2 weeks (one sprint) | Derived from closed work over prior sprints |
| Cost / budget utilization | 7 days | Billing cycles don't change hourly |
| License utilization | 7 days | Roster changes slowly |
| Roster / team composition | 24 hours | A single join/leave matters |

If the most recent probe exceeds the freshness budget, re-run before quoting. If you can't re-run (source unavailable), downgrade confidence per Rule DR-D.

### Rule DR-D: Honest Downgrade

When the live probe is unreachable, refuse to fabricate a number. Two acceptable moves:

1. **State the gap explicitly.** Example: "Azure DevOps MCP unavailable at this time; Phase 2 effort estimate withheld until counts can be verified. Earliest deliverable: [date]."
2. **Use the most recent known figure with explicit freshness.** Example: "Based on 42 open items as of 2026-04-14 (7 days old; exceeds 24h freshness budget for this metric). Confidence: LOW. Recommend re-probing before finalizing."

Never acceptable:

- Inventing a plausible-looking figure ("approximately 40 items").
- Citing "recent" / "current" / "latest" without a specific date.
- Reusing a figure from an older deliverable without acknowledging the reuse and its timestamp.

### Rule DR-E: Probe-to-Deliverable Trace

Every live-data claim in the final deliverable must be traceable to a probe in the authoring session. A reader (or a future auditor) should be able to find:

- Where the probe ran (in-thread log, CI artifact, or Data Source tab).
- What the probe returned.
- How the deliverable's number derives from the probe (transformation, aggregation, filter).

For dashboards, this lives in the Data Source tab (Rule 30 of `pm-dashboard-design`). For reports and estimates, this lives in an appendix or footnote.

## Procedure

When this skill activates, walk the procedure:

1. **Identify live-data claims in the draft.** Scan for: numeric counts (`\d+ (items|tasks|bugs|users|hours)`), percentages tied to live systems (utilization, completion %), cost figures, velocity figures, team-size references. If the draft has none, this skill does not apply — exit.

2. **Classify each claim.** For each claim: What's the source (DevOps, cost API, CSV export, prior deliverable)? What's the freshness budget (Rule DR-C)?

3. **Run probes.** For each claim, run the appropriate probe:
   - DevOps counts: MCP `wit_query_by_wiql` with the relevant WIQL, or `az boards query` CLI.
   - Velocity: compute from closed work over N prior sprints (probe returns the closed list).
   - Cost: fetch from cost API or cite the CSV export timestamp.
   - Roster: consume the canonical `roster.json` (per pm-devops-integration Canonical Roster File pattern).
   Capture probe output verbatim in-thread.

4. **Verify freshness.** For each probe, compare its timestamp to the freshness budget. Re-run if stale.

5. **Annotate the deliverable.** Per Rule DR-B, add provenance to the draft: probe query, timestamp, raw result, confidence level. For dashboards, these go in the Data Source tab. For reports, they go in a footnote or appendix.

6. **Downgrade where needed.** If any probe failed or returned stale/unexpected results, apply Rule DR-D — explicitly state the gap and confidence level in the deliverable. Never hide the uncertainty.

7. **Pre-publish check.** Before handing the draft back, verify every live-data claim has provenance recorded. If any are missing, revisit steps 3–5 for those.

## Pre-Publish Self-Check

```
Data-Readiness Self-Check

[ ] Every live-data claim has a probe query recorded
[ ] Every probe has a timestamp ≤ its freshness budget (Rule DR-C)
[ ] Every claim has an explicit confidence level (HIGH/MEDIUM/LOW)
[ ] Failed probes resulted in honest downgrade (not fabricated numbers)
[ ] Probe results are traceable from the deliverable back to the authoring session
[ ] For dashboards: Data Source tab populated per pm-dashboard-design Rule 30
[ ] For estimates: the math shown derives from probe results, not memory

```

## When Not To Activate

- Purely qualitative reports (no live counts or figures).
- Template or scaffold drafts that haven't been populated with data yet — the skill activates when data is added.
- Historical / retrospective analyses where the numbers are a snapshot of a past date (not a live claim). In that case, record the snapshot date explicitly and note that re-probing is not meaningful.
- Pure math exercises (e.g., "if we had N engineers, the person-months would be...") — those are parametric, not live-data claims.

## Delegation and Cross-References

- The `pm-estimation` skill references this skill's Data Readiness Gate as a pre-condition for any live-data estimate.
- The `pm-devops-integration` skill provides the probe recipes this skill calls.
- The `pm-report-reviewer` agent may flag unannotated live-data claims as part of its quality rubric (RQ-style checks on claims that look like they need provenance but lack it).

## MCP-First, CLI-Fallback, Never-Hook

This skill deliberately does its probes at authoring time via MCP or CLI, never via a hook. Reasons:

- Hooks run with tight timeouts; network probes regularly exceed them.
- PAT tokens in hook subprocesses are fragile — they can leak, they can fail auth silently, they can cause retries that double-count.
- Claude needs to react to probe failure with judgment (retry, degrade to LOW confidence, escalate to user) — a hook can only emit a warning string.

When the Azure DevOps MCP (or equivalent) is not loaded in the session, this skill's probes fall back to CLI via the Bash tool. When neither is available, Rule DR-D (Honest Downgrade) is the only correct response.

## Mistakes This Skill Prevents

| Lesson | Mistake | How this skill prevents it |
|---|---|---|
| 16 | "~40 open items" without probe | Rule DR-A forces probe-before-quote |
| 24 | Estimate built on assumed sprint count | Rule DR-A + DR-C ensures fresh probe |
| 286 | Reused stale cost figure from 2-month-old deliverable | Rule DR-C freshness budget + DR-B provenance |
| 292–293 | Dashboard shipped with unverified headline KPI | Rule DR-E probe-to-deliverable trace |
| 354–356 | "Current" / "latest" without timestamp | Rule DR-B explicit timestamp |
