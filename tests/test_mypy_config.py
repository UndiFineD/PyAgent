#!/usr/bin/env python3
"""Meta-test to ensure mypy is configured and detects type issues."""
import subprocess
import sys
from pathlib import Path

import pytest


def test_mypy_detects_problem(tmp_path: Path) -> None:
    """Ensure mypy flags a simple type error or skip if not installed."""
    bad = tmp_path / "bad.py"
    bad.write_text("def f() -> int:\n    return 'str'\n")
    res = subprocess.run(
        [sys.executable, "-m", "mypy", str(bad)],
        capture_output=True,
        text=True,
    )
    if "No module named mypy" in (res.stderr or ""):
        pytest.skip("mypy not installed in environment")

    assert res.returncode != 0
    assert (res.stdout or res.stderr) != ""
