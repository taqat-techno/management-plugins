#!/usr/bin/env python3
"""Lesson Drift Detector — Tier 3 Lifecycle Hook (Stop)

At session end, compares the root global_lessons.md with the plugin's
embedded copy. If they differ, warns the user to run 'sync lessons'.

Exit codes: 0=pass (with optional description)
"""

import json
import os
import sys


def count_lines(file_path):
    """Count lines in a file. Returns 0 if file doesn't exist."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    except (OSError, UnicodeDecodeError):
        return 0


def get_lesson_count(file_path):
    """Count numbered lessons (lines starting with digit followed by period)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        import re
        return len(re.findall(r'^\d+\.\s+\*\*', content, re.MULTILINE))
    except (OSError, UnicodeDecodeError):
        return 0


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        input_data = {}

    # Determine paths
    plugin_root = os.environ.get('CLAUDE_PLUGIN_ROOT', os.path.dirname(os.path.dirname(__file__)))

    # Root global_lessons.md (source of truth)
    # Navigate from plugin root up to project root
    project_root = os.path.dirname(os.path.dirname(plugin_root))
    root_file = os.path.join(project_root, 'global_lessons.md')

    # Plugin's embedded copy
    plugin_file = os.path.join(plugin_root, 'global_lessons.md')

    # Check if both files exist
    if not os.path.exists(root_file):
        sys.exit(0)
    if not os.path.exists(plugin_file):
        result = {
            "description": "[pm-guidelines] Plugin's global_lessons.md copy is missing. Run 'sync lessons' to create it from the root source."
        }
        print(json.dumps(result))
        sys.exit(0)

    # Quick comparison: line count
    root_lines = count_lines(root_file)
    plugin_lines = count_lines(plugin_file)

    if root_lines == plugin_lines:
        # Same line count — likely in sync (skip deeper check for speed)
        sys.exit(0)

    # Drift detected — count lessons for more useful message
    root_lessons = get_lesson_count(root_file)
    plugin_lessons = get_lesson_count(plugin_file)

    diff_lines = root_lines - plugin_lines
    diff_lessons = root_lessons - plugin_lessons

    parts = []
    if diff_lines != 0:
        parts.append(f"{abs(diff_lines)} lines {'added' if diff_lines > 0 else 'removed'}")
    if diff_lessons != 0:
        parts.append(f"{abs(diff_lessons)} lessons {'added' if diff_lessons > 0 else 'removed'}")

    drift_detail = ', '.join(parts) if parts else 'content changed'

    result = {
        "description": f"[pm-guidelines] global_lessons.md has drifted from plugin copy ({drift_detail}).\n\nRun 'sync lessons' to update the plugin with new lessons and route them to the correct skills/hooks."
    }
    print(json.dumps(result))
    sys.exit(0)


if __name__ == '__main__':
    main()
