# Session-Log Compression Decision Sheet (R-A)

**Generated:** 2026-05-07 (re-baselined 2026-05-08)
**HEAD SHA:** `96f41ec` (refine/session-logs-compression branch)
**Source file:** `D:\Global Lessons\global_lessons.md` (738 lessons, 113 categories, current max #745)

## Why this exists

R-A from the meta-recommendation plan: three "session log" categories accumulated 87 micro-lessons during single working sessions. Most don't generalize beyond their session. Compression target: **3:1** (87 → ~25), but a **2.2:1 first pass (87 → 39)** is the conservative recommendation — leaves another optional trim pass if you want tighter.

## How to use this sheet

Mark each cluster row with one of:

- ✅ **Accept** — fold the listed source lessons into one new compressed lesson
- ❌ **Reject** — leave the source lessons as-is (no merge)
- ✏️ **Modify** — write your override in the Notes column (e.g., "merge with cluster X", "split this into 2 clusters", "keep #NNN out of the merge")

Cluster numbering: new compressed lessons take numbers **746 onwards** (current max is 745, since #744 + #745 shipped after the original sheet was generated).

Default action if you say "go with all": all clusters marked ✅, the 6 KEEP lessons stay verbatim, no deletions, **net 87 → 39**.

---

## Category 1 — PMO_OS Meetings Tab v14 Parity (May 5, 2026)

**43 lessons → 16 compressed + 2 KEEP standalone = 18 lessons**

| Cluster | New # | Proposed compressed lesson title | Folds in (old #s) | Decision |
|---|---|---|---|---|
| C1.1 | 746 | Electron renderer-vs-main pitfalls — `window.prompt`/`alert`/`confirm` are no-op, renderer `fetch()` to localhost blocked, new `ipcMain.handle` needs full restart | 660, 661, 662 | ✅ |
| C1.2 | 747 | Native Electron primitives over heavyweight deps — `webContents.printToPDF` not Puppeteer; `webContents.send` + preload bridge for menu→renderer | 664, 681 | ✅ |
| C1.3 | 748 | Embeddable Python is the right way to ship Python sidecars in Electron — recipe + extraResources + launcher + CI | 671, 675 | ✅ |
| C1.4 | 749 | Pure helpers in `src/lib/` keep Electron logic vitest-testable — extract validation/sanitization/path-resolution from any IPC handler | 665, 696 | ✅ |
| C1.5 | 750 | Frozen-artifact discipline + window-title hardcoding — never edit FROZEN HTML files; never bake version strings; affordance-diff every UI migration | 663, 687, 695, 697 | ✅ |
| C1.6 | 751 | tRPC + React Query migration patterns — compatibility shim (`asState`), primary/secondary mutation try/catch isolation, embedded baselines as static JSON | 679, 680, 683 | ✅ |
| C1.7 | 752 | First-launch onboarding patterns — Setup Wizard auto-redirect via sticky boolean; derive roster at runtime over static JSON; 4-layer email opt-in defenses | 673, 684, 685 | ✅ |
| C1.8 | 753 | electron-updater hardening end-to-end — GitHub provider for public, generic+OneDrive for private, `token` field + DPAPI store; SHA-512 verify .exe before install | 670, 678, 686, 693 | ✅ |
| C1.9 | **KEEP #699** | Tag from clean master — cherry-pick release commit, never tag from a feature branch carrying parallel-agent WIP | 699 | ✅ KEEP standalone |
| C1.10 | 754 | Cross-runtime deploy hazards — code+filesystem changes need explicit restart guidance; cross-volume moves need COPY → SHA-256 VERIFY → DELETE | 698, 700 | ✅ |
| C1.11 | 755 | Bilingual hardcoded-string scanner evolution — custom over ESLint when on a deadline; iterative heuristic tuning; emoji split from label; type hoist for `Promise<X>` false-positive | 666, 667, 672, 689 | ✅ |
| C1.12 | 756 | MENA workweek + bilingual document patterns — Sun-Thu for SLA math; `_PIPE_TAIL` regex for `EN \| AR:` headers; `days_back` for centered calendar windows | 658, 659, 691 | ✅ |
| C1.13 | 757 | Cross-machine PowerShell + Task Scheduler discipline — PS 5.1 dialect over PS 7+; `RunLevel Limited` for user-COM tasks (extends #612 integrity rule) | 677, 692 | ✅ |
| C1.14 | **KEEP #682** | Telemetry on desktop — reuse the rotating log file (pino), don't add a SQLite events table; aggregator is a pure function over `string[]` | 682 | ✅ KEEP standalone |
| C1.15 | **KEEP #668** | Cold-launch determinism testing — gate on steady-state mean (iters 2-5) not run mean; variance metric is the build-stability signal | 668 | ✅ KEEP standalone |
| C1.16 | 758 | Living-doc fork-vs-edit + multi-PR audit doc as deliverable — when >50% of phase milestones DONE, fork `_vNext.md`; ship `Tab_X_Migration_Audit.md` for 5+ component refactors | 674, 694 | ✅ |
| C1.17 | 759 | Verify external-state memory before acting + AskUserQuestion to confirm scope on multi-screenshot reports — both prevent shipping work the user didn't ask for | 688, 690 | ✅ |
| C1.18 | 760 | Pinned-version dependency traps — electron-store v9+ ESM-only (pin v8); `app.getAppPath()` not `__dirname/..` for in-asar files | 669, 676 | ✅ |

**Subtotal: 43 → 18 lessons** (15 clusters folded + 3 KEEP standalone)

---

## Category 2 — PMO Dashboard v13 Phases 5-8 Build (May 2, 2026)

**24 lessons → 9 compressed + 2 KEEP standalone = 11 lessons**

| Cluster | New # | Proposed compressed lesson title | Folds in (old #s) | Decision |
|---|---|---|---|---|
| C2.1 | 761 | Outlook + Word + Calendar COM lifecycle — folder index 9 + `IncludeRecurrences=true`; Visible=false + readonly + Close+Quit+ReleaseComObject; integrity-level match for COM activation | 601, 604, 612 | ✅ |
| C2.2 | 762 | PowerShell HTTP listener building blocks — `Read-PostBody` helper; pre-script ENV guards; multi-res ICO via `System.Drawing` | 602, 618, 619 | ✅ |
| C2.3 | 763 | Phased single-file build patterns — per-phase IIFE + console.log signature; additive-only ships continuously without per-day verify; entry schema scales via optional `scope` discriminator | 600, 608, 609 | ✅ |
| C2.4 | 764 | Persistent storage patterns for dashboards — `_data/{purpose}/YYYY-MM/{date}.{ext}` JSON sharding; `Storage.setItem` patch for auto-save (filtered by key) | 603, 607 | ✅ |
| C2.5 | **KEEP #605** | Bilingual standalone artifacts via paired-span + Blob URL — proven STP v3 pattern reused for Board Pack generator | 605 | ✅ KEEP standalone |
| C2.6 | 765 | Windows scheduling primitives — Task Scheduler 'Wake to run' + 'Run if missed' for 8 AM daily push; Developer Mode required for electron-builder symlink extraction | 606, 617 | ✅ |
| C2.7 | 766 | Cadence + roadmap shifts touch ~15-30 files across 3 tiers — preserve historical artifacts as point-in-time records; pre-warn stakeholders for dual-track demos | 613, 614 | ✅ |
| C2.8 | 767 | STP demo deck clone-and-edit + bulk pre-build — 9-item checklist per deck; 7-edit minimum set when bulk pre-building N future decks | 610, 611 | ✅ |
| C2.9 | 768 | Phase-A scaffold pull-forward + multi-repo workspace pattern — Day 1+Day 4 same evening when sample data is structured; separate repos for governance vs product | 615, 620 | ✅ |
| C2.10 | **KEEP #616** | Electron bring-up environment trap — `ELECTRON_RUN_AS_NODE=1` poisons init; pin npm `pre*` guards to fail-fast | 616 | ✅ KEEP standalone |
| C2.11 | 769 | Cross-dashboard integration drift — jump-list `_v{N}.html` hrefs, `localhost:<PORT>` constants, `new Date(value + 'Z')` NaN trap when source has timezone — all silent until clicked | 621, 622, 623 | ✅ |

**Subtotal: 24 → 11 lessons** (9 clusters folded + 2 KEEP standalone)

---

## Category 3 — V16 Drift Fix Session (Apr 28, 2026)

**20 lessons → 6 compressed + 4 KEEP standalone = 10 lessons**

| Cluster | New # | Proposed compressed lesson title | Folds in (old #s) | Decision |
|---|---|---|---|---|
| C3.1 | 770 | Coverage-matrix BEFORE creating new files — also reframe AskUserQuestion options around it; migrate net-new content to canonical files BEFORE deleting orphans | 520, 524, 531 | ✅ |
| C3.2 | 771 | Multi-version HTML clone hygiene — clean past-version chatter on v[N-1]→v[N] clone; wire new files into cross-ref nav; reframe stale badges on superseded cards | 515, 522, 525 | ✅ |
| C3.3 | 772 | Bilingual + audit-check drift catchers — AR-mirror visual review (toggle every modified file); audit-check needs V[N]-specific accommodation rules when vocabulary shifts | 521, 529 | ✅ |
| C3.4 | 773 | Date-bump + subagent re-invocation discipline — distinguish event-dates from Modified-dates; subagents don't re-run for same-version content edits → end-of-session sweep needed | 519, 527 | ✅ |
| C3.5 | 774 | HTML rendering bugs that pass content review — nested `<a>` inside `<a class="card">` breaks grid layout; post-push browser visual check is mandatory for any card/grid/table change | 513, 532 | ✅ |
| C3.6 | 775 | Wording precision in stakeholder docs — "100% complete" misleading when planning gates remain; Consolidated Blockers needs 3-tier (Resolved/Active/In-flight); AskUserQuestion options must use plain-language ops descriptions | 517, 518, 523 | ✅ |
| C3.7 | **KEEP #530** | AskUserQuestion + recommendation discipline — "(Recommended)" tag carries anchoring weight; surface counter-arguments inline; user's "why?" is the late-signal that reasoning was shallow | 530 | ✅ KEEP standalone |
| C3.8 | 776 | Cross-repo push-order + git-stash hygiene — source-of-truth/Hub repo first when commits are linked; `git stash push -u --keep-index` preserves staged today-edits | 514, 526 | ✅ |
| C3.9 | **KEEP #528** | Plan-mode discipline: overwrite plan file per new task, mark informational Q&A explicitly | 528 | ✅ KEEP standalone |
| C3.10 | **KEEP #516** | Hub V2 KPI strip + grand-totals drift on Planned R[N] epic add — standalone reports follow published authoritative numbers + flag with conditional notation | 516 | ✅ KEEP standalone |

**Subtotal: 20 → 10 lessons** (6 clusters folded + 4 KEEP standalone)

---

## Grand totals (default = "go with all")

| Metric | Before | After |
|---|---|---|
| Lessons across the 3 categories | 87 | **39** |
| Compression ratio | — | ~2.2:1 |
| New compressed lessons (746-776) | — | 31 |
| Lessons kept verbatim (KEEP standalone) | — | 8 |
| Lessons folded | 79 | — |
| Lessons deleted (zero by default) | — | 0 |
| Net global_lessons.md count | 738 | **690** |

---

## Optional 2nd-pass tighter compression (39 → ~33)

If you want closer to the original 3:1 target, mark these additional merges:

| 2nd-Pass | Merge | Result | Decision |
|---|---|---|---|
| 2P-A | Merge C2.6 (Windows scheduling) into C1.13 (PS + Task Scheduler) | -1 lesson | ☐ |
| 2P-B | Merge C1.11 (scanner heuristics) into C1.12 (MENA + locale defaults) — both are i18n drift | -1 lesson | ☐ |
| 2P-C | Merge C2.2 (PS HTTP listener) into C1.13 (PowerShell discipline) | -1 lesson | ☐ |
| 2P-D | Drop KEEP on C2.5 (Board Pack via Blob URL); fold into C1.2 (native Electron primitives) | -1 lesson | ☐ |
| 2P-E | Merge C3.5 (HTML render bugs) into C3.2 (clone hygiene) — both HTML quality gates | -1 lesson | ☐ |
| 2P-F | Drop KEEP on C2.10 (`ELECTRON_RUN_AS_NODE` trap); fold into C1.18 (pinned-version traps) | -1 lesson | ☐ |
| **All 2nd pass** | | **39 → 33 (~2.6:1)** | ☐ Accept all 2nd-pass |

---

## Hard rules I'll follow when applying

- **Provenance tails** — every compressed lesson body ends with `(Folded former #N1, #N2, #N3.)` so the lineage is auditable
- **Sub-incident citations preserved** — if multiple folded lessons had distinct cost stories, the new lesson body cites all of them as separate paragraphs (no detail loss, just structural compression)
- **Cross-refs intact** — any `(See also #M)` references to lessons OUTSIDE this compression scope stay valid; references TO folded lessons get updated to point at the new compressed lesson number
- **Old numbers retired, not reused** — folded lesson numbers (e.g., 600, 601, 602...) don't get reassigned to new content
- **Per-category commits** — one commit per category for cleaner rollback
- **Final reflog dogfood** — Rule 38-bis check before pushing

---

## Open question for you

Pick one of these and reply:

1. **"go with all (1st pass only)"** — accept all clusters, no 2nd-pass merges. 87 → 39. Conservative.
2. **"go with all + all 2nd-pass"** — accept everything including the 6 tighter merges. 87 → 33. Closer to 3:1 target.
3. **Per-row marks** — paste the sheet back with ✅/❌/✏️ per row.
4. **"defer"** — keep the sheet as a working doc, do nothing this session.
