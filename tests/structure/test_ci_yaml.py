#!/usr/bin/env python3
"""Tests for CI workflow."""

from pathlib import Path

import yaml


def test_ci_runs_pytest() -> None:
    """The CI workflow should include a step that runs pytest."""
    with open(".github/workflows/ci.yml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    steps = data["jobs"]["test"]["steps"]
    assert any("pytest" in (step.get("run") or "") for step in steps)


def test_ci_does_not_run_shared_precommit_profile() -> None:
    """The CI workflow should not duplicate the local-only shared precommit profile."""
    with open(".github/workflows/ci.yml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    steps = data["jobs"]["test"]["steps"]
    assert not any("python scripts/ci/run_checks.py --profile precommit" in (step.get("run") or "") for step in steps)


def test_setup_md_has_local_testing_section() -> None:
    """docs/setup.md must have a Local Testing section documenting pre-commit + pytest."""
    content = Path("docs/setup.md").read_text(encoding="utf-8")
    assert "## Local Testing" in content, (
        "docs/setup.md must contain a '## Local Testing' section that documents "
        "how to run pre-commit and pytest locally (prj0000075 AC-05)"
    )
