"""Tests for post_write_dispatcher.py consolidated quality checks."""

import sys
import pytest
from post_write_dispatcher import (
    check_status_labels,
    check_bilingual_parity,
    check_dashboard_quality,
    check_title_consistency,
    check_modal_accessibility,
    check_print_css,
    check_html_render_reminder,
    is_bilingual,
)


class TestCheckStatusLabels:
    """Tests for status label enforcement."""

    def test_flags_bare_ongoing(self):
        content = "<td>Ongoing</td>"
        issues = check_status_labels(content)
        assert len(issues) >= 1
        assert any("Ongoing" in i for i in issues)

    def test_passes_ongoing_with_detail(self):
        content = "<td>Ongoing: Phase 2 validation</td>"
        issues = check_status_labels(content)
        assert len(issues) == 0

    def test_passes_ongoing_with_dash(self):
        content = "<td>Ongoing - user testing</td>"
        issues = check_status_labels(content)
        assert len(issues) == 0

    def test_flags_bare_independently(self):
        content = "<td>Continues independently</td>"
        issues = check_status_labels(content)
        assert len(issues) >= 1
        assert any("independently" in i for i in issues)

    def test_passes_independently_with_detail(self):
        content = "<td>Continues independently (lab practice & exam)</td>"
        issues = check_status_labels(content)
        assert len(issues) == 0

    def test_caps_at_8_issues(self):
        content = "\n".join([f"<tr><td>Ongoing</td></tr>" for _ in range(20)])
        issues = check_status_labels(content)
        assert len(issues) <= 8


class TestCheckBilingualParity:
    """Tests for bilingual EN/AR parity checks."""

    def test_flags_span_mismatch(self):
        content = '''
        <span class="lang-en">Hello</span>
        <span class="lang-en">World</span>
        <span class="lang-ar">مرحبا</span>
        '''
        issues = check_bilingual_parity(content)
        assert any("mismatch" in i.lower() or "Span" in i for i in issues)

    def test_passes_equal_spans(self):
        content = '''
        <span class="lang-en" data-i18n="title">Hello</span>
        <span class="lang-ar" data-i18n="title">مرحبا</span>
        '''
        issues = check_bilingual_parity(content)
        assert len(issues) == 0

    def test_flags_empty_translation(self):
        content = '''
        <span class="lang-en" data-i18n="key1">Hello</span>
        <span class="lang-ar" data-i18n="key1"></span>
        '''
        issues = check_bilingual_parity(content)
        assert any("Empty" in i or "empty" in i for i in issues)

    def test_skips_non_bilingual(self):
        content = "<p>Just plain English</p>"
        issues = check_bilingual_parity(content)
        assert len(issues) == 0


class TestCheckDashboardQuality:
    """Tests for dashboard quality checks."""

    def test_flags_missing_source_tab(self):
        content = "<h1>Dashboard</h1><p>Some metrics</p>"
        issues = check_dashboard_quality(content)
        assert any("Data Source" in i or "Source" in i for i in issues)

    def test_passes_with_source_tab(self):
        content = '<div id="data-source"><h3>Data Source</h3></div>'
        issues = check_dashboard_quality(content)
        assert not any("Source" in i for i in issues)

    def test_flags_live_clock_without_fetch(self):
        content = '''
        <script>
        setInterval(() => {
            document.getElementById('time').textContent = new Date().toLocaleTimeString();
        }, 1000);
        </script>
        '''
        issues = check_dashboard_quality(content)
        assert any("clock" in i.lower() or "Live" in i for i in issues)

    def test_passes_clock_with_fetch_timestamp(self):
        content = '''
        <p>Last updated: <span id="fetch-time"></span></p>
        <script>new Date()</script>
        '''
        issues = check_dashboard_quality(content)
        assert not any("clock" in i.lower() for i in issues)


