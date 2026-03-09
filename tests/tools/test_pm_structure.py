#!/usr/bin/env python3
"""Tests for the PM structure in the tools directory."""
import importlib.util
import os


def test_pm_package_missing(tmp_path) -> None:
    """Test that the PM package does not exist in the tools directory."""
    assert not os.path.isdir("src/tools/pm")
    assert importlib.util.find_spec("tools.pm") is None
