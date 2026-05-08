#!/usr/bin/env python3
"""Electron Renderer Pitfall Check — PreToolUse hook.

Lesson #746 (a/b/c) — three classes of silent failure in Electron development:
  (a) window.prompt/alert/confirm are no-op in renderers — return null without rendering UI
  (b) Renderer fetch() to localhost is silently blocked by Chromium loopback CORS
  (c) New ipcMain.handle() requires full dev:all restart — Vite HMR does NOT propagate

Scope: only fires when the target project has `electron` as a direct dependency
       (detected via nearest package.json walk). Prevents false positives in
       non-Electron React projects that happen to have src/components/*.tsx paths.

Trigger: PreToolUse on Write|Edit when file_path matches:
  - **/src/components/**/*.tsx (renderer code)
  - **/src/**/*.tsx (broader renderer scope)
  - **/electron/**/*.ts (main-process code)

Action:
  - BLOCK on window.prompt/alert/confirm in renderer file (#746a)
  - BLOCK on renderer-side fetch('http://localhost:...) or fetch('http://127.0.0.1:...) (#746b)
  - WARN (do not block) on newly-added ipcMain.handle( in main-process file (#746c)

Exit codes: 0=pass/warn-only, 2=block
"""

import json
import os
import re
import sys
from pathlib import Path


def find_nearest_package_json(file_path):
    """Walk up from file_path looking for package.json. Return path or None."""
    try:
        path = Path(file_path).resolve()
    except (OSError, ValueError):
        return None
    if path.is_file():
        path = path.parent
    for directory in [path] + list(path.parents):
        candidate = directory / 'package.json'
        if candidate.exists():
            return candidate
        if directory == Path.home() or str(directory) in ('/', 'C:\\', 'D:\\'):
            break
    return None


def project_uses_electron(package_json_path):
    """Return True if package.json declares electron as a direct or dev dependency."""
    try:
        with open(package_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (IOError, OSError, json.JSONDecodeError):
        return False
    deps = {}
    for key in ('dependencies', 'devDependencies', 'peerDependencies'):
        deps.update(data.get(key) or {})
    return 'electron' in deps


def is_renderer_file(file_path):
    """Heuristic: renderer files are .tsx/.jsx/.ts inside src/ but NOT inside electron/."""
    normalized = file_path.replace('\\', '/').lower()
    if '/electron/' in normalized:
        return False
    if normalized.endswith(('.tsx', '.jsx')):
        return True
    if '/src/' in normalized and normalized.endswith('.ts'):
        return True
    return False


def is_main_process_file(file_path):
    """Heuristic: main-process files live under electron/ and are .ts/.cts."""
    normalized = file_path.replace('\\', '/').lower()
    return '/electron/' in normalized and normalized.endswith(('.ts', '.cts', '.js', '.cjs'))


def extract_changed_content(tool_input, tool_name):
    """For Edit, return new_string. For Write, return content. For multi-edit, join all new_strings."""
    if tool_name == 'Write':
        return tool_input.get('content', '')
    if tool_name == 'Edit':
        return tool_input.get('new_string', '')
    if tool_name == 'MultiEdit':
        edits = tool_input.get('edits', []) or []
        return '\n'.join((e.get('new_string', '') or '') for e in edits)
    return ''


# Risky patterns — compiled once at import
PATTERN_BROWSER_DIALOG = re.compile(r'\bwindow\.(prompt|alert|confirm)\s*\(')
PATTERN_RENDERER_LOCALHOST_FETCH = re.compile(
    r"""\bfetch\s*\(\s*['"`]https?://(localhost|127\.0\.0\.1)[:/]""",
    re.IGNORECASE,
)
PATTERN_IPCMAIN_HANDLE = re.compile(r'\bipcMain\.handle\s*\(')


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError) as e:
        print(f"pm-guidelines:electron_renderer_check: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(0)

    tool_name = input_data.get('tool_name', '')
    tool_input = input_data.get('tool_input', {}) or {}
    file_path = tool_input.get('file_path', '')

    if not file_path or tool_name not in ('Write', 'Edit', 'MultiEdit'):
        sys.exit(0)

    # Scope guard: only Electron projects (mitigation per plan risk #1)
    pkg_json = find_nearest_package_json(file_path)
    if not pkg_json or not project_uses_electron(pkg_json):
        sys.exit(0)

    content = extract_changed_content(tool_input, tool_name)
    if not content:
        sys.exit(0)

    is_renderer = is_renderer_file(file_path)
    is_main = is_main_process_file(file_path)

    if not (is_renderer or is_main):
        sys.exit(0)

    # === Renderer-only checks (BLOCK) ===
    if is_renderer:
        m = PATTERN_BROWSER_DIALOG.search(content)
        if m:
            result = {
                "decision": "block",
                "reason": (
                    f"[pm-guidelines #746a] window.{m.group(1)} is silently NO-OP in Electron renderers — "
                    f"returns null without rendering any dialog. Code depending on it hangs the UI in "
                    f"whatever state was set just before.\n\n"
                    f"Fix: render React state-driven <input>/modal in the component DOM tree. "
                    f"For inline fallbacks, use per-row state to switch between 'button' and "
                    f"'input + submit + cancel' (autoFocus + onKeyDown Enter, keyboard-accessible). "
                    f"For yes/no confirms, use a modal component or dialog.showMessageBox via main-process IPC."
                )
            }
            print(json.dumps(result))
            sys.exit(2)

        m = PATTERN_RENDERER_LOCALHOST_FETCH.search(content)
        if m:
            result = {
                "decision": "block",
                "reason": (
                    f"[pm-guidelines #746b] Renderer-side fetch() to localhost is silently blocked by "
                    f"Chromium's loopback CORS even with Access-Control-Allow-Origin: *. "
                    f"Chromium evaluates the origin pair before consulting CORS headers; the fetch "
                    f"rejects with 'Failed to fetch' and no console error.\n\n"
                    f"Fix: route ALL renderer-side localhost fetches through "
                    f"window.api.net.fetch (main-process proxy via ipcRenderer.invoke('devops:fetch', ...)). "
                    f"Node's fetch in main doesn't enforce browser origin policy. "
                    f"Copy from existing helpers (sidecar-fetch.ts, devops-fetch.ts) — don't write fetch() from scratch."
                )
            }
            print(json.dumps(result))
            sys.exit(2)

    # === Main-process check (WARN — don't block) ===
    if is_main and PATTERN_IPCMAIN_HANDLE.search(content):
        # WARN via stderr — does NOT block. Exit 0 so the edit proceeds.
        print(
            "[pm-guidelines #746c] WARN: ipcMain.handle channel detected in main-process code.\n"
            "  Vite HMR does NOT propagate to the main process — `npm run dev:all` needs a FULL RESTART\n"
            "  to register a new IPC handler. Pair with renderer-side typeof guard + graceful fallback\n"
            "  for the case where the handler isn't registered yet (typeof check + try/catch on invoke +\n"
            "  error-message regex 'No handler registered'). The fallback should be a real working\n"
            "  alternative (inline input, manual path entry), not just an error message.",
            file=sys.stderr,
        )
        # exit 0 — warn only

    sys.exit(0)


if __name__ == '__main__':
    main()
