---
name: pm-session-discipline
description: |
  PM session workflow discipline — memory vs tasks distinction, lesson capture protocol, session log updates, and git-pull-before-analysis rituals. Use when managing session state, capturing lessons, or deciding what goes into memory vs todo lists.


  <example>
  Context: User asks to save something to memory
  user: "Remember this for next time"
  assistant: "I will use the pm-session-discipline skill to determine if this belongs in memory (future conversations) or tasks (current session), and save it to the right place."
  <commentary>Memory decision trigger - classify what goes where.</commentary>
  </example>

  <example>
  Context: Session is ending after significant work
  user: "We're done for today"
  assistant: "I will use the pm-session-discipline skill to capture session lessons, update the session log in MEMORY.md, and record any corrections or validated approaches."
  <commentary>Session end trigger - proactive lesson capture.</commentary>
  </example>

  <example>
  Context: User wants to analyze repo data
  user: "Analyze the latest deliverables in the repo"
  assistant: "I will use the pm-session-discipline skill to ensure we pull latest before analyzing, check git diff after pull, and record the session context."
  <commentary>Analysis start trigger - pull-before-analyze ritual.</commentary>
  </example>
license: "MIT"
metadata:
  version: "1.3.0"
  priority: 50
  model: sonnet
  filePattern:
    - "**/MEMORY.md"
    - "**/memory/**"
    - "**/lessons.md"
    - "**/tasks/todo.md"
  bashPattern:
    - "git pull"
    - "git diff"
    - "git log"
    - "git status"
    - "git push"
  promptSignals:
    phrases:
      - "save lesson"
      - "remember this"
      - "session log"
      - "capture lessons"
      - "update memory"
      - "end of session"
      - "we're done"
      - "wrap up"
      - "done for today"
      - "pull before"
      - "fast-forward"
      - "powershell regex"
      - "edit the HTML"
      - "regenerate HTML"
    minScore: 6
---

# PM Session Discipline

## Rule 36: Save Lessons at End of Every Session

Don't wait for the user to ask. At the end of each working session, proactively:

1. **Identify corrections** — Did the user correct your approach? Save the pattern to prevent repeating.
2. **Identify validations** — Did a non-obvious approach work well? Save positive patterns too.
3. **Update project memory** — Record key decisions, team composition changes, estimation methodology used.
4. **Update global lessons** — If the lesson applies across projects, add to `researches/PM-guidelines.md`.

### What to Capture

| Capture | Example |
|---------|---------|
| Corrections | "User said: don't use abbreviations in board reports" |
| Validated approaches | "Single bundled PR was the right call for this refactor" |
| Key decisions | "v2 plan reduced from 9 months to 4 months" |
| Team context | "Backend team at 80% allocation through Q2" |

### What NOT to Capture

| Skip | Why |
|------|-----|
| Current debug state | Ephemeral — only useful right now |
| Temp file paths | Will change next session |
| Code patterns | Derivable from reading the code |
| Git history | Use `git log` / `git blame` |

## Rule 37: Memory is for Future Conversations

### Decision Matrix

| Information Type | Save To | Why |
|-----------------|---------|-----|
| Task breakdown for current work | `tasks/todo.md` (TodoWrite) | Only useful this session |
| Correction that applies to future work | Memory file | Prevents repeating mistakes |
| Project estimation methodology | Memory file | Context for future estimates |
| Current file being debugged | Nowhere (ephemeral) | Changes constantly |
| Team member allocation percentages | Memory file | Informs future planning |
| Build command that just worked | Nowhere (in CLAUDE.md already) | Documented elsewhere |

### The Test

Before saving to memory, ask: **"Will future-me need this to understand the project, or is this only useful right now?"**

- If only useful now → tasks/todo.md or don't save
- If useful in future → memory file with clear description

## Rule 38: Update Session Log After Every Pull

When working with repos that receive external updates:

### The Pull Ritual

```
1. git pull                          # Get latest
2. git diff --stat HEAD~1           # See what changed (files + line counts)
3. git log --oneline -5             # See recent commit messages
4. Record in session context:
   - Date: 2026-03-24
   - Commits pulled: abc1234..def5678
   - Files changed: proposal_v2.html (+45), backlog.xlsx (+12)
   - Key changes: "v2 reduced duration from 9 to 4 months"

```

### Why This Matters

- Commit messages like "design modifications" are vague
- `git diff --stat` tells you EXACTLY what changed and how much
- Without this, you risk analyzing stale data or missing important changes

## Pull-Before-Analysis Checklist

Before reading ANY data/analysis file from a git repo:

