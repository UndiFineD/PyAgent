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

"""Tests for the consolidate_llm_context outputs.

These tests validate that expected output files are generated with deterministic
content based on the repository structure.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _run_script(tmp_path, args=None) -> Path:
    args = args or []
    cmd = [
        sys.executable,
        "scripts/consolidate_llm_context.py",
        "--repo-root",
        str(tmp_path),
        "--output-dir",
        str(tmp_path / "out"),
        "--apply",
    ]
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return tmp_path / "out"


def test_outputs_are_created_and_contain_sources(tmp_path):
    (tmp_path / "docs" / "architecture").mkdir(parents=True)
    (tmp_path / "docs" / "architecture" / "b.md").write_text("# B\nContent B\n")
    (tmp_path / "docs" / "architecture" / "a.md").write_text("# A\nContent A\n")

    (tmp_path / "features").mkdir(parents=True)
    (tmp_path / "features" / "hello.description.md").write_text("Hello description")
    (tmp_path / "features" / "world.improvements.md").write_text("World improvements")

    out = _run_script(tmp_path)

    llms = (out / "llms.txt").read_text()
    assert "llms-architecture.txt" in llms
    assert "llms-improvements.txt" in llms

    arch = (out / "llms-architecture.txt").read_text()
    assert "## Source: docs/architecture/a.md" in arch
    assert "## Source: docs/architecture/b.md" in arch
    # Ensure deterministic ordering (a before b)
    assert arch.index("a.md") < arch.index("b.md")

    imp = (out / "llms-improvements.txt").read_text()
    assert "Hello description" in imp
    assert "World improvements" in imp
