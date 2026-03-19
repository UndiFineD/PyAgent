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

"""End-to-end integration tests for consolidate_llm_context."""

from __future__ import annotations

import subprocess
import sys


def test_full_integration_happy_path(tmp_path):
    # Setup source files
    (tmp_path / "docs" / "architecture").mkdir(parents=True)
    (tmp_path / "docs" / "architecture" / "a.md").write_text("# A\nArchitecture A\n")
    (tmp_path / "docs" / "architecture" / "b.md").write_text("# B\nArchitecture B\n")

    (tmp_path / "pkg").mkdir(parents=True)
    py_path = tmp_path / "pkg" / "m.py"
    py_path.write_text("""# Package module\n\n""" + "def f():\n    return 1\n")
    md = tmp_path / "pkg" / "m.description.md"
    md.write_text("Module M does f things.\n")

    out_dir = tmp_path / "out"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/consolidate_llm_context.py",
            "--repo-root",
            str(tmp_path),
            "--output-dir",
            str(out_dir),
            "--apply",
            "--migrate-docstrings",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr

    # Outputs should exist
    assert (out_dir / "llms.txt").exists()
    assert (out_dir / "llms-architecture.txt").exists()
    assert (out_dir / "llms-improvements.txt").exists()
    assert (out_dir / "consolidation_report.txt").exists()

    # Source markdowns should be deleted
    assert not (tmp_path / "docs" / "architecture" / "a.md").exists()
    assert not (tmp_path / "pkg" / "m.description.md").exists()

    # Module docstring should contain migrated text
    content = py_path.read_text()
    assert "Module M does f things." in content
    assert content.count("LLM CONTEXT (auto-generated) START") == 1
