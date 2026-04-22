# Ragtools Evaluation Report

**Period:** April 12 – April 16, 2026  
**Author:** Mahmoud Elshahed, IT Project Manager  
**Date:** April 16, 2026  

---

## 1. Executive Summary

Ragtools is the local AI-powered knowledge base system deployed on the IT PM workstation to enable semantic search across all project documentation. It indexes Markdown files from 43 project folders on the D:\ drive, embedding them into a Qdrant vector database using the `all-MiniLM-L6-v2` sentence-transformer model.

## Key Metrics (Current State):

| Metric | Value |
|--------|-------|
| Installation Date | April 12, 2026 |
| Current Version | v2.4.x (rag-plugin 0.4.0) |
| Indexed Projects | 43 |
| Total Chunks | 28,741 |
| Data Size | 173 MB |
| Embedding Model | all-MiniLM-L6-v2 (384 dimensions) |
| Service Mode | Direct (MCP) — HTTP server down |
| Search Quality | 0.47–0.72 on topical queries |

**Verdict:** The system is **operationally functional** via MCP direct mode but has **two active issues** — the HTTP service has crashed (PID mismatch), and Qdrant is running above the recommended local-mode threshold (27,604 points vs 20,000 max recommended). Six governance lessons were codified during this period, and the RAG-FIRST RULE was activated on Apr 15 to mandate knowledge base consultation before answering domain questions.

---

## 2. Timeline

### Day 1 — April 12, 2026: Installation & Initial Indexing

- Ragtools installed at `C:\Users\DELL\AppData\Local\Programs\RAGTools\rag.exe`
- Data directory created at `C:\Users\DELL\AppData\Local\ragtools\`
- Qdrant embedded database initialized at `data\qdrant\`
- Configuration file `config.toml` created (version = 2)
- **42 projects registered** (IDs 1–42) covering:
  - KhairGate HUB: 11 entries
  - Project Management: 9 entries
  - DevOps: 4 entries
  - HR: 2 entries
  - Personal: 3 entries
  - Other projects: 13 entries
- Batch script generated 37 `<folder-name>.md` files for indexed folders
- `scan_baseline.json` created as point-in-time snapshot
- **Bug (discovered later):** Script silently skipped folder names with parentheses — e.g., `KhairGate (HUB)` was missed

### Day 2 — April 13, 2026: Coverage Audit & 6 Lessons Learned

**Session ID:** `b159d02d-6639-4c54-8bbb-425606ad3971`

A comprehensive 3-check RAG coverage audit was performed, revealing multiple gaps:

1. **Missing MD file:** `D:\KhairGate (HUB)\KhairGate (HUB).md` — skipped by the Apr 12 batch script due to unescaped parentheses
2. **Missed sub-folder:** `D:\Project Management\Project management Quarter Plan\Projects Handling Review Meeting 6-4-2026` — new sub-folder inside an already-indexed parent, invisible to "new top-level folders" check
3. **WebFetch failure:** `WebFetch http://127.0.0.1:21420/projects` returned ECONNREFUSED — tool silently upgrades HTTP→HTTPS, but localhost doesn't bind HTTPS
4. **Stale baseline:** `scan_baseline.json` from Apr 12 missed a folder created Apr 13 at 06:50

**Actions taken:**
- Created missing `KhairGate (HUB).md`
- Added project #43: `project-management-quarter-plan`
- Config updated at 19:45 with new project entry
- **6 lessons codified** as Global Lessons #363–368 (Source-Root RAG Sync & Live-Scan Discipline)

**Final state:** 43 projects (42 numeric + 1 named)

### Day 3 — April 14, 2026: Plugin v0.4.0 & Functional Test

**RAG Plugin upgraded to v0.4.0** — major command consolidation:

| Old Commands | New Command | Change |
|---|---|---|
| `/rag-status` + `/rag-repair` | `/rag-doctor` | Unified diagnostics |
| `/rag-upgrade` | `/rag-setup` | State-aware install/upgrade |
| 9 total commands | 6 user-facing + 1 maintainer | -33% surface area |

