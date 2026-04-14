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

"""CI contract tests for prj0000117 workspace unification slice."""

from typing import Any

import yaml


def _load_ci_workflow() -> dict[str, Any]:
    """Load and parse the CI workflow YAML document.

    Returns:
        dict[str, Any]: Parsed .github/workflows/ci.yml mapping.

    """
    with open(".github/workflows/ci.yml", encoding="utf-8") as workflow_file:
        data = yaml.safe_load(workflow_file)
    return data if isinstance(data, dict) else {}


def _iter_run_commands(workflow: dict[str, Any]) -> list[str]:
    """Collect run command text from all workflow job steps.

    Args:
        workflow: Parsed CI workflow mapping.

    Returns:
        list[str]: Normalized command text entries.

    """
    commands: list[str] = []
    jobs = workflow.get("jobs", {})
    if not isinstance(jobs, dict):
        return commands

    for job_data in jobs.values():
        if not isinstance(job_data, dict):
            continue
        steps = job_data.get("steps", [])
        if not isinstance(steps, list):
            continue
        for step in steps:
            if not isinstance(step, dict):
                continue
            run_value = step.get("run")
            if isinstance(run_value, str):
                commands.append(run_value.strip())
    return commands


def test_ci_quick_job_remains_lightweight_without_matrix_sharding() -> None:
    """Assert CI quick job remains lightweight.

    This enforces AC-WS-007 by ensuring the primary quick workflow job avoids
    matrix expansion that would violate lightweight CI intent.

    """
    workflow = _load_ci_workflow()
    jobs = workflow.get("jobs", {})
    assert isinstance(jobs, dict), "ci.yml must define a jobs mapping"

    quick_job = jobs.get("quick", {})
    assert isinstance(quick_job, dict), "ci.yml must define jobs.quick as a mapping"
    assert "strategy" not in quick_job, "ci.yml jobs.quick must remain non-matrix for lightweight CI"


def test_ci_contains_single_benchmark_smoke_command() -> None:
    """Assert CI includes one benchmark smoke command for stats_baseline.

    This enforces AC-WS-004 and AC-WS-007 at contract level by requiring a
    single benchmark smoke command marker in CI configuration.

    """
    workflow = _load_ci_workflow()
    commands = _iter_run_commands(workflow)

    target_command = "cargo bench --bench stats_baseline -- --noplot"
    matches = [command for command in commands if target_command in command]
    assert len(matches) == 1, (
        f"ci.yml must include exactly one benchmark smoke command for stats_baseline: {target_command}"
    )


def test_ci_benchmark_smoke_command_keeps_rust_core_execution_context() -> None:
    """Assert benchmark smoke step still executes in rust_core context.

    This enforces AC-WS-004 and AC-WS-007 by requiring either a working
    directory declaration or explicit pushd/cd command into rust_core.

    """
    workflow = _load_ci_workflow()
    jobs = workflow.get("jobs", {})
    assert isinstance(jobs, dict), "ci.yml must define jobs as a mapping"

    matching_steps: list[dict[str, Any]] = []
    for job_data in jobs.values():
        if not isinstance(job_data, dict):
            continue
        steps = job_data.get("steps", [])
        if not isinstance(steps, list):
            continue
        for step in steps:
            if not isinstance(step, dict):
                continue
            run_value = step.get("run")
            if isinstance(run_value, str) and "cargo bench --bench stats_baseline -- --noplot" in run_value:
                matching_steps.append(step)

    assert len(matching_steps) == 1, "ci.yml must contain exactly one stats_baseline benchmark smoke step"
    benchmark_step = matching_steps[0]

    run_text = benchmark_step.get("run", "")
    assert isinstance(run_text, str), "benchmark smoke step run must be a string"

    has_working_dir = benchmark_step.get("working-directory") == "rust_core"
    has_inline_cd = "pushd rust_core" in run_text or "cd rust_core" in run_text
    assert has_working_dir or has_inline_cd, (
        "benchmark smoke step must run in rust_core context via working-directory or pushd/cd rust_core"
    )
