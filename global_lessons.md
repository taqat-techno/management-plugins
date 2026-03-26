# Global Lessons Learned — Cross-Project Best Practices

> Accumulated from real project sessions. Apply these across ALL projects.
> Last updated: March 26, 2026 (137 lessons, 25 categories)
>

## Report Writing

1. **Be specific, not vague** — "Udemy training completed" > "Core training completed". Name the platform, tool, or system explicitly.
2. **Reports must stand alone** — The reader (CEO, Operation Manager, Engineering Manager) shouldn't need the author in the room to explain what a cell means.
3. **Every cell should be self-explanatory** — If someone reads a table cell and asks "what does this mean?", rewrite it.
4. **Same state = same label** — Use identical wording across all rows/departments for the same status. Don't say "Phase completed" for one and "Training done" for another.

## Status Labels & Completion Markers

5. **"Ongoing" is a lazy status** — Replace with specific next steps: "Phase 2: To Be Defined", "Certification prep continues independently (lab practice & exam)". Show intentional planning, not vagueness.
6. **Completion markers must be consistent** — If one department shows "Training completed" in a phase, ALL completed departments must show it. Never leave blank or `--` for a completed item.
7. **Explain what "independently" means** — If something continues outside the plan scope, say what specifically continues (e.g., "lab practice & exam"), not just "continues independently".

## Bilingual Documents (EN/AR)

8. **Always update both languages for every text change** — Never edit English without updating the Arabic span. Easy to forget on small fixes.
9. **Verify RTL visually** — Arabic layout can break borders, alignment, and table padding. Always open the HTML and toggle to Arabic after changes.
10. **Check both languages after toggle** — A change that looks fine in English might overflow or misalign in Arabic RTL mode.

## Stakeholder Communication & Emails

11. **Give email options, not just one draft** — Provide 3 versions: formal (detailed), concise (professional), action-oriented (direct). Different audiences need different tones.
12. **"Dear All" for multiple managers** — Avoids hierarchy issues. Let the To/CC fields handle the addressing.
13. **Always include what's attached and why** — Don't just say "please find attached". List what the attachment contains (bullet points).

## HTML Deliverables

14. **Open HTML after every change** — Code edits can look correct but render wrong. Always verify in the browser.
15. **Version control in filenames** — Use `_v2`, `_v3` suffixes. Keep old versions in versioned folders (`v1/`, `v2/`, `V3/`).

## Data Validation

16. **Always validate email/source dates first** — Before merging versions, check if source files actually changed. File size comparison catches identical files.
17. **Cost model is the #1 change trigger** — Major version changes are usually driven by pricing/subscription model changes, not content changes.
18. **Use PowerShell COM for .msg extraction** — `Outlook.Application` works but files must not be open in Outlook.

## OKR & KPI Dashboards

19. **OKR scoring must be automatic** — Don't rely on manual status entry for KR progress. Use editable "Current" fields that auto-calculate progress percentage, bar color, and status badge. Manual scoring drifts and becomes inconsistent.
20. **Inverse metrics need special handling** — KPIs where lower is better (bug escape rate, carry-over tasks) need inverse progress calculation: if current <= target, it's 100%. Don't use the same formula as "higher is better" metrics.
21. **Separate OKR (strategic) from KPI (operational)** — OKRs are quarterly aspirational goals with key results. KPIs are ongoing team metrics. Mixing them in one table confuses the audience. Use separate tabs/sections.

## Search Index Maintenance

22. **Rebuild search index after every pull** — When new HTML pages are added to a repo with a client-side search engine, the search index (e.g., `search-index.js`) won't include them automatically. Always check if new pages need to be added to the file list AND rebuild the index.
23. **New pages must be registered in build script** — Adding a new HTML file to the repo doesn't make it searchable. The file must also be added to the FILES array in the build script (e.g., `build-index.js`). This is a two-step process: (1) add to list, (2) rebuild.

## Project Estimation & Story Points

24. **Always verify project duration across all files** — Different documents (backlog, proposal, basis of calculation) may show conflicting durations. Cross-check all sources after every pull — the latest versioned file (v2) is the source of truth.
25. **Story points need a documented scale** — If a backlog uses SP without defining what each value means, derive the scale from actual story examples. Group stories by SP value, analyze complexity patterns, and document the scale for team alignment.
26. **Person-months ≠ calendar months** — Always calculate effective person-months (allocation % × duration) not headcount × months. A team of 11 at mixed allocations (20%-100%) may only deliver 15.93 person-months in 4 calendar months.
27. **AI acceleration changes all estimates** — When a project uses AI-assisted development, traditional effort estimates don't apply. Document the multiplier per role (QA gets highest ~4x, PM gets lowest ~1.5x) so stakeholders understand the compressed timeline.

