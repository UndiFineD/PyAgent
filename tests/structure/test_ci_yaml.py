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
    """Return CI test-job steps that enforce coverage gate behavior.

    Args:
        ci_workflow: Parsed workflow document.

    Returns:
        Step entries that indicate coverage gating commands.

    """
    steps = ci_workflow["jobs"]["test"]["steps"]
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
    steps = data["jobs"]["test"]["steps"]
    assert any("pytest" in (step.get("run") or "") for step in steps)


def test_ci_does_not_run_shared_precommit_profile() -> None:
    """Verify CI does not duplicate the local-only shared precommit profile.

    Returns:
        None.

    """
    data = _load_ci_workflow()
    steps = data["jobs"]["test"]["steps"]
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


def test_ci_has_mypy_strict_lane_blocking_step() -> None:
    """Verify CI contains the strict-lane mypy command.

    Returns:
        None.

    """
    data = _load_ci_workflow()

    steps = data["jobs"]["test"]["steps"]
    expected_command = "python -m mypy --config-file mypy-strict-lane.ini"
    assert any(expected_command in (step.get("run") or "") for step in steps), (
        "CI must include a strict-lane mypy run command: python -m mypy --config-file mypy-strict-lane.ini"
    )


def test_ci_mypy_strict_lane_step_is_blocking() -> None:
    """Verify strict-lane mypy command is not softened.

    Returns:
        None.

    """
    data = _load_ci_workflow()

    steps = data["jobs"]["test"]["steps"]
    strict_steps = [step for step in steps if "mypy-strict-lane.ini" in (step.get("run") or "")]
    assert strict_steps, "Expected at least one CI step that runs mypy with mypy-strict-lane.ini."

    for step in strict_steps:
        run_cmd = step.get("run") or ""
        assert "|| true" not in run_cmd and "||true" not in run_cmd, (
            "Strict-lane mypy CI command must be blocking; soft-fail operator found."
        )
        assert "continue-on-error" not in step, "Strict-lane mypy CI step must not set continue-on-error."
        assert "set +e" not in run_cmd, "Strict-lane mypy CI step must not disable fail-fast semantics."


def test_ci_has_coverage_gate_step() -> None:
    """Verify CI includes a dedicated coverage gate path in jobs.test.

    Returns:
        None.

    """
    data = _load_ci_workflow()
    coverage_gate_steps = _find_coverage_gate_steps(data)
    assert coverage_gate_steps, (
        "CI must include a blocking coverage gate command in jobs.test. "
        "Expected '--cov-fail-under' or 'coverage report' in at least one step."
    )


def test_ci_coverage_gate_path_is_blocking() -> None:
    """Verify CI coverage gate path is fail-closed.

    Returns:
        None.

    """
    data = _load_ci_workflow()
    test_job = data["jobs"]["test"]
    coverage_gate_steps = _find_coverage_gate_steps(data)
    assert coverage_gate_steps, "Coverage gate step must exist before blocking semantics are validated."

    assert not test_job.get("continue-on-error", False), "jobs.test must not set continue-on-error for coverage gating"

    for step in coverage_gate_steps:
        run_cmd = (step.get("run") or "").lower()
        assert "|| true" not in run_cmd and "||true" not in run_cmd, (
            "Coverage gate step must not use soft-fail operator '|| true'."
        )
        assert "set +e" not in run_cmd, "Coverage gate step must not disable fail-fast semantics with 'set +e'."
        assert not step.get("continue-on-error", False), "Coverage gate step must not set continue-on-error."
