#!/usr/bin/env python3
"""PowerShell Safety Check — Tier 2 Quality Hook (PreToolUse)

Detects unsafe patterns in PowerShell commands:
- Em-dashes and curly quotes that cause silent parse failures (Guideline 72)
- .ps1 file creation without companion .bat launcher (Guideline 73)

Exit codes: 0=pass (with optional description)
"""

import json
import re
import sys


# Unicode characters that crash PowerShell silently
DANGEROUS_CHARS = {
    '\u2014': 'em-dash (--)',
    '\u2013': 'en-dash (-)',
    '\u2018': 'left single curly quote',
    '\u2019': 'right single curly quote (apostrophe)',
    '\u201c': 'left double curly quote',
    '\u201d': 'right double curly quote',
}


def check_dangerous_chars(command):
    """Find Unicode characters that crash PowerShell."""
    issues = []
    for char, name in DANGEROUS_CHARS.items():
        if char in command:
            issues.append(f'Contains {name} (U+{ord(char):04X}) — PowerShell will crash silently. Use ASCII alternative.')
    return issues


def check_ps1_without_bat(command):
    """Check if creating a .ps1 file without mentioning a .bat launcher."""
    issues = []
    # Detect if the command creates or writes a .ps1 file
    if re.search(r'\.ps1\b', command, re.IGNORECASE):
        # Check if it also references a .bat file
        if not re.search(r'\.bat\b', command, re.IGNORECASE):
            # Only warn if it looks like file creation, not just running
            if any(kw in command.lower() for kw in ['write', 'create', 'new-item', 'set-content', 'out-file', '>', 'tee']):
                issues.append('Creating .ps1 without companion .bat launcher — users need a .bat file with -NoExit to see errors (Rule 73)')
    return issues


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError) as e:
        print(f"pm-guidelines:powershell_safety_check: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(0)

    tool_name = input_data.get('tool_name', '')
    tool_input = input_data.get('tool_input', {})

    # Only check Bash commands
    if tool_name != 'Bash':
        sys.exit(0)

    command = tool_input.get('command', '')
    if not command:
        sys.exit(0)

    # Only check if command involves PowerShell
    is_powershell = any(kw in command.lower() for kw in ['powershell', '.ps1', 'pwsh', 'set-content', 'new-item', 'out-file'])
    if not is_powershell:
        sys.exit(0)

    issues = []
    issues.extend(check_dangerous_chars(command))
    issues.extend(check_ps1_without_bat(command))

    if not issues:
        sys.exit(0)

    issue_text = '\n'.join(f'  - {i}' for i in issues[:5])
    result = {
        "description": f"[pm-guidelines] PowerShell safety issues:\n{issue_text}\n\nTip: Use ASCII-only strings in PowerShell and always provide .bat launchers."
    }
    print(json.dumps(result))
    sys.exit(0)


if __name__ == '__main__':
    main()
