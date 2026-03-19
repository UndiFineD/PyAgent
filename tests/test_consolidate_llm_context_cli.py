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

"""Tests for the consolidate_llm_context CLI."""

from __future__ import annotations

import subprocess
import sys


def test_default_is_dry_run(tmp_path):
    """Running without --apply should not modify any files."""
    result = subprocess.run(
        [sys.executable, "scripts/consolidate_llm_context.py", "--repo-root", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Dry-run" in result.stdout


def test_apply_flag_changes_behavior(tmp_path):
    """The --apply flag should be accepted and change mode."""
    result = subprocess.run(
        [
            sys.executable,
            "scripts/consolidate_llm_context.py",
            "--repo-root",
            str(tmp_path),
            "--apply",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "apply" in result.stdout.lower()
    assert "dry-run" not in result.stdout.lower()
