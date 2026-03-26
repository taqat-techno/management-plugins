---
name: pm-report-writing
description: |
  PM report and document quality standards — enforces specificity, self-explanatory cells, consistent labels, title consistency, acronym expansion, two-audience awareness, and stakeholder email drafting with 3-version pattern. Use when generating status reports, proposals, email drafts, board presentations, or any table-based PM deliverable.


  <example>
  Context: User asks to write a status report
  user: "Write a status report for the training program across departments"
  assistant: "I will use the pm-report-writing skill to generate a report with specific labels (platform names, phase details), consistent status markers across all rows, and self-explanatory cells."
  <commentary>Core trigger - status report generation with quality enforcement.</commentary>
  </example>

  <example>
  Context: User asks to draft an email to stakeholders
  user: "Draft an email to the managers about the project update"
  assistant: "I will use the pm-report-writing skill to provide 3 email versions (formal, concise, action-oriented) with 'Dear All' addressing, and bullet-pointed attachment descriptions."
  <commentary>Email drafting trigger - 3-version pattern with attachment listing.</commentary>
  </example>

  <example>
  Context: User asks to create a project summary table
  user: "Create a summary table of all department progress"
  assistant: "I will use the pm-report-writing skill to ensure every cell is self-explanatory, status labels are identical across rows for the same state, and no cell requires the author to explain it."
  <commentary>Table quality trigger - consistent labels and standalone cells.</commentary>
  </example>

  <example>
  Context: User asks to prepare a proposal document
  user: "Prepare a project proposal for the board"
  assistant: "I will use the pm-report-writing skill to ensure the document stands alone — every term is defined, every number has context, and the reader doesn't need the author in the room."
  <commentary>Proposal trigger - standalone document quality.</commentary>
  </example>
license: "MIT"
metadata:
  version: "1.2.0"
  priority: 80
  model: sonnet
  filePattern:
    - "**/researches/**"
    - "**/reports/**"
    - "**/deliverables/**"
    - "**/tasks/**"
    - "**/proposals/**"
  bashPattern: []
  promptSignals:
    phrases:
      - "write report"
      - "draft email"
      - "status update"
      - "prepare summary"
      - "stakeholder communication"
      - "project update"
      - "progress report"
      - "send email"
      - "board report"
      - "CEO report"
      - "board presentation"
      - "monthly report"
      - "performance report"
    minScore: 6
---

# PM Report Writing Standards

## Core Principles

Every document you generate must pass this test: **Can the reader (CEO, Operations Manager, Engineering Manager) understand every cell, label, and status without the author in the room?**

## Rule 1: Be Specific, Not Vague

| Bad | Good |
|-----|------|
| "Core training completed" | "Udemy training completed" |
| "System configured" | "Azure DevOps board configured with 4 sprints" |
| "Meeting held" | "Kickoff meeting with 12 attendees on Mar 15" |
| "Tools set up" | "Jenkins CI/CD pipeline deployed to staging" |

Always name the platform, tool, system, or deliverable explicitly.

## Rule 2: Reports Must Stand Alone

The reader should NEVER need the author present to explain what a cell means. Before finalizing any document, read each cell and ask: "Would someone unfamiliar with this project understand this?"

If the answer is no, rewrite it with:
- Full context (not abbreviations)
- Specific quantities (not "some" or "several")
- Named deliverables (not "the document")

## Rule 3: Every Cell Self-Explanatory

For tables, EVERY cell must be independently comprehensible:
- No empty cells or `--` for completed items
- No ambiguous abbreviations without first defining them
- No cell that requires cross-referencing another cell to understand

## Rule 4: Same State = Same Label

When multiple rows/departments share the same status, use IDENTICAL wording:

| Bad | Good |
|-----|------|
| Row 1: "Phase completed" | Row 1: "Training completed" |
| Row 2: "Training done" | Row 2: "Training completed" |
| Row 3: "Finished" | Row 3: "Training completed" |

Scan all rows in the same column and enforce identical labels for identical states.

## Rule 5: No Lazy Status Labels

Never use these without specifics:

| Banned | Replacement |
|--------|-------------|
| "Ongoing" | "Phase 2: User acceptance testing (target: Apr 15)" |
| "In Progress" | "Sprint 3/6: 14 of 22 stories completed (64%)" |
| "Continues independently" | "Certification prep continues independently (lab practice & exam scheduling)" |
| "TBD" | "Phase 2: scope to be defined in Apr 5 planning session" |

Every status must show **intentional planning**, not vagueness.

## Email Drafting Standards

### Rule: Always Provide 3 Versions

