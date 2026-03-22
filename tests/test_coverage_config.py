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
from pathlib import Path

PYPROJECT = Path(__file__).parent.parent / "pyproject.toml"


def test_pyproject_has_coverage_run_section():
    """pyproject.toml must declare [tool.coverage.run]."""
    content = PYPROJECT.read_text(encoding="utf-8")
    assert "[tool.coverage.run]" in content


def test_coverage_run_has_source():
    """coverage.run must set source = [\"src\"]."""
    content = PYPROJECT.read_text(encoding="utf-8")
    assert 'source = ["src"]' in content


def test_pyproject_has_coverage_report_section():
    """pyproject.toml must declare [tool.coverage.report]."""
    content = PYPROJECT.read_text(encoding="utf-8")
    assert "[tool.coverage.report]" in content


def test_coverage_report_fail_under_set():
    """coverage.report must have a fail_under threshold."""
    content = PYPROJECT.read_text(encoding="utf-8")
    assert "fail_under" in content


def test_pytest_cov_importable():
    """pytest-cov must be installed in the venv."""
    result = subprocess.run(
        [sys.executable, "-c", "import pytest_cov; print(pytest_cov.__version__)"],
        capture_output=True, text=True, timeout=10
    )
    assert result.returncode == 0, f"pytest-cov not importable: {result.stderr}"


def test_coverage_branch_enabled():
    """branch coverage must be enabled for richer analysis."""
    content = PYPROJECT.read_text(encoding="utf-8")
    assert "branch = true" in content
