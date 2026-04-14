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

"""Red-phase tests for deterministic dependency generation contracts."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PYTHON_EXE = sys.executable
GENERATOR_SCRIPT = REPO_ROOT / "scripts" / "deps" / "generate_requirements.py"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(name="tmp_dependency_workspace")
def fixture_tmp_dependency_workspace(tmp_path: Path) -> Path:
    """Create a temporary workspace with a valid pyproject file.

    Args:
        tmp_path: Per-test temporary directory provided by pytest.

    Returns:
        Path: Workspace path containing pyproject.toml.

    """
    shutil.copy2(FIXTURES_DIR / "pyproject_valid.toml", tmp_path / "pyproject.toml")
    return tmp_path


def _run_generator(workspace: Path) -> subprocess.CompletedProcess[str]:
    """Run the planned dependency generator command in a workspace.

    Args:
        workspace: Directory that contains pyproject.toml.

    Returns:
        subprocess.CompletedProcess[str]: Captured command result.

    """
    return subprocess.run(
        [str(PYTHON_EXE), str(GENERATOR_SCRIPT), "--output", "requirements.txt"],
        cwd=workspace,
        check=False,
        capture_output=True,
        text=True,
    )


def _sha256(file_path: Path) -> str:
    """Compute a file hash used for no-op regeneration assertions.

    Args:
        file_path: Path to the file to hash.

    Returns:
        str: Lowercase SHA-256 hex digest.

    """
    return hashlib.sha256(file_path.read_bytes()).hexdigest()


def test_generate_requirements_is_byte_stable(tmp_dependency_workspace: Path) -> None:
    """Generator should succeed and write identical bytes on repeated runs.

    Args:
        tmp_dependency_workspace: Workspace containing canonical dependency source.

    """
    first = _run_generator(tmp_dependency_workspace)
    assert first.returncode == 0, first.stderr or first.stdout

    first_bytes = (tmp_dependency_workspace / "requirements.txt").read_bytes()
    second = _run_generator(tmp_dependency_workspace)
    assert second.returncode == 0, second.stderr or second.stdout

    second_bytes = (tmp_dependency_workspace / "requirements.txt").read_bytes()
    assert first_bytes == second_bytes


def test_generate_requirements_is_noop_when_re_run(tmp_dependency_workspace: Path) -> None:
    """Second generator run should not modify the already generated artifact.

    Args:
        tmp_dependency_workspace: Workspace containing canonical dependency source.

    """
    initial = _run_generator(tmp_dependency_workspace)
    assert initial.returncode == 0, initial.stderr or initial.stdout

    requirements_path = tmp_dependency_workspace / "requirements.txt"
    before_hash = _sha256(requirements_path)

    repeat = _run_generator(tmp_dependency_workspace)
    assert repeat.returncode == 0, repeat.stderr or repeat.stdout

    after_hash = _sha256(requirements_path)
    assert before_hash == after_hash


def test_generation_normalizes_newline_and_order(tmp_dependency_workspace: Path) -> None:
    """Generated requirements should be normalized for ordering and newline style.

    Args:
        tmp_dependency_workspace: Workspace containing canonical dependency source.

    """
    result = _run_generator(tmp_dependency_workspace)
    assert result.returncode == 0, result.stderr or result.stdout

    generated = (tmp_dependency_workspace / "requirements.txt").read_text(encoding="utf-8")
    assert generated.endswith("\n")

    lines = [line for line in generated.splitlines() if line and not line.startswith("#")]
    assert lines == sorted(lines, key=str.lower)
