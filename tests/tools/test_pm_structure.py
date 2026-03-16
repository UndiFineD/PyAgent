#!/usr/bin/env python3
"""Tests for the PM structure in the tools directory."""

import importlib.util
import os


def test_pm_package_present(tmp_path) -> None:
    """Test that the PM package exists and is importable."""
    assert os.path.isdir("src/tools/pm")
    assert importlib.util.find_spec("tools.pm") is not None
