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
"""Tests for the SetupTests scaffold script (prj0000023)."""

from __future__ import annotations

from pathlib import Path

from scripts.SetupTests import create_test_structure


def test_creates_mirror_for_new_package(tmp_path: Path):
    src = tmp_path / "src"
    (src / "mypackage").mkdir(parents=True)
    (src / "mypackage" / "__init__.py").touch()
    tests = tmp_path / "tests"
    tests.mkdir()

    created = create_test_structure(str(src), str(tests))
    assert len(created) == 1
    assert (tests / "mypackage" / "__init__.py").exists()
    assert (tests / "mypackage" / "test_mypackage.py").exists()


def test_skips_existing_mirror(tmp_path: Path):
    src = tmp_path / "src"
    (src / "pkg").mkdir(parents=True)
    tests = tmp_path / "tests"
    (tests / "pkg").mkdir(parents=True)

    created = create_test_structure(str(src), str(tests))
    assert created == []  # already exists — nothing created


def test_dry_run_does_not_write(tmp_path: Path):
    src = tmp_path / "src"
    (src / "newpkg").mkdir(parents=True)
    tests = tmp_path / "tests"
    tests.mkdir()

    created = create_test_structure(str(src), str(tests), dry_run=True)
    assert len(created) == 1
    assert "[dry-run]" in created[0]
    assert not (tests / "newpkg").exists()


def test_skips_dunder_packages(tmp_path: Path):
    src = tmp_path / "src"
    (src / "__pycache__").mkdir(parents=True)
    tests = tmp_path / "tests"
    tests.mkdir()

    created = create_test_structure(str(src), str(tests))
    assert created == []