## DevOps API Integration

28. **Use real DevOps states, not made-up labels** — Dashboard metrics must match the exact states in Azure DevOps (To Do, In Progress, Resolved, Done, Closed). Using generic terms like "Active" or "Carry-over" creates confusion when comparing with the DevOps board. Always query actual states first with the States API before building queries.
29. **Query by Assigned To when Area Paths don't exist** — If a DevOps project doesn't have team-specific area paths (Backend, Frontend, etc.), query by `[System.AssignedTo] CONTAINS 'member name'` across all projects. This is more flexible than area paths and works cross-project.
30. **Always provide a Data Source tab** — When building dashboards that fetch from APIs, include a transparent "Source" tab showing the exact queries used, results returned, and verification links. The user should never have to trust the numbers blindly — they need to verify against the source system independently.
31. **Discover projects via API before hardcoding** — Don't assume which DevOps projects exist based on email analysis or conversation context. Use `/_apis/projects` to discover all projects, then let the user confirm which ones to include.
32. **Never expose PAT tokens in chat or files** — PAT tokens should only be entered in browser modals and stored in localStorage. Never save them in code, memory files, or conversation. If a user shares one, remind them not to.
33. **Arabic toggle must be planned from day one** — Every PM dashboard needs EN/AR toggle. Adding it after the fact requires touching every text element. Plan for `data-i18n` attributes from the start to avoid rework.
34. **"Last updated" means fetch time, not current time** — Dashboard timestamps should show when data was last retrieved from the API, not a live clock. A live clock gives false confidence that data is current when it may be hours old.
35. **Show full project names, not abbreviations** — In dashboards for CEO/Board, use full project names (e.g., "KhairGate (BMS)") instead of abbreviations (e.g., "BMS"). Abbreviations are internal shorthand that external stakeholders won't recognize.

## Session Workflow & Git Hygiene (Mar 16, 2026)

36. **Always pull before analyzing** — Never analyze or report on data without pulling latest from remote first. Stale local data leads to wrong conclusions (e.g., reporting 9-month plan when v2 already shows 4 months).
37. **URL.txt is the session start ritual** — For repos with a URL.txt, always run it first: fetch → compare → pull if needed → open HTML. This prevents working on outdated files.
38. **Check git diff after pull, not just commit message** — Commit messages like "design modifications" are vague. Always check `git diff --stat` to know exactly which files changed and how much, so you can assess impact.
39. **Version files may have internal inconsistencies** — A v2 file may still contain v1 data in some sections (e.g., team member durations showing 9 months in a 4-month plan). Flag these to the user rather than silently assuming one is correct.

## Data Analysis & Presentation (Mar 16, 2026)

40. **Derive what's not documented** — If a backlog has story points but no scale definition, reverse-engineer it from the data. Count distribution, group by SP value, read actual stories at each level, then present the derived scale for validation.
41. **Show the math, not just the result** — When presenting person-months, show: Allocation % × Duration = Person-Months for each member. Stakeholders trust calculations they can verify.
42. **Compare before and after** — When two versions of a plan exist (v1 vs v2), always present a variance table. Decision-makers need to see what changed and by how much (e.g., -56% duration, -66% effort).
43. **Define jargon when asked** — Terms like "person-month", "story point", "sprint velocity" are not obvious to all stakeholders. When the user asks "what does X mean?", give a concrete example from their own project data, not a textbook definition.

## Memory & Lessons Discipline (Mar 17, 2026)

44. **Save lessons at end of every session** — Don't wait for the user to ask. At the end of each working session, proactively capture lessons learned into `global_lessons.md` and project-specific memory files.
45. **Memory files are for future conversations, not current tasks** — Don't save ephemeral task details (current debug state, temp file paths). Save things that help future-you understand the project: team composition, estimation methodology, key decisions, file relationships.
46. **Update session log after every pull** — The session log in MEMORY.md is the project timeline. Record: date, commit range, new/updated files, key actions taken. This helps trace when changes were introduced.

## Consolidation & Multi-Source Architecture (Mar 24, 2026)

