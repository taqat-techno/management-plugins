# Global Lessons Learned — Cross-Project Best Practices

> Accumulated from real project sessions. Apply these across ALL projects.
> Last updated: March 25, 2026

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

28. **Always pull before analyzing** — Never analyze or report on data without pulling latest from remote first. Stale local data leads to wrong conclusions (e.g., reporting 9-month plan when v2 already shows 4 months).
29. **URL.txt is the session start ritual** — For repos with a URL.txt, always run it first: fetch → compare → pull if needed → open HTML. This prevents working on outdated files.
30. **Check git diff after pull, not just commit message** — Commit messages like "design modifications" are vague. Always check `git diff --stat` to know exactly which files changed and how much, so you can assess impact.
31. **Version files may have internal inconsistencies** — A v2 file may still contain v1 data in some sections (e.g., team member durations showing 9 months in a 4-month plan). Flag these to the user rather than silently assuming one is correct.

## Data Analysis & Presentation (Mar 16, 2026)

32. **Derive what's not documented** — If a backlog has story points but no scale definition, reverse-engineer it from the data. Count distribution, group by SP value, read actual stories at each level, then present the derived scale for validation.
33. **Show the math, not just the result** — When presenting person-months, show: Allocation % × Duration = Person-Months for each member. Stakeholders trust calculations they can verify.
34. **Compare before and after** — When two versions of a plan exist (v1 vs v2), always present a variance table. Decision-makers need to see what changed and by how much (e.g., -56% duration, -66% effort).
35. **Define jargon when asked** — Terms like "person-month", "story point", "sprint velocity" are not obvious to all stakeholders. When the user asks "what does X mean?", give a concrete example from their own project data, not a textbook definition.

## Memory & Lessons Discipline (Mar 17, 2026)

36. **Save lessons at end of every session** — Don't wait for the user to ask. At the end of each working session, proactively capture lessons learned into `global_lessons.md` and project-specific memory files.
37. **Memory files are for future conversations, not current tasks** — Don't save ephemeral task details (current debug state, temp file paths). Save things that help future-you understand the project: team composition, estimation methodology, key decisions, file relationships.
38. **Update session log after every pull** — The session log in MEMORY.md is the project timeline. Record: date, commit range, new/updated files, key actions taken. This helps trace when changes were introduced.

## Consolidation & Multi-Source Architecture (Mar 24, 2026)

39. **Never modify source files in consolidation projects** — Keep all source analyses untouched (e.g., S1: 468 files, S2: 21 files). Build an independent consolidated output (HUB v3.0). This preserves original analysis integrity for audit trails.
40. **Track conflicts explicitly with IDs and side-by-side display** — Number conflicts (CF-01 to CF-12) and show both positions without auto-resolution. Let governance decide. Transparent conflict management builds stakeholder trust.
41. **Color-coded source attribution on every data point** — Use consistent color tags (S1=blue, S2=orange, Merged=purple, New=green) so readers can trace any claim to its origin. Critical for multi-source projects.
42. **3-tier gap classification prevents analysis paralysis** — Classify gaps as Blocking / Important / Deferrable. Simple 3-tier system distinguishes urgency without overcomplicating prioritization.

## Portal & Pipeline Architecture (Mar 24, 2026)

43. **Zero-dependency static HTML is the most durable deliverable** — No build system, no bundler, no server. Works offline, on any machine, forever. Essential for board presentations and long-term archival.
44. **Modular CSS from day one saves rework** — Separate CSS files (variables, base, layout, nav, components, RTL, print) allow targeted changes without breaking unrelated pages. Invest in CSS architecture early.
45. **Numbered scripts enforce execution order** — Name pipeline scripts 01→22 to make execution order self-documenting. Anyone can run them in sequence without reading a README.
46. **Large JSON intermediates enable independent downstream scripts** — Files like `db_objects.json` (20MB) are large but let any downstream script work without re-extracting from source. The storage cost is worth the decoupling.
47. **FOLDER_OBJECTIVE_MAP.html serves as the project atlas** — A visual map of all folders and their purposes is essential when projects exceed 10 subfolders. New team members can orient themselves immediately.
48. **Recommendations stay as recommendations until governance approves** — Never auto-apply analysis recommendations to source files. Present findings; let the board decide. Technical teams provide analysis; governance decides.

## Dashboard Maintenance & Adoption (Mar 24, 2026)

49. **Maintenance burden kills dashboards** — If a dashboard requires > 30 manual inputs per week for one person, it won't be used. v1 had ~113 manual inputs and was never populated. v2 cut to ~24 by auto-fetching everything possible from DevOps APIs. Design rule: if an API can provide it, never ask the PM to type it.
50. **KRs must be outcomes, not activities** — "Weekly agendas with DevOps metrics pre-populated" is a task, not a key result. "Decision turnaround time < 3 days" is a measurable outcome. Before finalizing OKRs, test each KR: "Could someone else observe and verify this was achieved?" If not, rewrite it.
51. **PMs need their own scorecard for CEO visibility** — Team KPIs (sprint velocity, bug rate) measure the team, not the PM. Add a dedicated PM Scorecard with metrics the CEO evaluates the PM on: decision turnaround time, scope change control, meeting compliance, stakeholder satisfaction pulse. Without this, the PM is invisible in their own dashboard.
52. **localStorage snapshots enable trend tracking without a backend** — Save a weekly snapshot object into a history array on every "Save" click. Use inline SVG sparklines (no Chart.js dependency) to show week-over-week progress. Cap at 13 weeks (~500KB). Add Export/Import JSON for backup. This gives trend visibility with zero infrastructure.

