"""Tests for pat_token_guard.py security hook.

NOTE: Secret patterns are constructed at runtime to avoid
triggering the pat_token_guard hook on this test file itself.
"""

import pytest
from pat_token_guard import scan_for_secrets, is_excluded_path, get_content_to_scan


def _make_github_token():
    """Build a fake GitHub PAT at runtime to avoid hook detection."""
    prefix = "ghp_"
    body = "A" * 40
    return prefix + body


def _make_sk_key():
    """Build a fake sk- key at runtime."""
    return "sk-" + "A" * 40


def _make_aws_key():
    """Build a fake AWS key at runtime."""
    return "AKIA" + "I" * 4 + "O" * 4 + "S" * 4 + "F" * 4


def _make_npm_token():
    """Build a fake npm token at runtime."""
    return "npm_" + "A" * 40


def _make_bearer():
    """Build a fake bearer token at runtime."""
    return "Bearer " + "eyJ" + "a" * 50


class TestScanForSecrets:
    """Tests for scan_for_secrets()."""

    def test_catches_github_pat(self):
        content = f"token = {_make_github_token()}"
        results = scan_for_secrets(content)
        assert len(results) >= 1
        assert any("GitHub" in stype for _, stype in results)

    def test_catches_sk_key(self):
        content = f"api_key = {_make_sk_key()}"
        results = scan_for_secrets(content)
        assert len(results) >= 1
        assert any("sk-" in stype for _, stype in results)

    def test_catches_aws_key(self):
        content = f"aws_key = {_make_aws_key()}"
        results = scan_for_secrets(content)
        assert len(results) >= 1
        assert any("AWS" in stype for _, stype in results)

    def test_catches_bearer_token(self):
        content = f"Authorization: {_make_bearer()}"
        results = scan_for_secrets(content)
        assert len(results) >= 1
        assert any("Bearer" in stype for _, stype in results)

    def test_catches_npm_token(self):
        content = _make_npm_token()
        results = scan_for_secrets(content)
        assert len(results) >= 1

    def test_passes_normal_code(self):
        content = "const name = 'hello world'; function getData() { return 42; }"
        results = scan_for_secrets(content)
        assert len(results) == 0

    def test_passes_short_strings(self):
        content = "sk = 'abc'"
        results = scan_for_secrets(content)
        assert len(results) == 0

    def test_azure_pat_with_context(self):
        # 52-char base32 with secret context keyword
        pat = "a" * 52
        content = f"token = {pat}"
        results = scan_for_secrets(content)
        assert any("Azure" in stype for _, stype in results)

    def test_azure_pat_without_context(self):
        # 52-char base32 WITHOUT secret context keyword
        pat = "a" * 52
        content = f"hash_value = {pat}"
        results = scan_for_secrets(content)
        # Should NOT flag without context keywords
        assert not any("Azure" in stype for _, stype in results)


class TestIsExcludedPath:
    """Tests for is_excluded_path()."""

    def test_env_example_excluded(self):
        assert is_excluded_path(".env.example") is True

    def test_readme_excluded(self):
        assert is_excluded_path("project/README.md") is True

    def test_normal_file_not_excluded(self):
        assert is_excluded_path("src/config.py") is False

    def test_empty_path(self):
        assert is_excluded_path("") is False


class TestGetContentToScan:
    """Tests for get_content_to_scan()."""

    def test_bash_command(self):
        result = get_content_to_scan({"command": "echo hello"}, "Bash")
        assert result == "echo hello"

    def test_write_content(self):
        result = get_content_to_scan({"content": "file content"}, "Write")
        assert result == "file content"

    def test_edit_new_string(self):
        result = get_content_to_scan({"new_string": "new code"}, "Edit")
        assert result == "new code"

    def test_unknown_tool(self):
        result = get_content_to_scan({"data": "something"}, "Read")
        assert result == ""