47. **Never modify source files in consolidation projects** — Keep all source analyses untouched (e.g., S1: 468 files, S2: 21 files). Build an independent consolidated output (HUB v3.0). This preserves original analysis integrity for audit trails.
48. **Track conflicts explicitly with IDs and side-by-side display** — Number conflicts (CF-01 to CF-12) and show both positions without auto-resolution. Let governance decide. Transparent conflict management builds stakeholder trust.
49. **Color-coded source attribution on every data point** — Use consistent color tags (S1=blue, S2=orange, Merged=purple, New=green) so readers can trace any claim to its origin. Critical for multi-source projects.
50. **3-tier gap classification prevents analysis paralysis** — Classify gaps as Blocking / Important / Deferrable. Simple 3-tier system distinguishes urgency without overcomplicating prioritization.

## Portal & Pipeline Architecture (Mar 24, 2026)

51. **Zero-dependency static HTML is the most durable deliverable** — No build system, no bundler, no server. Works offline, on any machine, forever. Essential for board presentations and long-term archival.
52. **Modular CSS from day one saves rework** — Separate CSS files (variables, base, layout, nav, components, RTL, print) allow targeted changes without breaking unrelated pages. Invest in CSS architecture early.
53. **Numbered scripts enforce execution order** — Name pipeline scripts 01→22 to make execution order self-documenting. Anyone can run them in sequence without reading a README.
54. **Large JSON intermediates enable independent downstream scripts** — Files like `db_objects.json` (20MB) are large but let any downstream script work without re-extracting from source. The storage cost is worth the decoupling.
55. **FOLDER_OBJECTIVE_MAP.html serves as the project atlas** — A visual map of all folders and their purposes is essential when projects exceed 10 subfolders. New team members can orient themselves immediately.
56. **Recommendations stay as recommendations until governance approves** — Never auto-apply analysis recommendations to source files. Present findings; let the board decide. Technical teams provide analysis; governance decides.

## Dashboard Maintenance & Adoption (Mar 24, 2026)

57. **Maintenance burden kills dashboards** — If a dashboard requires > 30 manual inputs per week for one person, it won't be used. v1 had ~113 manual inputs and was never populated. v2 cut to ~24 by auto-fetching everything possible from DevOps APIs. Design rule: if an API can provide it, never ask the PM to type it.
58. **KRs must be outcomes, not activities** — "Weekly agendas with DevOps metrics pre-populated" is a task, not a key result. "Decision turnaround time < 3 days" is a measurable outcome. Before finalizing OKRs, test each KR: "Could someone else observe and verify this was achieved?" If not, rewrite it.
59. **PMs need their own scorecard for CEO visibility** — Team KPIs (sprint velocity, bug rate) measure the team, not the PM. Add a dedicated PM Scorecard with metrics the CEO evaluates the PM on: decision turnaround time, scope change control, meeting compliance, stakeholder satisfaction pulse. Without this, the PM is invisible in their own dashboard.
60. **localStorage snapshots enable trend tracking without a backend** — Save a weekly snapshot object into a history array on every "Save" click. Use inline SVG sparklines (no Chart.js dependency) to show week-over-week progress. Cap at 13 weeks (~500KB). Add Export/Import JSON for backup. This gives trend visibility with zero infrastructure.

## Enhanced Standalone Auto-Updater Rules (Mar 24, 2026)

61. **Surface updates are NOT enough** — After every Hub V2 pull, audit internal content (Document Control tables, assumptions, risk descriptions, internal text references), not just headers/footers/KPIs. V5-V10 missed this completely.
62. **Each pull with drift = new standalone folder** — Never edit existing version in place. Copy folder, increment version, apply fixes. Each version is a frozen snapshot.
63. **Create own reports, never copy Hub V2's** — PM creates own variance/story reports based on previous template. Hub V2 reports are Mohamed's internal documents with different branding.
64. **Hub V2 pages don't belong in standalone** — Only PM-created artifacts go in the standalone folder. Hub V2 pages (health-dashboard, etc.) are linked via nav, not copied.
65. **Document Control tables must match folder version** — Version field, Updated date, Data Source (with commit hash) must be current in every file after every update.
66. **Footer must show specific date** — "Modified: DD Mon YYYY" not generic "March 2026". Every file, every version.
67. **Phase 0 vs full program must be distinguished** — Budget, Timeline, Hiring show full 22-month program but kickoff is Phase 0 only. Both must be shown.
68. **Old reports don't belong in kickoff package** — Only latest variance + story variance versions. Remove historical snapshots (v10, v11, v1, v2).
69. **BA Review is a loop, not one-shot** — Mahmoud reviews → Mohamed fixes → Mahmoud verifies. Loop until no critical issues. Track pass number.
70. **Read lessons BEFORE executing** — At start of every session, read feedback files before touching any code. Prevents repeating past mistakes.
71. **Never assume git author = current user** — Check git log. MahmoudEl-Afify ≠ Mahmoud Elshahed.
72. **Validate Hub V2 claims against actual data** — Don't trust page counts, story counts, or status claims. Count actual files. Read actual KPI strips.
73. **Interactive buttons must sync via same localStorage key** — All files using status buttons must share `kg-action-progress` key. Labels must match across files (3 states for ADRs).
74. **Resolved sections should be collapsed by default** — `<details>` without `open` for ALL RESOLVED / CLOSED sections. Focus on pending items.

