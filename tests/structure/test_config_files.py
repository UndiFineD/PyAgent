#!/usr/bin/env python3
"""Tests for configuration files in the project."""

import os


def test_pytest_config_present() -> None:
    """pytest.ini should be present in the project root."""
    assert os.path.isfile("pytest.ini")


def test_conftest_imports_src() -> None:
    """conftest.py should be able to import from src without error."""
