#!/usr/bin/env python3
"""Meta-test to ensure mypy is configured and detects type issues."""
import os
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

    # some configurations or newer versions occasionally return zero when a
    # trivial error is introduced. we used to skip unconditionally, but that
    # made the assertions below unreachable; now we only skip if the caller
    # explicitly requests leniency via an environment variable. this keeps the
    # test strict by default and will surface real configuration problems.
    if res.returncode == 0:
        if os.environ.get("MYPY_LENIENT"):
            pytest.skip(
                "mypy did not report the deliberate type error (lenient mode)"
            )
        # otherwise we fall through to the assertions so the failure is visible

    assert res.returncode != 0
    assert (res.stdout or res.stderr) != ""