## OKR Dashboard v2 Lessons (Mar 25, 2026)

75. **Tab-based navigation beats sidebar for dashboards under 10 views** — v1 used 12 sidebar items; v2 consolidated to 7 tabs. Fewer navigation choices = faster cognitive load for executives. Only use sidebar when you have 10+ sections or need persistent visibility of all options.
76. **Bilingual i18n must use data attributes, not duplicate HTML** — v2 uses `data-i18n` keys with a JS translation map (~223 keys). Duplicating entire pages for EN/AR doubles maintenance and guarantees drift. Plan for `data-i18n` from the start so every text element is toggle-ready.
77. **Print CSS must show all tabs, not just the active one** — Dashboard print styles that hide inactive tabs produce blank pages. Use `display: block !important` on all `.tab-content`, add `page-break-before: always` between sections, and inject section titles via `content: attr(data-tab-title)` pseudo-elements. Always test Ctrl+P after adding print styles.
78. **Metric cards should be clickable drill-downs, not dead-end numbers** — Showing "To Do: 12" is useless without knowing who owns what. Every aggregate metric card should open a per-member or per-project breakdown modal on click (`showTeamDetailModal`). This was the key UX improvement in Team Pulse v2 — all 6 teams, 4 states each, 24 clickable drill-downs.
79. **Declare cached variables BEFORE loadData() runs** — JS `var` hoisting hoists the declaration but not the `= {}` initializer. If `var cache = {}` appears after `loadData()`, the initializer overwrites whatever `loadData()` restored from localStorage. Always declare cache variables before any load function that populates them.
80. **Never duplicate team members across teams** — Double-counting inflates metrics silently and makes drill-downs misleading. One person = one team. If they work across teams, pick their primary. OKR v2 had 4 members in both Mobile and Qatar — split them to eliminate overlap.
81. **WIQL returns work item IDs for free — don't discard them** — `data.workItems` from Azure DevOps contains `[{id, url}]`. The original `runWIQL` threw away IDs and returned only `.length`. `runWIQLWithIds` preserves them at zero extra API cost. Cache IDs in localStorage so drill-down links survive page reloads.
82. **Dashboards need a built-in user guide** — A PM won't use a dashboard they don't understand. Embed a step-by-step weekly workflow, a timeline with deadlines, and an auto-vs-manual field reference directly in the dashboard. Don't rely on external documentation — the guide must live inside the HTML.
83. **Always open HTML after edits — no exceptions** — Never leave the user to open files manually. Run `Start-Process` or equivalent as the final step after every HTML edit session. This was explicitly called out as a failure and saved as a feedback memory.

## Auto-Updater & UX Redesign Lessons (Mar 25, 2026)

