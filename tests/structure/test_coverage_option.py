#!/usr/bin/env python3
"""Tests for coverage option in pytest.ini."""


def test_cov_option_present() -> None:
    """pytest.ini should contain the --cov option for coverage reporting."""
    # read pytest.ini to ensure coverage addopts configured
    content = open("pytest.ini", encoding="utf8").read()
    assert "--cov=src" in content
