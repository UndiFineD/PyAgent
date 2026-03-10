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

    res = subprocess.run([sys.executable, "-m", "ruff", str(bad)], capture_output=True, text=True, check=False)
    if res.returncode == 0:
        # ruff reported no issues — that's unexpected for this file
        assert False, "ruff did not report issues for deliberately bad file"

    if "No module named ruff" in (res.stderr or ""):
        import pytest

        pytest.skip("ruff not installed in environment")

    assert res.returncode != 0

    # long-line check
    long_file = tmp_path / "long.py"
    long_file.write_text("a = '" + "x" * 121 + "'\n")
    long_res = subprocess.run(
        [sys.executable, "-m", "ruff", str(long_file)],
        capture_output=True,
        text=True,
        check=False,
    )
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
