---
name: pm-link-integrity
description: |
  Link-integrity workflow for file moves, renames, and folder reorganizations in PM deliverables. Catalogues inbound hyperlinks, confirms with user, rewrites, and validates post-move so sidebar nav, breadcrumbs, and relative hrefs never break silently. Use whenever you move or rename PM files or restructure deliverable folders. For version-bump side-effects see pm-standalone-updater. For session-end validation reminder see pm-session-discipline.


  <example>
  Context: User wants to archive old dashboard versions
  user: "Move old versions of the dashboard into /archive/"
  assistant: "I will use the pm-link-integrity skill. First I will catalogue every inbound link to those files, confirm the scope with you, then perform the move, rewrite links, and validate."
  <commentary>Core trigger — file move with potential inbound references.</commentary>
  </example>

  <example>
  Context: User wants to rename a folder
  user: "Rename the /researches/ folder to /research/"
  assistant: "I will use the pm-link-integrity skill — folder renames are the highest-risk form of reorganization; treating it as N file moves."
  <commentary>Folder-rename trigger — multiplier effect across every file under the folder.</commentary>
  </example>

  <example>
  Context: User runs a git mv via shell
  user: "git mv old_report.html new_report.html"
  assistant: "I will use the pm-link-integrity skill to catalogue inbound links before the rename lands and rewrite them."
  <commentary>Bash-pattern trigger — mv / git mv / Move-Item surfaces the same risk.</commentary>
  </example>

  <example>
  Context: User wants to consolidate scattered files
  user: "Consolidate all the weekly reports under /deliverables/weekly/"
  assistant: "I will use the pm-link-integrity skill to walk each file through the 9-step procedure so every inbound link is rewritten before any file moves."
  <commentary>Consolidation trigger — many moves at once, high breakage surface.</commentary>
  </example>
license: "MIT"
metadata:
  version: "1.0.0"
  priority: 75
  model: sonnet
  filePattern: []
  bashPattern:
    - "mv\\s"
    - "Move-Item"
    - "git mv"
    - "Rename-Item"
    - "ren\\s"
  promptSignals:
    phrases:
      - "move file"
      - "move these files"
      - "rename folder"
      - "rename this to"
      - "reorganize"
      - "restructure"
      - "consolidate folders"
      - "archive old"
      - "clean up old versions"
      - "relocate"
      - "move to archive"
      - "archive these"
    minScore: 5
---

# PM Link Integrity Standards

Moving or renaming a file in a PM deliverable folder is almost never an isolated change. Dashboards, index pages, sidebar nav, breadcrumbs, README links, and search indexes can all reference the file. The mistake is to move first and grep later — by the time you discover the orphans, the report has already been sent.

This skill enforces a catalogue-first workflow: grep for every inbound reference, confirm the scope with the user, perform the move atomically, rewrite every reference, and validate post-move. No silent breakage.

Related skills: `pm-standalone-updater` (version-bump folders), `pm-consolidation` (multi-source merges), `pm-session-discipline` (end-of-session checklist includes link-integrity validation).

## The Six Rules

### Rule LI-01: Catalogue Inbound Links Before Moving

Before any file move, grep for ALL inbound references. Not just `href="..."` — also every other form a link can take:

| Link form | Pattern |
|---|---|
| HTML anchor | `href="..."` or `href='...'` |
| HTML resource | `src="..."`, `data-link="..."`, `data-href="..."` |
| Inline JS | `onclick="location=...", window.location = "..."` |
| Markdown | `](./path)`, `](../path)`, `](/path)` |
| Sidebar nav JSON | any `"url": "...", "path": "..."` fields in `nav.json`, `_data/*.yml` |
| Sitemap | `<loc>...</loc>` in `sitemap.xml` |
| Search index | generated index files under `search/`, `_search/`, `index.json` |

Command template:

```bash
grep -rEn '(href|src|data-link|data-href)=["'\''][^"'\'']*<target-filename>' .
grep -rEn '\]\((\./|\.\./|/)[^)]*<target-filename>' .

```

For a folder rename, repeat for every file under the folder.

### Rule LI-02: Confirm with User Before Moving

Present the inbound-link catalogue to the user before proceeding. The user may not have realized how many places reference the file. Format:

```
Inbound links to <target>:
  docs/index.html:47     — <a href="../reports/old.html">
  nav/sidebar.json:12    — "path": "/reports/old.html"
  README.md:23           — [Old report](./reports/old.html)

Total: 3 references across 3 files. Proceed with move + rewrite? (yes / no / show more)

```

If the catalogue is empty, confirm with the user before moving ("No inbound links found — proceed anyway?"). An empty catalogue is rare and usually means the grep missed a pattern.

### Rule LI-03: Atomic Move, Then Rewrite, Then Validate

Perform the move in this order:

1. `git mv OLD NEW` (preserves history) — or `mv OLD NEW` if not under git.
2. For each catalogued inbound link: rewrite to the new path. Preserve relative-vs-absolute: a relative href stays relative; an absolute path stays absolute.
3. Post-move grep for OLD path — must return zero results.
4. Post-move grep for NEW path — must return expected count (= pre-move inbound count + 0 for the moved file itself).

