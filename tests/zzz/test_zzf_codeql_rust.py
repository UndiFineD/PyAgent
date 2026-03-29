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
"""CodeQL meta-test: validates Rust database is fresh and analysis is clean.

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
DB_PATH = REPO_ROOT / "databases" / "rust-db"
SARIF_PATH = REPO_ROOT / "results" / "rust.sarif"
SOURCE_ROOT = REPO_ROOT / "rust_core"
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
            "database",
            "create",
            str(DB_PATH),
            "--language=rust",
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
            "database",
            "analyze",
            str(DB_PATH),
            "codeql/rust-queries:codeql-suites/rust-security-and-quality.qls",
            "--format=sarif-latest",
            f"--output={SARIF_PATH}",
            "--threads=2",
            "--ram=4096",
        ],
        check=True,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )


def test_rust_sarif_is_fresh_or_rebuilt() -> None:
    """Rust SARIF must exist and be < 24h old, or be rebuilt now."""
    if os.environ.get("CODEQL_SKIP"):
        pytest.skip("CODEQL_SKIP is set")
    if not _codeql_available():
        pytest.skip("CodeQL CLI not available")

    force_rebuild = bool(os.environ.get("CODEQL_REBUILD"))
    age = _sarif_age_hours()

    if force_rebuild or age is None or age > MAX_SARIF_AGE_HOURS:
        reason = (
            "CODEQL_REBUILD set"
            if force_rebuild
            else ("SARIF missing" if age is None else f"SARIF is {age:.1f}h old (>{MAX_SARIF_AGE_HOURS}h)")
        )
        print(f"\nRebuilding Rust CodeQL database: {reason}")
        try:
            _rebuild_db()
            _run_analysis()
        except subprocess.CalledProcessError as exc:
            pytest.fail(f"CodeQL Rust build/analysis failed:\n{exc.stderr}")

    assert SARIF_PATH.exists(), "Rust SARIF was not produced"
    age_after = _sarif_age_hours()
    assert age_after is not None and age_after <= MAX_SARIF_AGE_HOURS, (
        f"Rust SARIF is {age_after:.1f}h old — run with CODEQL_REBUILD=1 to refresh"
    )


def test_rust_sarif_execution_succeeded() -> None:
    """The Rust analysis run must have completed without errors."""
    if os.environ.get("CODEQL_SKIP"):
        pytest.skip("CODEQL_SKIP is set")
    if not SARIF_PATH.exists():
        pytest.skip("Rust SARIF not found")

    sarif = json.loads(SARIF_PATH.read_text(encoding="utf-8"))
    run = sarif["runs"][0]
    invocations = run.get("invocations", [])
    assert invocations, "No invocation metadata in Rust SARIF"
    assert invocations[0].get("executionSuccessful") is True, "Rust CodeQL analysis did not complete successfully"


def test_rust_sarif_scanned_files() -> None:
    """Rust SARIF must reference at least one artifact."""
    if os.environ.get("CODEQL_SKIP"):
        pytest.skip("CODEQL_SKIP is set")
    if not SARIF_PATH.exists():
        pytest.skip("Rust SARIF not found")

    sarif = json.loads(SARIF_PATH.read_text(encoding="utf-8"))
    artifacts = sarif["runs"][0].get("artifacts", [])
    assert len(artifacts) > 0, "Rust SARIF contains no scanned artifacts"


def test_rust_no_security_findings() -> None:
    """No security findings of any kind in Rust (higher bar than other langs)."""
    if os.environ.get("CODEQL_SKIP"):
        pytest.skip("CODEQL_SKIP is set")
    if not SARIF_PATH.exists():
        pytest.skip("Rust SARIF not found")

    _security_rule_prefixes = (
        "rust/sql-injection",
        "rust/path-injection",
        "rust/command-injection",
        "rust/reflected-xss",
        "rust/clear-text-logging",
        "rust/clear-text-storage",
        "rust/weak-cryptographic-algorithm",
        "rust/hardcoded-credentials",
        "rust/use-of-http",
        "rust/cleartext-transmission",
        "rust/disabled-certificate-check",
    )

    sarif = json.loads(SARIF_PATH.read_text(encoding="utf-8"))
    results = sarif["runs"][0].get("results", [])
    security_findings = [r for r in results if any(r.get("ruleId", "").startswith(p) for p in _security_rule_prefixes)]
    if security_findings:
        details = "\n".join(
            f"  {r['ruleId']} @ {r['locations'][0]['physicalLocation']['artifactLocation']['uri']}"
            f":{r['locations'][0]['physicalLocation']['region']['startLine']}"
            for r in security_findings
        )
        pytest.fail(f"Rust security findings detected:\n{details}")
