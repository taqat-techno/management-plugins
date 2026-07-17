---
name: pm-subagent-verification
description: |
  Verification discipline for any claim produced by a subagent, an Explore/search agent, a workflow result, or a prior-session summary, BEFORE that claim is propagated into a plan, a fix-list, a deliverable, or another agent's input. Subagent and search output is TRIAGE, not ground truth: spot-check 2-3 of its load-bearing claims by direct grep/Read; if the first is wrong, distrust the rest. Always grep before writing "X is missing / identical / absent" into a plan. Label every relayed claim as verified vs subagent-reported. Run a mandatory prior-occupant proper-noun grep before cloning any template. Use whenever you run multi-agent workflows, act on summarized findings, or clone a "template" that may be a filled-in prior artifact. This is the activatable layer of the verify-the-claim discipline.

  <example>
  Context: A multi-agent workflow returned a fix-list.
  user: "The review agents found 6 issues — go fix them."
  assistant: "I'll apply pm-subagent-verification first: I'll grep-confirm 2-3 of the 6 findings against the source before editing. If the first one doesn't reproduce, I'll re-verify the rest rather than fixing non-bugs."
  <commentary>Subagent findings are triage — verify before acting.</commentary>
  </example>

  <example>
  Context: About to write an absence claim into a plan.
  user: "Add to the plan that the config has no retry setting."
  assistant: "pm-subagent-verification: before writing 'no retry setting' I'll grep the config myself — absence claims are the easiest to get wrong from a summary."
  <commentary>Never assert missing/identical/absent without a direct grep.</commentary>
  </example>

  <example>
  Context: Cloning a 'template'.
  user: "Clone this interview-form template for the new candidate."
  assistant: "pm-subagent-verification: I'll grep the file for prior-occupant proper nouns first — a 'template' is often a filled-in prior artifact, and copying it would leak the previous candidate's data."
  <commentary>Prior-occupant grep before any template clone (data-leak guard).</commentary>
  </example>

  <example>
  Context: Relaying a prior-session summary as fact.
  user: "Last session you said the migration was done — build on that."
  assistant: "pm-subagent-verification: I'll re-establish that first-hand (check the migration state directly) and label it verified before building on it, rather than treating the prior summary as ground truth."
  <commentary>Demote relayed claims to 'not independently verified' until re-checked.</commentary>
  </example>
license: "MIT"
metadata:
  version: "1.0.0"
  priority: 70
  model: sonnet
  filePattern: []
  promptSignals:
    phrases:
      - "the agent found"
      - "the subagent said"
      - "the review found"
      - "according to the search"
      - "is missing"
      - "is identical"
      - "is absent"
      - "has no"
      - "clone this template"
      - "use this as a template"
      - "the summary says"
      - "the workflow returned"
      - "last session you said"
    minScore: 6
---

# PM Subagent-Claim Verification

Read-only auditors, Explore/search agents, workflow results, and prior-session summaries are **triage signals, not ground truth**. They can themselves be the source of a false claim — and a constructive review that returns "all clear" only *confirms*; it does not prove. Propagating an unverified subagent claim into a plan, a fix-list, or a deliverable causes two recurring failures: **fixing non-bugs** (wasting a cycle on a finding that doesn't reproduce) and **shipping wrong data** (e.g. cloning a "template" that was a filled-in prior artifact and leaking the previous occupant's content).

This skill makes a 10-second grep the gate before any of those claims is acted on or written down.

## The rules

1. **Triage, not truth.** After any subagent/search/workflow run, spot-check **2-3 load-bearing claims** by direct grep/Read against the source. If the **first** one is wrong, distrust the rest and re-verify the whole set.
2. **Grep before any absence/equality claim.** Never write "X is missing / absent / identical / has no Y" into a plan or deliverable without a direct grep that proves it. Absence claims are the easiest to get wrong from a summary.
3. **Label provenance.** Distinguish **verified** (re-established first-hand this turn) from **subagent-reported** (relayed). Demote any relayed claim to "not independently verified" until re-checked.
4. **Prior-occupant grep before any template clone.** Before cloning a "template," grep it for proper nouns / prior-occupant data — a "template" is frequently a filled-in prior artifact. This is a data-leak guard, not a nicety.
5. **Disagreement = low confidence.** When parallel agents disagree, treat the claim as low-confidence and resolve it first-hand before propagating.

## Procedure

1. Identify the load-bearing claims in the subagent/search/summary output (the ones a plan or deliverable will rely on).
2. Pick 2-3 and verify by grep/Read against the real source. Stop-and-widen if the first fails.
3. For any "missing/absent/identical" claim, run the confirming grep explicitly.
4. Before a template clone, grep for prior-occupant proper nouns.
5. Tag each propagated claim verified / subagent-reported; carry the tag into the plan or report.

## Related surfaces (no duplication)

- `pm-report-reviewer` — the read-only review *orchestrator*; it delegates to specialist auditors. This skill governs how you **trust the output** of those auditors (and of any Explore/workflow) before you act on it — the complementary half of the review loop.
- `lesson-gap-analyzer` — produces coverage findings; this skill says to spot-check them before treating a "GAP" as fact.

## Source lessons

#814, #833, #836, #946, #959, #980, #981 (and the multi-agent verification + template-clone-leak incidents).
