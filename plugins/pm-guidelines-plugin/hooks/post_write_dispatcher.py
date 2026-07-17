#!/usr/bin/env python3
"""Post-Write Dispatcher — Unified Tier 2 Quality Hook (PostToolUse)

Consolidates 7 individual quality checks into a single process:
- Status label enforcement (Guidelines 5, 7)
- Bilingual EN/AR parity (Guidelines 8-10)
- Dashboard quality (Guidelines 30, 34)
- HTML render reminder (Guideline 15)
- Title consistency (Guideline 119)
- Modal accessibility (Guideline 123)
- Print CSS (Guideline 77)

One process, one file read, one JSON output. Replaces 7 sequential hooks.

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
    from pm_utils import is_pm_deliverable, is_html_file, is_dashboard_file, is_powershell_file, read_file_safe
except ImportError as e:
    print(f"pm-guidelines:post_write_dispatcher: import failed: {e}", file=sys.stderr)
    sys.exit(0)


# ---------------------------------------------------------------------------
# Check: Status Labels (from status_label_enforcer.py)
# ---------------------------------------------------------------------------

def check_status_labels(content):
    """Find vague 'Ongoing' and 'independently' without specifics."""
    issues = []
    for i, line in enumerate(content.split('\n'), 1):
        # "Ongoing" without colon, dash, or parentheses detail
        if re.search(r'\bOngoing\b', line, re.IGNORECASE):
            after_ongoing = re.split(r'\bOngoing\b', line, flags=re.IGNORECASE)[-1]
            has_detail = bool(re.search(r'[:(\-\u2013\u2014]', after_ongoing.strip()[:10]))
            if not has_detail:
                issues.append(f'  [Status] Line {i}: "Ongoing" without specifics \u2014 replace with next steps')

        # "independently" without explanation
        if re.search(r'\bindependently\b', line, re.IGNORECASE):
            after = re.split(r'\bindependently\b', line, flags=re.IGNORECASE)[-1]
            has_detail = bool(re.search(r'[(\[]', after.strip()[:10]))
            if not has_detail:
                issues.append(f'  [Status] Line {i}: "independently" without explanation \u2014 specify what continues')

    return issues[:8]


# ---------------------------------------------------------------------------
# Check: Bilingual Parity (from bilingual_parity_check.py)
# ---------------------------------------------------------------------------

def is_bilingual(content):
    """Check if file contains bilingual markers."""
    return bool(
        re.search(r'data-i18n', content) or
        re.search(r'class=["\'][^"\']*lang-(en|ar)', content) or
        re.search(r'lang=["\']ar["\']', content)
    )


def check_bilingual_parity(content):
    """Check EN/AR span pairing and i18n completeness."""
    if not is_bilingual(content):
        return []

    issues = []

    # Check i18n key completeness — empty translations
    i18n_keys = re.findall(r'data-i18n=["\']([^"\']+)["\']', content)
    unique_keys = set(i18n_keys)
    for key in unique_keys:
        pattern = rf'data-i18n=["\']({re.escape(key)})["\'][^>]*>([^<]*)<'
        matches = re.findall(pattern, content)
        for _, text in matches:
            if not text.strip():
                issues.append(f'  [Bilingual] Empty translation for key "{key}" \u2014 fill in both EN and AR')
                break

    # Check lang-en vs lang-ar span count
    en_count = len(re.findall(r'class=["\'][^"\']*lang-en', content))
    ar_count = len(re.findall(r'class=["\'][^"\']*lang-ar', content))
    if en_count != ar_count:
        issues.append(f'  [Bilingual] Span mismatch: {en_count} EN vs {ar_count} AR \u2014 every EN span needs an AR sibling')

    return issues[:5]


# ---------------------------------------------------------------------------
# Check: Dashboard Quality (from dashboard_quality_check.py)
# ---------------------------------------------------------------------------

def check_dashboard_quality(content):
    """Check for source tab and live clock issues."""
    issues = []

    # Source tab check
    source_patterns = [
        r'data.?source', r'source.?tab', r'data.?transparency',
        r'query.?details', r'api.?source', r'verification.?link',
    ]
    has_source = any(re.search(p, content, re.IGNORECASE) for p in source_patterns)
    if not has_source:
        issues.append('  [Dashboard] Missing "Data Source" tab \u2014 dashboards must include query details')

    # Live clock check
    live_clock_patterns = [
        r'new\s+Date\(\)', r'setInterval.*Date',
        r'toLocaleTimeString', r'clock.*setInterval',
    ]
    for pattern in live_clock_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            has_fetch_time = bool(re.search(
                r'(last.?fetched|last.?updated|data.?as.?of|fetched.?at|retrieved.?at)',
                content, re.IGNORECASE
            ))
            if not has_fetch_time:
                issues.append('  [Dashboard] Live clock without fetch timestamp \u2014 show when data was retrieved, not current time')
            break

    return issues


# ---------------------------------------------------------------------------
# Check: Title Consistency (from title_consistency_check.py)
# ---------------------------------------------------------------------------

TITLE_PATTERNS = [
    (re.compile(r'\bIT\s+Project\s+Manager\b', re.IGNORECASE), 'IT Project Manager'),
    (re.compile(r'\bProject\s+Manager\b', re.IGNORECASE), 'Project Manager'),
    (re.compile(r'(?<!\w)PM(?!\w)(?!\s*[\d:])'), 'PM'),
]


def check_title_consistency(content):
    """Find inconsistent role title variants in the same file."""
    variants = {}
    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith(('<!--', '//', '/*', '*', '.', '#')) or '<style' in line:
            continue

        for pattern, name in TITLE_PATTERNS:
            if pattern.search(line):
                if name == 'Project Manager' and re.search(r'\bIT\s+Project\s+Manager\b', line, re.IGNORECASE):
                    continue
                if name not in variants:
                    variants[name] = []
                variants[name].append(i)

    if len(variants) <= 1:
        return []

    issues = []
    for name, line_nums in variants.items():
        line_refs = ', '.join(str(ln) for ln in line_nums[:3])
        suffix = f' (+{len(line_nums) - 3} more)' if len(line_nums) > 3 else ''
        issues.append(f'  [Title] "{name}" on lines {line_refs}{suffix}')

    header = f'  [Title] {len(variants)} role title variants found \u2014 use one consistently:'
    return [header] + issues[:5]


# ---------------------------------------------------------------------------
# Check: Modal Accessibility (from modal_accessibility_check.py)
# ---------------------------------------------------------------------------

def check_modal_accessibility(content):
    """Check if modals have max-height and overflow set."""
    has_modal = bool(re.search(
        r'\.modal\b|modal-dialog|modal-content|showModal|\.modal\s*\{',
        content, re.IGNORECASE
    ))
    if not has_modal:
        return []

    missing = []
    if not re.search(r'max-height\s*:', content):
        missing.append('max-height')
    if not re.search(r'overflow(-y)?\s*:\s*(auto|scroll)', content):
        missing.append('overflow: auto/scroll')

    if missing:
        return [f'  [Modal] Missing {", ".join(missing)} on modal \u2014 Close button may be unreachable on small screens']
    return []


# ---------------------------------------------------------------------------
# Check: Print CSS (from print_css_check.py)
# ---------------------------------------------------------------------------

def check_print_css(content):
    """Check for @media print with break-inside: avoid."""
    has_print_media = bool(re.search(r'@media\s+print', content))

    if not has_print_media:
        return ['  [Print] No @media print block \u2014 dashboard will produce broken printouts']

    if not re.search(r'break-inside\s*:\s*avoid', content):
        return ['  [Print] @media print missing break-inside: avoid \u2014 cards/tables may split across pages']

    return []


# ---------------------------------------------------------------------------
# Check: HTML Render Reminder (from html_render_reminder.py)
# ---------------------------------------------------------------------------

def check_html_render_reminder(file_path, content):
    """Remind to open HTML in browser after changes."""
    msg = '[Render] HTML modified \u2014 open in browser to verify rendering.'
    if is_bilingual(content):
        msg += ' Bilingual: check BOTH EN and AR views.'
    return [f'  {msg}']


# ---------------------------------------------------------------------------
# Check: Nested-anchor in card (lesson #774a)
# ---------------------------------------------------------------------------

# Matches <a class="...card..."> ... <a ...> before the outer closes.
# HTML5 parser auto-closes the outer when it hits the inner → grid layout collapses.
_NESTED_ANCHOR_PATTERN = re.compile(
    r'<a[^>]*class\s*=\s*["\'][^"\']*\bcard\b[^"\']*["\'][^>]*>[^<]*(?:<(?!/a\b)[^>]*>[^<]*)*<a\s',
    re.IGNORECASE | re.DOTALL,
)


def check_nested_anchor_in_card(content):
    """Find nested <a> inside <a class="card">. Lesson #774(a)."""
    if not _NESTED_ANCHOR_PATTERN.search(content):
        return []

    # Find line numbers of the offending outer anchors
    issues = []
    for i, line in enumerate(content.split('\n'), 1):
        if re.search(r'<a[^>]*class\s*=\s*["\'][^"\']*\bcard\b', line, re.IGNORECASE):
            # Look ahead for nested <a> within next 30 lines (cards are usually compact)
            lookahead = '\n'.join(content.split('\n')[i - 1:i + 30])
            if _NESTED_ANCHOR_PATTERN.search(lookahead):
                issues.append(
                    f'  [Render #774a] Line {i}: nested <a> inside <a class="card"> '
                    'auto-closes outer at parser level — grid collapses to 1-col with empty placeholder. '
                    'Replace inner with <code> or move link OUTSIDE the card.'
                )
                if len(issues) >= 3:
                    break
    return issues


