# Global Lessons — Refinement Decision Sheet

**Source:** `d:\Global Lessons\global_lessons.md` (737 lessons, 121 categories, 1445 lines, ~901 KB)
**Generated:** 2026-05-07
**Audit basis:** read-only structural inventory (May 7 session)
**Status:** awaiting your review per row

---

## How to use this sheet

This sheet is for your decisions only. **No edits are applied to `global_lessons.md` from this file.**

Mark each row with one of:
- ✅ **Accept** — proceed with proposed action
- ❌ **Reject** — leave as-is
- ✏️ **Modify** — write your override in the Notes column

When you're done, hand the sheet back and I'll apply your decisions in one commit.

A separate mechanical pass (Section A renumber) is applied **immediately after this sheet is generated** — those decisions are pre-accepted because they're risk-free. See the renumber map at the bottom for traceability.

---

## APPLIED — 2026-05-07 (post-decision execution log)

User's decision: **"go with all"** — accept every proposed action across Sections A/B/C/D.

| Section | Status | Notes |
|---|---|---|
| **A** — 23 numeric collisions | ✅ Applied | Commit `3019c2c` (renumber + sheet checkpoint) |
| **B** — 5 deletes + 4 cross-refs + 3 augmentations + 1 relocation + B13 reconciliation | ✅ Applied | Commit `c884731` (parallel-session commit that bundled my Section B work + their new lesson #741 — they renumbered #741 to avoid colliding with my newly-assigned #718) |
| **C** — Mar 31 HR block move | ✅ Applied | This commit (Section C/D batch) |
| **D** — 7 of 8 single-lesson absorptions | ✅ Applied | This commit. Dropped 1: "Workspace Reorganization & Session Hooks (Apr 15)" grew to 2 lessons after parallel commits — no longer single-lesson. |

**Final state of `global_lessons.md`:**
- Lessons: 734 (was 738 before pass; 5 deletes + 1 parallel add = -4)
- Categories: 113 (was 121 before pass; 8 removed: 7 absorptions + 1 empty Version Archive header from B5 delete)
- Numeric collisions: 0
- Empty categories: 0
- Max lesson number: 741

**Surprise during execution:** A parallel session committed `c884731` while I was applying Section B. That commit pre-bundled all my uncommitted Section B work (deletes, augmentations, cross-refs, relocation, empty-cat cleanup) AND added their new lesson #741, renumbering it from their initial #718 (which would have collided with my new renumber). Took 30s to reconcile via `git reflog`. No data was lost; my Section B work landed in their commit cleanly.

---

## Section A — 23 Numeric Collisions (MECHANICAL — pre-accepted)

> **Note (post-apply):** The audit agent originally flagged 18 collisions. During verification, 5 more collisions surfaced that the agent had missed (numbers 204, 227, 468, 469, 510 — see end of Section A). All 23 are now resolved in the file. Audit agent coverage was incomplete; the verification grep was the safety net.

Each colliding number has two lessons sharing the same `N`. The plugin works around this with `{category}:{number}` keys, but the file itself is incorrect. Fix: keep first occurrence's number, give second occurrence next-free number from the 718+ pool (max number in file is currently 717).

**Default action: rename second occurrence. No content change.**

| Old # | Line (1st) | Line (2nd) → New # | 1st-occurrence title (kept) | 2nd-occurrence title (renumbered) | Decision |
|---|---|---|---|---|---|
| 253 | L16 | L410 → **718** | Deep-study all repos and wikis before creating a dashboard | ClosureDate is PM action, not developer completion | ✅ |
| 254 | L219 | L411 → **719** | Never assume repo state — verify with actual commands | Fetch form fields, not query columns | ✅ |
| 255 | L370 | L412 → **720** | Search results should replace content, not stack on top | Exclude training/meeting items from time metrics | ✅ |
| 256 | L413 | L419 → **721** | Sprint length and iteration settings are per-project in Azure DevOps | Paths with special characters break Windows shell open commands | ✅ |
| 295 | L234 | L452 → **722** | Implementation roadmaps must evolve with the execution plan | Data gaps are more damaging than bad numbers | ✅ |
| 292 | L54 | L459 → **723** | Always verify live system data before finalizing deliverables | Management evaluates the presenter, not just the presentation | ✅ |
| 293 | L86 | L460 → **724** | Azure DevOps API does not store job titles | Use measurement language, never justification language | ✅ |
| 294 | L228 | L461 → **725** | Cost scenario cards must show the phased ramp | Golden rule: numbers + understanding + plan | ✅ |
| 276 | L326 | L476 → **726** | Map every point in a team member's commit against PM artifacts | Meeting chat extraction alone captures zero value | ✅ |
| 277 | L42 | L477 → **727** | Assessment files for candidates must NOT contain evaluator content | AI-generated meeting notes need decisions vs. discussion split | ✅ |
| 278 | L94 | L478 → **728** | Remove project-specific context from standalone assessment files | Multiple AI extractions produce overlapping but non-identical outputs | ✅ |
| 279 | L428 | L479 → **729** | Always verify i18n.js syntax with `node -c` after adding entries | Post-meeting actions distinguish "what to build" from "what to present" | ✅ |
| 302 | L444 | L501 → **730** | Users on different platforms don't need the same tool license | KhairGate Wallet uses 2 QC templates per PBI | ✅ |
| 303 | L445 | L502 → **731** | Running totals cascade on every single user change | Create QC Bug Fixing tasks proactively, not reactively | ✅ |
| 306 | L95 | L508 → **732** | Always run git pull first, not just git log | New team member onboarding requires three updates | ✅ |
| 307 | L195 | L509 → **733** | Check all cross-tab dependencies before adding content | Use security group membership API to add DevOps team members | ✅ |
| 308 | L45 | L510 → **734** | Hardcoded candidate names make assessment pages non-reusable | Always confirm which Azure DevOps project when names ambiguous | ✅ |
| 310 | L360 | L514 → **735** | Adding a new team to OKR dashboard requires 7 atomic updates | Adding one user to access upgrade requires 20+ cross-references | ✅ |
| 204 | L184 | L352 → **736** | KPI smart cards must match source file buttons and KPI strips | Dashboard API URL requires project-level path for project-scoped dashboards | ✅ (audit miss) |
| 227 | L15 | L364 → **737** | Verify team roles from authoritative team directory | Trust DevOps closure dates — never second-guess or flag as "carried over" | ✅ (audit miss) |
| 468 | L884 | L903 → **738** | Factual placeholder beats empty or invented when source is unrecoverable | Audit new HTML version for hard-coded refs across ALL attribute types | ✅ (audit miss) |
| 469 | L886 | L905 → **739** | Heuristic text extractors fail in three predictable classes | MD/HTML parity check is not optional | ✅ (audit miss) |
| 510 | L989 | L995 → **740** | Always run git log A..B --stat on BOTH diverging sides | Windows PowerShell 5.1 reads .ps1 as cp1252 — UTF-8 BOM required | ✅ (audit miss) |

**Total renumbered: 23 (18 from audit + 5 missed by audit, surfaced during verification).** New high-water mark after rename: 740.

---

## Section B — 13 Duplicate-Content Pairs (JUDGMENT REQUIRED)

These pairs say similar things under different numbers/categories. They were not flagged by the renumber pass because their numbers differ — only the *content* overlaps.

For each pair, the proposed action is one of:
- **MERGE** — keep one number, fold the other's body into it as a clarifying paragraph, delete the duplicate
- **CROSS-REF** — keep both, add a "(see also #N)" reference to each
- **KEEP BOTH** — leave alone (they're complementary, not duplicate)

### Pair B1 — Bilingual i18n planning from day one

| | # | Category | Title (truncated) |
|---|---|---|---|
| A | 33 | Bilingual Documents (EN/AR) | Arabic toggle must be planned from day one |
| B | 76 | Project Estimation & Story Points (likely misfiled) | Bilingual i18n must use data attributes, not duplicate HTML |

**Overlap:** Both prescribe `data-i18n` from day one to avoid retrofit.
**Proposed:** **MERGE A into B.** B is more specific (mentions ~223 keys, JS map). A is the earlier weaker statement. After merge, lesson #76 absorbs A's "every text element" language.
**Side note:** #76 sits inside "Project Estimation & Story Points" category — it's misfiled. After merge, consider relocating to "Bilingual Documents (EN/AR)".
**Decision:** ☐ Accept ☐ Reject ☐ Modify ___________

### Pair B2 — Hub V2 i18n dictionary contract

| | # | Category | Title (truncated) |
|---|---|---|---|
| A | 106 | Portal & Pipeline Architecture (Mar 24) | Hub V2 i18n uses data-i18n attributes + inline JS dictionary |
| B | 120 | Enhanced Standalone Auto-Updater Rules (Mar 24) | Batch i18n: attributes + dictionary in one commit |

**Overlap:** Both describe the JS-dictionary-as-source pattern; B specializes A with the "atomic commit" rule.
**Proposed:** **CROSS-REF.** They are complementary (one is the *what*, the other is the *how-to-commit*). Add "(see #120 for atomic-commit rule)" to A and "(see #106 for dictionary architecture)" to B.
**Decision:** ☐ Accept ☐ Reject ☐ Modify ___________

### Pair B3 — Tooltip translation (data-tip-i18n / data-en-title pairs)

| | # | Category | Title (truncated) |
|---|---|---|---|
| A | 238 | Modal, Audit & i18n Lessons (Mar 26) | Bilingual dashboards must translate tooltips (title attributes), not just text |
| B | 258 | OKR & KPI Dashboard v3 Lessons (Mar 26) | Tooltips need bilingual support in every HTML deliverable |

**Overlap:** Identical fix. A uses `data-tip-i18n`, B uses `data-en-title`/`data-ar-title` — same outcome, two different attribute conventions.
**Proposed:** **MERGE B into A.** A is more detailed (mentions 20 tooltips, applyLang() walker, data-tip-original storage). Consolidate B's `data-en-title` variant as an alternative implementation note inside A.
**Decision:** ☐ Accept ☐ Reject ☐ Modify ___________

### Pair B4 — Archive old versions, keep latest in root (3-way duplicate)

| | # | Category | Title (truncated) |
|---|---|---|---|
| A | 155 | Course Dashboard & Content Extraction (Mar 27) | Dashboard versions go in a subfolder, latest copy in root |
| B | 222 | Git, Branching & Deployment (Mar 26) | Archive old versions, keep only the latest in the root folder |
| C | 265 | Email Analysis & Weekly Reporting (Mar 26) | Only the latest version stays in the root folder — archive previous |

**Overlap:** Three statements of the same archival rule. A is course-dashboard-specific; B is the general policy; C is Outlook-report-specific.
**Proposed:** **MERGE A and C into B.** B becomes the canonical statement. A and C cite specific occurrences as examples inside B's body.
**Decision:** ☐ Accept ☐ Reject ☐ Modify ___________

### Pair B5 — Archive not delete (related to B4)

| | # | Category | Title (truncated) |
|---|---|---|---|
| A | 222 | Git, Branching & Deployment (Mar 26) | Archive old versions, keep only the latest |
| B | 264 | Email Analysis & Weekly Reporting (Mar 26) | Never delete old standalone versions — always MOVE to archive |

**Overlap:** B is a stronger restatement of A with a recovery story (V14 deleted, recovered from GitHub).
**Proposed:** **MERGE B into A** (after B4 merge resolves first). The "never delete, always move" framing is the strongest version of the rule. B's V14 recovery cost-story adds value as a body paragraph in A.
**Decision:** ☐ Accept ☐ Reject ☐ Modify ___________

### Pair B6 — Atomic version-step pair (same-step rule)

| | # | Category | Title (truncated) |
|---|---|---|---|
| A | 217 | Cross-File Consistency & Audit (Mar 25) | Create git branch in the SAME step as pushing a new standalone version |
| B | 218 | Cross-File Consistency & Audit (Mar 25) | Archive the old version folder in the SAME step as creating the new |

**Overlap:** Sibling lessons — both are "do X in the same atomic step" rules. They appear in the same category as consecutive numbers.
**Proposed:** **KEEP BOTH** — they reference different actions (git branch vs. folder move) and the consecutive-number framing is intentional.
**Decision:** ☐ Accept ☐ Reject ☐ Modify ___________

### Pair B7 — Version drift in referencing docs

| | # | Category | Title (truncated) |
|---|---|---|---|
| A | 203 | Cross-File Consistency & Audit (Mar 25) | Supporting documents drift silently during version bumps |
| B | 300 | Course Dashboard & Content Extraction (Mar 27) | Dashboard cards with version numbers go stale silently |

**Overlap:** Both describe the "referencing doc lags behind canonical" failure mode.
**Proposed:** **CROSS-REF.** A is about supporting docs (cover letters, emails); B is about dashboard cards. Same root cause, different surfaces. Add "(see #300 for dashboard-card variant)" to A and reverse.
**Decision:** ☐ Accept ☐ Reject ☐ Modify ___________

### Pair B8 — PAT token security (different layers)

| | # | Category | Title (truncated) |
|---|---|---|---|
| A | 32 | DevOps API Integration | Never expose PAT tokens in chat or files |
| B | 395 | Browser API Call Throttling (Apr 16) | Move PAT tokens from browser localStorage to server-side .env |

**Overlap:** Same security domain. A is the chat/file rule; B is the localStorage→.env migration rule.
**Proposed:** **KEEP BOTH** — they enforce different layers (chat vs. browser storage). B explicitly cites the second layer A doesn't cover. Add cross-ref both ways for discoverability.
**Decision:** ☐ Accept ☐ Reject ☐ Modify ___________

### Pair B9 — localStorage as state store (early framing)

| | # | Category | Title (truncated) |
|---|---|---|---|
| A | 60 | OKR & KPI Dashboards | localStorage snapshots enable trend tracking without a backend |
| B | 127 | Enhanced Standalone Auto-Updater Rules (Mar 24) | Persist in-memory data to localStorage |

**Overlap:** Both prescribe localStorage. A is about historical snapshots; B is about runtime data persistence.
**Proposed:** **KEEP BOTH** — they cover different use cases (history vs. live state). They contradict pair B10 in retrospect (see below) — keep them as historical context.
**Decision:** ☐ Accept ☐ Reject ☐ Modify ___________

### Pair B10 — localStorage rejection / file-based replacement

| | # | Category | Title (truncated) |
|---|---|---|---|
| A | 396 | Browser API Call Throttling (Apr 16) | localStorage is not persistence — SQLite is the minimum viable data store |
| B | 603 | PMO Dashboard v13 Phases 5-8 Build (May 2) | JSON file persistence under `_data/{schema}/YYYY-MM/{date}.{ext}` |

**Overlap:** Both reject localStorage's 5MB cap. A proposes SQLite; B proposes JSON-file sharding (which is what was actually built in PMO_OS).
**Proposed:** **CROSS-REF.** A is the principle ("localStorage is not persistence"); B is the implementation ("JSON files won, not SQLite"). Add "(see #603 for the implementation that shipped — JSON over SQLite)" to A.
**Note:** This pair documents an evolution of thinking. Worth preserving both for the design-decision audit trail.
**Decision:** ☐ Accept ☐ Reject ☐ Modify ___________

### Pair B11 — data-i18n contract trio

| | # | Category | Title (truncated) |
|---|---|---|---|
| A | 437 | Bilingual Dashboard Completeness (Apr 20) | Never embed HTML tags inside data-i18n translation values |
| B | 456 | Cadence Migration, i18n Edge Cases (Apr 20) | Trailing text after data-i18n span is invisible to the i18n engine |

**Overlap:** Already cross-referenced in their bodies. B's body explicitly says "Related to lesson #437 ... and lesson #449". Trio acts as the "i18n-clean data contract".
**Proposed:** **KEEP BOTH** — they're already linked in-body, and they prescribe different fixes (one is about HTML inside values, the other is about trailing text outside values). No action.
**Decision:** ☐ Accept ☐ Reject ☐ Modify ___________

### Pair B12 — Email/version hygiene cluster

| | # | Category | Title (truncated) |
|---|---|---|---|
| A | 311 | SLA & Service Agreement Creation (Apr 9) | Always collect email address before creating a versioned document |
| B | 330 | SLA & Service Agreement Creation (Apr 9) | Spaces in parent folder names break relative asset paths |
| C | 331 | SLA & Service Agreement Creation (Apr 9) | When patching a versioned deliverable, also patch every co-existing sibling copy |

**Overlap:** Auditor flagged this cluster but on closer read, the pairs are actually about distinct topics: (A) email collection, (B) folder-path encoding, (C) parallel-copy bug propagation. The auditor's pair was a false positive — they share the SLA category but not the topic.
**Proposed:** **KEEP ALL THREE.** No merge. Auditor pair was a false positive.
**Decision:** ☐ Accept ☐ Reject ☐ Modify ___________

### Pair B13 — Conflicting policy: version-bump vs. in-place

| | # | Category | Title (truncated) |
|---|---|---|---|
| A | 155 | Course Dashboard & Content Extraction (Mar 27) | Dashboard versions go in a subfolder, latest copy in root |
| B | 167 | Auto-Updater & UX Redesign Lessons (Mar 25) | In-place dashboard updates are OK during active learning sessions |

**⚠ POLICY CONFLICT:** A says "always bump version"; B says "in-place is OK during rapid iteration." This isn't duplication — it's a *contradiction* the file silently carries.
**Proposed:** **RECONCILE.** Either:
- Option (i): keep both, add a "When to bump vs. iterate" decision note inside one of them — e.g., "version-bump for structural changes, in-place for additive content during active learning"
- Option (ii): pick one as the canonical rule, retire the other
**Recommended:** Option (i) — both rules are correct in their context (B explicitly carves out "active learning sessions" as the in-place exception).
**Decision:** ☐ Accept (i) ☐ Accept (ii) ☐ Reject ☐ Modify ___________

---

## Section C — Out-of-Order Date Block (1 fix)

**Issue:** Line 197 `## HR & Recruitment (Mar 31, 2026)` appears between `## Cross-File Consistency & Audit Lessons (Mar 25, 2026)` (line 171) and `## Git, Branching & Deployment Lessons (Mar 26, 2026)` (line 205). The Mar 31 block was inserted into a Mar 25-26 cluster instead of after the Mar 30 categories at lines 321-353.

**Proposed:** Move the entire Mar 31 HR & Recruitment block (lines 197-204) to after line 353 (end of Cross-Project Dashboard & Query Copy Mar 30 block), before the Apr 1 categories begin at line 354.

**Risk:** Zero — same content, just moved. No number changes.

**Decision:** ☐ Accept ☐ Reject ☐ Modify ___________

---

## Section D — Single-Lesson Categories (13 — consolidation candidates)

These categories contain only 1 lesson each. Candidates for absorption into related larger categories.

| Category | Line | Lesson # | Suggested target |
|---|---|---|---|
| Azure DevOps Batch Work-Item Creation (Apr 15) | 682 | (1) | Merge into "DevOps API Integration" |
| Workspace Reorganization & Session Hooks (Apr 15) | 686 | (1) | Merge into "Session Workflow & Git Hygiene" |
| UI/UX Design Brief Generation (Apr 16) | 692 | (1) | Keep — distinct topic |
| Browser API Call Throttling & Dashboard Stability (Apr 16) | 696 | (1) | Keep — distinct topic |
| Counts vs Itemized Lists (Apr 12) | 582 | (1) | Merge into "Source Attribution & PM Deliverable Rigor" |
| Executive Summary Reports (Apr 1) | 362 | (1) | Merge into "Executive Reports & One-Pagers" |
| HTML Deliverable Defaults (Apr 21) | 872 | (1) | Merge into "HTML Deliverables" |
| Iterative Email Drafting (Apr 12) | 578 | (1) | Merge into "Stakeholder Communication & Emails" |
| Session Continuity & Closure Handoffs (Apr 21) | 868 | (1) | Merge into "Session Workflow & Git Hygiene" |
| Localhost Server Management (Mar 30) | 328 | (1) | Keep — distinct topic |
| Tool & Environment (Apr 2) | 417 | (1) | Keep — distinct topic |
| Translation & i18n (Apr 5) | 421 | (1) | Merge into "Bilingual Documents (EN/AR)" |
| Claude Automation (Apr 5) | 425 | (1) | Keep — distinct topic |

**Bulk decision:**
- ☐ Accept all "Merge" suggestions (8 merges)
- ☐ Reject all (keep file as-is)
- ☐ Per-row decision (mark each row)

---

## Renumber Map (Section A — pre-applied for traceability)

This map records the rename applied to `global_lessons.md` immediately after this sheet was generated. Use it to retro-fit any external references.

| Old # | New # | Lesson title (renumbered occurrence) |
|---|---|---|
| 253 (2nd) | 718 | ClosureDate is PM action, not developer completion |
| 254 (2nd) | 719 | Fetch form fields, not query columns |
| 255 (2nd) | 720 | Exclude training/meeting items from time metrics |
| 256 (2nd) | 721 | Paths with special characters break Windows shell |
| 295 (2nd) | 722 | Data gaps are more damaging than bad numbers |
| 292 (2nd) | 723 | Management evaluates the presenter, not just the presentation |
| 293 (2nd) | 724 | Use measurement language, never justification language |
| 294 (2nd) | 725 | Golden rule for management: numbers + understanding + plan |
| 276 (2nd) | 726 | Meeting chat extraction alone captures zero value |
| 277 (2nd) | 727 | AI-generated meeting notes need decisions vs. discussion split |
| 278 (2nd) | 728 | Multiple AI extractions overlapping but non-identical |
| 279 (2nd) | 729 | Post-meeting actions: build vs. present |
| 302 (2nd) | 730 | KhairGate Wallet uses 2 QC templates per PBI |
| 303 (2nd) | 731 | Create QC Bug Fixing tasks proactively |
| 306 (2nd) | 732 | New team member onboarding requires three updates |
| 307 (2nd) | 733 | Use security group membership API for DevOps team add |
| 308 (2nd) | 734 | Confirm which Azure DevOps project when names ambiguous |
| 310 (2nd) | 735 | Adding one user to access upgrade requires 20+ refs |
| 204 (2nd, audit miss) | 736 | Dashboard API URL requires project-level path |
| 227 (2nd, audit miss) | 737 | Trust DevOps closure dates — never second-guess |
| 468 (2nd, audit miss) | 738 | Audit new HTML version for hard-coded refs across ALL attribute types |
| 469 (2nd, audit miss) | 739 | MD/HTML parity check is not optional |
| 510 (2nd, audit miss) | 740 | Windows PowerShell 5.1 reads .ps1 as cp1252 — UTF-8 BOM required |

**New high-water mark:** 740 (was 717)
**Next new lesson number:** 741
**Total lessons in file:** 738 (audit claimed 737 — off by 1)
**Collisions remaining:** 0 (verified by `grep -oE '^[0-9]+\. \*\*' | sort | uniq -d`)