When drafting emails for stakeholders, always provide:

1. **Formal** — Full detail, structured sections, suitable for board/executive audience
2. **Concise** — Professional but brief, suitable for busy managers
3. **Action-oriented** — Direct, focuses on what the reader needs to do next

### Addressing

- **Multiple managers**: Use "Dear All" — avoids hierarchy issues. Let To/CC fields handle addressing.
- **Single recipient**: Use their title + name ("Dear Dr. Ahmad")

### Attachments

NEVER just say "please find attached." Always list what the attachment contains:

```
Attached: Q1 Progress Report
- Department-level training completion status (5 departments)
- Budget utilization summary (82% of allocated)
- Risk register with 3 open items
- Next quarter timeline and milestones
```

## Rule 6: Two-Audience Report Pattern (Rule 133 from memory)

The same project data often serves two different audiences. Never mix them in one document:

| Aspect | Internal Performance Report | CEO/Board Report |
|--------|---------------------------|------------------|
| **Audience** | Engineering Manager, Team Leads | CEO, Board, Operations Manager |
| **Individual hours** | Yes — per-developer breakdown | No — project-level only |
| **Bug details** | Full list with assignees | Count + trend only |
| **Rankings** | Developer scorecard, velocity per person | Team-level KPIs |
| **Tone** | Analytical, data-heavy | Executive summary, achievements + risks |
| **Signature** | IT Project Manager | Matching current governance structure |

When asked to "create a report," always clarify the audience first. If both audiences need it, create two separate documents from the same data source.

## Rule 7: Title Consistency (Rules 119, 133)

Use the exact same job title in every occurrence within a document:

| Bad | Good |
|-----|------|
| Header: "IT Project Manager" / Footer: "PM" | Both: "IT Project Manager" |
| Signature: "Project Manager" / Meta: "IT PM" | Both: "IT Project Manager" |

Check these locations: page header, signature block, print summary, meta tags, author fields. Title mismatches erode credibility in board-facing reports.

## Rule 8: Spell Out Acronyms for Board (Rule 132)

CEO and Board members don't share internal jargon. Every acronym must have its full form nearby:

| Bad | Good |
|-----|------|
| "OKR & KPI Dashboard" | "Objectives & Key Results (OKR) & Key Performance Indicators (KPI) Dashboard" |
| "BMS Integration" | "Building Management System (BMS) Integration" |
| "WIQL Query" | "Work Item Query Language (WIQL) Query" |

The abbreviated form is for navigation (tabs, sidebar). The full form is for comprehension (headers, titles).

## Rule 9: Categorize by Participants, Not Keywords (Rule 134)

When assigning topics or email threads to project categories:

```
BAD:  "Terms and Conditions (English)" → Relief Center (keyword match on "Terms")
GOOD: Check participants (Dr. Bahaa, Hacene, Syed) → BMS/KhairGate (correct project)
```

Always check the participant list before assigning. Keywords are ambiguous; people are not.

## Rule 10: Embed Update Process in Deliverable (Rule 137)

If a report has a recurring update workflow, document it inside the report itself:

```html
<div class="info-card">
    <h4>How This Report Gets Updated</h4>
    <ol>
        <li>Export inbox_emails.csv and sent_emails.csv from Outlook</li>
        <li>Run topic_summary.py to generate topic_summary.csv</li>
        <li>Open this HTML and click "Update Data" on the Dashboard tab</li>
        <li>Review new topics and assign to correct project categories</li>
        <li>Save and distribute via Teams</li>
    </ol>
    <p><strong>Schedule:</strong> Every Thursday before weekly meeting</p>
</div>
```

Anyone opening the report should understand how it gets updated without needing external documentation.

## Quality Checklist (Run Before Finalizing)

Before completing any PM document, verify:

**Content Quality**
- [ ] Every cell is self-explanatory without the author present
- [ ] Same state uses identical wording across all rows
- [ ] No "Ongoing" / "TBD" / "In Progress" without specific next steps
- [ ] Platform/tool/system names are explicit (not generic)
- [ ] Numbers have context (not just "15" but "15 of 22 completed")

**Consistency & Audience**
- [ ] Abbreviations defined on first use (especially for board audience)
- [ ] Same job title used consistently throughout (header, signature, meta)
- [ ] Two-audience split considered (internal detail vs board summary)
- [ ] Topic categorization verified by participants, not keywords

**Emails**
- [ ] 3 versions provided (formal, concise, action-oriented)
- [ ] Attachments listed with bullet points describing contents

**Recurring Reports**
- [ ] Update workflow embedded in the deliverable itself
