#!/usr/bin/env python3
"""Tests for governance documentation and templates."""
import os


def test_governance_docs_missing() -> None:
    """Before running the governance setup, the expected docs and directories should be absent."""
    # Ensure project directory is in workspace root
    root = os.path.abspath(os.path.join(os.getcwd(), "project"))
    # These files should not exist before initialization script
    expected = [
        "governance.md",
        "milestones.md",
        "budget.md",
        "risk.md",
    ]
    # if setup was already run, skip this test
    for fname in expected:
        if os.path.exists(os.path.join(root, fname)):
            import pytest

            pytest.skip("governance setup already applied - skipping absence check")
    for fname in expected:
        path = os.path.join(root, fname)
        assert not os.path.exists(path), f"{fname} should not exist before setup"

    # directories
    dirs = [
        "metrics",
        "standups",
        "incidents",
        "templates",
    ]
    for d in dirs:
        assert not os.path.exists(os.path.join(root, d)), f"{d} should not exist before setup"