# ---------------------------------------------------------------------------
# Check: PowerShell 5.1 dialect (lesson #757a)
# ---------------------------------------------------------------------------

_PS7_PATTERNS = [
    (re.compile(r'(?<![\w$])\?\?(?!\=)'), '`??` null-coalescing (PS 7+)'),
    (re.compile(r'(?<![\w$])\?\s*[^:?\s][^:]*\s+:\s+'), '`?:` ternary (PS 7+)'),
    (re.compile(r'\bJoin-Path\s+(?:[^\s,;]+\s+){2,}[^\s,;]+'), 'multi-arg Join-Path (PS 5.1 takes only 2)'),
]


def check_ps51_dialect(content):
    """Find PS 7+ syntax in PS scripts. Lesson #757(a)."""
    issues = []
    for i, line in enumerate(content.split('\n'), 1):
        # Skip comments
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        for pattern, desc in _PS7_PATTERNS:
            if pattern.search(line):
                issues.append(
                    f'  [PS-Dialect #757a] Line {i}: {desc}. '
                    'Windows default is PS 5.1; substitute with if/else or [System.IO.Path]::Combine.'
                )
                if len(issues) >= 5:
                    return issues
                break  # one finding per line
    return issues


# ---------------------------------------------------------------------------
# Check: Bilingual numeric-mirror disparity (lesson #772a — companion to bilingual_parity)
# ---------------------------------------------------------------------------

