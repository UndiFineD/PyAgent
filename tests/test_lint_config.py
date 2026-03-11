#!/usr/bin/env python3
"""Meta-test to ensure test files meet basic linting standards."""

import subprocess
import sys
from pathlib import Path


def test_ruff_finds_error(tmp_path: Path) -> None:
    """Ensure ruff flags a simple lint issue or skip if ruff not installed.

    Also verify that max-line-length enforcement is in effect (120 chars).
    """
    bad = tmp_path / "bad.py"
    bad.write_text("import os\n\n\n")

    def run_ruff_for_file(path: Path) -> subprocess.CompletedProcess[str]:
        # Try the simple invocation first, but fall back to the explicit 'check' command
        cmd = [sys.executable, "-m", "ruff", str(path)]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        # some ruff CLI builds require the 'check' subcommand (error shows 'unrecognized subcommand')
        if proc.returncode != 0 and "unrecognized subcommand" in (proc.stderr or ""):
            cmd2 = [sys.executable, "-m", "ruff", "check", str(path)]
            proc = subprocess.run(
                cmd2, capture_output=True, text=True, check=False
            )
        return proc

    res = run_ruff_for_file(bad)
    if res.returncode == 0:
        # ruff reported no issues — that's unexpected for this file
        raise AssertionError("ruff did not report issues for deliberately bad file")

    if "No module named ruff" in (res.stderr or ""):
        import pytest

        pytest.skip("ruff not installed in environment")

    assert res.returncode != 0

    # long-line check
    long_file = tmp_path / "long.py"
    long_file.write_text("a = '" + "x" * 121 + "'\n")
    long_res = run_ruff_for_file(long_file)
    # if ruff installed and configured, it should complain about E501 line too long
    if "No module named ruff" not in (long_res.stderr or ""):
        assert long_res.returncode != 0
        assert "E501" in (long_res.stdout + long_res.stderr)

    # check that flake8 configuration enforces max-line-length=120
    flake = tmp_path / ".flake8"
    # copy the project's .flake8 so we can inspect it without modifying
    import shutil
    proj = Path(".flake8")
    if proj.exists():
        shutil.copy(proj, flake)
        content = flake.read_text(encoding="utf-8")
        assert "max-line-length = 120" in content
