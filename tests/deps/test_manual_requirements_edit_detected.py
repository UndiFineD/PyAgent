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

"""Red-phase tests for manual edits to generated requirements artifacts."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PYTHON_EXE = sys.executable
PARITY_SCRIPT = REPO_ROOT / "scripts" / "deps" / "check_dependency_parity.py"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(name="workspace_with_manual_edit")
def fixture_workspace_with_manual_edit(tmp_path: Path) -> Path:
    """Create a workspace that simulates manual edits to generated requirements.

    Args:
        tmp_path: Per-test temporary directory provided by pytest.

    Returns:
        Path: Workspace containing pyproject and manually edited requirements.

    """
    shutil.copy2(FIXTURES_DIR / "pyproject_valid.toml", tmp_path / "pyproject.toml")
    shutil.copy2(FIXTURES_DIR / "requirements_drifted.txt", tmp_path / "requirements.txt")
    return tmp_path


def test_manual_requirements_edit_is_detected(workspace_with_manual_edit: Path) -> None:
    """Parity checker should identify manual edits and fail with a clear message.

    Args:
        workspace_with_manual_edit: Workspace containing drifted requirements.

    """
    result = subprocess.run(
        [str(PYTHON_EXE), str(PARITY_SCRIPT), "--check"],
        cwd=workspace_with_manual_edit,
        check=False,
        capture_output=True,
        text=True,
    )

    output = f"{result.stdout}\n{result.stderr}".lower()
    assert result.returncode == 1
    assert "manual edit detected" in output
