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
"""Tests that validate the lightweight workflow count and security.yml structure.

Acceptance criteria:
- Exactly 2 workflow files: ci.yml and security.yml
- security.yml is valid YAML with jobs.security_smoke
- security.yml runs secret scan guardrail
- security.yml triggers on push/PR to main
"""

from pathlib import Path

import yaml

_WORKFLOWS_DIR = Path(".github/workflows")
_SECURITY_YML = _WORKFLOWS_DIR / "security.yml"
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
    """Only ci.yml and security.yml must exist in .github/workflows/."""
    yml_files = sorted(f.name for f in _WORKFLOWS_DIR.glob("*.yml"))
    assert yml_files == ["ci.yml", "security.yml"], (
        f"Expected exactly ['ci.yml', 'security.yml'], got {yml_files}. "
        "Delete redundant workflow files or add missing ones."
    )


# ---------------------------------------------------------------------------
# T1-b: security.yml is valid YAML with jobs.security_smoke
# ---------------------------------------------------------------------------


def test_security_yml_exists_and_has_analyze_job() -> None:
    """security.yml must exist and contain a jobs.security_smoke entry."""
    assert _SECURITY_YML.exists(), "security.yml does not exist"
    data = _load_security_yml()
    assert "jobs" in data, "security.yml must have a 'jobs' key"
    assert "security_smoke" in data["jobs"], "security.yml must have a 'jobs.security_smoke' key"


# ---------------------------------------------------------------------------
# T1-c: security.yml declares minimal read permissions
# ---------------------------------------------------------------------------


def test_security_yml_has_security_events_write_permission() -> None:
    """security.yml should keep minimal permissions for lightweight scans."""
    data = _load_security_yml()
    perms = data.get("permissions", {})
    assert perms.get("contents") == "read", "security.yml must keep 'permissions.contents: read'"


# ---------------------------------------------------------------------------
# T1-d: security.yml runs secret scan command
# ---------------------------------------------------------------------------


def test_security_yml_runs_secret_scan_guardrail() -> None:
    """security.yml must run the repository secret-scan guardrail command."""
    data = _load_security_yml()
    steps = data["jobs"]["security_smoke"]["steps"]
    run_values = [step.get("run", "") for step in steps]
    assert any("python scripts/security/run_secret_scan.py" in command for command in run_values), (
        "security.yml must include secret scan guardrail command."
    )


# ---------------------------------------------------------------------------
# T1-e: security.yml triggers on push and pull_request to main
# ---------------------------------------------------------------------------


def test_security_yml_has_schedule_trigger() -> None:
    """security.yml must trigger on push/pull_request to main."""
    data = _load_security_yml()
    on_block = data.get("on", data.get(True, {}))  # YAML 'on' parses as True in some versions
    assert isinstance(on_block, dict), "security.yml must define an 'on' trigger mapping"
    assert "push" in on_block, "security.yml must include push trigger"
    assert "pull_request" in on_block, "security.yml must include pull_request trigger"
    push_branches = on_block.get("push", {}).get("branches", [])
    pr_branches = on_block.get("pull_request", {}).get("branches", [])
    assert "main" in push_branches, "security.yml push trigger must include main"
    assert "main" in pr_branches, "security.yml pull_request trigger must include main"


# ---------------------------------------------------------------------------
# T1-f: security.yml avoids CodeQL matrix in lightweight mode
# ---------------------------------------------------------------------------


def test_security_yml_references_custom_python_queries() -> None:
    """security.yml should not include CodeQL steps in lightweight mode."""
    content = _SECURITY_YML.read_text(encoding="utf-8")
    assert "codeql-action" not in content, "security.yml should not include codeql-action in lightweight mode"
