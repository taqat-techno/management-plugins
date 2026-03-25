#!/usr/bin/env python3
"""Version Drift Detector — Tier 2 Quality Hook (PostToolUse)

Checks if files in standalone/kickoff directories have stale
Document Control tables (Guidelines 57-58):
- Version field must match folder version
- Updated date must be specific (DD Mon YYYY), not generic

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
    from pm_utils import read_file_safe
except ImportError as e:
    print(f"pm-guidelines:version_drift_detector: import failed: {e}", file=sys.stderr)
    sys.exit(0)


# Patterns indicating standalone/kickoff directories
STANDALONE_PATTERNS = [
    r'standalone',
    r'kickoff',
    r'auto.?update',
    r'version',
]

# Generic date patterns that are too vague (Rule 58)
VAGUE_DATE_PATTERNS = [
    r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}',  # "March 2026"
    r'\d{4}-\d{2}',  # "2026-03" (month only)
]

# Specific date pattern (acceptable)
SPECIFIC_DATE_PATTERN = r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}'


def is_standalone_path(file_path):
    """Check if file is in a standalone/kickoff directory."""
    path_lower = file_path.lower().replace('\\', '/')
    return any(re.search(p, path_lower) for p in STANDALONE_PATTERNS)


def extract_folder_version(file_path):
    """Extract version number from folder path (e.g., v12 from /standalone/v12/file.html)."""
    match = re.search(r'[/\\]v(\d+)[/\\]', file_path, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def check_document_control(content, folder_version):
    """Check Document Control table for staleness."""
    issues = []

    # Check for Document Control section
    doc_ctrl_match = re.search(r'(?:Document\s+Control|Doc\s+Control)', content, re.IGNORECASE)
    if not doc_ctrl_match:
        return issues  # No Document Control table — not applicable

    # Extract the Document Control section (next ~20 lines)
    start = doc_ctrl_match.start()
    section = content[start:start + 2000]

    # Check version field matches folder
    if folder_version:
        version_match = re.search(r'(?:Version|Ver\.?)\s*[:\|]\s*v?(\d+)', section, re.IGNORECASE)
        if version_match:
            doc_version = version_match.group(1)
            if doc_version != folder_version:
                issues.append(f'Document Control version "v{doc_version}" does not match folder version "v{folder_version}" (Rule 57)')

    # Check for vague dates (Rule 58)
    for vague_pattern in VAGUE_DATE_PATTERNS:
        vague_match = re.search(vague_pattern, section)
        if vague_match:
            # Check if there's also a specific date nearby
            specific_match = re.search(SPECIFIC_DATE_PATTERN, section)
            if not specific_match:
                issues.append(f'Document Control has vague date "{vague_match.group()}" — use specific format "DD Mon YYYY" (Rule 58)')
                break

    return issues


def check_footer_date(content):
    """Check footer for specific date format."""
    issues = []
    # Look for Modified/Updated in footer area (last 500 chars)
    footer = content[-500:]
    modified_match = re.search(r'(?:Modified|Updated)\s*:\s*(.{5,30})', footer, re.IGNORECASE)
    if modified_match:
        date_text = modified_match.group(1).strip()
        # Check if it's a vague date
        for vague_pattern in VAGUE_DATE_PATTERNS:
            if re.search(vague_pattern, date_text):
                issues.append(f'Footer date "{date_text}" is too vague — use "DD Mon YYYY" format (Rule 58)')
                break
    return issues


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError) as e:
        print(f"pm-guidelines:version_drift_detector: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(0)

    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    if not file_path or not is_standalone_path(file_path):
        sys.exit(0)

    content = read_file_safe(file_path)
    if not content:
        sys.exit(0)

    folder_version = extract_folder_version(file_path)

    issues = []
    issues.extend(check_document_control(content, folder_version))
    issues.extend(check_footer_date(content))

    if not issues:
        sys.exit(0)

    issue_text = '\n'.join(f'  - {i}' for i in issues[:5])
    result = {
        "description": f"[pm-guidelines] Version drift detected:\n{issue_text}\n\nEnsure Document Control tables and footers match the current folder version and use specific dates."
    }
    print(json.dumps(result))
    sys.exit(0)


if __name__ == '__main__':
    main()
