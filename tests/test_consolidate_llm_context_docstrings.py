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

"""Tests docstring migration behavior for consolidate_llm_context."""

from __future__ import annotations

import subprocess
import sys


def _run_script(tmp_path, args=None) -> subprocess.CompletedProcess[str]:
    args = args or []
    cmd = [
        sys.executable,
        "scripts/consolidate_llm_context.py",
        "--repo-root",
        str(tmp_path),
        "--output-dir",
        str(tmp_path / "out"),
        "--apply",
        "--migrate-docstrings",
    ]
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result


def test_migrate_docstrings_inserts_block_and_is_idempotent(tmp_path):
    # Create a Python module with license header and a function.
    module = tmp_path / "mymodule.py"
    module.write_text(
        """# My module\n\n"""
        "def foo():\n"
        "    return 'foo'\n"
    )

    # Create a corresponding markdown file that should be migrated.
    markdown = tmp_path / "mymodule.description.md"
    markdown.write_text("This module does foo things.\n")

    # Run consolidation with migration enabled.
    _run_script(tmp_path)

    updated = module.read_text()
    assert "LLM CONTEXT (auto-generated) START" in updated
    assert "This module does foo things." in updated
    assert not markdown.exists(), "Source markdown should be removed in apply mode"

    # Running again should not duplicate the block.
    _run_script(tmp_path)
    updated_again = module.read_text()
    assert updated_again.count("LLM CONTEXT (auto-generated) START") == 1