## Enhanced Standalone Auto-Updater Rules (Mar 24, 2026)

53. **Surface updates are NOT enough** — After every Hub V2 pull, audit internal content (Document Control tables, assumptions, risk descriptions, internal text references), not just headers/footers/KPIs. V5-V10 missed this completely.
54. **Each pull with drift = new standalone folder** — Never edit existing version in place. Copy folder, increment version, apply fixes. Each version is a frozen snapshot.
55. **Create own reports, never copy Hub V2's** — PM creates own variance/story reports based on previous template. Hub V2 reports are Mohamed's internal documents with different branding.
56. **Hub V2 pages don't belong in standalone** — Only PM-created artifacts go in the standalone folder. Hub V2 pages (health-dashboard, etc.) are linked via nav, not copied.
57. **Document Control tables must match folder version** — Version field, Updated date, Data Source (with commit hash) must be current in every file after every update.
58. **Footer must show specific date** — "Modified: DD Mon YYYY" not generic "March 2026". Every file, every version.
59. **Phase 0 vs full program must be distinguished** — Budget, Timeline, Hiring show full 22-month program but kickoff is Phase 0 only. Both must be shown.
60. **Old reports don't belong in kickoff package** — Only latest variance + story variance versions. Remove historical snapshots (v10, v11, v1, v2).
61. **BA Review is a loop, not one-shot** — Mahmoud reviews → Mohamed fixes → Mahmoud verifies. Loop until no critical issues. Track pass number.
62. **Read lessons BEFORE executing** — At start of every session, read feedback files before touching any code. Prevents repeating past mistakes.
63. **Never assume git author = current user** — Check git log. MahmoudEl-Afify ≠ Mahmoud Elshahed.
64. **Validate Hub V2 claims against actual data** — Don't trust page counts, story counts, or status claims. Count actual files. Read actual KPI strips.
65. **Interactive buttons must sync via same localStorage key** — All files using status buttons must share `kg-action-progress` key. Labels must match across files (3 states for ADRs).
66. **Resolved sections should be collapsed by default** — `<details>` without `open` for ALL RESOLVED / CLOSED sections. Focus on pending items.

## OKR Dashboard v2 Lessons (Mar 25, 2026)

67. **Tab-based navigation beats sidebar for dashboards under 10 views** — v1 used 12 sidebar items; v2 consolidated to 7 tabs. Fewer navigation choices = faster cognitive load for executives. Only use sidebar when you have 10+ sections or need persistent visibility of all options.
68. **Auto-fetch coverage determines dashboard adoption** — v1 had ~113 manual inputs and was never populated. v2 auto-fetches ~44 data points via WIQL, leaving only ~24 manual inputs. The practical threshold for PM dashboard adoption is < 30 manual inputs/week. If an API can provide it, never ask the PM to type it.
69. **Bilingual i18n must use data attributes, not duplicate HTML** — v2 uses `data-i18n` keys with a JS translation map (~223 keys). Duplicating entire pages for EN/AR doubles maintenance and guarantees drift. Plan for `data-i18n` from the start so every text element is toggle-ready.
70. **Print CSS must show all tabs, not just the active one** — Dashboard print styles that hide inactive tabs produce blank pages. Use `display: block !important` on all `.tab-content`, add `page-break-before: always` between sections, and inject section titles via `content: attr(data-tab-title)` pseudo-elements. Always test Ctrl+P after adding print styles.
71. **Metric cards should be clickable drill-downs, not dead-end numbers** — Showing "To Do: 12" is useless without knowing who owns what. Every aggregate metric card should open a per-member or per-project breakdown modal on click (`showTeamDetailModal`). This was the key UX improvement in Team Pulse v2 — all 6 teams, 4 states each, 24 clickable drill-downs.

## Auto-Updater & UX Redesign Lessons (Mar 25, 2026)

72. **PowerShell em-dash crash** — Unicode characters (em-dash, curly quotes) in PowerShell string literals cause silent parse failures. The window closes instantly with no error. Always use ASCII alternatives (`--` not `—`, straight quotes not curly).
73. **Always provide .bat launcher for PS scripts** — "Right-click → Run with PowerShell" closes the window on any error. Create a `.bat` file with `powershell -ExecutionPolicy Bypass -NoExit -File script.ps1` so errors stay visible.
74. **Disable update buttons when no drift** — "Full Update" when already up-to-date is misleading and risky. Separate into 3 buttons: Check (always available), Pull+Update (only when drift), Audit Only (always available). Grey out unavailable actions.
75. **Automate recurring failures** — If a check is missed 3+ times across sessions, build a tool. The auto-updater script exists because manual drift fixes repeatedly missed Document Control tables, assumptions, and internal content. Human checklists fail; scripts don't forget.
76. **3 page types define nav UX** — Action pages (green, interactive buttons for decisions), Reference pages (blue, read-only for board review), Audit pages (purple, health history snapshots). Organize navigation by type, not by arbitrary categories. Directors need to know: "where do I click?" vs "where do I read?"
77. **Merge overlapping pages** — Two pages covering the same topic (KICKOFF_READINESS_GUIDE + KICKOFF_READINESS_VALIDATION) confuse the Director. One source of truth per topic. If you create a summary page, merge it into the original rather than adding another file.
