#!/usr/bin/env python3
"""Modal Accessibility Check — Tier 2 Quality Hook (PostToolUse)

Detects modals in dashboard HTML that lack max-height and overflow CSS,
which can make modal content inaccessible on small screens (Guideline 123).

Exit codes: 0=pass (with optional description)
"""

import json
import os
import re
import sys

PLUGIN_ROOT = os.environ.get('CLAUDE_PLUGIN_ROOT', os.path.dirname(__file__))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, os.path.join(PLUGIN_ROOT, 'hooks'))

try:
    from pm_utils import is_dashboard_file, read_file_safe
except ImportError as e:
    print(f"pm-guidelines:modal_accessibility_check.py: import failed: {e}", file=sys.stderr)
    sys.exit(0)


def check_modal_accessibility(content):
    """Check if modals have max-height and overflow set."""
    has_modal = bool(re.search(
        r'\.modal\b|modal-dialog|modal-content|showModal|\.modal\s*\{',
        content, re.IGNORECASE
    ))
    if not has_modal:
        return None

    has_max_height = bool(re.search(r'max-height\s*:', content))
    has_overflow = bool(re.search(r'overflow(-y)?\s*:\s*(auto|scroll)', content))

    issues = []
    if not has_max_height:
        issues.append('max-height not set on modal')
    if not has_overflow:
        issues.append('overflow: auto/scroll not set on modal')

    if issues:
        return '  ' + '; '.join(issues) + ' — Close/Back buttons may be unreachable on small screens'
    return None


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError) as e:
        print(f"pm-guidelines:modal_accessibility_check: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(0)

    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    if not is_dashboard_file(file_path):
        sys.exit(0)

    content = read_file_safe(file_path)
    if not content:
        sys.exit(0)

    issue = check_modal_accessibility(content)
    if not issue:
        sys.exit(0)

    result = {
        "description": (
            f"[pm-guidelines] Modal accessibility issue:\n{issue}\n\n"
            "Tip: Add max-height: 85vh and overflow-y: auto to .modal-content."
        )
    }
    print(json.dumps(result))
    sys.exit(0)


if __name__ == '__main__':
    main()
