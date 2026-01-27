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


"""Agent specializing in automated testing and coverage analysis.
Inspired by SGI-Bench and py.test.
"""

from __future__ import annotations

import logging
import subprocess

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class TestAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """Executes unit and integration tests and analyzes failures."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = self.file_path.parent.parent.parent
        self._system_prompt = (
            "You are the Test Agent. "
            "Your role is to ensure the functional correctness of the codebase. "
            "Execute pytest suites, capture failures, and explain them to the developers. "
            "Always suggest a potential cause for every test failure."
        )

    @as_tool
    def run_tests(self, path: str = "tests") -> str:
        """Executes pytest on the specified directory."""
        logging.info(f"TestAgent running tests in: {path}")
        try:
            import sys

            # Converted to list-based execution to prevent shell injection
            cmd = [sys.executable, "-m", "pytest", path, "--tb=short", "--maxfail=5"]
            result = subprocess.run(cmd, shell=False, capture_output=True, text=True, check=False)

            # Phase 108: Record test execution patterns
            self._record(
                f"pytest {path}",
                f"RC={result.returncode}\n{result.stdout[-1000:]}",
                provider="Shell",
                model="pytest",
            )

            report = ["## 🧪 Test Execution Report\n"]
            if result.returncode == 0:
                report.append("✅ **Status**: All tests passed.")
                report.append(f"```text\n{result.stdout.splitlines()[-1] if result.stdout else 'No output'}\n```")
            else:
                report.append(f"❌ **Status**: {result.returncode} tests FAILED.\n")
                report.append("### Failure Details")
                report.append(f"```text\n{result.stdout}\n```")

            return "\n".join(report)
        except (subprocess.SubprocessError, RuntimeError, OSError) as e:
            import traceback
            tb = traceback.format_exc()

            # Phase 275: Log failure to context lineage if available
            if hasattr(self, "context") and self.context:
                self.context.log_failure(
                    stage="test_execution",
                    error=str(e),
                    details={"path": path},
                    stack_trace=tb
                )

            logging.error(f"TestAgent execution failed: {e}\n{tb}")
            return f"Error running tests: {e}\nTraceback:\n{tb}"

    @as_tool
    def run_file_tests(self, file_path: str) -> str:
        """Runs tests for a single file."""
        return self.run_tests(file_path)

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Runs tests based on user prompt."""
        path = target_file if target_file else (prompt if prompt else "tests")
        return self.run_tests(path)
