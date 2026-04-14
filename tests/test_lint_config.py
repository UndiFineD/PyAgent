#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
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
"""Tests that verify ruff and mypy lint configuration is present and correct."""

import subprocess
import sys
from pathlib import Path

PYPROJECT = Path(__file__).parent.parent / "pyproject.toml"
MYPY_INI = Path(__file__).parent.parent / "mypy.ini"


def test_pyproject_has_ruff_section():
    """pyproject.toml must declare [tool.ruff]."""
    content = PYPROJECT.read_text(encoding="utf-8")
    assert "[tool.ruff]" in content


def test_ruff_line_length_120():
    """Ruff must enforce 120-char lines to match project standard."""
    content = PYPROJECT.read_text(encoding="utf-8")
    assert "line-length = 120" in content


def test_ruff_selects_core_rules():
    """Ruff must select E, F, W, I (core pyflakes/pycodestyle/isort rules)."""
    content = PYPROJECT.read_text(encoding="utf-8")
    # E/F/W/I must all appear in the select list
    for rule in ('"E"', '"F"', '"W"', '"I"'):
        assert rule in content, f"ruff select missing rule {rule}"


def test_mypy_section_present():
    """pyproject.toml must declare [tool.mypy]."""
    content = PYPROJECT.read_text(encoding="utf-8")
    assert "[tool.mypy]" in content


def test_mypy_ignore_missing_imports():
    """Mypy must set ignore_missing_imports = true for gradual adoption."""
    content = PYPROJECT.read_text(encoding="utf-8")
    assert "ignore_missing_imports = true" in content


def test_ruff_binary_importable():
    """Ruff must be importable via Python (installed in the venv)."""
    result = subprocess.run([sys.executable, "-m", "ruff", "--version"], capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, f"ruff --version failed: {result.stderr}"


def test_ruff_check_exits_cleanly_on_good_file(tmp_path):
    """Ruff must not report errors on a minimal clean Python file."""
    sample = tmp_path / "clean.py"
    sample.write_text('"""Clean module."""\n\nx = 1\n', encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", str(sample)], capture_output=True, text=True, timeout=15
    )
    assert result.returncode == 0, f"ruff reported errors on clean file:\n{result.stdout}"
