---
name: pm-standalone-updater
description: |
  Enhanced standalone auto-updater and UX redesign standards — versioned folder management, Document Control table enforcement, BA review loops, PowerShell safety, page type navigation, and kickoff package discipline. Use when working on standalone versions, kickoff packages, auto-updater scripts, or version drift fixes.


  <example>
  Context: User wants to update a standalone version after Hub V2 pull
  user: "Pull latest from Hub V2 and update the standalone"
  assistant: "I will use the pm-standalone-updater skill to create a new versioned folder, audit ALL internal content (not just headers), and update Document Control tables with current commit hash."
  <commentary>Core trigger - standalone version update requiring deep audit beyond surface changes.</commentary>
  </example>

  <example>
  Context: User wants to prepare a kickoff package
  user: "Prepare the kickoff package for the board presentation"
  assistant: "I will use the pm-standalone-updater skill to ensure only latest report versions are included, Phase 0 vs full program is distinguished, and no Hub V2 pages are copied into standalone."
  <commentary>Kickoff package trigger - curating correct artifacts with version discipline.</commentary>
  </example>

  <example>
  Context: User wants to create an auto-updater script
  user: "Build a script that checks for Hub V2 drift and applies updates"
  assistant: "I will use the pm-standalone-updater skill to build a PowerShell script with ASCII-safe strings, a companion .bat launcher, and separated Check/Pull+Update/Audit buttons."
  <commentary>Auto-updater script trigger - PowerShell safety and UX button design.</commentary>
  </example>

  <example>
  Context: User is doing a BA review cycle
  user: "Review the standalone files Mohamed updated"
  assistant: "I will use the pm-standalone-updater skill to run a BA review loop — checking Document Control tables, internal content accuracy, and tracking the review pass number."
  <commentary>BA review trigger - review loop with pass tracking.</commentary>
  </example>
license: "MIT"
metadata:
  version: "1.0.0"
  priority: 75
  filePattern:
    - "**/standalone*"
    - "**/kickoff*"
    - "**/auto-update*"
    - "**/version*"
    - "**/*updater*"
    - "**/*drift*"
  bashPattern: []
  promptSignals:
    phrases:
      - "standalone update"
      - "kickoff package"
      - "version drift"
      - "document control"
      - "auto-updater"
      - "BA review"
      - "hub v2 pull"
      - "version folder"
      - "powershell script"
    minScore: 6
---

# PM Standalone Auto-Updater & UX Standards

## Core Principle: Surface Updates Are NOT Enough (Rule 53)

After every Hub V2 pull, audit **ALL** internal content:

| What to Audit | Why |
|---------------|-----|
| Document Control tables | Version, date, data source must match current folder |
| Assumptions & constraints | Hub V2 may have changed scope or budget |
| Risk descriptions | New risks or changed severity |
| Internal text references | Page counts, story counts, status claims |
| KPI strips & metrics | Values may have drifted |

V5-V10 missed this completely by only checking headers/footers/KPIs.

## Version Management

### Each Pull with Drift = New Folder (Rule 54)

Never edit an existing version in place. Each version is a frozen snapshot:

```
standalone/
├── v10/    # Frozen
├── v11/    # Frozen
├── v12/    # Current — new folder after latest pull
```

Copy folder, increment version, apply fixes.

### Document Control Tables (Rule 57)

Every file in every version must have current:

| Field | Required Value |
|-------|---------------|
| Version | Must match folder version (e.g., "v12") |
| Updated | Specific date: "25 Mar 2026" (not "March 2026") |
| Data Source | Commit hash from Hub V2 (e.g., `abc1234`) |

### Footer Date (Rule 58)

`Modified: DD Mon YYYY` — not generic month. Every file, every version.

## Content Ownership Rules

### Create Own Reports (Rule 55)

PM creates own variance/story reports based on **previous PM template**. Hub V2 reports are Mohamed's internal documents with different branding. Never copy them.

### Hub V2 Pages Don't Belong in Standalone (Rule 56)

Only PM-created artifacts go in the standalone folder. Hub V2 pages (health-dashboard, etc.) are **linked via nav**, not copied.

### Old Reports Don't Belong in Kickoff (Rule 60)

Only latest variance + story variance versions. Remove historical snapshots (v10, v11, v1, v2).

## Phase & Program Distinction (Rule 59)

Budget, Timeline, and Hiring show full 22-month program, but kickoff is Phase 0 only. Both must be shown clearly:

```html
<div class="phase-0">
    <h3>Phase 0 — Kickoff (Current)</h3>
    <!-- Phase 0 specific scope, budget, timeline -->
</div>
<div class="full-program">
    <h3>Full Program (22 months)</h3>
    <!-- Complete program overview -->
</div>
```

