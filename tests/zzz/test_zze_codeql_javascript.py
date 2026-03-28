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
"""CodeQL meta-test: validates JavaScript database is fresh and analysis is clean.

Set CODEQL_SKIP=1 to bypass entirely.
Set CODEQL_REBUILD=1 to force a database rebuild even when the SARIF is fresh.
"""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def _resolve_codeql_exe() -> Path:
    """Resolve CodeQL CLI path: CODEQL_EXE env var → PATH → repo-local fallback."""
    from_env = os.environ.get("CODEQL_EXE")
    if from_env:
        return Path(from_env)
    on_path = shutil.which("codeql")
    if on_path:
        return Path(on_path)
    return REPO_ROOT / "codeql" / "codeql.exe"


CODEQL_EXE = _resolve_codeql_exe()
DB_PATH = REPO_ROOT / "databases" / "javascript-db"
SARIF_PATH = REPO_ROOT / "results" / "javascript.sarif"
SOURCE_ROOT = REPO_ROOT / "web"
MAX_SARIF_AGE_HOURS = 24


def _codeql_available() -> bool:
    return CODEQL_EXE.exists()


def _sarif_age_hours() -> float | None:
    if not SARIF_PATH.exists():
        return None
    import time
    return (time.time() - SARIF_PATH.stat().st_mtime) / 3600


def _rebuild_db() -> None:
    subprocess.run(
        [
            str(CODEQL_EXE),
            "database", "create", str(DB_PATH),
            "--language=javascript",
            f"--source-root={SOURCE_ROOT}",
            "--overwrite",
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def _run_analysis() -> None:
    SARIF_PATH.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            str(CODEQL_EXE),
            "database", "analyze", str(DB_PATH),
            "codeql/javascript-queries:codeql-suites/javascript-security-and-quality.qls",
            "--format=sarif-latest",
            f"--output={SARIF_PATH}",
            "--threads=2",
        ],
        check=True,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )


def test_javascript_sarif_is_fresh_or_rebuilt() -> None:
    """JavaScript SARIF must exist and be < 24h old, or be rebuilt now."""
    if os.environ.get("CODEQL_SKIP"):
        pytest.skip("CODEQL_SKIP is set")
    if not _codeql_available():
        pytest.skip("CodeQL CLI not available")

    force_rebuild = bool(os.environ.get("CODEQL_REBUILD"))
    age = _sarif_age_hours()

    if force_rebuild or age is None or age > MAX_SARIF_AGE_HOURS:
        reason = "CODEQL_REBUILD set" if force_rebuild else (
            "SARIF missing" if age is None else f"SARIF is {age:.1f}h old (>{MAX_SARIF_AGE_HOURS}h)"
        )
        print(f"\nRebuilding JavaScript CodeQL database: {reason}")
        try:
            _rebuild_db()
            _run_analysis()
        except subprocess.CalledProcessError as exc:
            pytest.fail(f"CodeQL JavaScript build/analysis failed:\n{exc.stderr}")

    assert SARIF_PATH.exists(), "JavaScript SARIF was not produced"
    age_after = _sarif_age_hours()
    assert age_after is not None and age_after <= MAX_SARIF_AGE_HOURS, (
        f"JavaScript SARIF is {age_after:.1f}h old — run with CODEQL_REBUILD=1 to refresh"
    )


def test_javascript_sarif_execution_succeeded() -> None:
    """The JavaScript analysis run must have completed without errors."""
    if os.environ.get("CODEQL_SKIP"):
        pytest.skip("CODEQL_SKIP is set")
    if not SARIF_PATH.exists():
        pytest.skip("JavaScript SARIF not found")

    sarif = json.loads(SARIF_PATH.read_text(encoding="utf-8"))
    run = sarif["runs"][0]
    invocations = run.get("invocations", [])
    assert invocations, "No invocation metadata in JavaScript SARIF"
    assert invocations[0].get("executionSuccessful") is True, (
        "JavaScript CodeQL analysis did not complete successfully"
    )


def test_javascript_sarif_scanned_files() -> None:
    """JavaScript SARIF must reference at least one artifact."""
    if os.environ.get("CODEQL_SKIP"):
        pytest.skip("CODEQL_SKIP is set")
    if not SARIF_PATH.exists():
        pytest.skip("JavaScript SARIF not found")

    sarif = json.loads(SARIF_PATH.read_text(encoding="utf-8"))
    artifacts = sarif["runs"][0].get("artifacts", [])
    assert len(artifacts) > 0, "JavaScript SARIF contains no scanned artifacts"


def test_javascript_no_new_security_findings() -> None:
    """No HIGH/CRITICAL security findings in JavaScript."""
    if os.environ.get("CODEQL_SKIP"):
        pytest.skip("CODEQL_SKIP is set")
    if not SARIF_PATH.exists():
        pytest.skip("JavaScript SARIF not found")

    _security_rule_prefixes = (
        "js/sql-injection",
        "js/code-injection",
        "js/path-injection",
        "js/command-injection",
        "js/reflected-xss",
        "js/stored-xss",
        "js/xxe",
        "js/server-side-request-forgery",
        "js/clear-text-logging",
        "js/clear-text-storage",
        "js/weak-cryptographic-algorithm",
        "js/hardcoded-credentials",
        "js/prototype-pollution",
        "js/request-forgery",
    )

    sarif = json.loads(SARIF_PATH.read_text(encoding="utf-8"))
    results = sarif["runs"][0].get("results", [])
    security_findings = [
        r for r in results
        if any(r.get("ruleId", "").startswith(p) for p in _security_rule_prefixes)
    ]
    if security_findings:
        details = "\n".join(
            f"  {r['ruleId']} @ {r['locations'][0]['physicalLocation']['artifactLocation']['uri']}"
            f":{r['locations'][0]['physicalLocation']['region']['startLine']}"
            for r in security_findings
        )
        pytest.fail(f"JavaScript security findings detected:\n{details}")
