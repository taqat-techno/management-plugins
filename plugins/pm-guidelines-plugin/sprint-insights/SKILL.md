---
name: sprint-insights
description: |
  Sprint-governance reporting workflow for an Azure DevOps project. Activate whenever Mahmoud requests "Sprint Insights" — or a sprint report, governance validation, gap-closure verification, or executive sprint brief — for a project. Enforces the confirmed 3-step discipline: (1) derive the deliverables folder name FROM the ADO project and CONFIRM it with Mahmoud before acting; (2) set up / reconcile the folder; (3) produce the bilingual EN/AR deliverable set from LIVE, read-only ADO data. Pairs with the `/sprint-insights` slash command and the `feedback-sprint-insights-request-workflow` memory rule.

  <example>
  Context: Mahmoud asks for sprint insights on a project.
  user: "Sprint Insights for Relief Center"
  assistant: "Activating sprint-insights. First I'll derive and CONFIRM the folder name (`D:\Relief Center\Sprint Governance & Reporting\`) before generating anything, then pull live read-only ADO and build the bilingual deliverable set."
  <commentary>Phrase "Sprint Insights" + a project → run the name-gate, then the exercise.</commentary>
  </example>

  <example>
  Context: A governance/sprint request tied to a DevOps project.
  user: "Put together the governance validation + gap closure for the Wallet sprint."
  assistant: "That's the sprint-insights workflow. I'll confirm the target project + folder name first, then generate the governance validation and gap-closure reports from a live read-only ADO pull."
  <commentary>Governance-validation / gap-closure for a sprint → same skill.</commentary>
  </example>
---

# sprint-insights — Sprint Governance & Reporting for an Azure DevOps project

Produce (or refresh) the full sprint-governance deliverable set for a given Azure DevOps project. The deliverables folder is named after the ADO project, its name is **confirmed with Mahmoud first**, the folder is set up correctly, then bilingual EN/AR reports are generated from **live, read-only** ADO data.

Canonical copies of this workflow: the `/sprint-insights` slash command (`~/.claude/commands/sprint-insights.md`) and memory `feedback-sprint-insights-request-workflow.md` + `project_bms_wallet_unified_syed.md`. Precedent to mirror: `D:\KhairGate BMS and Wallet\Sprint Governance & Reporting\`.

## Step 1 — RESOLVE & CONFIRM THE FOLDER NAME (GATE — do NOT skip)

1. Identify the target Azure DevOps project (resolve partial names via `core_list_projects`; if ambiguous, ask).
2. Derive the deliverables folder — default pattern `D:\<ADO Project Name>\Sprint Governance & Reporting\` (never a bare generic `Sprint Insights` folder beside the project's source folders).
3. **Present the proposed folder name/path to Mahmoud and WAIT for explicit confirmation.** Create/move/generate nothing until he approves.

## Step 2 — FOLDER SETUP / RECONCILIATION

- **New:** create the confirmed folder + a `README.md` index.
- **Existing but mis-named/mis-located:** run the move/rename reconciliation checklist — verify cross-links are relative, update memory path refs, restore/confirm `.pm-protected-paths` freeze coverage, retitle `README`/H1, recreate `.claude` settings, RAG check, delete any leftover husk. (The directory-in-use lock blocks an atomic rename from inside the session → use `robocopy /MOVE`; note the empty husk to delete after the session ends.)

## Step 3 — PRODUCE THE DELIVERABLES (live ADO, read-only)

Pull live from Azure DevOps (WIQL / REST via `az rest` or the DevOps MCP), snapshotting `ASOF` at each sprint close vs current. **Read-only — never move or modify work items.** If the project splits work by Area Path, keep **streams never mixed** (tag every metric Area · Sprint · Iteration · Source). Generate, bilingual EN/AR (paired-span + RTL, house style):

1. Sprint Report (current insights + past-sprint carry-forward)
2. Governance Validation Report (vs the prior cycle's success criteria)
3. Gap-Closure Verification (did prior actions land? per-dimension trend + evidence)
4. Executive Board Brief (one-page BLUF + KPI cards + single ask; no work-item IDs)
5. Success Criteria Validation (lead-facing PASS/PARTIAL/FAIL scorecard)
6. Operational Action Plan (lead-facing item-level open-work + live ADO links)
7. Action-item register (internal) + cover email to the team lead

Validate each HTML: `pm-bilingual-qa` span parity + a live Playwright render pass.

## Critical rules

1. **Confirm the folder name BEFORE acting** (the Step-1 gate).
2. **Read-only on ADO work items** — reporting only; never move/reassign/edit.
3. **Bilingual EN/AR**, house style; **MENA Sun–Thu** workweek for any SLA/date math.
4. **Version every update** — never overwrite a prior version; supersede with `_vN+1`.
5. **Streams never mixed** — a single-stream number is never presented as "overall".
6. **Never fabricate SP velocity** — if Story-Point coverage <15%, use PBI/work-item throughput with QC-lag + recency caveats.
7. **Label in-sprint vs eventual** completion (Done@close/committed vs current membership).

## Linked skills

`pm-data-readiness` + `pm-devops-integration` (live-pull + WIQL discipline), `pm-bilingual-standards` + `pm-report-writing` (parity + structure), `pm-source-provenance` (every load-bearing number carries a live source). Run `/PM-lessons-check` on generated HTML.
