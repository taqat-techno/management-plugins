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
3. **NEVER infer completion from a state's CATEGORY — confirm the team's actual convention first.** A project may use a terminal state that Azure DevOps categorises as *Resolved* rather than *Completed*. On TaqaTechno projects **`Closed` means delivered AND PMO-closed**: the team sets `Done`, then the PM applies `Closed` on a weekly closure run so work rolls into monthly/quarterly reporting, stamping `Custom.ClosureDate`. So **delivered = `State IN ('Done','Closed')` for Tasks and `State = 'Done'` for PBIs/Features/Epics**. Verify via revision history (`/workItems/{id}/revisions`) before reporting delivery. The stock `Microsoft.VSTS.Common.ClosedDate` may be empty — that is NOT evidence of incompletion. ADO's built-in velocity/burndown widgets under-read because they key on category; WIQL-based PMO reporting is correct. Mention that only as a neutral footnote, never as a defect, and **never recommend moving `Closed` items back to `Done`** — that breaks the PMO closure process.
4. **`Removed` is excluded from every population AND from the narrative, permanently** — never a numerator, never a denominator, never a row, never named, and never the subject of a reconciliation count. Do NOT write "N total less M Removed"; report the in-scope figure only. **Items explicitly marked for deletion** (titled `test`, `[DELETE ME]`, duplicate stubs) get the same treatment — but have them set to `Removed` AT SOURCE rather than filtering by title, because a title heuristic silently drops genuine work (e.g. "A/B test the checkout").
5. **Match the denominator to the population the metric is about** — actual-hours coverage over *completed* items, remaining-work over *in-progress* items, estimates over *planned* items. Dividing by "all tasks" turns a healthy 100% into a false 18%.
6. **Classify completed work before characterising it** — group finished items by title prefix and logged hours before saying what the team has been doing.
7. **A batch of same-day status changes is a process signature, not automatically a defect** — check for a scheduled ritual (e.g. the weekly PMO closure run) before flagging.
8. **Bilingual EN/AR**, house style; **MENA Sun–Thu** workweek. Compute working-day counts, never assert them.
9. **Version every update** — never overwrite a prior version; supersede with `_vN+1`.
10. **Streams never mixed** — a single-stream number is never presented as "overall".
11. **Never fabricate SP velocity** — <15% coverage → use throughput with caveats; and never quote a point velocity when zero backlog items have reached `Done`.
12. **Publish in-sprint vs eventual** completion as columns, never bare percentages: `Planned @close · Completed @close · In-sprint %` then `Items now · Completed now · Eventual %`, under a two-tier header separating *at close (immutable, `ASOF`)* from *today (live membership, no `ASOF`)*. Labelling the denominator in a callout is **not** sufficient — a reader reuses the only denominator on the row (`Planned`) and concludes the report is arithmetically wrong. Cross-check `Items now − Completed now` against the open/stranded count published elsewhere. Evidence: KhairGate Jul-19 v1 → v2 correction; global lesson #1291.
13. **Re-pull rather than reuse a cached snapshot** — a live project changes during a session.
14. **Every data-table column carries a `?` tooltip** giving its exact definition *and the query behind it* — bilingual EN/AR paired spans inside the bubble so the existing language toggle drives it, `tabindex="0"` for keyboard, edge-clamped on first/last column and RTL-mirrored so none clip offscreen, `@media print{display:none}`. Skip only self-evident prose columns (Recommendation / Owner / Why). A definition that lives only in a callout is skipped by the reader who is staring at the number. Global lesson #1332.

## Linked skills

`pm-data-readiness` + `pm-devops-integration` (live-pull + WIQL discipline), `pm-bilingual-standards` + `pm-report-writing` (parity + structure), `pm-source-provenance` (every load-bearing number carries a live source). Run `/PM-lessons-check` on generated HTML.