- [ ] `git pull` run this session
- [ ] `git diff --stat` reviewed to understand changes
- [ ] Session log updated with pull details
- [ ] Version files checked for internal consistency (v2 file shouldn't contain v1 data)
- [ ] `git log OLD..NEW --oneline` run to see ALL intermediate commits (not just net diff)

## Rule: Git Log OLD..NEW After Fast-Forward Pull

After running `git pull`, always run `git log OLD_HEAD..HEAD --oneline` to see ALL intermediate commits. A fast-forward pull hides intermediate commits — `git diff` alone only shows the net result.

### Why This Matters

Fast-forward merges compress multiple commits into a single diff. If someone made 5 commits (add feature, fix bug, revert, re-add, fix typo), `git diff` shows only the final state. You miss the revert, the bug fix, and the reasoning in commit messages.

### The Ritual

```bash
# Before pull — save current HEAD
OLD_HEAD=$(git rev-parse HEAD)

# Pull
git pull

# See ALL intermediate commits (not just net diff)
git log $OLD_HEAD..HEAD --oneline

# THEN do the diff for content changes
git diff --stat $OLD_HEAD..HEAD

```

This was validated 14+ times in the Enhanced Standalone project. Without `git log OLD..NEW`, intermediate commits were repeatedly missed during fast-forward pulls.

## Rule: Never Use PowerShell Regex for HTML Patching

PowerShell's `-replace` operator and `[regex]::Replace()` silently mangle HTML attributes — reordering them, stripping quotes, or corrupting special characters.

### Safe Alternatives

| Task | WRONG | RIGHT |
|------|-------|-------|
| Replace text in HTML | `(Get-Content f.html) -replace $pattern, $replacement` | Use the Edit tool or `python -c "..."` |
| Batch HTML edits | PowerShell pipeline with regex | Python script with `re.sub()` or BeautifulSoup |
| Insert HTML block | String concatenation in PS1 | Edit tool with line-targeted insertion |

### Why PowerShell Fails on HTML

- Regex engine handles `"` and `'` differently in attribute values
- `-replace` is case-insensitive by default, causing unintended matches
- Pipeline encoding can corrupt UTF-8 characters in Arabic content
- No dry-run mode — damage is immediate and silent

This caused data corruption in multiple report build sessions.

## Rule 36-bis: Session-End Repo Discipline

The Stop hook (`session_end_lessons.py`) reminds you to capture lessons. It does NOT check that your repos are clean and pushed — that's this rule's job.

At the end of every session, before closing the window, walk through this checklist. Do not rely solely on the hook; it only prompts, it does not verify.

End-of-session checklist:

```
[ ] `git status` in every active repo — no uncommitted changes left behind
    unless intentional WIP (see below)
[ ] `git log @{upstream}..HEAD --oneline` in every active repo — no
    unpushed commits unless intentional
[ ] Session log updated with files changed and key outcomes
[ ] If any file moved this session: pm-link-integrity validation ran
[ ] If any externally-sent deliverable: pm-context-boundary scrub ran
[ ] Lessons captured — surprising failures AND confirmed-good choices both recorded

```

Intentional WIP state must be recorded in the session log with the reason. Example:

> Wallet feature X is mid-implementation; resuming Tuesday. Not pushing until test coverage is added. Dirty state in `d:/KhairGate (HUB)/`: 3 modified files.

Unrecorded WIP becomes next-session-Claude's confusion. Always annotate.

## Rule HTML-MD-01: MD is the Source of Truth

When both an `.md` and a sibling `.html` with the same stem exist in a PM deliverable folder, the Markdown file is canonical. The HTML is the generated artifact. The source-of-truth direction is MD -> HTML, never the reverse.

## Forbidden:

- Editing the HTML directly to add content that isn't in the MD.
- Updating a KPI row in the HTML and not the MD.
- Regenerating HTML from MD without first reconciling drift.

## Allowed:

- HTML-only concerns: CSS tweaks, JavaScript behaviour, embedded widgets, print-CSS, bilingual span pair wiring. These do not belong in the MD source.
- Deleting the MD if it is demonstrably stale AND the HTML is now the intended source (document the switch in a commit message and in CLAUDE.md so a future author doesn't re-generate from the stale MD).
- Editing the MD and re-running the export pipeline to regenerate the HTML.

**Red flag:** if `stat` shows the HTML is newer than its MD sibling, someone edited the HTML directly. Options are:

1. Update the MD to match the HTML changes (confirm with user first — the changes may be intentional).
2. Revert the HTML changes.
3. Retire the MD (if the workflow has genuinely moved to HTML-as-source).

The `pm-md-html-parity-checker` agent (coming in Phase 2) diagnoses which option fits. Until that agent ships, diagnose manually with a visual diff.

### Why This Rule Exists

HTML pages lose content on every regeneration from MD. If a KPI row, an assumption, a risk, or a table column was added directly to HTML, the next regenerate silently drops it. The user discovers the loss only when they re-open the file — often days later, often in front of a stakeholder.
