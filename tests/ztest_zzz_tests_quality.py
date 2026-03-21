#!/usr/bin/env python3
"""Meta-test to ensure test files meet structural quality standards."""
# Copyright 2026 UndiFineD
#
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

import ast
from pathlib import Path

import pytest


def _has_pytest_raises(tree: ast.AST) -> bool:
    """Helper to detect if pytest.raises is used in the test file."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            # matches pytest.raises(...) or context manager usage not detectable here
            if isinstance(func, ast.Attribute) and func.attr == "raises":
                return True
            if isinstance(func, ast.Name) and func.id == "raises":
                return True
    return False


def test_all_test_files_meet_quality(pytestconfig: pytest.Config) -> None:
    """Meta-test that checks every test_*.py file for structural quality:
    Verbosity is controlled by pytest's -v/--verbose flag; when set the
    test prints each filename and the checks being executed.
    - contains at least one assert or pytest.raises
    - parses as valid Python syntax
    Lint and type-tool execution coverage is delegated to dedicated tests.
    """
    failures: list[str] = []

    repo_root = Path(__file__).resolve().parent.parent
    test_files = sorted(repo_root.glob("tests/test_*.py"))
    assert test_files, "no test files found"
    verbose = pytestconfig.getoption("verbose")
    if verbose:
        print(f"quality: found {len(test_files)} test files to inspect")

    for f in test_files:
        # skip this meta-test itself to avoid recursion
        if f.name == Path(__file__).name:
            continue
        if verbose:
            print(f"quality: checking {f}")
        text = f.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text)
        except SyntaxError as e:
            failures.append(f"{f}: syntax error: {e}")
            continue

        has_assert = any(isinstance(n, ast.Assert) for n in ast.walk(tree))
        has_raises = _has_pytest_raises(tree)
        if verbose:
            print(f"  has_assert={has_assert} has_raises={has_raises}")
        if not (has_assert or has_raises):
            failures.append(f"{f}: no assert or pytest.raises found")

    if failures:
        pytest.fail("\n\n".join(failures))
