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
"""TDD red-phase tests for security scheduled workflow contracts."""

import os
from typing import Any

import yaml

WORKFLOW_PATH = ".github/workflows/security-scheduled.yml"


def _load_security_workflow() -> dict[str, Any]:
    """Load and parse the security scheduled workflow YAML file."""
    with open(WORKFLOW_PATH, encoding="utf-8") as workflow_file:
        data = yaml.safe_load(workflow_file)
    return data if isinstance(data, dict) else {}


def _on_block(workflow: dict[str, Any]) -> dict[str, Any]:
    """Normalize the workflow trigger block from parsed YAML."""
    trigger_block = workflow.get("on", workflow.get(True, {}))
    return trigger_block if isinstance(trigger_block, dict) else {}


def _codeql_init_step(codeql_job: dict[str, Any]) -> dict[str, Any]:
    """Return the CodeQL init step from the codeql-scan job."""
    steps = codeql_job.get("steps", [])
    assert isinstance(steps, list), "codeql-scan.steps must be a list"

    init_step = next(
        (
            step
            for step in steps
            if isinstance(step, dict)
            and isinstance(step.get("uses"), str)
            and step["uses"].startswith("github/codeql-action/init")
        ),
        None,
    )
    assert init_step is not None, "codeql-scan must include a CodeQL init step"
    return init_step


def test_security_workflow_exists() -> None:
    """Security scheduled workflow file must exist (AC-SEC-001)."""
    assert os.path.isfile(WORKFLOW_PATH)


def test_security_workflow_trigger_is_schedule_and_dispatch_only() -> None:
    """Security workflow trigger contract must be schedule + dispatch only (AC-SEC-001)."""
    workflow = _load_security_workflow()
    on_block = _on_block(workflow)

    assert "schedule" in on_block, "security workflow must define an 'on.schedule' trigger"
    schedule = on_block.get("schedule", [])
    assert isinstance(schedule, list) and schedule, "security workflow schedule must include at least one cron entry"
    assert any(isinstance(entry, dict) and entry.get("cron") for entry in schedule), (
        "security workflow schedule must include a cron expression"
    )
    assert "workflow_dispatch" in on_block, "security workflow must define workflow_dispatch trigger"
    assert "pull_request" not in on_block, "security workflow must not define a pull_request trigger"


def test_security_workflow_permissions_least_privilege() -> None:
    """Security workflow must declare minimum permissions (AC-SEC-002)."""
    workflow = _load_security_workflow()
    permissions = workflow.get("permissions", {})

    assert isinstance(permissions, dict), "security workflow permissions must be a mapping"
    assert permissions.get("contents") == "read", "security workflow permissions.contents must be 'read'"
    assert permissions.get("security-events") == "write", (
        "security workflow permissions.security-events must be 'write'"
    )


def test_security_workflow_has_dependency_audit_job() -> None:
    """Security workflow must define dependency-audit job (AC-SEC-003)."""
    workflow = _load_security_workflow()
    jobs = workflow.get("jobs", {})

    assert isinstance(jobs, dict), "security workflow jobs must be a mapping"
    assert "dependency-audit" in jobs, "security workflow must define jobs.dependency-audit"


def test_security_workflow_has_codeql_scan_job() -> None:
    """Security workflow must define codeql-scan job (AC-SEC-003)."""
    workflow = _load_security_workflow()
    jobs = workflow.get("jobs", {})

    assert isinstance(jobs, dict), "security workflow jobs must be a mapping"
    assert "codeql-scan" in jobs, "security workflow must define jobs.codeql-scan"


def test_security_workflow_codeql_language_python_only() -> None:
    """CodeQL configuration must set python as the only language (AC-SEC-003)."""
    workflow = _load_security_workflow()
    codeql_job = workflow.get("jobs", {}).get("codeql-scan", {})
    assert isinstance(codeql_job, dict), "security workflow jobs.codeql-scan must be a mapping"

    init_step = _codeql_init_step(codeql_job)
    with_block = init_step.get("with", {})
    assert isinstance(with_block, dict), "CodeQL init step must provide a with mapping"

    languages = with_block.get("languages")
    assert isinstance(languages, str), "CodeQL init step languages must be a string"
    assert languages.strip() == "python", "CodeQL init languages must be exactly 'python'"


def test_security_workflow_codeql_references_custom_queries() -> None:
    """CodeQL configuration must reference the python custom query pack (AC-SEC-003)."""
    workflow = _load_security_workflow()
    codeql_job = workflow.get("jobs", {}).get("codeql-scan", {})
    assert isinstance(codeql_job, dict), "security workflow jobs.codeql-scan must be a mapping"

    init_step = _codeql_init_step(codeql_job)
    with_block = init_step.get("with", {})
    assert isinstance(with_block, dict), "CodeQL init step must provide a with mapping"

    queries_value = with_block.get("queries", "")
    config_value = with_block.get("config", "")
    references = [value for value in [queries_value, config_value] if isinstance(value, str)]
    assert any("codeql-custom-queries-python" in value for value in references), (
        "CodeQL init must reference codeql/codeql-custom-queries-python/ via queries or config"
    )