Other v0.4.0 changes:
- Windows stdio pipe bug fixed (v0.3.3 retraction)
- MCP wiring finalized: flat `.mcp.json` shape, `rag serve` direct spawn
- Decisions D-020 (direct spawn vs Python wrapper) and D-021 (state-aware consolidation) implemented

## Functional test results:

| Metric | Value |
|--------|-------|
| Indexed Files | 705 |
| Total Chunks | 33,331 |
| Projects | 43 |
| Largest Project | ID 7 (KhairGateWorld-Repository) — 228 files, 11,854 chunks |
| Search Quality | 0.47–0.72 on topical queries |
| Noise Floor | < 0.45 |

### Day 4 — April 15, 2026: RAG-FIRST RULE Activated

The **RAG-FIRST RULE** was added as line 1 of `C:\Users\DELL\.claude\CLAUDE.md` with "user override" designation:

> *"For EVERY question I ask — domain, PM, project, DevOps, lessons, decisions, file locations, versions, history, conventions — you MUST call `search_knowledge_base` FIRST before answering."*

**Three narrow exemptions:**
1. Answer already in current turn's messages/tool results
2. Ragtools product operation questions (use `/rag-*` commands)
3. Pure general-programming / public-knowledge / math / trivia questions

**Search discipline established:**
- Default `top_k=5`
- Weak results (<0.5) allow one reformulated query before fallback
- Cite source files inline when grounding answers
- Never say "I don't have information about X" without searching first

### Day 5 — April 16, 2026 (Today): Current State Assessment

**Service startup at 10:03:**
- HTTP server started on `127.0.0.1:21420` (PID 16236)
- File watcher started for 43 projects (debounce=3000ms)
- Startup sync: **167 files indexed, 87 deleted, 517 unchanged**

**Service crash:**
- PID 16236 is no longer running
- 3 `rag.exe` processes active (PIDs 8100, 3548, 9764) — these are MCP direct-mode instances, NOT the HTTP server
- HTTP endpoint returns connection refused (exit code 7)
- MCP direct mode remains functional

**File watcher activity (while service was alive):**
- 10:38 — Project 1 (Global Lessons): 1 file indexed, 16 skipped
- 12:16–12:19 — Project 30 (Relief Center): 7 incremental updates (1 file each cycle)

---

## 3. Coverage Audit — 43 Indexed Projects

### By Category

| Category | Count | Project IDs |
|----------|-------|-------------|
| **KhairGate HUB** | 11 | 2, 3, 4, 5, 6, 7, 8, 38, 39, 40, 41 |
| **Project Management** | 10 | 9, 10, 11, 12, 13, 14, 15, 16, 17, project-management-quarter-plan |
| **DevOps** | 4 | 18, 19, 20, 21 |
| **Personal** | 3 | 27, 28, 29 |
| **HR** | 2 | 23, 24 |
| **Other Projects** | 13 | 1, 22, 25, 26, 30, 31, 32, 33, 34, 35, 36, 37, 42 |
| **Total** | **43** | |

### Full Project Registry