84. **PowerShell em-dash crash** — Unicode characters (em-dash, curly quotes) in PowerShell string literals cause silent parse failures. The window closes instantly with no error. Always use ASCII alternatives (`--` not `—`, straight quotes not curly).
85. **Always provide .bat launcher for PS scripts** — "Right-click → Run with PowerShell" closes the window on any error. Create a `.bat` file with `powershell -ExecutionPolicy Bypass -NoExit -File script.ps1` so errors stay visible.
86. **Disable update buttons when no drift** — "Full Update" when already up-to-date is misleading and risky. Separate into 3 buttons: Check (always available), Pull+Update (only when drift), Audit Only (always available). Grey out unavailable actions.
87. **Automate recurring failures** — If a check is missed 3+ times across sessions, build a tool. The auto-updater script exists because manual drift fixes repeatedly missed Document Control tables, assumptions, and internal content. Human checklists fail; scripts don't forget.
88. **3 page types define nav UX** — Action pages (green, interactive buttons for decisions), Reference pages (blue, read-only for board review), Audit pages (purple, health history snapshots). Organize navigation by type, not by arbitrary categories. Directors need to know: "where do I click?" vs "where do I read?"
89. **Merge overlapping pages** — Two pages covering the same topic (KICKOFF_READINESS_GUIDE + KICKOFF_READINESS_VALIDATION) confuse the Director. One source of truth per topic. If you create a summary page, merge it into the original rather than adding another file.

## Cross-File Consistency & Audit Lessons (Mar 25, 2026)

