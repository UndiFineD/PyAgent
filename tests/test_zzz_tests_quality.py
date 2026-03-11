#!/usr/bin/env python3
"""Meta-test to ensure all test files meet basic quality standards:"""
import ast
import subprocess
import sys
from pathlib import Path

import pytest

failures: list[str] = []
warnings: list[str] = []


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


def test_all_test_files_meet_quality() -> None:
    """Meta-test that checks every test_*.py file for basic quality:
    - contains at least one assert or pytest.raises
    - passes ruff lint
    - passes mypy type check
    This helps ensure "who tests the tester" by enforcing quality on test files themselves.
    """
    repo_root = Path(__file__).resolve().parent.parent
    test_files = sorted(repo_root.glob("tests/test_*.py"))
    assert test_files, "no test files found"

    for f in test_files:
        # skip this meta-test itself to avoid recursion
        if f.name == Path(__file__).name:
            continue
        text = f.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text)
        except SyntaxError as e:
            failures.append(f"{f}: syntax error: {e}")
            continue

        has_assert = any(isinstance(n, ast.Assert) for n in ast.walk(tree))
        has_raises = _has_pytest_raises(tree)
        if not (has_assert or has_raises):
            failures.append(f"{f}: no assert or pytest.raises found")

        # run ruff on this file (use explicit 'check' subcommand)
        ruff_cmd = [sys.executable, "-m", "ruff", "check", str(f)]
        try:
            ruff = subprocess.run(ruff_cmd, capture_output=True, text=True, check=False)
        except FileNotFoundError:
            warnings.append(f"{f}: ruff not installed or not available in PATH")
            ruff = None
        if ruff is not None and ruff.returncode != 0:
            # if ruff isn't installed in the venv, python -m ruff will exit with ModuleNotFoundError
            if "No module named ruff" in (ruff.stderr or ""):
                warnings.append(f"{f}: ruff not installed in environment: {ruff.stderr}")
            else:
                failures.append(f"{f}: ruff reported issues:\n{ruff.stdout}{ruff.stderr}")

        # run mypy on this single file (ignore missing imports to reduce noise)
        mypy_cmd = [
            sys.executable,
            "-m",
            "mypy",
            "--no-incremental",
            "--ignore-missing-imports",
            str(f),
        ]
        try:
            mypy = subprocess.run(mypy_cmd, capture_output=True, text=True, check=False)
        except FileNotFoundError:
            warnings.append(f"{f}: mypy not installed or not available in PATH")
            mypy = None
        if mypy is not None and mypy.returncode != 0:
            if "No module named mypy" in (mypy.stderr or ""):
                warnings.append(f"{f}: mypy not installed in environment: {mypy.stderr}")
            else:
                failures.append(f"{f}: mypy reported issues:\n{mypy.stdout}{mypy.stderr}")

    # Report warnings (but don't fail the meta-test on missing dev tools)
    if warnings:
        pytest.skip("Warnings while running quality checks:\n" + "\n".join(warnings))

    if failures:
        pytest.fail("\n\n".join(failures))
