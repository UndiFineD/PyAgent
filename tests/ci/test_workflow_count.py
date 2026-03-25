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
"""Tests that validate the CI workflow count and security.yml structure (prj0000075).

Acceptance criteria:
- Exactly 2 workflow files: ci.yml and security.yml
- security.yml is valid YAML with jobs.analyze
- security.yml declares security-events: write permission
- security.yml uses github/codeql-action (init, autobuild, analyze)
- security.yml triggers on push/PR to main and on a schedule
"""

from pathlib import Path

import yaml

_WORKFLOWS_DIR = Path(".github/workflows")
_SECURITY_YML = _WORKFLOWS_DIR / "security.yml"
_CI_YML = _WORKFLOWS_DIR / "ci.yml"


def _load_security_yml() -> dict:
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
# T1-b: security.yml is valid YAML with jobs.analyze
# ---------------------------------------------------------------------------

def test_security_yml_exists_and_has_analyze_job() -> None:
    """security.yml must exist and contain a jobs.analyze entry."""
    assert _SECURITY_YML.exists(), "security.yml does not exist"
    data = _load_security_yml()
    assert "jobs" in data, "security.yml must have a 'jobs' key"
    assert "analyze" in data["jobs"], "security.yml must have a 'jobs.analyze' key"


# ---------------------------------------------------------------------------
# T1-c: security.yml declares security-events: write
# ---------------------------------------------------------------------------

def test_security_yml_has_security_events_write_permission() -> None:
    """security.yml must declare security-events: write for SARIF upload."""
    data = _load_security_yml()
    perms = data.get("permissions", {})
    assert perms.get("security-events") == "write", (
        "security.yml must declare 'permissions.security-events: write' "
        "so that CodeQL SARIF results can be uploaded to the Security tab."
    )


# ---------------------------------------------------------------------------
# T1-d: security.yml uses all three codeql-action steps
# ---------------------------------------------------------------------------

def test_security_yml_uses_codeql_action_steps() -> None:
    """security.yml must use codeql-action init, autobuild, and analyze steps."""
    data = _load_security_yml()
    steps = data["jobs"]["analyze"]["steps"]
    uses_values = [step.get("uses", "") for step in steps]

    assert any("codeql-action/init" in u for u in uses_values), (
        "security.yml must include a 'github/codeql-action/init' step"
    )
    assert any("codeql-action/autobuild" in u for u in uses_values), (
        "security.yml must include a 'github/codeql-action/autobuild' step"
    )
    assert any("codeql-action/analyze" in u for u in uses_values), (
        "security.yml must include a 'github/codeql-action/analyze' step"
    )


# ---------------------------------------------------------------------------
# T1-e: security.yml triggers include schedule
# ---------------------------------------------------------------------------

def test_security_yml_has_schedule_trigger() -> None:
    """security.yml must include a scheduled trigger for regular background scans."""
    data = _load_security_yml()
    on_block = data.get("on", data.get(True, {}))  # YAML 'on' parses as True in some versions
    # Accept either 'on' key (string) or boolean True (PyYAML quirk)
    if isinstance(on_block, dict):
        assert "schedule" in on_block, (
            "security.yml must have a 'schedule' trigger for weekly background CodeQL scans"
        )
    else:
        # Try direct key lookup
        triggers = data.get("on") or data.get(True)
        assert triggers is not None and "schedule" in triggers, (
            "security.yml must have a 'schedule' trigger"
        )


# ---------------------------------------------------------------------------
# T1-f: security.yml wires in custom Python query pack
# ---------------------------------------------------------------------------

def test_security_yml_references_custom_python_queries() -> None:
    """security.yml config must reference the local codeql-custom-queries-python pack."""
    content = _SECURITY_YML.read_text(encoding="utf-8")
    assert "codeql-custom-queries-python" in content, (
        "security.yml must reference the custom Python query pack "
        "('./codeql/codeql-custom-queries-python') so that local eval/shell-injection "
        "queries run during CodeQL analysis."
    )
