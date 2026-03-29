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
"""Tests that verify pytest-cov / coverage configuration is present."""
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

PYPROJECT = Path(__file__).parent.parent / "pyproject.toml"


def _load_pyproject_toml() -> dict[str, Any]:
    """Load pyproject.toml as a parsed TOML document.

    Returns:
        Parsed TOML document as a nested dictionary.

    """
    return tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))


def test_pyproject_has_coverage_run_section() -> None:
    """Verify pyproject.toml declares the coverage run section.

    Returns:
        None.

    """
    content = PYPROJECT.read_text(encoding="utf-8")
    assert "[tool.coverage.run]" in content


def test_coverage_run_has_source() -> None:
    """Verify coverage run config tracks the src package.

    Returns:
        None.

    """
    content = PYPROJECT.read_text(encoding="utf-8")
    assert 'source = ["src"]' in content


def test_pyproject_has_coverage_report_section() -> None:
    """Verify pyproject.toml declares the coverage report section.

    Returns:
        None.

    """
    content = PYPROJECT.read_text(encoding="utf-8")
    assert "[tool.coverage.report]" in content


def test_coverage_report_fail_under_is_present() -> None:
    """Verify coverage.report includes a fail_under threshold.

    Returns:
        None.

    """
    pyproject = _load_pyproject_toml()
    report_cfg = pyproject.get("tool", {}).get("coverage", {}).get("report", {})
    assert "fail_under" in report_cfg, "[tool.coverage.report].fail_under must be defined"


def test_coverage_report_fail_under_stage1_minimum() -> None:
    """Verify stage-1 coverage minimum enforces fail_under >= 40.

    Returns:
        None.

    """
    pyproject = _load_pyproject_toml()
    fail_under = pyproject.get("tool", {}).get("coverage", {}).get("report", {}).get("fail_under")
    assert isinstance(fail_under, int), "[tool.coverage.report].fail_under must be an integer"
    assert fail_under >= 40, (
        "Stage-1 coverage ratchet requires [tool.coverage.report].fail_under >= 40"
    )


def test_pytest_cov_importable() -> None:
    """Verify pytest-cov is installed in the active environment.

    Returns:
        None.

    """
    result = subprocess.run(
        [sys.executable, "-c", "import pytest_cov; print(pytest_cov.__version__)"],
        capture_output=True, text=True, timeout=10
    )
    assert result.returncode == 0, f"pytest-cov not importable: {result.stderr}"


def test_coverage_branch_enabled() -> None:
    """Verify branch coverage is enabled.

    Returns:
        None.

    """
    content = PYPROJECT.read_text(encoding="utf-8")
    assert "branch = true" in content
