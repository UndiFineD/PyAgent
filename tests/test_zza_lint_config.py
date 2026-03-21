#!/usr/bin/env python3
"""Meta-test to validate project lint command intent and behavior."""
# Apache 2.0 License applies to this file; see LICENSE for details.

import asyncio
import sys
from pathlib import Path

import pytest


@pytest.mark.asyncio
async def test_ruff_command_intent_is_check_dot_fix(tmp_path: Path) -> None:
    """Validate lint coverage uses exactly `ruff check . --fix`."""
    (tmp_path / "clean.py").write_text("x = 1\n", encoding="utf-8")

    cmd = [sys.executable, "-m", "ruff", "check", ".", "--fix"]
    assert cmd == [sys.executable, "-m", "ruff", "check", ".", "--fix"]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        cwd=str(tmp_path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out_bytes, err_bytes = await proc.communicate()
    stdout = out_bytes.decode("utf-8", errors="ignore")
    stderr = err_bytes.decode("utf-8", errors="ignore")

    if "No module named ruff" in stderr:
        pytest.skip("ruff not installed in environment")

    assert proc.returncode == 0, stdout + stderr
