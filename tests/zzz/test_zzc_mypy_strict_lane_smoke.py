#!/usr/bin/env python3
"""Smoke tests for strict-lane mypy behavior."""

import subprocess
import sys
from pathlib import Path

import pytest

STRICT_CONFIG_PATH = Path("mypy-strict-lane.ini")
BAD_FIXTURE_PATH = Path("tests/fixtures/mypy_strict_lane/bad_case.py")


def test_mypy_strict_lane_rejects_known_bad_fixture() -> None:
    """Require strict-lane mypy to fail on deterministic bad fixture.

    Returns:
        None.

    """
    assert STRICT_CONFIG_PATH.exists(), (
        "Expected strict-lane config at mypy-strict-lane.ini before smoke validation can run."
    )
    assert BAD_FIXTURE_PATH.exists(), "Expected known-bad fixture at tests/fixtures/mypy_strict_lane/bad_case.py."

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mypy",
            "--config-file",
            str(STRICT_CONFIG_PATH),
            str(BAD_FIXTURE_PATH),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    stderr = result.stderr or ""
    stdout = result.stdout or ""

    if "No module named mypy" in stderr:
        pytest.skip("mypy not installed in environment")

    assert result.returncode != 0, "Strict-lane mypy must return non-zero on known-bad fixture."
    combined_output = f"{stdout}\n{stderr}"
    assert "bad_case.py" in combined_output, "mypy output must reference the known-bad fixture path."
    assert "error:" in combined_output.lower(), "mypy output must contain a concrete type-check error."