Never skip step 3 or 4. Silent orphans are the class of failure this skill exists to prevent.

### Rule LI-04: Validate Nav Menus and Breadcrumbs

For each `<a href>` inside `<nav>`, `.sidebar`, `.breadcrumb`, `.nav-link`, `[role="navigation"]` regions, verify every target file exists:

```bash
# after the move, for each href found in nav regions
for href in $(grep -oE 'href="[^"]+"' nav-regions.html); do
    path=$(echo "$href" | sed -E 's/href="(.*)"/\1/')
    [ -f "$path" ] || echo "MISSING: $path"
done

```

Nav menus are the public face of the document. A broken nav link is visible to every reader.

### Rule LI-05: Abort on Validation Failure

If any post-move check fails (orphan OLD reference, missing NEW target, unresolved nav link), abort and report. Never silently leave the filesystem in a half-rewritten state. Offer to revert the move:

```
Validation failed:
  - 1 orphan reference to old path in docs/sitemap.xml:14
  - 1 nav link target not found: sidebar.json:12 -> /reports/old.html

Options: (1) fix the remaining references, (2) revert the move (git mv NEW OLD).

```

### Rule LI-06: Folder Rename = N File Moves

A folder rename is not one operation — it's one move per file in the folder. Catalogue, confirm, rewrite, and validate for EVERY file inside before the folder operation is considered complete.

For deep folder renames (e.g., `researches/` → `research/` with sub-folders), walk the directory tree first and produce a per-file table:

```
Files to move under researches/ -> research/:
  researches/2025-q1.html     (3 inbound)
  researches/2025-q2.html     (2 inbound)
  researches/analysis/a.html  (5 inbound)
  researches/analysis/b.html  (1 inbound)

Total: 11 inbound references across 4 files. Proceed?

```

## Nine-Step Procedure

When this skill activates, walk the full procedure:

1. **Identify target(s).** What files or folders are moving, and to where? If unclear, ask.
2. **Grep for inbound links.** Use Rule LI-01 patterns. For a folder rename, grep per-file.
3. **Present catalogue.** Per Rule LI-02. Get explicit user confirmation before any filesystem change.
4. **Perform the move.** `git mv` preferred; `mv` / `Move-Item` as fallback. Never delete + re-create.
5. **Rewrite links.** For each inbound reference, rewrite to the new path. Preserve relative vs absolute.
6. **Post-move grep: OLD path.** Must return zero. If non-zero, abort per Rule LI-05.
7. **Post-move grep: NEW path.** Must return expected count. Missing references mean a rewrite failed.
8. **Validate nav.** Per Rule LI-04. Every `<a href>` in nav / sidebar / breadcrumb regions must resolve.
9. **Report.** Print the summary: files moved, links rewritten, broken links remaining (must be 0). If not 0, Rule LI-05 applies.

## When Not To Activate

- Code-level renames of variables, functions, or classes. Those are refactors, not PM-deliverable moves.
- Deleting a file without replacement. (Deletion is a different workflow — the inbound references need resolving but there's no NEW path to rewrite to.)
- Copying a file. (Copies don't invalidate the original path; no inbound rewrite needed.)
- Git operations that don't move files (`git branch`, `git checkout`, `git reset`).

## Edge Cases

- **Template-variable hrefs** (`{{ .BaseURL }}/foo.html`, `${basePath}/foo.html`): log a warning, skip rewrite. The templating engine determines the resolved path; rewriting the template would break it. Flag for the user to update the templating context manually.
- **Symbolic links**: follow the link to find the real target. Rewrite the symlink's target file, not the symlink path itself.
- **Case-insensitive filesystems** (Windows, default macOS): test path equality case-insensitively but preserve the original case in rewrites. Git history cares about case.
- **External absolute URLs** that happen to contain the target filename (e.g., `https://example.com/foo.html` when moving a local `foo.html`): never rewrite these. They are unrelated.
- **Bilingual file pairs** (`report_en.html` and `report_ar.html`): if one moves, check whether the other also moves with it. Usually yes.
- **Backup files** (`foo.html.bak`, `foo.html~`): skip — backups are not linked from docs.

## Mistakes This Skill Prevents

| Lesson | Mistake | How this skill prevents it |
|---|---|---|
| 90 | Moved `reports/2024-Q3.html` to archive; dashboard nav still pointed to old path | LI-01 + LI-04: nav validation catches the orphan |
| 91 | Renamed proposal file; 4 index pages had stale anchors | LI-01 + LI-03: inbound catalogue surfaces the 4 index references |
| 191 | Folder rename broke 12 relative hrefs | LI-06: folder rename treated as 12 file moves |
| 211 | Moved assets but didn't fix relative paths | LI-05: post-move grep catches the orphans before shipping |
| 312 | Breadcrumb pointed to old parent folder | LI-04: nav-region validation |
| 476–481 | Bulk reorganization; sidebar broken across 6 pages | Skill is built for exactly this scenario |