| ID | Name | Path |
|----|------|------|
| 1 | Global Lessons | `D:\Global Lessons` |
| 2 | KhairGate HUB-xhatem-Github | `D:\KhairGate (HUB)\xhatem-Github` |
| 3 | KhairGate HUB-Investigation Results | `D:\KhairGate (HUB)\Investigation Results` |
| 4 | KhairGate HUB-khairworld-trial-main V.4 | `D:\KhairGate (HUB)\khairworld-trial-main V.4` |
| 5 | KhairGate HUB-Mixed-Mode | `D:\KhairGate (HUB)\Mixed-Mode` |
| 6 | KhairGate HUB-Migration_Analysis (Basha) | `D:\KhairGate (HUB)\Basha\Migration_Analysis 1\Migration_Analysis` |
| 7 | KhairGate HUB-KhairGateWorld-Repository | `D:\KhairGate (HUB)\KhairGateWorld-Repository` |
| 8 | KhairGate HUB-KhairWorld BRD | `D:\KhairGate (HUB)\KhairWorld BRD` |
| 9 | Project Management-Source-Root | `D:\Project Management\Source-Root` |
| 10 | Project Management-QA-QC & Dev Activity RACI | `D:\Project Management\QA-QC & Devlopment Activity - RACI Matrix` |
| 11 | Project Management-Monthly Reports | `D:\Project Management\Monthly Reports` |
| 12 | Project Management-Department Workflows | `D:\Project Management\Department Workflows` |
| 13 | Project Management-Weekly Meeting | `D:\Project Management\Weekly Meeting` |
| 14 | Project Management-Taqat Alignment Framework | `D:\Project Management\Taqat Alignment Framework - Hatem` |
| 15 | Project Management-Outlook | `D:\Project Management\Outlook` |
| 16 | Project Management-OKR & KPI | `D:\Project Management\OKR & KPI` |
| 17 | Project Management-Claude Courses | `D:\Project Management\Claude Courses` |
| 18 | DevOps-Semir Reports | `D:\DevOps\Semir Reprots` |
| 19 | DevOps-Process Best Practice Rules | `D:\DevOps\DevOps Process Best Practice Rules` |
| 20 | DevOps-Bug Criteria | `D:\DevOps\Bug Criteria` |
| 21 | DevOps-General | `D:\DevOps\General` |
| 22 | Udemy | `D:\Udemy` |
| 23 | HR-Senior Odoo Developer | `D:\HR\Senior Odoo Developer` |
| 24 | HR-Software QC Engineer | `D:\HR\QC\Software QC Engineer` |
| 25 | Water for Mosques | `D:\Water for Mosques` |
| 26 | Alaqraboon | `D:\Alaqraboon` |
| 27 | Personal-Scrum Master Certification | `D:\Personal\Scrum Master Certification Scrum Methodologies` |
| 28 | Personal-Hatem | `D:\Personal\Hatem` |
| 29 | Personal-PM2Agile Course | `D:\Personal\PM2Agile Course` |
| 30 | Relief Center | `D:\Relief Center` |
| 31 | BMS | `D:\BMS` |
| 32 | KhairGate Wallet (original) | `D:\KhairGate (Wallet)` |
| 33 | TfsData | `D:\TfsData` |
| 34 | Taqat Trading & Business Solutions | `D:\Taqat Trading & Business Solutions` |
| 35 | Afriqat | `D:\Afriqat` |
| 36 | IndoQat | `D:\IndoQat` |
| 37 | Herbal Gardens | `D:\Herbal-Gardens` |
| 38 | KhairGate HUB-Hub-Analysis | `D:\KhairGate (HUB)\xhatem-Github\Khairgate_analysis\KhairGate-Hub-Analysis` |
| 39 | KhairGate HUB-Hub-Analysis-V2 | `D:\KhairGate (HUB)\xhatem-Github\Khairgate_analysis\KhairGate-Hub-Analysis-V2` |
| 40 | KhairGate HUB-Migration_Analysis (xhatem) | `D:\KhairGate (HUB)\xhatem-Github\Khairgate_analysis\Migration_Analysis` |
| 41 | KhairGate HUB-Mixed-Mode (xhatem) | `D:\KhairGate (HUB)\xhatem-Github\Khairgate_analysis\Mixed-Mode` |
| 42 | KhairGate Wallet | `D:\KhairGate Wallet` |
| QP | Project Management-Quarter Plan | `D:\Project Management\Project management Quarter Plan` |

---

## 4. Incidents & Lessons Learned

### Lesson #363 — Coverage Audit Requires 3 Checks, Not 1

**Date:** Apr 13, 2026 | **Severity:** High  
**Incident:** Answered "no new folders on D:\" when asked if RAG needed updating — missed sub-folder drift.  
**Rule:** Every RAG coverage audit must run: (1) new top-level folders vs baseline, (2) every folder's root MD via Glob, (3) live RAG list diff.  
**Status:** Codified in global_lessons.md and memory

### Lesson #364 — RAG Entries Are Per Sub-Session, Not Per Root Folder

**Date:** Apr 13, 2026 | **Severity:** Medium  
**Incident:** Nearly added a duplicate root-level entry that would have bloated the index.  
**Rule:** Before adding a new RAG entry, check if the path is already covered by existing sub-entries. Never add root entries on top of sub-entries.  
**Status:** Codified and enforced

