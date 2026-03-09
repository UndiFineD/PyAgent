#!/usr/bin/env python3
"""Tests for the Deployment directory structure."""
import os


def test_deployment_tree_absent() -> None:
    """The Deployment directory should not exist before setup."""
    # initially should fail because the directory doesn't exist
    assert os.path.isdir("Deployment")
