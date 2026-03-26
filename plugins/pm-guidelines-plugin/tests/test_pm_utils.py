"""Tests for pm_utils.py shared utility functions."""

import os
import pytest
from pm_utils import is_pm_deliverable, is_html_file, is_dashboard_file, read_file_safe


class TestIsPmDeliverable:
    """Tests for is_pm_deliverable()."""

    def test_html_in_reports_dir(self):
        assert is_pm_deliverable("D:/projects/reports/status.html") is True

    def test_html_in_dashboards_dir(self):
        assert is_pm_deliverable("D:/projects/dashboards/kpi.html") is True

    def test_md_in_deliverables_dir(self):
        assert is_pm_deliverable("D:/projects/deliverables/plan.md") is True

    def test_html_with_pm_keyword(self):
        assert is_pm_deliverable("D:/work/my_dashboard_v3.html") is True

    def test_html_with_parent_pattern(self):
        assert is_pm_deliverable("D:/Project Management/files/test.html") is True

    def test_python_file_rejected(self):
        assert is_pm_deliverable("D:/src/main.py") is False

    def test_html_in_code_dir(self):
        # HTML file but not in PM directory and no PM keywords
        assert is_pm_deliverable("D:/src/templates/index.html") is False

    def test_empty_path(self):
        assert is_pm_deliverable("") is False

    def test_none_path(self):
        assert is_pm_deliverable(None) is False

    def test_backslash_paths(self):
        assert is_pm_deliverable("D:\\projects\\reports\\status.html") is True


class TestIsHtmlFile:
    """Tests for is_html_file()."""

    def test_html_extension(self):
        assert is_html_file("file.html") is True

    def test_htm_extension(self):
        assert is_html_file("file.htm") is True

    def test_md_extension(self):
        assert is_html_file("file.md") is False

    def test_py_extension(self):
        assert is_html_file("file.py") is False

    def test_empty_path(self):
        assert is_html_file("") is False

    def test_none_path(self):
        assert is_html_file(None) is False


class TestIsDashboardFile:
    """Tests for is_dashboard_file()."""

    def test_dashboard_keyword(self):
        assert is_dashboard_file("OKR_KPI_Dashboard_v3.html") is True

    def test_report_keyword(self):
        assert is_dashboard_file("weekly_report.html") is True

    def test_metrics_keyword(self):
        assert is_dashboard_file("team_metrics.html") is True

    def test_no_keyword(self):
        assert is_dashboard_file("index.html") is False

    def test_non_html(self):
        assert is_dashboard_file("dashboard.md") is False


class TestReadFileSafe:
    """Tests for read_file_safe()."""

    def test_read_existing_file(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("hello world", encoding="utf-8")
        assert read_file_safe(str(f)) == "hello world"

    def test_read_nonexistent_file(self):
        assert read_file_safe("/nonexistent/path/file.txt") == ""

    def test_read_oversized_file(self, tmp_path):
        f = tmp_path / "big.txt"
        f.write_text("x" * 600_000, encoding="utf-8")
        assert read_file_safe(str(f), max_size=500_000) == ""

    def test_read_within_size_limit(self, tmp_path):
        f = tmp_path / "small.txt"
        f.write_text("small content", encoding="utf-8")
        assert read_file_safe(str(f), max_size=500_000) == "small content"
