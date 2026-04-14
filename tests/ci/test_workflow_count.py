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
"""Tests that validate the workflow count and security-scheduled.yml structure.

Acceptance criteria:
- Exactly 2 workflow files: ci.yml and security-scheduled.yml
- security-scheduled.yml is valid YAML with jobs.dependency-audit and jobs.codeql-scan
- security-scheduled.yml runs pip-audit and CodeQL scans
- security-scheduled.yml triggers on schedule and workflow_dispatch
"""

from pathlib import Path

import yaml

_WORKFLOWS_DIR = Path(".github/workflows")
_SECURITY_YML = _WORKFLOWS_DIR / "security-scheduled.yml"
_CI_YML = _WORKFLOWS_DIR / "ci.yml"


def _load_security_yml() -> dict:
    """Load and return security.yml as a parsed mapping.

    Returns:
        dict: Parsed YAML mapping for .github/workflows/security.yml.

    """
    with _SECURITY_YML.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# T1-a: Exactly 2 workflow files
# ---------------------------------------------------------------------------


def test_exactly_two_workflow_files() -> None:
    """Only ci.yml and security-scheduled.yml must exist in .github/workflows/."""
    yml_files = sorted(f.name for f in _WORKFLOWS_DIR.glob("*.yml"))
    assert yml_files == ["ci.yml", "security-scheduled.yml"], (
        f"Expected exactly ['ci.yml', 'security-scheduled.yml'], got {yml_files}. "
        "Delete redundant workflow files or add missing ones."
    )


# ---------------------------------------------------------------------------
# T1-b: security.yml is valid YAML with jobs.security_smoke
# ---------------------------------------------------------------------------


def test_security_yml_exists_and_has_analyze_job() -> None:
    """security-scheduled.yml must exist and contain dependency-audit and codeql-scan jobs."""
    assert _SECURITY_YML.exists(), "security-scheduled.yml does not exist"
    data = _load_security_yml()
    assert "jobs" in data, "security-scheduled.yml must have a 'jobs' key"
    assert "dependency-audit" in data["jobs"], "security-scheduled.yml must have a 'jobs.dependency-audit' key"
    assert "codeql-scan" in data["jobs"], "security-scheduled.yml must have a 'jobs.codeql-scan' key"


# ---------------------------------------------------------------------------
# T1-c: security.yml declares minimal read permissions
# ---------------------------------------------------------------------------


def test_security_yml_has_security_events_write_permission() -> None:
    """security-scheduled.yml should keep minimal permissions for security scans."""
    data = _load_security_yml()
    perms = data.get("permissions", {})
    assert perms.get("contents") == "read", "security-scheduled.yml must keep 'permissions.contents: read'"
    assert perms.get("security-events") == "write", (
        "security-scheduled.yml must have 'permissions.security-events: write'"
    )


# ---------------------------------------------------------------------------
# T1-d: security.yml runs secret scan command
# ---------------------------------------------------------------------------


def test_security_yml_runs_secret_scan_guardrail() -> None:
    """security-scheduled.yml must run dependency audit and CodeQL scans."""
    data = _load_security_yml()
    # Check dependency-audit job
    audit_steps = data["jobs"]["dependency-audit"]["steps"]
    audit_runs = [step.get("run", "") for step in audit_steps]
    assert any("pip-audit" in command for command in audit_runs), (
        "security-scheduled.yml must include pip-audit command."
    )
    # Check codeql-scan job
    codeql_steps = data["jobs"]["codeql-scan"]["steps"]
    assert len(codeql_steps) > 0, "security-scheduled.yml codeql-scan must have steps"


# ---------------------------------------------------------------------------
# T1-e: security.yml triggers on push and pull_request to main
# ---------------------------------------------------------------------------


def test_security_yml_has_schedule_trigger() -> None:
    """security-scheduled.yml must trigger on schedule and workflow_dispatch."""
    data = _load_security_yml()
    on_block = data.get("on", data.get(True, {}))  # YAML 'on' parses as True in some versions
    assert isinstance(on_block, dict), "security-scheduled.yml must define an 'on' trigger mapping"
    assert "schedule" in on_block, "security-scheduled.yml must include schedule trigger"
    assert "workflow_dispatch" in on_block, "security-scheduled.yml must include workflow_dispatch trigger"


# ---------------------------------------------------------------------------
# T1-f: security.yml avoids CodeQL matrix in lightweight mode
# ---------------------------------------------------------------------------


def test_security_yml_references_custom_python_queries() -> None:
    """security-scheduled.yml should include CodeQL for scheduled security scanning."""
    content = _SECURITY_YML.read_text(encoding="utf-8")
    assert "codeql-action" in content, "security-scheduled.yml should include codeql-action for scheduled scans"
    assert "python" in content, "security-scheduled.yml should scan Python language"
