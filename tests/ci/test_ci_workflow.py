#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for CI workflow."""

import os

import yaml


def _load_ci_workflow() -> dict:
    """Load and return ci.yml as a parsed mapping.

    Returns:
        dict: Parsed YAML mapping for .github/workflows/ci.yml.

    """
    with open(".github/workflows/ci.yml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _on_block(workflow: dict) -> dict:
    """Normalize workflow trigger block from parsed YAML.

    Args:
        workflow: Parsed workflow mapping.

    Returns:
        dict: Trigger block under the ``on`` key.

    """
    return workflow.get("on", workflow.get(True, {}))


def test_ci_workflow_exists() -> None:
    """The CI workflow file should exist in the expected location."""
    path = ".github/workflows/ci.yml"
    assert os.path.isfile(path)


def test_ci_workflow_sanity() -> None:
    """The CI workflow file should contain expected keys and structure."""
    data = _load_ci_workflow()
    assert "jobs" in data
    assert "quick" in data["jobs"]


def test_ci_workflow_pull_request_trigger_includes_project_branches() -> None:
    """PR trigger contract includes explicit project-branch policy pattern.

    This enforces AC-QWB-001 / IFACE-QWB-001 for project-branch PR governance.
    """
    data = _load_ci_workflow()
    on_block = _on_block(data)
    pr_trigger = on_block.get("pull_request")
    assert isinstance(pr_trigger, dict), "ci.yml must define pull_request trigger as a mapping"

    branches = pr_trigger.get("branches", [])
    assert isinstance(branches, list), "ci.yml pull_request.branches must be a list"
    assert "main" in branches, "ci.yml pull_request.branches must continue to include 'main'"
    assert "prj[0-9][0-9][0-9][0-9][0-9][0-9][0-9]-*" in branches, (
        "ci.yml pull_request.branches must include explicit project-branch pattern "
        "'prj[0-9][0-9][0-9][0-9][0-9][0-9][0-9]-*'"
    )
    assert "prj*" not in branches, "ci.yml pull_request.branches must not use ambiguous wildcard 'prj*'"


def test_ci_workflow_required_check_identity_contract() -> None:
    """Required-check identity contract uses stable lightweight check names.

    This enforces AC-QWB-004 / IFACE-QWB-004 so branch protection policies
    reference deterministic workflow/job identities.
    """
    data = _load_ci_workflow()

    assert data.get("name") == "CI / Lightweight", (
        "ci.yml workflow name must remain 'CI / Lightweight' for required-check stability"
    )

    jobs = data.get("jobs", {})
    assert "quick" in jobs, "ci.yml must define a quick job for required-check identity"

    quick = jobs["quick"]
    assert quick.get("name") == "Quick Checks", (
        "ci.yml quick job name must remain 'Quick Checks' for required-check stability"
    )


def test_ci_workflow_quick_job_runs_precommit_and_placeholder_tests() -> None:
    """Quick job should run pre-commit and placeholder smoke tests."""
    data = _load_ci_workflow()
    jobs = data.get("jobs", {})
    quick = jobs.get("quick", {})
    steps = quick.get("steps", [])

    step_names = [step.get("name", "") for step in steps if isinstance(step, dict)]
    assert "Run pre-commit hooks" in step_names
    assert "Run quick placeholder tests" in step_names


def test_ci_workflow_has_no_sharding_and_no_rust_build() -> None:
    """Lightweight CI should avoid matrix sharding and Rust build in CI path."""
    data = _load_ci_workflow()
    quick_job = data.get("jobs", {}).get("quick", {})
    steps = [step for step in quick_job.get("steps", []) if isinstance(step, dict)]

    assert "strategy" not in quick_job, "quick CI job must not use matrix sharding"

    rust_steps = [step for step in steps if "Rust" in (step.get("name") or "")]
    assert not rust_steps, "lightweight CI quick job should not include Rust build steps"


def test_ci_workflow_quick_job_runs_precommit_command() -> None:
    """Quick job step must invoke pre-commit with --all-files flag (AC-SEC-004).

    Asserts the command text in the Run pre-commit hooks step to prevent
    silent drift where the step exists by name but the command changes.

    """
    data = _load_ci_workflow()
    jobs = data.get("jobs", {})
    quick = jobs.get("quick", {})
    steps = quick.get("steps", [])

    pre_commit_step = next(
        (step for step in steps if isinstance(step, dict) and step.get("name") == "Run pre-commit hooks"),
        None,
    )
    assert pre_commit_step is not None, "ci.yml quick job must have a 'Run pre-commit hooks' step"
    run_command: str = pre_commit_step.get("run", "")
    assert "pre-commit run --all-files" in run_command, (
        "ci.yml 'Run pre-commit hooks' step must invoke 'pre-commit run --all-files'"
    )
