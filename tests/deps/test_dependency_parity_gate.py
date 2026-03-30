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

"""Red-phase tests for dependency parity checker command contracts."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PYTHON_EXE = REPO_ROOT / ".venv" / "Scripts" / "python.exe"
PARITY_SCRIPT = REPO_ROOT / "scripts" / "deps" / "check_dependency_parity.py"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(name="workspace_with_drifted_requirements")
def fixture_workspace_with_drifted_requirements(tmp_path: Path) -> Path:
    """Create a workspace where requirements.txt intentionally differs from source.

    Args:
        tmp_path: Per-test temporary directory provided by pytest.

    Returns:
        Path: Workspace with pyproject and drifted requirements fixture.

    """
    shutil.copy2(FIXTURES_DIR / "pyproject_valid.toml", tmp_path / "pyproject.toml")
    shutil.copy2(FIXTURES_DIR / "requirements_drifted.txt", tmp_path / "requirements.txt")
    return tmp_path


@pytest.fixture(name="workspace_with_matching_requirements")
def fixture_workspace_with_matching_requirements(tmp_path: Path) -> Path:
    """Create a workspace where requirements.txt is expected to match generation.

    Args:
        tmp_path: Per-test temporary directory provided by pytest.

    Returns:
        Path: Workspace with pyproject and expected requirements fixture.

    """
    shutil.copy2(FIXTURES_DIR / "pyproject_valid.toml", tmp_path / "pyproject.toml")
    shutil.copy2(FIXTURES_DIR / "requirements_expected.txt", tmp_path / "requirements.txt")
    return tmp_path


def _run_parity_check(workspace: Path) -> subprocess.CompletedProcess[str]:
    """Run the planned parity checker command in a workspace.

    Args:
        workspace: Directory that contains pyproject.toml and requirements.txt.

    Returns:
        subprocess.CompletedProcess[str]: Captured command result.

    """
    return subprocess.run(
        [str(PYTHON_EXE), str(PARITY_SCRIPT), "--check"],
        cwd=workspace,
        check=False,
        capture_output=True,
        text=True,
    )


def test_parity_check_returns_nonzero_on_mismatch(workspace_with_drifted_requirements: Path) -> None:
    """Parity checker should fail when committed and generated files diverge.

    Args:
        workspace_with_drifted_requirements: Workspace with intentional drift.

    """
    result = _run_parity_check(workspace_with_drifted_requirements)

    assert result.returncode == 1
    assert "dependency parity check failed" in (result.stdout + result.stderr).lower()


def test_parity_check_returns_zero_on_match(workspace_with_matching_requirements: Path) -> None:
    """Parity checker should pass when committed and generated files are equivalent.

    Args:
        workspace_with_matching_requirements: Workspace expected to be in parity.

    """
    result = _run_parity_check(workspace_with_matching_requirements)

    assert result.returncode == 0
    assert "parity check passed" in (result.stdout + result.stderr).lower()


def test_parity_failure_includes_remediation_command(workspace_with_drifted_requirements: Path) -> None:
    """Parity mismatch output should include an exact regeneration remediation command.

    Args:
        workspace_with_drifted_requirements: Workspace with intentional drift.

    """
    result = _run_parity_check(workspace_with_drifted_requirements)

    output = f"{result.stdout}\n{result.stderr}".lower()
    assert "python scripts/deps/generate_requirements.py --output requirements.txt" in output
