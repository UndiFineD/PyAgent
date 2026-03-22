#!/usr/bin/env python3
"""Tests for coverage option in pytest.ini."""


def test_cov_option_present() -> None:
    """requirements-ci.txt should declare pytest-cov so coverage is available in CI."""
    content = open("requirements-ci.txt", encoding="utf8").read()
    assert "pytest-cov" in content
