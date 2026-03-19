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

"""Tests cleanup and consolidation report generation."""

from __future__ import annotations

import subprocess
import sys


def test_apply_mode_writes_report_and_deletes_sources(tmp_path):
    (tmp_path / "docs" / "architecture").mkdir(parents=True)
    arch = tmp_path / "docs" / "architecture" / "a.md"
    arch.write_text("# A\n")

    imp = tmp_path / "foo.description.md"
    imp.write_text("desc\n")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/consolidate_llm_context.py",
            "--repo-root",
            str(tmp_path),
            "--output-dir",
            str(tmp_path / "out"),
            "--apply",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

    report_path = tmp_path / "out" / "consolidation_report.txt"
    assert report_path.exists(), "Expected consolidation_report.txt to be created"
    report = report_path.read_text()
    assert "Sources deleted" in report
    assert "docs/architecture/a.md" in report
    assert "foo.description.md" in report

    assert not arch.exists(), "Architecture source should be deleted in apply mode"
    assert not imp.exists(), "Improvement source should be deleted in apply mode"
