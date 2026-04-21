---
name: pm-context-boundary
description: |
  Boundary-scrub workflow for deliverables crossing from internal to external audiences — board presentations, client-facing shares, vendor handoffs, cross-team handoffs. Scrubs internal WI IDs, WIQL fragments, internal URLs, project codenames, unapplied email directives, and draft-marked documents. Blocks publishing until every flag is resolved or acknowledged. For report-writing rules see pm-report-writing. For session-end reminder see pm-session-discipline.


  <example>
  Context: User wants to finalize a deliverable for the board
  user: "Finalize the Q2 report for the board meeting"
  assistant: "I will use the pm-context-boundary skill. Board is an external audience; I will run the boundary-scrub before treating this as final."
  <commentary>Core trigger — board delivery requires internal-term scrub.</commentary>
  </example>

  <example>
  Context: User wants to share a dashboard with a client
  user: "Send this dashboard link to the client"
  assistant: "I will use the pm-context-boundary skill — external send requires scrub of internal IDs, WIQL fragments, and directive sync."
  <commentary>External send trigger — classic leakage surface.</commentary>
  </example>

  <example>
  Context: User wants to hand off work to a vendor
  user: "Hand off the spec to the vendor team"
  assistant: "I will use the pm-context-boundary skill — vendor handoff is a boundary crossing; I will scrub internal tooling names and unreleased feature references."
  <commentary>Vendor handoff trigger — less public than a board but still external.</commentary>
  </example>

  <example>
  Context: User drafts an internal-only status update
  user: "Draft internal status update for the team"
  assistant: "I will use pm-report-writing. pm-context-boundary does not activate — audience is internal."
  <commentary>Anti-trigger — skill should NOT activate for purely internal content.</commentary>
  </example>
license: "MIT"
metadata:
  version: "1.0.0"
  priority: 80
  model: opus
  filePattern:
    - "**/external/**"
    - "**/client/**"
    - "**/public/**"
    - "**/board/**"
    - "**/*external*"
    - "**/*client*"
    - "**/*board*"
    - "**/*final*"
  bashPattern: []
  promptSignals:
    phrases:
      - "send to client"
      - "external delivery"
      - "board presentation"
      - "board meeting"
      - "CEO review"
      - "customer-facing"
      - "send to stakeholder"
      - "finalize for client"
      - "external email"
      - "hand off to"
      - "share with vendor"
      - "publish externally"
      - "vendor handoff"
      - "client review"
    minScore: 6
---

# PM Context-Boundary Standards

Deliverables that cross a context boundary — internal → external, dev → client, team A → team B, single-project → portfolio — are the highest-risk surface for accidental leakage. Internal work-item IDs appear in client proposals. WIQL queries sit in dashboard Data Source tabs that get forwarded. Exec directives ("don't mention X") never make it into the document because nobody checked.

This skill runs a structured scrub before any external deliverable goes out the door. Blocking by default; the user must resolve or explicitly acknowledge each flag before publishing.

Related skills: `pm-report-writing` (general content rules, three-version email pattern), `pm-session-discipline` (end-of-session reminder to verify scrub ran), `pm-report-reviewer` agent (delegates boundary checks via RQ-12).

## The Seven Rules

### Rule CB-01: Internal ID Scrub

Grep the deliverable for internal work-item patterns and flag every occurrence with line number:

```
\bWI-\d+\b
\bTASK-\d+\b
\b[A-Z]{2,5}-\d+\b        (project-prefix tickets, e.g., KG-234, BMS-1019)
\b#\d{4,}\b               (raw ticket numbers, e.g., #1234)
```

These are development-team shorthand. Clients don't know what WI-12458 refers to and shouldn't see it.

Exception: when a ticket ID has been explicitly approved for client visibility (the client uses the same DevOps instance, for example), the user can acknowledge and proceed.

### Rule CB-02: WIQL Fragment Scrub

Grep for WIQL syntax markers. These betray dev-tooling internals:

```
\bSELECT\b                 (inside an HTML code block or plaintext)
FROM WorkItems
\[System\.
\[Microsoft\.VSTS\.
@Me
AssignedTo
\bIterationPath\b
\bAreaPath\b
```

A Data Source tab containing "exact queries" (encouraged by `pm-dashboard-design` for internal transparency) becomes a liability when the dashboard is shared externally. The scrub catches this.

### Rule CB-03: Internal URL Scrub

Grep for URL patterns that betray internal systems:

```
\*\.internal\.\w+           (e.g., dashboard.internal.company.com)
dev\.azure\.com/[^/]+/_apis
teams\.microsoft\.com/l/meetup-join/
slack\.com/archives/
localhost:\d+
127\.0\.0\.1
file:///
```

Also inspect `href` attributes, not just visible text. Links labeled "read more" can hide Teams deep links.

### Rule CB-04: Project Codename Scrub

If a `.project-name` file exists in the deliverable's nearest ancestor folder, read it. Otherwise, derive the project from the folder name.

