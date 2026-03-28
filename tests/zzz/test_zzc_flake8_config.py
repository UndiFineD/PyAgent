#!/usr/bin/env python3
"""Meta-test to validate flake8 command/config behavior."""

import subprocess
import sys
from pathlib import Path

import pytest


def test_flake8_repo_config_has_no_repo_issues() -> None:
    """Ensure the checked-in flake8 config is usable on project-owned files."""
    repo_root = Path(__file__).resolve().parents[2]
    repo_config = repo_root / ".flake8"
    assert repo_config.exists(), "Expected a repo-level .flake8 file"

    config_text = repo_config.read_text(encoding="utf-8")
    expected_settings = [
        "[flake8]",
        "max-line-length = 120",
        "extend-ignore = E203, W503",
        ".venv,",
        ".venv_ci,",
        ".agents,",
        "build,",
        "dist,",
    ]
    for expected_setting in expected_settings:
        assert expected_setting in config_text, f"Missing expected flake8 setting: {expected_setting}"

    smoke_targets = [
        str(repo_root / "tests" / "zzz" / "test_zzc_flake8_config.py"),
    ]

    res = subprocess.run(
        [sys.executable, "-m", "flake8", "--config", str(repo_config), *smoke_targets],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
    )
    if "No module named flake8" in (res.stderr or ""):
        pytest.skip("flake8 not installed in environment")

    output = ((res.stdout or "") + (res.stderr or "")).strip()
    assert res.returncode == 0, output or "flake8 reported issues for smoke targets"
