#!/usr/bin/env python3
"""Tests for the Deployment directory structure."""

import os


def test_deployment_tree_absent() -> None:
    """The Deployment directory should not exist before setup."""
    # initially it should not exist (setup has not been run yet)
    assert not os.path.isdir("Deployment")