Grep the deliverable for mentions of OTHER project names (from a known list: KhairGate, Relief Center, Afriqat, Herbal Gardens, Alaqraboon, Wallet, HUB, BMS, Property Management, Pearl Pixels, plus any in the user's in-thread context).

Flag each occurrence. Exception: portfolio / multi-project / cross-program reports legitimately cross-reference — suppress this rule when the document title or H1 matches `/portfolio|multi-project|cross-program/i`.

### Rule CB-05: Email Directive Sync

Ask the user explicitly:

> Any recent email directives from the approver about this deliverable? Paste them here, or confirm none.

Parse the pasted text for imperatives:

- "don't mention X"
- "remove Y"
- "replace A with B"
- "defer announcement of Z"
- "emphasize that ..."
- "cut the section on ..."

For each directive, grep the document to verify it was actually applied:

- `don't mention Salesforce migration` → grep for `Salesforce`, `migration`; if found, flag.
- `replace "Phase 1" with "Initial Phase"` → grep for `Phase 1`; if found, flag.

Unapplied directives are the most common high-severity leakage: the user got the email but forgot to update the doc.

### Rule CB-06: Unreleased Feature Scrub (optional config)

If `.pm-context/unreleased-features.txt` exists in the project, read it line by line. Each line is a feature codename or name that must not appear externally. Grep and flag.

When the config doesn't exist, skip this rule — no false positives from guessing.

### Rule CB-07: Draft Status Gate

Confirm the document status is "Final" / "Approved" / equivalent, not "Draft" / "WIP" / "TBD". External audiences should never receive a document marked Draft.

Detection patterns:

- Status table cell containing `Draft`, `WIP`, `In Progress`, `TBD`, `Tentative`
- Filename ending in `-draft`, `-wip`, `-v0`
- Document Control table showing the latest revision as "Draft"

## Procedure

When this skill activates, walk the procedure:

1. **Identify the deliverable and target audience.** If audience is ambiguous, ASK: "Is this going to the board, a client, another team, a vendor, or an external stakeholder?"
2. **Run CB-01 through CB-04 in order.** Collect all flags with line numbers.
3. **Invoke CB-05.** Prompt the user for recent email directives; parse and verify.
4. **Run CB-06** if the config file exists.
5. **Run CB-07.** Confirm document status.
6. **Produce the scrub report** in this exact format:

```
## Boundary Scrub Report — <file>

**Target audience:** <board | client | vendor | other-team>

### Findings
| Rule | Severity | Item | Line | Suggested fix |
|---|---|---|---|---|
| CB-01 | Critical | `WI-12458` | 87 | Remove or replace with client-safe label |
| CB-02 | Critical | `[System.AssignedTo]` | 204 | Remove WIQL fragment from Data Source tab |
| CB-05 | Critical | Directive "don't mention Salesforce" — found "Salesforce migration" | 124 | Apply directive or confirm override |

### Verdict
<BOUNDARY CLEAR | ISSUES FOUND — N items>
```

7. **If ISSUES FOUND, block delivery** until each item is resolved or explicitly acknowledged by the user ("This WI-ID is intentional — it's been approved for client visibility"). Record acknowledgments.

## Optional Project Conventions

This skill degrades gracefully when these files are absent. They are optional but improve accuracy:

- `.project-name` — single-line project identifier (e.g., `KhairGate Wallet`) in the project root.
- `.pm-context/internal-terms.txt` — newline-separated blocklist of internal terms specific to this project.
- `.pm-context/unreleased-features.txt` — newline-separated blocklist of unreleased feature names.
- `.pm-context/approved-externally.txt` — newline-separated allowlist of internal-looking terms that HAVE been approved for external visibility (so they're not flagged).

When a project uses these conventions, record it in the project's CLAUDE.md so the convention persists.

## When Not To Activate

- Draft-internal status updates, team-only memos, session logs. Internal audiences legitimately see WI IDs and WIQL.
- Code review / PR description context. That's GitHub / DevOps, not external.
- Personal notes, memory files, CLAUDE.md. Those are internal by nature.
- Portfolio reports titled as such (Rule CB-04 exception) — multi-project cross-reference is their whole purpose.

## Edge Cases

- **Internal Teams/Slack deep links hidden inside `<a href>` anchors.** CB-03 must inspect the href attribute value, not only the visible link text.
- **Screenshots embedded as base64 blobs.** Flag any base64 blob >10KB and ask the user to confirm it's client-safe; embedded screenshots sometimes show an internal dashboard in the background.
- **Bilingual EN/AR content.** Scrub both language spans. A WI ID in the Arabic span is just as leaky as one in the English span.
- **Quoted email threads inside the deliverable.** If the deliverable embeds a forwarded email thread, scrub that content too — historical ticket IDs in a quoted email are still external exposure.
- **Meeting recordings linked by SharePoint URL.** SharePoint URLs often contain internal tenant IDs — flag these under CB-03.
- **CSV/JSON exports attached alongside the deliverable.** Ask whether those attachments were also scrubbed. Often they aren't.

## Mistakes This Skill Prevents

| Lesson | Mistake | How this skill prevents it |
|---|---|---|
| 35 | Internal WI IDs in client proposal | CB-01 |
| 277 | Dev-team codename in executive report | CB-04 |
| 282 | WIQL query string in client dashboard Data Source tab | CB-02 |
| 337–343 | Exec emailed "don't mention X"; doc still had it | CB-05 |
| 357–362 | Internal Teams channel URL in external PDF | CB-03 |
| 370–374 | Unreleased feature name in customer-facing slide | CB-06 (with config) |