### Lesson #365 — WebFetch Auto-Upgrades HTTP to HTTPS

**Date:** Apr 13, 2026 | **Severity:** Medium  
**Incident:** WebFetch to `http://127.0.0.1:21420` returned ECONNREFUSED despite server being up.  
**Rule:** For any localhost HTTP service, use `curl` via Bash, never WebFetch.  
**Status:** Codified; all subsequent localhost calls use curl

### Lesson #366 — Baselines Go Stale Within 24 Hours

**Date:** Apr 13, 2026 | **Severity:** Medium  
**Incident:** Baseline from Apr 12 missed folder created Apr 13 at 06:50.  
**Rule:** Always cross-check against live sources. Never answer "nothing new" from a baseline >24 hours old without live verification.  
**Status:** Codified and enforced

### Lesson #367 — Batch Scripts Skip Special Characters Silently

**Date:** Apr 12/13, 2026 | **Severity:** High  
**Incident:** Batch created 37 MD files but silently skipped `KhairGate (HUB)` due to unescaped parentheses.  
**Rule:** Test batch operations against edge-case names before running. Add post-run verification.  
**Status:** Codified; gap was manually closed

### Lesson #368 — Remove-Then-Re-Add for RAG Updates

**Date:** Apr 13, 2026 | **Severity:** Low  
**Rule:** Existing entries must be deleted before re-adding (RAG caches stale metadata). New entries go directly via POST.  
**Status:** Codified as operational procedure

---

## 5. RAG-FIRST RULE

**Effective:** April 15, 2026  
**Location:** Line 1 of `C:\Users\DELL\.claude\CLAUDE.md`  
**Override Level:** User override — takes precedence over all other retrieval rules

### Rule Summary

Every domain question must trigger a `search_knowledge_base` call BEFORE the assistant answers. The assistant must never claim "I don't have information about X" without having searched in the current turn.

### Exemptions

| # | Exemption | Example |
|---|-----------|---------|
| a | Answer already in current turn's context | Tool results from the same turn |
| b | Ragtools product operations | Use `/rag-doctor`, `/rag-setup` instead |
| c | Pure general knowledge / math / trivia | No chance of being in local notes |

### Search Discipline

- Default `top_k=5`
- Weak results (<0.5): one reformulated query allowed before fallback
- Results >= 0.7: ground answer and cite source files inline
- Results 0.5–0.7: use as context, label "from my notes:", suggest verification
- Results < 0.5 or empty: state "I checked your knowledge base and didn't find information about X"

---

## 6. Current Health & Diagnostics

### Active Issues

#### Issue 1: HTTP Service Down (PID Mismatch)

- **Service PID file:** `data/service.pid` contains PID 16236
- **Actual running processes:** rag.exe PIDs 8100, 3548, 9764 (none match 16236)
- **Root cause:** The HTTP server process (PID 16236) started at 10:03:46, completed startup sync by 10:13:58, but subsequently crashed or was killed
- **Impact:** HTTP endpoints (`/health`, `/ui/projects/list`) return connection refused
- **Workaround:** MCP direct mode works — `index_status`, `list_projects`, and `search_knowledge_base` all functional
- **Recommended fix:** Restart the service with `rag serve` or restart Claude Code session

#### Issue 2: Chunk Count Drop (33,331 to 28,741)

- **Drop magnitude:** -4,590 chunks (-13.8%)
- **Root cause (confirmed from logs):** Startup sync on Apr 16 at 10:13:58 reported:
  - **167 files indexed** (new or modified since last run)
  - **87 files deleted** from the index (source files no longer exist on disk)
  - **517 files unchanged** (skipped)
