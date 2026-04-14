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


def _get_job(ci_workflow: dict[str, Any], job_name: str) -> dict[str, Any]:
    """Return a named workflow job.

    Args:
        ci_workflow: Parsed workflow document.
        job_name: Job key under ``jobs``.

    Returns:
        The selected job mapping.

    """
    return ci_workflow.get("jobs", {}).get(job_name, {})


def _get_job_steps(ci_workflow: dict[str, Any], job_name: str) -> list[dict[str, Any]]:
    """Return step list for a named workflow job.

    Args:
        ci_workflow: Parsed workflow document.
        job_name: Job key under ``jobs``.

    Returns:
        List of step mappings.

    """
    return _get_job(ci_workflow, job_name).get("steps", [])


def _normalize_needs(needs_value: Any) -> list[str]:
    """Normalize GitHub Actions ``needs`` values into a list of names.

    Args:
        needs_value: Scalar or list value from workflow YAML.

    Returns:
        Normalized list of dependency job names.

    """
    if needs_value is None:
        return []
    if isinstance(needs_value, str):
        return [needs_value]
    if isinstance(needs_value, list):
        return [str(entry) for entry in needs_value]
    return []


def _collect_coverage_run_text(ci_workflow: dict[str, Any]) -> str:
    """Collect normalized run-command text from the coverage job.

    Args:
        ci_workflow: Parsed workflow document.

    Returns:
        Lower-cased concatenated run commands from ``jobs.coverage.steps``.

    """
    run_chunks: list[str] = []
    for step in _get_job_steps(ci_workflow, "coverage"):
        run_text = step.get("run")
        if isinstance(run_text, str):
            run_chunks.append(run_text.lower())
    return "\n".join(run_chunks)


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
    """Verify workflow has exactly one dedicated coverage job.

    Returns:
        None.

    """
    data = _load_ci_workflow()
    jobs = data.get("jobs", {})
    coverage_job_names = [job_name for job_name in jobs if job_name == "coverage"]
    assert len(coverage_job_names) == 1, "CI must define exactly one jobs.coverage gate."


def test_ci_coverage_gate_path_is_blocking() -> None:
    """Verify coverage path is fail-closed and depends on quick.

    Returns:
        None.

    """
    data = _load_ci_workflow()
    quick_job = _get_job(data, "quick")
    coverage_job = _get_job(data, "coverage")

    assert quick_job, "CI must preserve jobs.quick as the lightweight lane."
    assert coverage_job, "CI must define jobs.coverage for required coverage gating."

    coverage_needs = _normalize_needs(coverage_job.get("needs"))
    assert "quick" in coverage_needs, "jobs.coverage.needs must include quick."

    assert not quick_job.get("continue-on-error", False), "jobs.quick must remain fail-closed."
    assert not coverage_job.get("continue-on-error", False), "jobs.coverage must be fail-closed."


def test_ci_coverage_job_uses_canonical_pytest_cov_flags() -> None:
    """Verify coverage job uses the canonical pytest-cov invocation contract.

    Returns:
        None.

    """
    data = _load_ci_workflow()
    coverage_run_text = _collect_coverage_run_text(data)

    required_markers = (
        "pytest",
        "--cov=src",
        "--cov-branch",
        "--cov-config=pyproject.toml",
        "--cov-report=term-missing",
        "--cov-report=xml",
    )
    for marker in required_markers:
        assert marker in coverage_run_text, f"Coverage command must include canonical marker: {marker}"


def test_ci_coverage_path_rejects_inline_threshold_and_soft_fail_markers() -> None:
    """Verify coverage gate rejects threshold duplication and soft-fail controls.

    Returns:
        None.

    """
    data = _load_ci_workflow()
    coverage_job = _get_job(data, "coverage")
    coverage_run_text = _collect_coverage_run_text(data)

    forbidden_run_markers = ("--cov-fail-under", "|| true", "set +e")
    for marker in forbidden_run_markers:
        assert marker not in coverage_run_text, f"Coverage path must reject soft-fail marker: {marker}"

    assert not coverage_job.get("continue-on-error", False), "jobs.coverage must reject continue-on-error."

    coverage_steps = _get_job_steps(data, "coverage")
    for step in coverage_steps:
        assert not step.get("continue-on-error", False), (
            "jobs.coverage steps must reject continue-on-error in coverage path."
        )
