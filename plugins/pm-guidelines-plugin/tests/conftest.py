"""Shared fixtures for pm-guidelines hook tests."""

import json
import os
import sys

import pytest

# Add hooks directory to path so we can import modules
PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS_DIR = os.path.join(PLUGIN_ROOT, 'hooks')

if HOOKS_DIR not in sys.path:
    sys.path.insert(0, HOOKS_DIR)

# Set CLAUDE_PLUGIN_ROOT so hooks can find pm_utils
os.environ['CLAUDE_PLUGIN_ROOT'] = PLUGIN_ROOT


@pytest.fixture
def fixtures_dir():
    """Return path to test fixtures directory."""
    return os.path.join(os.path.dirname(__file__), 'fixtures')


@pytest.fixture
def tmp_html(tmp_path):
    """Factory fixture to create temporary HTML files."""
    def _create(content, filename="test_dashboard_report.html"):
        f = tmp_path / filename
        f.write_text(content, encoding="utf-8")
        return str(f)
    return _create


@pytest.fixture
def make_stdin():
    """Factory fixture to create mock stdin JSON for hook testing."""
    def _make(file_path, tool_name="Write", **extra_input):
        data = {
            "tool_name": tool_name,
            "tool_input": {"file_path": file_path, **extra_input}
        }
        return json.dumps(data)
    return _make