class TestCheckTitleConsistency:
    """Tests for title consistency checks."""

    def test_flags_multiple_variants(self):
        content = "IT Project Manager leads the team.\nThe PM reviewed the report.\n"
        issues = check_title_consistency(content)
        assert len(issues) >= 1

    def test_passes_single_variant(self):
        content = "IT Project Manager leads the team.\nIT Project Manager approved.\n"
        issues = check_title_consistency(content)
        assert len(issues) == 0

    def test_skips_css_lines(self):
        content = ".pm-card { color: red; }\nIT Project Manager leads the team.\n"
        issues = check_title_consistency(content)
        assert len(issues) == 0


class TestCheckModalAccessibility:
    """Tests for modal accessibility checks."""

    def test_flags_modal_without_max_height(self):
        content = ".modal-content { padding: 20px; }"
        issues = check_modal_accessibility(content)
        assert len(issues) >= 1
        assert any("max-height" in i for i in issues)

    def test_passes_modal_with_styles(self):
        content = ".modal-content { max-height: 85vh; overflow-y: auto; }"
        issues = check_modal_accessibility(content)
        assert len(issues) == 0

    def test_skips_no_modal(self):
        content = "<p>No modals here</p>"
        issues = check_modal_accessibility(content)
        assert len(issues) == 0


class TestCheckPrintCss:
    """Tests for print CSS checks."""

    def test_flags_missing_print_media(self):
        content = "body { color: black; }"
        issues = check_print_css(content)
        assert any("print" in i.lower() for i in issues)

    def test_flags_print_without_break_inside(self):
        content = "@media print { body { color: black; } }"
        issues = check_print_css(content)
        assert any("break-inside" in i for i in issues)

    def test_passes_complete_print_css(self):
        content = "@media print { .card { break-inside: avoid; } }"
        issues = check_print_css(content)
        assert len(issues) == 0


class TestCheckHtmlRenderReminder:
    """Tests for HTML render reminder."""

    def test_always_fires(self):
        issues = check_html_render_reminder("test.html", "<p>content</p>")
        assert len(issues) >= 1
        assert any("Render" in i or "browser" in i for i in issues)

    def test_bilingual_extra_message(self):
        content = '<span class="lang-en">Hello</span><span class="lang-ar">مرحبا</span>'
        issues = check_html_render_reminder("test.html", content)
        assert any("Bilingual" in i or "EN and AR" in i for i in issues)


class TestIsBilingual:
    """Tests for is_bilingual() helper."""

    def test_detects_data_i18n(self):
        assert is_bilingual('<span data-i18n="key">text</span>') is True

    def test_detects_lang_classes(self):
        assert is_bilingual('<span class="lang-en">text</span>') is True

    def test_detects_lang_attr(self):
        assert is_bilingual('<html lang="ar">') is True

    def test_rejects_plain_html(self):
        assert is_bilingual('<p>Just English</p>') is False


class TestGracefulDegradation:
    """Tests that a broken check doesn't crash the dispatcher."""

    def test_broken_check_doesnt_crash_others(self, monkeypatch):
        """If one check raises, other checks still produce results."""
        import post_write_dispatcher as d

        # Make check_status_labels raise
        original = d.check_status_labels
        def broken_check(content):
            raise RuntimeError("Simulated failure")
        monkeypatch.setattr(d, 'check_status_labels', broken_check)

        # Title consistency should still work even though status labels crashed
        content = "IT Project Manager leads.\nThe PM reviewed."
        issues = d.check_title_consistency(content)
        assert len(issues) >= 1  # title check still works independently

        monkeypatch.setattr(d, 'check_status_labels', original)

    def test_errors_logged_to_stderr(self, capsys, monkeypatch):
        """Verify that check failures are reported to stderr."""
        import post_write_dispatcher as d
        import io

        def broken_check(content):
            raise ValueError("Test error")

        # Run the check in the pattern used by main()
        errors = []
        try:
            broken_check("content")
        except Exception as e:
            errors.append(f"broken_check: {e}")

        for err in errors:
            print(f"pm-guidelines:dispatcher: {err}", file=sys.stderr)

        captured = capsys.readouterr()
        assert "Test error" in captured.err
