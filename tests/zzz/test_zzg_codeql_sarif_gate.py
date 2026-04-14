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
"""CodeQL SARIF security gate: validates combined findings across all three languages.

This is the final enforcement gate – it checks that:
- All three SARIF files exist and are fresh (< 24h)
- No HIGH or CRITICAL security findings exist in any language
- No regressions vs the committed baseline finding count

Set CODEQL_SKIP=1 to bypass entirely.
"""

import json
import os
import shutil
import time
from pathlib import Path
from typing import NamedTuple

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "results"
MAX_SARIF_AGE_HOURS = 24


class _SarifSpec(NamedTuple):
    lang: str
    path: Path
    # Maximum number of total findings allowed (including known quality issues).
    # Increase this number only when a deliberate new finding is accepted.
    max_total_findings: int


_SARIF_SPECS: list[_SarifSpec] = [
    _SarifSpec("python", RESULTS_DIR / "python.sarif", 20),
    _SarifSpec("javascript", RESULTS_DIR / "javascript.sarif", 10),
    _SarifSpec("rust", RESULTS_DIR / "rust.sarif", 0),
]

# Rule IDs whose presence constitutes a hard security failure regardless of count.
# These map to OWASP Top 10 / CWE high-severity categories.
_hard_fail_rule_prefixes = (
    "py/sql-injection",
    "js/sql-injection",
    "rust/sql-injection",
    "py/code-injection",
    "js/code-injection",
    "py/path-injection",
    "js/path-injection",
    "rust/path-injection",
    "py/command-injection",
    "js/command-injection",
    "rust/command-injection",
    "py/reflective-xss",
    "js/reflected-xss",
    "rust/reflected-xss",
    "py/xxe",
    "js/xxe",
    "py/ssrf",
    "js/server-side-request-forgery",
    "py/clear-text-logging",
    "js/clear-text-logging",
    "rust/clear-text-logging",
    "py/clear-text-storage",
    "js/clear-text-storage",
    "rust/clear-text-storage",
    "py/weak-crypto",
    "js/weak-cryptographic-algorithm",
    "rust/weak-cryptographic-algorithm",
    "py/hardcoded-credentials",
    "js/hardcoded-credentials",
    "rust/hardcoded-credentials",
    "js/prototype-pollution",
    "js/request-forgery",
    "rust/disabled-certificate-check",
    "rust/cleartext-transmission",
    "rust/use-of-http",
)


def _codeql_available() -> bool:
    """Return whether CodeQL CLI is available in this environment."""
    if os.environ.get("CODEQL_EXE"):
        return Path(os.environ["CODEQL_EXE"]).exists()
    on_path = shutil.which("codeql")
    if on_path:
        return True
    return (REPO_ROOT / "codeql" / "codeql.exe").exists()


def test_all_sarif_files_exist() -> None:
    """All three SARIF result files must exist."""
    if os.environ.get("CODEQL_SKIP"):
        pytest.skip("CODEQL_SKIP is set")

    missing = [str(s.path) for s in _SARIF_SPECS if not s.path.exists()]
    assert not missing, "Missing SARIF files (run tests/zzz/test_zzd/e/f to generate them):\n" + "\n".join(
        f"  {p}" for p in missing
    )


def test_all_sarif_files_are_fresh() -> None:
    """All SARIF files must be < 24h old."""
    if os.environ.get("CODEQL_SKIP"):
        pytest.skip("CODEQL_SKIP is set")
    if not _codeql_available():
        pytest.skip("CodeQL CLI not available")

    stale = []
    for spec in _SARIF_SPECS:
        if not spec.path.exists():
            stale.append(f"{spec.lang}: missing")
            continue
        age = (time.time() - spec.path.stat().st_mtime) / 3600
        if age > MAX_SARIF_AGE_HOURS:
            stale.append(f"{spec.lang}: {age:.1f}h old (>{MAX_SARIF_AGE_HOURS}h)")

    assert not stale, "Stale SARIF files detected — run with CODEQL_REBUILD=1 to refresh:\n" + "\n".join(
        f"  {s}" for s in stale
    )


def test_all_analyses_completed_successfully() -> None:
    """All three CodeQL runs must have executionSuccessful=True."""
    if os.environ.get("CODEQL_SKIP"):
        pytest.skip("CODEQL_SKIP is set")

    failures = []
    for spec in _SARIF_SPECS:
        if not spec.path.exists():
            continue
        sarif = json.loads(spec.path.read_text(encoding="utf-8"))
        invocations = sarif["runs"][0].get("invocations", [])
        if not invocations or not invocations[0].get("executionSuccessful"):
            failures.append(spec.lang)

    assert not failures, f"CodeQL runs did not complete successfully: {failures}"


def test_no_hard_fail_security_findings() -> None:
    """Zero tolerance for OWASP Top 10 / high-severity CWE findings in any language."""
    if os.environ.get("CODEQL_SKIP"):
        pytest.skip("CODEQL_SKIP is set")

    all_security: list[str] = []
    for spec in _SARIF_SPECS:
        if not spec.path.exists():
            continue
        sarif = json.loads(spec.path.read_text(encoding="utf-8"))
        for r in sarif["runs"][0].get("results", []):
            rule_id = r.get("ruleId", "")
            if any(rule_id.startswith(p) for p in _hard_fail_rule_prefixes):
                loc = r["locations"][0]["physicalLocation"]
                uri = loc["artifactLocation"]["uri"]
                line = loc["region"]["startLine"]
                all_security.append(f"  [{spec.lang}] {rule_id} @ {uri}:{line}")

    assert not all_security, "Security findings require immediate remediation:\n" + "\n".join(all_security)


def test_finding_count_within_baseline() -> None:
    """Total findings per language must not exceed the committed baseline maximum."""
    if os.environ.get("CODEQL_SKIP"):
        pytest.skip("CODEQL_SKIP is set")

    regressions: list[str] = []
    for spec in _SARIF_SPECS:
        if not spec.path.exists():
            continue
        sarif = json.loads(spec.path.read_text(encoding="utf-8"))
        count = len(sarif["runs"][0].get("results", []))
        if count > spec.max_total_findings:
            regressions.append(f"  {spec.lang}: {count} findings > baseline {spec.max_total_findings}")

    assert not regressions, (
        "Finding count regressions detected (update max_total_findings in test_zzg if intentional):\n"
        + "\n".join(regressions)
    )
