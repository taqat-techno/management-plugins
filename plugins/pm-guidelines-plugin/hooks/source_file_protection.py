#!/usr/bin/env python3
"""Source File Protection — Tier 1 Security Hook (PreToolUse)

Blocks edits to files designated as either:
  (a) protected source analyses (.pm-protected-paths) — generic block message
  (b) FROZEN deliverables (.pm-frozen-paths) — references lesson #750, points at successor system

Reads patterns from config file(s) in the project root or user home.
If neither config exists, this hook is a no-op.

Exit codes: 0=pass, 2=block
"""

import json
import os
import re
import sys
from pathlib import Path


def find_config_file(filename='.pm-protected-paths'):
    """Find named config file in CWD or parents."""
    cwd = Path(os.getcwd())
    for directory in [cwd] + list(cwd.parents):
        config = directory / filename
        if config.exists():
            return config
        # Stop at home directory
        if directory == Path.home():
            break
    return None


def load_protected_patterns(config_path):
    """Load glob patterns from config file (one per line, # for comments)."""
    patterns = []
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
    except (IOError, OSError):
        pass
    return patterns


def glob_to_regex(glob_pattern):
    """Convert a simple glob pattern to regex."""
    # Escape special regex chars except * and ?
    regex = ''
    i = 0
    while i < len(glob_pattern):
        c = glob_pattern[i]
        if c == '*':
            if i + 1 < len(glob_pattern) and glob_pattern[i + 1] == '*':
                # ** matches anything including /
                regex += '.*'
                i += 2
                # Skip trailing /
                if i < len(glob_pattern) and glob_pattern[i] == '/':
                    i += 1
                continue
            else:
                # * matches anything except /
                regex += '[^/]*'
        elif c == '?':
            regex += '[^/]'
        elif c in '.+^${}()|[]\\':

            regex += '\\' + c
        else:
            regex += c
        i += 1
    return regex


def is_protected(file_path, patterns):
    """Check if file_path matches any protected pattern."""
    # Normalize path separators
    normalized = file_path.replace('\\', '/')

    for pattern in patterns:
        pattern_normalized = pattern.replace('\\', '/')
        regex = glob_to_regex(pattern_normalized)
        if re.search(regex, normalized, re.IGNORECASE):
            return pattern
    return None


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError) as e:
        print(f"pm-guidelines:source_file_protection: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(0)

    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    if not file_path:
        sys.exit(0)

    # Pass 1: FROZEN-paths check (lesson #750 — never edit FROZEN HTML; new work goes to successor system)
    frozen_config = find_config_file('.pm-frozen-paths')
    if frozen_config:
        frozen_patterns = load_protected_patterns(frozen_config)
        if frozen_patterns:
            matched_frozen = is_protected(file_path, frozen_patterns)
            if matched_frozen:
                result = {
                    "decision": "block",
                    "reason": (
                        f"[pm-guidelines] FROZEN artifact — edits forbidden.\n\n"
                        f"This file is declared FROZEN (matched pattern: {matched_frozen}).\n"
                        f"All NEW feature work belongs in the successor system, not this file.\n"
                        f"  - PMO Dashboard v10/v11/v12/v13/v14 → PMO_OS Electron app at D:\\PMO_OS\\\n"
                        f"  - Sunday Talking Points v3/v4/... → next-version deck (vN+1)\n\n"
                        f"See lesson #750 for the full discipline (frozen-artifact, version-bump, UI migration affordance-diff).\n\n"
                        f"To override (testing is read-only-allowed; edits are NOT), remove the path from {frozen_config}.\n"
                        f"To add a new frozen path, edit {frozen_config} (one absolute path per line, # for comments)."
                    )
                }
                print(json.dumps(result))
                sys.exit(2)

    # Pass 2: PROTECTED-paths check (existing behavior — generic source-analysis block)
    config = find_config_file('.pm-protected-paths')
    if not config:
        # No config = no enforcement
        sys.exit(0)

    # Load patterns
    patterns = load_protected_patterns(config)
    if not patterns:
        sys.exit(0)

    # Check if file is protected
    matched_pattern = is_protected(file_path, patterns)
    if not matched_pattern:
        sys.exit(0)

    # Block the edit
    result = {
        "decision": "block",
        "reason": f"[pm-guidelines] Blocked: this file is a protected source analysis (matched pattern: {matched_pattern}).\n\nSource analyses must remain untouched. Build consolidated output independently instead.\n\nTo modify protected paths, edit: {config}"
    }
    print(json.dumps(result))
    sys.exit(2)


if __name__ == '__main__':
    main()
