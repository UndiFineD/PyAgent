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

"""Red-phase tests for malformed pyproject parse failure contracts."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PYTHON_EXE = REPO_ROOT / ".venv" / "Scripts" / "python.exe"
GENERATOR_SCRIPT = REPO_ROOT / "scripts" / "deps" / "generate_requirements.py"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(name="malformed_workspace")
def fixture_malformed_workspace(tmp_path: Path) -> Path:
    """Create a workspace with a malformed pyproject source file.

    Args:
        tmp_path: Per-test temporary directory provided by pytest.

    Returns:
        Path: Workspace with malformed pyproject.toml.

    """
    shutil.copy2(FIXTURES_DIR / "pyproject_malformed.toml", tmp_path / "pyproject.toml")
    return tmp_path


def test_malformed_pyproject_fails_with_structured_error(malformed_workspace: Path) -> None:
    """Generator should emit a structured parse failure for malformed pyproject.

    Args:
        malformed_workspace: Workspace with malformed pyproject fixture.

    """
    result = subprocess.run(
        [str(PYTHON_EXE), str(GENERATOR_SCRIPT), "--output", "requirements.txt"],
        cwd=malformed_workspace,
        check=False,
        capture_output=True,
        text=True,
    )

    output = f"{result.stdout}\n{result.stderr}".lower()
    assert result.returncode != 0
    assert "failed to parse pyproject.toml" in output