def check_bilingual_numeric_mirror(content):
    """Warn if EN spans contain digits the AR spans don't mirror.

    Heuristic: count digits inside lang-en vs lang-ar spans. If they differ
    significantly (>20%), the AR mirror likely fell behind an EN content edit.
    Lesson #772(a) — AR-mirror drift is silent until language is toggled.
    """
    if not is_bilingual(content):
        return []

    en_blocks = re.findall(r'class=["\'][^"\']*lang-en[^"\']*["\'][^>]*>([^<]+)<', content)
    ar_blocks = re.findall(r'class=["\'][^"\']*lang-ar[^"\']*["\'][^>]*>([^<]+)<', content)

    if not en_blocks or not ar_blocks:
        return []

    en_digits = sum(len(re.findall(r'\d+', t)) for t in en_blocks)
    ar_digits = sum(len(re.findall(r'\d+', t)) for t in ar_blocks)

    # Both empty or both equal — no drift signal
    if en_digits == 0 and ar_digits == 0:
        return []

    if en_digits == 0 or ar_digits == 0:
        return [
            f'  [Bilingual #772a] Numeric mirror disparity: {en_digits} digit-tokens in EN vs '
            f'{ar_digits} in AR. Toggle EN↔AR in browser; verify counts/dates/numbers match.'
        ]

    # Allow up to 20% difference (Arabic numerals + Eastern-Arabic numerals)
    ratio = max(en_digits, ar_digits) / max(min(en_digits, ar_digits), 1)
    if ratio > 1.2:
        return [
            f'  [Bilingual #772a] Numeric mirror disparity: {en_digits} digit-tokens in EN vs '
            f'{ar_digits} in AR (ratio {ratio:.2f}). AR mirror may be stale after EN edit. '
            'Toggle EN↔AR in browser; sync the numbers.'
        ]
    return []


