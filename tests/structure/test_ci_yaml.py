#!/usr/bin/env python3
"""Tests for CI workflow."""

import yaml


def test_ci_runs_pytest() -> None:
    """The CI workflow should include a step that runs pytest."""
    data = yaml.safe_load(open(".github/workflows/ci.yml", encoding="utf-8"))
    steps = data["jobs"]["test"]["steps"]
    assert any("pytest" in (step.get("run") or "") for step in steps)


def test_ci_does_not_run_shared_precommit_profile() -> None:
    """The CI workflow should not duplicate the local-only shared precommit profile."""
    data = yaml.safe_load(open(".github/workflows/ci.yml", encoding="utf-8"))
    steps = data["jobs"]["test"]["steps"]
    assert not any("python scripts/ci/run_checks.py --profile precommit" in (step.get("run") or "") for step in steps)
