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
    assert "test" in data["jobs"]


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
    """Required-check identity contract uses stable governance check names.

    This enforces AC-QWB-004 / IFACE-QWB-004 so branch protection policies
    reference deterministic workflow/job identities.
    """
    data = _load_ci_workflow()

    assert data.get("name") == "CI / Branch Governance", (
        "ci.yml workflow name must remain 'CI / Branch Governance' for required-check stability"
    )

    jobs = data.get("jobs", {})
    assert "governance" in jobs, "ci.yml must define a governance job for required-check identity"

    governance = jobs["governance"]
    assert governance.get("name") == "Governance Gate", (
        "ci.yml governance job name must remain 'Governance Gate' for required-check stability"
    )


def test_ci_workflow_governance_job_runs_precommit_and_mypy_once() -> None:
    """Governance job should own pre-commit and strict mypy checks."""
    data = _load_ci_workflow()
    jobs = data.get("jobs", {})
    governance = jobs.get("governance", {})
    steps = governance.get("steps", [])

    step_names = [step.get("name", "") for step in steps if isinstance(step, dict)]
    assert "Run pre-commit quality hooks (without duplicate shared-check profile)" in step_names
    assert "Run mypy strict lane" in step_names


def test_ci_workflow_test_shards_do_not_repeat_mypy_and_limit_rust_build() -> None:
    """Shard job should avoid repeated mypy and skip Rust build for lightweight shards."""
    data = _load_ci_workflow()
    test_job = data.get("jobs", {}).get("test", {})
    steps = [step for step in test_job.get("steps", []) if isinstance(step, dict)]

    mypy_steps = [step for step in steps if step.get("name") == "Run mypy strict lane"]
    assert not mypy_steps, "test shard job should not re-run strict mypy in every shard"

    rust_steps = [step for step in steps if step.get("name") == "Build Rust extension"]
    assert rust_steps, "test shard job must define a Rust build step"
    rust_if = rust_steps[0].get("if", "")
    assert "matrix.shard != 1" in rust_if and "matrix.shard != 2" in rust_if and "matrix.shard != 3" in rust_if, (
        "Rust build must be skipped for lightweight shards 1-3"
    )
