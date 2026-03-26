#!/usr/bin/env python3
"""Title Consistency Check — Tier 2 Quality Hook (PostToolUse)

Detects inconsistent role title usage in PM deliverables:
- "Project Manager" vs "IT Project Manager" vs "PM" in the same file (Guideline 133)

Exit codes: 0=pass (with optional description)
"""

import json
import os
import re
import sys

# Add plugin root for shared utils
PLUGIN_ROOT = os.environ.get('CLAUDE_PLUGIN_ROOT', os.path.dirname(__file__))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, os.path.join(PLUGIN_ROOT, 'hooks'))

try:
    from pm_utils import is_pm_deliverable, read_file_safe
except ImportError as e:
    print(f"pm-guidelines:title_consistency_check.py: import failed: {e}", file=sys.stderr)
    sys.exit(0)


# Title patterns to detect — order matters (check longest first)
TITLE_PATTERNS = [
    (re.compile(r'\bIT\s+Project\s+Manager\b', re.IGNORECASE), 'IT Project Manager'),
    (re.compile(r'\bProject\s+Manager\b', re.IGNORECASE), 'Project Manager'),
    (re.compile(r'(?<!\w)PM(?!\w)(?!\s*[\d:])'), 'PM'),  # standalone PM, not PM2, PM:, etc.
]


def find_title_variants(content):
    """Find all role title variants and their line numbers."""
    variants = {}  # variant_name -> [line_numbers]
    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        # Skip comment lines, script blocks, and CSS
        stripped = line.strip()
        if stripped.startswith(('<!--', '//', '/*', '*', '.', '#')) or '<style' in line:
            continue

        for pattern, name in TITLE_PATTERNS:
            if pattern.search(line):
                # For "Project Manager", skip if "IT Project Manager" is on the same line
                if name == 'Project Manager' and re.search(r'\bIT\s+Project\s+Manager\b', line, re.IGNORECASE):
                    continue
                if name not in variants:
                    variants[name] = []
                variants[name].append(i)

    return variants


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError) as e:
        print(f"pm-guidelines:title_consistency_check: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(0)

    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    if not is_pm_deliverable(file_path):
        sys.exit(0)

    content = read_file_safe(file_path)
    if not content:
        sys.exit(0)

    variants = find_title_variants(content)

    # Only warn if more than one variant is found
    if len(variants) <= 1:
        sys.exit(0)

    issues = []
    for name, lines in variants.items():
        line_refs = ', '.join(str(ln) for ln in lines[:3])
        suffix = f' (+{len(lines) - 3} more)' if len(lines) > 3 else ''
        issues.append(f'  "{name}" on lines {line_refs}{suffix}')

    issue_text = '\n'.join(issues[:5])
    result = {
        "description": (
            f"[pm-guidelines] Title inconsistency found — {len(variants)} variants of the role title:\n"
            f"{issue_text}\n\n"
            "Tip: Use the same title everywhere (e.g., \"IT Project Manager\"). "
            "Mismatches erode credibility in board-facing reports."
        )
    }
    print(json.dumps(result))
    sys.exit(0)


if __name__ == '__main__':
    main()