## BA Review Loop (Rule 61)

BA Review is a **loop**, not one-shot:

```
Pass 1: Mahmoud reviews → finds issues
Pass 2: Mohamed fixes → Mahmoud re-verifies
Pass 3: (if needed) → loop until no critical issues
```

Track pass number in Document Control or review notes. Document what was found and what was fixed in each pass.

## Session Discipline

### Read Lessons BEFORE Executing (Rule 62)

At start of every session, read feedback files before touching any code. This prevents repeating past mistakes.

### Never Assume Git Author (Rule 63)

Check `git log`. `MahmoudEl-Afify` is not `Mahmoud Elshahed`. Always verify author identity from git history.

### Validate Claims Against Data (Rule 64)

Don't trust page counts, story counts, or status claims in Hub V2. Count actual files. Read actual KPI strips. Verify everything independently.

## Interactive UX Rules

### Shared localStorage Key (Rule 65)

All files using status buttons must share the **same** localStorage key (e.g., `kg-action-progress`). Labels must match across files:

```javascript
// All files read/write the same key
const STATE_KEY = 'kg-action-progress';
// ADR buttons: 3 states — "Pending Review" / "Accepted" / "Rejected"
// Must match exactly across all files
```

### Collapsed Resolved Sections (Rule 66)

Use `<details>` **without** `open` attribute for ALL RESOLVED / CLOSED sections. Focus on pending items:

```html
<!-- Pending: open by default -->
<details open>
    <summary>Pending Items (5)</summary>
    ...
</details>

<!-- Resolved: collapsed by default -->
<details>
    <summary>Resolved Items (12)</summary>
    ...
</details>
```

## PowerShell Safety (Rules 72-73)

### Em-Dash Crash (Rule 72)

Unicode characters (em-dash `---`, curly quotes) in PowerShell string literals cause **silent parse failures**. The window closes instantly with no error.

| Bad | Good |
|-----|------|
| `"section --- details"` | `"section -- details"` |
| `"it's ready"` (curly) | `"it's ready"` (straight) |

Always use ASCII alternatives.

### .bat Launcher Required (Rule 73)

"Right-click > Run with PowerShell" closes the window on any error. Always provide a companion `.bat` file:

```bat
@echo off
powershell -ExecutionPolicy Bypass -NoExit -File "%~dp0script.ps1"
pause
```

`-NoExit` keeps the window open so errors stay visible.

## Button State Design (Rule 74)

Separate actions by availability:

| Button | When Available | Color |
|--------|---------------|-------|
| Check for Updates | Always | Blue |
| Pull + Update | Only when drift detected | Green (grey when no drift) |
| Audit Only | Always | Purple |

Grey out unavailable actions. "Full Update" when already up-to-date is misleading.

## Automation Threshold (Rule 75)

If a check is missed **3+ times** across sessions, build a tool. Human checklists fail; scripts don't forget.

The auto-updater script exists because manual drift fixes repeatedly missed Document Control tables, assumptions, and internal content.

## Page Type Navigation (Rule 76)

Three page types define nav UX:

| Type | Color | Purpose | User Action |
|------|-------|---------|-------------|
| **Action** | Green | Interactive buttons for decisions | Click to decide |
| **Reference** | Blue | Read-only for board review | Read and discuss |
| **Audit** | Purple | Health history snapshots | Review trends |

Organize navigation by type, not by arbitrary categories. Directors need to know: "where do I click?" vs "where do I read?"

## Page Consolidation (Rule 77)

Two pages covering the same topic confuse the Director. **One source of truth per topic.**

If you create a summary page, merge it into the original rather than adding another file. Example: `KICKOFF_READINESS_GUIDE` + `KICKOFF_READINESS_VALIDATION` should be one page.

## Auto-Updater Checklist

Before delivering any standalone update or auto-updater script:

- [ ] ALL internal content audited (not just headers/footers)
- [ ] New versioned folder created (never edited in place)
- [ ] Document Control tables match folder version and date
- [ ] Footer shows specific date (DD Mon YYYY)
- [ ] Only PM-created artifacts in standalone (no Hub V2 copies)
- [ ] Only latest report versions in kickoff package
- [ ] Phase 0 vs full program clearly distinguished
- [ ] BA review pass number tracked
- [ ] PowerShell strings use ASCII only (no em-dashes/curly quotes)
- [ ] .bat launcher provided for every .ps1 script
- [ ] Buttons disabled when action unavailable
- [ ] Navigation organized by page type (Action/Reference/Audit)
- [ ] No duplicate pages covering same topic