# ---------------------------------------------------------------------------
# Main Dispatcher
# ---------------------------------------------------------------------------

def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError) as e:
        print(f"pm-guidelines:post_write_dispatcher: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(0)

    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    if not file_path:
        sys.exit(0)

    try:
        # Classify file type once
        pm = is_pm_deliverable(file_path)
        html = is_html_file(file_path)
        dashboard = is_dashboard_file(file_path)
        powershell = is_powershell_file(file_path)

        # Gate: must be PM-relevant OR a PowerShell script
        if not (pm or html or dashboard or powershell):
            sys.exit(0)

        # Read file content once
        content = read_file_safe(file_path)
        if not content:
            sys.exit(0)

        issues = []
        errors = []

        # PM deliverable checks
        if pm:
            for check_fn in [check_status_labels, check_title_consistency]:
                try:
                    issues.extend(check_fn(content))
                except Exception as e:
                    errors.append(f"{check_fn.__name__}: {e}")

        # HTML + PM checks
        if html and pm:
            try:
                issues.extend(check_html_render_reminder(file_path, content))
            except Exception as e:
                errors.append(f"check_html_render_reminder: {e}")

        # Bilingual checks (any HTML with bilingual markers)
        if html:
            for check_fn in [check_bilingual_parity, check_bilingual_numeric_mirror, check_nested_anchor_in_card]:
                try:
                    issues.extend(check_fn(content))
                except Exception as e:
                    errors.append(f"{check_fn.__name__}: {e}")

        # Dashboard-specific checks
        if dashboard:
            for check_fn in [check_dashboard_quality, check_modal_accessibility, check_print_css]:
                try:
                    issues.extend(check_fn(content))
                except Exception as e:
                    errors.append(f"{check_fn.__name__}: {e}")

        # PowerShell-specific checks
        if powershell:
            try:
                issues.extend(check_ps51_dialect(content))
            except Exception as e:
                errors.append(f"check_ps51_dialect: {e}")

        # Log any check failures to stderr
        for err in errors:
            print(f"pm-guidelines:dispatcher: {err}", file=sys.stderr)

        if not issues and not errors:
            sys.exit(0)

        parts = []
        if issues:
            parts.append('\n'.join(issues))
        if errors:
            parts.append(f'  [{len(errors)} check(s) failed — see stderr for details]')

        total = len(issues)
        result = {
            "description": f"[pm-guidelines] Quality checks ({total} issue{'s' if total != 1 else ''}):\n" + '\n'.join(parts)
        }
        print(json.dumps(result))
        sys.exit(0)

    except Exception as e:
        print(f"pm-guidelines:dispatcher: FATAL: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
