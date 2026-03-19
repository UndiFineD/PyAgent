#!/usr/bin/env python3
"""Code quality runner focused on changed files.

This tool is intended to support the @8ql workflow by performing targeted
linters/type checks/tests only on the files changed in the current branch.

It is deliberately conservative: if a given tool (ruff/mypy/pytest) is not
installed, it will be skipped rather than failing the run.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable, List

try:
    from src.tools.git_utils import main as _git_utils_main
except ImportError:  # pragma: no cover
    from tools.git_utils import main as _git_utils_main

from .tool_registry import register_tool


def _run_cmd(cmd: list[str], capture: bool = False) -> int:
    """Run a command and optionally capture its output."""
    proc = subprocess.run(cmd, check=False, capture_output=capture, text=True)
    if proc.stdout and capture:
        print(proc.stdout, end="")
    if proc.stderr and capture:
        print(proc.stderr, file=sys.stderr, end="")
    return proc.returncode


def _get_changed_files(base: str) -> List[str]:
    """Return a list of changed files relative to `base` branch."""
    # Use git_utils 'changed' command for consistency.
    # It prints one file per line.
    proc = subprocess.run(
        [sys.executable, "-m", "src.tools", "git-utils", "changed", "--base", base],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return []

    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def _select_python_files(files: Iterable[str]) -> List[str]:
    """Filter the given list of files to include only Python files."""
    return [f for f in files if f.endswith(".py")]


def main(args: list[str] | None = None) -> int:
    """Main entry point for the code_quality tool."""
    parser = argparse.ArgumentParser(prog="code_quality")
    parser.add_argument("--base", default="main", help="Base branch to compare changes against")
    parser.add_argument(
        "--files",
        nargs="*",
        help="Optional list of files to check instead of detecting changed files via git",
    )
    parser.add_argument("--skip-ruff", action="store_true", help="Skip ruff linting")
    parser.add_argument("--skip-mypy", action="store_true", help="Skip mypy typechecking")
    parser.add_argument("--skip-pytest", action="store_true", help="Skip running pytest")

    parsed = parser.parse_args(args=args)

    if parsed.files:
        changed_files = parsed.files
        print(f"Using {len(changed_files)} explicit file(s) for quality checks")
    else:
        changed_files = _get_changed_files(parsed.base)
        if not changed_files:
            print("No changed files detected; skipping quality checks.")
            return 0

    py_files = _select_python_files(changed_files)
    if not py_files:
        print("No Python files changed; skipping code quality checks.")
        return 0

    failed = False

    if not parsed.skip_ruff and shutil.which("ruff"):
        print("Running ruff on changed files...")
        if _run_cmd(["ruff", "check", *py_files], capture=True) != 0:
            failed = True
    else:
        print("Skipping ruff (not installed or disabled)")

    if not parsed.skip_mypy and shutil.which("mypy"):
        print("Running mypy on changed files...")
        # Use an isolated cache directory to avoid stale/invalid mypy caches.
        with tempfile.TemporaryDirectory(prefix="mypy-cache-") as cache_dir:
            if _run_cmd(["mypy", "--cache-dir", cache_dir, *py_files], capture=True) != 0:
                failed = True
    else:
        print("Skipping mypy (not installed or disabled)")

    if not parsed.skip_pytest and shutil.which("pytest"):
        test_files = [f for f in changed_files if f.startswith("tests/") and f.endswith(".py")]
        if test_files:
            print("Running pytest on changed test files...")
            if _run_cmd(["pytest", "-q", *test_files], capture=True) != 0:
                failed = True
        else:
            print("No changed test files; skipping pytest")
    else:
        print("Skipping pytest (not installed or disabled)")

    return 1 if failed else 0


register_tool(
    "code_quality",
    main,
    "Run lint/typecheck/tests on changed files (for @8ql workflow)",
)
