#!/usr/bin/env python3
"""Print CSS Check — Tier 2 Quality Hook (PostToolUse)

Verifies dashboard HTML files have print styles with break-inside: avoid.
Dashboards without print CSS produce broken printouts (Guideline 77).

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
    print(f"pm-guidelines:print_css_check.py: import failed: {e}", file=sys.stderr)
    sys.exit(0)


def check_print_css(content):
    """Check for @media print with break-inside: avoid."""
    has_print_media = bool(re.search(r'@media\s+print', content))

    if not has_print_media:
        return '  No @media print block found — dashboard will produce broken printouts'

    has_break_inside = bool(re.search(r'break-inside\s*:\s*avoid', content))
    if not has_break_inside:
        return '  @media print exists but missing break-inside: avoid — cards/tables may split across pages'

    return None


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError) as e:
        print(f"pm-guidelines:print_css_check: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(0)

    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    if not is_dashboard_file(file_path):
        sys.exit(0)

    content = read_file_safe(file_path)
    if not content:
        sys.exit(0)

    issue = check_print_css(content)
    if not issue:
        sys.exit(0)

    result = {
        "description": (
            f"[pm-guidelines] Print CSS issue:\n{issue}\n\n"
            "Tip: Add @media print { .card, table { break-inside: avoid; } h2, h3 { break-after: avoid; } }"
        )
    }
    print(json.dumps(result))
    sys.exit(0)


if __name__ == '__main__':
    main()