90. **Deleting a file breaks all relative links to it** — When we deleted root-level HUB_PULL_HISTORY.html, 14 V11 sidebar nav links (`../HUB_PULL_HISTORY.html`) broke silently. Always grep for all references BEFORE deleting any file, and fix links in the same commit.
91. **Don't duplicate files across locations** — Having HUB_PULL_HISTORY at root AND inside V11 caused staleness (root was March 18, V11 was current). One copy, one location. If other files need it, link to it — don't copy it.
92. **Location-specific terms don't belong in hiring risks** — "Qatar market" implies on-site only. Hiring may be hybrid/remote. Use skill-based language instead: "Odoo 19 skill scarcity" not "Qatar market scarcity". Applies to all R-08 references across PM_RISK_REGISTER, ADR_APPROVAL_REQUEST, and any hiring-related text.
93. **Health dashboard verdict must reference cards by name** — A flat list of 7 pending items is unreadable. Group pending items under the card they belong to (e.g., "POC Readiness V.2 — ADR-1, Budget, Odoo hiring"). Board can then click the right card directly.
94. **Visual badges (ACTION NEEDED / CLEAR) save board reading time** — 7 cards with no visual priority = Board reads all 7. Amber badge + green badge = Board reads only the 3 that matter. Always add status badges when cards have mixed states.
95. **Track review loops explicitly** — The BA review between El-Afify and Mohamed had no visible status on the dashboard. Pass 2 was pending but nowhere documented. Add "Review Loop Status" tracking boxes to both the health dashboard card and the readiness page.
96. **Purpose tips in headers orient the reader** — Every page header should have a one-line description of what this page does. Board members open 15+ files — a tip below the title saves them from scrolling to understand context. Use `.summary` div pattern.
97. **Auto-updater covers KPIs but not consistency** — The PS1 server catches number drift (stories, SP) but misses text mismatches ("Qatar market" in 2 files), broken nav links, file count disagreements, and version tag staleness. Build a 6-check audit: KPIs + text + nav + file count + status sync + version tags.
98. **Sprint-plan-phase0 and phase0-poc-readiness are a pair, not duplicates** — Sprint plan = developer execution guide (Mohamed's, 2,196 lines). POC Readiness = PM status dashboard (ours, 227 lines). Different audiences, same data. Keep both but verify data consistency between them.
99. **Session handoff must include tracking file updates** — HUB_PULL_HISTORY, FOLDER_OBJECTIVE_MAP, and MEMORY.md must be updated at end of every session. Save a "FIRST TASKS Next Session" section in memory if context runs out.

## Git, Branching & Deployment Lessons (Mar 26, 2026)

100. **`git rm -rf .` deletes actual files, not just tracking** — When creating orphan branches inside the working folder, `git rm -rf .` permanently deleted V12 files. All session changes had to be re-applied from scratch. Always work from a DIFFERENT directory when creating orphan branches, or use `git worktree`.
101. **PowerShell arrays of hashtables don't serialize with ConvertTo-Json** — `@() += @{...}` pattern produces empty JSON arrays. Use `[System.Collections.ArrayList]::new()` with `.Add()` instead. Also increase `-Depth` to 10+ for nested structures.
102. **Wrong Hub V2 path = wrong KPIs** — `KhairGate-Hub-Analysis` (V1, stale) vs `KhairGate-Hub-Analysis-V2` (current). The auto-updater pointed to V1 for months without anyone noticing. Always verify the exact folder name when configuring paths to data sources.
103. **Greedy regex causes false positives in audits** — `Financial Readiness.*100%` matched "To reach 100%" text instead of the actual 80% value on the same line. Fix: use tight patterns that match specific HTML structure (e.g., `progress-label` div value), not greedy wildcards across the whole line.
104. **Multilingual regex needs wider context windows** — Arabic "العودة" (fallback) was 40+ chars before "Odoo 18" but the 20-char lookback missed it. Expand context windows to 80+ chars when checking multilingual content for contextual exclusions.
105. **Historical files must be excluded from audit checks** — HUB_PULL_HISTORY, variance reports, and ADR contain intentional references to old tech (Camunda, Odoo 18, USD). They document history, not current state. Audit rules that flag "stale content" must have an exclusion list for historical/audit files.
106. **Hub V2 i18n uses data-i18n attributes + inline JS dictionary** — Not JSON files. ~550+ terms in a JS object (`var T = {...}`) inside i18n.js. `toggleLang()` swaps `textContent` via `querySelectorAll('[data-i18n]')`. New pages need both the data-i18n attributes AND the dictionary entries to translate.
107. **Push ALL repos after changes, not just the one you're focused on** — Hub V2 changes (Arabic translations) were committed but not pushed until the user asked. When a session touches multiple repos, push all of them before ending.
108. **Orphan branches preserve version snapshots** — Each Enhanced Standalone version (v1-v12) as its own orphan branch with descriptive commit messages preserves the full evolution history. Use `git checkout --orphan v{N}` pattern.
109. **Auto-update lessons from audit findings with dedup** — Build the pipeline to write back to global_lessons.md automatically. Check for existing keywords before appending to avoid duplicates. Stale lesson files are worse than no lesson files.

## Dashboard & KPI Design Lessons (Mar 26, 2026)

110. **Separate work item types for accurate metrics** — Grouping Bug + Enhancement under "Task" hides defect trends. Each type needs its own WIQL query, KPI card, and column in drill-down tables. Without separation, you can't answer "how many bugs are open?" from the dashboard.
111. **Auto-calculate derived KPIs — don't let users manually set what can be computed** — Overall health = worst-of(Schedule, Quality, Scope) + blocker penalty. Manual "Overall" toggles drift from reality. Formula: min(S,Q,Scope), downgrade if blockers > 0, force Red if blockers > 3.
112. **Merge tiered tables into one unified view** — Tier 1 (full G/A/R) + Tier 2 (active items only) confused readers. One table, same columns, all 11 projects. Tiers are for prioritization logic, not UI separation.
113. **Column tooltips explain scoring criteria to non-technical readers** — Board members don't know what "Quality = Amber" means. Add `title` attributes: "Consider bug count, rework rate, QA pass rate." Every subjective column needs a tooltip.
114. **localStorage migration between dashboard versions** — v2→v3 key change (`okr-kpi-q2-2026-v2` → `-v3`) requires auto-migration logic on load. Users lose data without it. Always check for old key, transform data shape, write to new key, delete old.

## Document Consolidation Lessons (Mar 26, 2026)

115. **Identify the primary source before merging** — When 3 files cover the same meeting, one is always the most comprehensive. Use it as the skeleton; others are supplements for gaps only. Don't merge line-by-line — that creates duplicates.
116. **Email-ready HTML beats DOCX for meeting distribution** — Inline CSS, no attachment issues, renders in every mail client. For MoM/agenda distribution, HTML is the final format. DOCX is the input, not the output.

## Modal, Audit & i18n Lessons (Mar 26, 2026)

117. **Modal popups beat inline results for audit output** — Inline `<div id="results">` pushes page content down and gets lost on scroll. Modal overlay with backdrop = focused attention, dismissible, no layout shift. Include summary bar (pass/fail counts) + individual check cards.
118. **Remove vendor names from architecture documents** — "Camunda" → "external BPM tool". Docs survive tool changes without rewrites. Historical files (ADR, variance reports) keep vendor names as they document decisions made at that time. Only current-state docs use generic terms.
119. **Title consistency is a cross-file audit check** — "Project Manager" vs "IT Project Manager" appeared in 6+ files across V12. Title mismatches erode credibility with board readers. Add title verification to the audit engine. Exclude external stakeholder entries (e.g., Semir's role stays as-is).
120. **Batch i18n: attributes + dictionary in one commit** — Adding `data-i18n` attributes to HTML without updating the JS dictionary (`var T = {...}`) means keys resolve to raw key names. Always add both in the same commit. For Hub V2, that's 9 HTML files + i18n.js = one atomic commit.

## OKR & KPI Dashboard v3 Lessons (Mar 26, 2026)

121. **Numbers must reconcile across dashboard views** — If Executive Summary shows 26 Bugs total, Team Pulse must also total 26. Add an "Unassigned" card to catch work items with no owner. Formula: Project total = Sum(all teams) + Unassigned. If they don't match, users lose trust in the dashboard.
122. **Consistent drill-down pattern across all metrics** — Every clickable number must follow the same flow: Card number → Breakdown table → Work Items popup (with DevOps links) → Back button. Don't skip levels for Bugs/Enhancements while keeping them for To Do/In Progress. Inconsistency confuses users.
123. **Modal max-height prevents off-screen Close button** — A project with 18+ work items pushes the Close button below the viewport. Always set `max-height: 85vh; overflow: auto` on modal content. The Close and Back buttons must always be reachable.
124. **Don't add redundant summary strips** — A live data strip in the header repeating KPI card values adds clutter, not clarity. Use header space for report purpose/benefits instead. Data lives in KPI cards; identity lives in the header.
125. **G/A/R toggles need deselect capability** — Click to select, click again to deselect back to "none". Without this, once you set a value you can never clear it. Check `el.classList.contains('selected')` before toggling.
126. **Separate work item types in WIQL queries** — Mixing Task+Bug in `IN ('Task', 'Bug')` hides bug counts. Use separate queries for Bug-only and Enhancement-only counts. This enables auto-populating KR2.1 (production bugs) and gives PM visibility into defect vs improvement work.
127. **Persist in-memory data to localStorage** — `lastProjectData` was only in JS memory — lost on page reload, breaking detail modals ("Click Fetch first"). Save runtime data structures to localStorage in `saveData()` and restore in `loadData()` if the UI depends on them.
128. **Use the Blocked field, not tags** — Azure DevOps has a dedicated `Microsoft.VSTS.CMMI.Blocked` field (Yes/No). Don't rely on `[System.Tags] CONTAINS 'Blocked'` which requires manual tagging. The field is built into the work item form.
129. **Move action buttons to sidebar footer** — Fixed bottom bars (Save/Export/Clear) waste 50px of vertical space on every page. Sidebar footer is always visible and doesn't consume main content area. Also move Fetch/PAT buttons there.
130. **Two-column header: purpose left, identity right** — Title + subtitle + benefits on the left; name + org + quarter + meta tags stacked right-aligned on the right. No wasted horizontal space. AR toggle goes top-right.
131. **Always add tooltips and legends for Board audience** — G/A/R buttons, column headers (Schedule/Quality/Scope), KPI cards — every element needs hover `title` explanation. Board members won't guess what "Quality = Amber" means. Add a visible legend box above the table.
132. **Spell out acronyms in the title** — "OKR & KPI" means nothing to a CEO. Show "Objectives & Key Results / Key Performance Indicators" beside the short title. The abbreviated form is for navigation (sidebar), the full form is for comprehension (header).
133. **Use correct job titles consistently** — "IT Project Manager" not "PM" or "Project Manager". Check every occurrence: header, print summary, PM Scorecard title, meta tags. Title mismatches erode credibility in Board-facing reports.

## Email Analysis & Weekly Reporting Lessons (Mar 26, 2026)

134. **Verify topic categorization by participants, not keywords** — "Terms and Conditions (English)" was placed under Relief Center based on keyword match. Checking participants (Dr. Bahaa, Hacene, Syed) immediately revealed it belongs to BMS/KhairGate. Always check the participant list in topic_summary.csv before assigning new topics to project categories.
135. **Email volume ≠ project status — never set badges from data alone** — A project with 12 new emails might be on track; a project with zero emails might be critically blocked. Status badges (URGENT, ACTIVE, MEDIUM, etc.) must come from the PM's manual input, not automated email counts. Email data provides trends and counts; human judgment provides status.
136. **Checkboxes without persistence are decoration** — HTML checkboxes that reset on page refresh provide no tracking value. Either add localStorage persistence or accept that status tracking is manual. For weekly snapshot reports, manual Thursday review is sufficient — don't over-engineer interactivity.
137. **Embed the update process in the deliverable itself** — If a report has a recurring update workflow, document the process steps inside the report (e.g., info card on the Dashboard tab). Anyone opening the report should understand how it gets updated without needing external documentation.