- **Explanation:** Between Apr 14 and Apr 16, files were moved, renamed, or deleted across the workspace (e.g., workspace reorganization on Apr 15 — lesson #388 about moving Taqat repos). The deleted 87 files had their chunks removed, while 167 new/modified files added fewer chunks than the deleted ones contained
- **Assessment:** This is **expected behavior** — the index correctly reflects the current state of the filesystem

#### Issue 3: Qdrant Local Mode Warning

- **Warning:** "Local mode is not recommended for collections with more than 20,000 points. Current collection contains 27,604 points"
- **Impact:** Potential performance degradation for large queries
- **Recommendation:** Monitor; if search latency increases, consider migrating to Qdrant in Docker

### System Health Summary

| Component | Status | Details |
|-----------|--------|---------|
| rag.exe binary | Installed | `C:\Users\DELL\AppData\Local\Programs\RAGTools\rag.exe` |
| Config file | Valid | `config.toml` v2, 43 projects, last modified Apr 13 |
| Qdrant database | Active | 173 MB, 28,741 chunks, 384-dim vectors, Cosine distance |
| Index state DB | Active | `index_state.db` (457 KB), last modified Apr 16 12:19 |
| HTTP service | DOWN | PID 16236 dead; curl returns exit 7 |
| MCP direct mode | UP | All 3 tools functional (`index_status`, `list_projects`, `search_knowledge_base`) |
| File watcher | WAS ACTIVE | Tracked changes in projects 1 and 30 before service died |
| Logs | Available | `data/logs/service.log` (125 KB) |

---

## 7. Recommendations

### Immediate Actions

1. **Restart HTTP service** — Run `rag serve` to restore the HTTP endpoint on port 21420. This will also restart the file watcher for live re-indexing.

2. **Verify file watcher coverage** — After restart, confirm the watcher picks up changes made while the service was down. The startup sync should handle this automatically.

### Short-Term (This Week)

3. **Add missing project folders** — The Apr 15 workspace reorganization may have created new sub-folders not yet registered in `config.toml`. Run the 3-check coverage audit (lesson #363) to identify gaps.

4. **Monitor Qdrant performance** — Track search latency. If queries slow down above 500ms, evaluate Docker deployment for Qdrant.

### Medium-Term (This Month)

5. **Service auto-restart mechanism** — The HTTP service crashed silently. Consider adding a Windows Task Scheduler job or a watchdog script that checks `curl http://127.0.0.1:21420/health` every 5 minutes and restarts `rag serve` if it fails.

6. **Scheduled re-indexing** — Add a weekly full re-index job to catch any drift between filesystem state and index state.

7. **Index size governance** — At 28,741 chunks across 43 projects, the index is near the Qdrant local-mode limit. Establish a policy for:
   - Archiving completed project folders (remove from config.toml, keep on disk)
   - Evaluating whether all 11 KhairGate HUB sub-entries are still needed
   - Setting ignore_patterns for large binary or generated files

### Long-Term

8. **Version tracking** — The binary doesn't report `--version`. Track rag-plugin versions via the Claude plugin cache directory (`plugins\cache\plugins\rag\<version>\`).

9. **Usage analytics** — Leverage the rag-plugin's usage-log toggle (`/rag-config`) to track which projects are searched most and least, informing index pruning decisions.

---

## Appendix: Configuration Reference

**Binary:** `C:\Users\DELL\AppData\Local\Programs\RAGTools\rag.exe`  
**Data:** `C:\Users\DELL\AppData\Local\ragtools\data\`  
**Config:** `C:\Users\DELL\AppData\Local\ragtools\config.toml`  
**Logs:** `C:\Users\DELL\AppData\Local\ragtools\data\logs\service.log`  
**Plugin:** `C:\Users\DELL\.claude\plugins\cache\plugins\rag\0.4.0\`  
**PID File:** `C:\Users\DELL\AppData\Local\ragtools\data\service.pid`  
**Qdrant DB:** `C:\Users\DELL\AppData\Local\ragtools\data\qdrant\`  

**Available Commands:**
| Command | Purpose |
|---------|---------|
| `/rag-doctor` | Diagnose + status + repair (unified) |
| `/rag-setup` | Install + upgrade + verify (state-aware) |
| `/rag-projects` | Project CRUD via HTTP API |
| `/rag-reset` | Destructive 3-level reset |
| `/rag-config` | Plugin-layer configuration |

**Port Map:**
| Port | Service |
|------|---------|
| 21420 | Ragtools (HTTP + MCP) |
| 5050 | Outlook Update Server |
| 5051 | KhairGate Standalone Update Server |
| 5052 | Taqat Dashboard Server |
| 5053 | D Drive Scan Server |
