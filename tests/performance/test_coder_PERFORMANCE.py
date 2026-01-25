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

# -*- coding: utf-8 -*-
"""Test classes from test_agent_coder.py - performance module."""

from __future__ import annotations
from pathlib import Path
import sys

# Try to import test utilities
try:
    from tests.utils.agent_test_utils import (
        AGENT_DIR,
        agent_sys_path,
        load_module_from_path,
        agent_dir_on_path,
        load_agent_module,
    )
except ImportError:
    # Fallback
    AGENT_DIR = Path(__file__).parent.parent.parent.parent / "src"

    class agent_sys_path:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed


class TestPerformanceProfiling:
    """Tests for code performance profiling."""

    def test_detect_performance_issue(self, tmp_path: Path) -> None:
        """Test detecting potential performance issues."""
        with agent_dir_on_path():
            # Fix: Use correct path to CoderAgent
            mod = load_agent_module("src/logic/agents/development/coder_agent.py")

        code = """
def slow_function(n):
    result=[]
    for i in range(n):
        result=result + [i]  # O(n) each iteration
    return result
"""
        target = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "result + [i]" in content


# =============================================================================
# Session 9: Migration Automation Tests
# =============================================================================
