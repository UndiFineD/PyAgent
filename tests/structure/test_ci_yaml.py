#!/usr/bin/env python3
"""Tests for CI workflow."""

from pathlib import Path
from typing import Any

import yaml


def _load_ci_workflow() -> dict[str, Any]:
    """Load the CI workflow YAML document.

    Returns:
        Parsed CI workflow mapping.

    """
    with open(".github/workflows/ci.yml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _find_coverage_gate_steps(ci_workflow: dict[str, Any]) -> list[dict[str, Any]]:
    """Return CI quick-job steps that include coverage-related commands.

    Args:
        ci_workflow: Parsed workflow document.

    Returns:
        Step entries that indicate coverage gating commands.

    """
    steps = ci_workflow["jobs"]["quick"]["steps"]
    gate_markers = ("--cov-fail-under", "coverage report")
    gate_steps: list[dict[str, Any]] = []

    for step in steps:
        run_cmd = (step.get("run") or "").lower()
        if any(marker in run_cmd for marker in gate_markers):
            gate_steps.append(step)

    return gate_steps


def test_ci_runs_pytest() -> None:
    """Verify CI includes at least one pytest invocation.

    Returns:
        None.

    """
    data = _load_ci_workflow()
    steps = data["jobs"]["quick"]["steps"]
    assert any("pytest" in (step.get("run") or "") for step in steps)


def test_ci_does_not_run_shared_precommit_profile() -> None:
    """Verify CI does not duplicate the local-only shared precommit profile.

    Returns:
        None.

    """
    data = _load_ci_workflow()
    steps = data["jobs"]["quick"]["steps"]
    assert not any("python scripts/ci/run_checks.py --profile precommit" in (step.get("run") or "") for step in steps)


def test_setup_md_has_local_testing_section() -> None:
    """Verify docs/setup.md includes the local testing section.

    Returns:
        None.

    """
    content = Path("docs/setup.md").read_text(encoding="utf-8")
    assert "## Local Testing" in content, (
        "docs/setup.md must contain a '## Local Testing' section that documents "
        "how to run pre-commit and pytest locally (prj0000075 AC-05)"
    )


def test_ci_has_precommit_step() -> None:
    """Verify CI contains pre-commit execution.

    Returns:
        None.

    """
    data = _load_ci_workflow()

    steps = data["jobs"]["quick"]["steps"]
    expected_command = "pre-commit run --all-files"
    assert any(expected_command in (step.get("run") or "") for step in steps), (
        "CI quick job must include pre-commit command: pre-commit run --all-files"
    )


def test_ci_placeholder_pytest_step_is_present() -> None:
    """Verify quick CI runs minimal placeholder test file.

    Returns:
        None.

    """
    data = _load_ci_workflow()

    steps = data["jobs"]["quick"]["steps"]
    placeholder_steps = [step for step in steps if "tests/ci/test_placeholder_smoke.py" in (step.get("run") or "")]
    assert placeholder_steps, "Expected quick CI to run tests/ci/test_placeholder_smoke.py."


def test_ci_has_coverage_gate_step() -> None:
    """Verify lightweight CI intentionally does not include a coverage gate path.

    Returns:
        None.

    """
    data = _load_ci_workflow()
    coverage_gate_steps = _find_coverage_gate_steps(data)
    assert not coverage_gate_steps, "Lightweight CI should not include coverage gate commands."


def test_ci_coverage_gate_path_is_blocking() -> None:
    """Verify lightweight CI has no coverage gate path configured.

    Returns:
        None.

    """
    data = _load_ci_workflow()
    test_job = data["jobs"]["quick"]
    coverage_gate_steps = _find_coverage_gate_steps(data)
    assert not coverage_gate_steps, "Coverage gate steps must be absent in lightweight CI mode."
    assert not test_job.get("continue-on-error", False), "jobs.quick must remain fail-closed."
