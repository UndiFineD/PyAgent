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
"""Tests for scripts/enforce_branch.py — branch naming and project-file isolation."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Ensure scripts/ is importable.
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import enforce_branch  # noqa: E402


# ---------------------------------------------------------------------------
# Branch naming — Rule 1
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("branch", ["main", "master", "dev", "develop"])
def test_base_branches_allowed_no_staged(branch: str) -> None:
    with (
        patch.object(enforce_branch, "get_current_branch", return_value=branch),
        patch.object(enforce_branch, "get_staged_files", return_value=[]),
    ):
        assert enforce_branch.main() == 0


@pytest.mark.parametrize("branch", [
    "prj001-core-system",          # 3-digit legacy
    "prj0000006-unified-tx",       # 7-digit current
    "prj0000042-crdt-security",
])
def test_project_branches_pass_naming(branch: str) -> None:
    with (
        patch.object(enforce_branch, "get_current_branch", return_value=branch),
        patch.object(enforce_branch, "get_staged_files", return_value=[]),
    ):
        assert enforce_branch.main() == 0


@pytest.mark.parametrize("branch", [
    "feature/some-feature",
    "bugfix-something",
    "prj-no-id",
    "my-branch",
])
def test_bad_branch_names_blocked(branch: str) -> None:
    with (
        patch.object(enforce_branch, "get_current_branch", return_value=branch),
        patch.object(enforce_branch, "get_staged_files", return_value=[]),
    ):
        assert enforce_branch.main() == 1


# ---------------------------------------------------------------------------
# Project-file isolation — Rule 2
# ---------------------------------------------------------------------------

_PRJ6_FILE = "docs/project/prj0000006/prj006-unified-transaction-manager.project.md"
_PRJ7_FILE = "docs/project/prj0000007/prj007-advanced_research.project.md"


def test_single_project_file_on_main_blocked() -> None:
    """Staging one project's doc on main must be blocked."""
    with (
        patch.object(enforce_branch, "get_current_branch", return_value="main"),
        patch.object(enforce_branch, "get_staged_files", return_value=[_PRJ6_FILE]),
    ):
        assert enforce_branch.main() == 1


def test_single_project_file_on_correct_branch_passes() -> None:
    """Same file on the correct project branch must pass."""
    with (
        patch.object(enforce_branch, "get_current_branch", return_value="prj0000006-unified-tx"),
        patch.object(enforce_branch, "get_staged_files", return_value=[_PRJ6_FILE]),
    ):
        assert enforce_branch.main() == 0


def test_single_project_file_on_wrong_branch_blocked() -> None:
    """Staging prj6 files on a prj7 branch must be blocked."""
    with (
        patch.object(enforce_branch, "get_current_branch", return_value="prj0000007-advanced-research"),
        patch.object(enforce_branch, "get_staged_files", return_value=[_PRJ6_FILE]),
    ):
        assert enforce_branch.main() == 1


def test_multi_project_governance_on_main_allowed() -> None:
    """Batch governance touching multiple projects is allowed on main."""
    with (
        patch.object(enforce_branch, "get_current_branch", return_value="main"),
        patch.object(enforce_branch, "get_staged_files", return_value=[_PRJ6_FILE, _PRJ7_FILE]),
    ):
        assert enforce_branch.main() == 0


def test_ci_file_on_main_allowed() -> None:
    """Infrastructure files (no prjNNNNNNN in path) are always OK on main."""
    with (
        patch.object(enforce_branch, "get_current_branch", return_value="main"),
        patch.object(enforce_branch, "get_staged_files", return_value=[".github/workflows/ci.yml"]),
    ):
        assert enforce_branch.main() == 0


# ---------------------------------------------------------------------------
# extract_project_ids helper
# ---------------------------------------------------------------------------

def test_extract_project_ids_empty() -> None:
    assert enforce_branch.extract_project_ids([]) == set()


def test_extract_project_ids_no_project_paths() -> None:
    assert enforce_branch.extract_project_ids(["src/core/UnifiedTransactionManager.py"]) == set()


def test_extract_project_ids_single() -> None:
    assert enforce_branch.extract_project_ids([_PRJ6_FILE]) == {"prj0000006"}


def test_extract_project_ids_multiple() -> None:
    assert enforce_branch.extract_project_ids([_PRJ6_FILE, _PRJ7_FILE]) == {"prj0000006", "prj0000007"}


def test_extract_project_ids_windows_backslash() -> None:
    win_path = _PRJ6_FILE.replace("/", "\\")
    assert enforce_branch.extract_project_ids([win_path]) == {"prj0000006"}
