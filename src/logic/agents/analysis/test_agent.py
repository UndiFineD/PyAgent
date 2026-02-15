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


"""
Test Agent - Executes pytest suites and analyzes failures

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
Instantiate with the path of the agent file (agent = TestAgent(file_path)) then call agent.run_tests(path="tests", force=False, bypass_shard_validation=False). Use force=True or bypass_shard_validation=True to skip shard integrity blocking when necessary. The method is decorated as a tool (@as_tool) so it is intended to be invoked by the system orchestration layer.

WHAT IT DOES:
- Verifies shard integrity via ShardCore before running tests (with optional bypass).
- Executes pytest using a safe, list-based subprocess invocation and captures stdout/stderr and return codes.
- Records execution metadata via the agent _record method and logs failures to the agent context using FailureClassification enums.
- Produces a concise test execution report and limits tracebacks and failures (maxfail=5) to keep outputs manageable.

WHAT IT SHOULD DO BETTER:
- More robust parsing and structured extraction of pytest failures (e.g., JSON output via pytest --json-report) to provide actionable diagnostics rather than string tails.
- Add configurable timeouts, parallel test execution options, and explicit coverage collection/integration rather than relying on external invocation flags.
- Migrate blocking subprocess calls to asyncio subprocess APIs for non-blocking integration with the agent event loop and better resource control.
- Improve isolation for test runs (virtual environments, reproducible dependencies) and richer failure classification mapping (per-test causes, flaky detection, rerun strategies).
- Increase testability of the agent itself (unit tests for shard bypass logic, mocked subprocess behavior, and context logging) and adopt StateTransaction for any filesystem changes per project conventions.

FILE CONTENT SUMMARY:
Agent specializing in automated testing and coverage analysis.
Inspired by SGI-Bench and py.test.
"""

from __future__ import annotations

import logging
import subprocess

from src.core.base.common.base_utilities import as_tool
from src.core.base.common.shard_core import ShardCore
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
# Phase 336: Failure Taxonomy
from src.core.base.common.models.core_enums import FailureClassification

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

    def shard_integrity_check(self, bypass: bool = False) -> bool:
        """
        Verify validation of shards, with optional bypass.
        Refactored to decouple testing from shard state (Phase 336).
        """
        if ShardCore().verify_integrity():
            return True

        msg = "Shard integrity check failed."
        if not bypass:
            logging.critical(f"{msg} Aborting operation. Use bypass=True to ignore.")
            if hasattr(self, "context") and self.context:
                self.context.log_failure(
                    stage="shard_integrity_check_abort",
                    error=msg,
                    details={},
                    failure_type=FailureClassification.SHARD_CORRUPTION.value
                )
            return False
        else:
            logging.warning(f"{msg} Proceeding due to bypass=True.")
            if hasattr(self, "context") and self.context:
                self.context.log_failure(
                    stage="shard_integrity_check_bypass",
                    error=msg,
                    details={},
                    failure_type=FailureClassification.SHARD_CORRUPTION.value
                )
            return True

    @as_tool
    def run_tests(self, path: str = "tests", force: bool = False, bypass_shard_validation: bool = False) -> str:
        """Executes pytest on the specified directory."""

        # Merge force and bypass flags
        should_bypass = force or bypass_shard_validation

        # Phase 336: Pattern 3 - TestAgent-Shard Coupling Mitigation
        # Verify shard integrity before running tests to prevent deadlocks
        if not self.shard_integrity_check(bypass=should_bypass):
            msg = "Shard integrity check failed."
            return f"❌ **system_error**: {msg} (Use force=True or bypass_shard_validation=True to bypass)"

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

            # Phase 336: Validation failure capture
            if result.returncode != 0 and hasattr(self, "context") and self.context:
                self.context.log_failure(
                    stage="test_execution_fail",
                    error=f"Tests failed in {path}",
                    details={
                        "return_code": result.returncode,
                        "stdout_tail": result.stdout[-500:],
                        "stderr_tail": result.stderr[-500:] if result.stderr else "",
                    },
                    failure_type=FailureClassification.TEST_INFRASTRUCTURE.value
                )

            report = ["## 🧪 Test Execution Report\n"]
            if result.returncode == 0:
                report.append("✅ **Status**: All t
"""

from __future__ import annotations

import logging
import subprocess

from src.core.base.common.base_utilities import as_tool
from src.core.base.common.shard_core import ShardCore
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
# Phase 336: Failure Taxonomy
from src.core.base.common.models.core_enums import FailureClassification

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

    def shard_integrity_check(self, bypass: bool = False) -> bool:
        """
        Verify validation of shards, with optional bypass.
        Refactored to decouple testing from shard state (Phase 336).
        """
        if ShardCore().verify_integrity():
            return True

        msg = "Shard integrity check failed."
        if not bypass:
            logging.critical(f"{msg} Aborting operation. Use bypass=True to ignore.")
            if hasattr(self, "context") and self.context:
                self.context.log_failure(
                    stage="shard_integrity_check_abort",
                    error=msg,
                    details={},
                    failure_type=FailureClassification.SHARD_CORRUPTION.value
                )
            return False
        else:
            logging.warning(f"{msg} Proceeding due to bypass=True.")
            if hasattr(self, "context") and self.context:
                self.context.log_failure(
                    stage="shard_integrity_check_bypass",
                    error=msg,
                    details={},
                    failure_type=FailureClassification.SHARD_CORRUPTION.value
                )
            return True

    @as_tool
    def run_tests(self, path: str = "tests", force: bool = False, bypass_shard_validation: bool = False) -> str:
        """Executes pytest on the specified directory."""

        # Merge force and bypass flags
        should_bypass = force or bypass_shard_validation

        # Phase 336: Pattern 3 - TestAgent-Shard Coupling Mitigation
        # Verify shard integrity before running tests to prevent deadlocks
        if not self.shard_integrity_check(bypass=should_bypass):
            msg = "Shard integrity check failed."
            return f"❌ **system_error**: {msg} (Use force=True or bypass_shard_validation=True to bypass)"

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

            # Phase 336: Validation failure capture
            if result.returncode != 0 and hasattr(self, "context") and self.context:
                self.context.log_failure(
                    stage="test_execution_fail",
                    error=f"Tests failed in {path}",
                    details={
                        "return_code": result.returncode,
                        "stdout_tail": result.stdout[-500:],
                        "stderr_tail": result.stderr[-500:] if result.stderr else "",
                    },
                    failure_type=FailureClassification.TEST_INFRASTRUCTURE.value
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

                # Heuristic classification of OS errors
                f_type = FailureClassification.TEST_INFRASTRUCTURE.value
                str_e = str(e).lower()
                if "recursion" in str_e:
                    f_type = FailureClassification.RECURSION_LIMIT.value
                elif "memory" in str_e:
                    f_type = FailureClassification.RESOURCE_EXHAUSTION.value
                elif "file not found" in str_e or "no such file" in str_e:
                    f_type = FailureClassification.STATE_CORRUPTION.value

                self.context.log_failure(
                    stage="test_execution_exception",
                    error=str(e),
                    details={"path": path, "command": cmd if 'cmd' in locals() else "unknown"},
                    stack_trace=tb,
                    failure_type=f_type
                )

            logging.error(f"TestAgent execution failed: {e}\n{tb}")

            # Phase 336: Trigger Static Analysis Fallback
            logging.info("TestAgent: Falling back to static code analysis.")
            return self.static_analysis_fallback(path)

    def static_analysis_fallback(self, path: str) -> str:
        """
        Phase 336: Static Analysis Fallback.
        Performs AST-based sanity checks when execution is blocked.
        """
        import ast
        import os

        report = ["## 🔍 Static Test Fallback Analysis\n"]
        report.append("⚠️ **Note**: Execution was blocked. Performing recursive static analysis.\n")

        target_files = []
        if os.path.isfile(path):
            target_files.append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for f in files:
                    if f.endswith(".py"):
                        target_files.append(os.path.join(root, f))

        total_issues = 0
        for f in target_files:
            try:
                with open(f, "r", encoding="utf-8") as file:
                    content = file.read()

                ast.parse(content)  # Check syntax

                # Check for risky imports or patterns often causing failures
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if alias.name in ["sys", "os"] and "recursion" in content:
                                report.append(f"- 🚩 `{f}`: Potential recursion limit issue detected.")
                                total_issues += 1
            except SyntaxError as e:
                report.append(f"- ❌ `{f}`: Syntax error detected: {e}")
                total_issues += 1
            except Exception as e:
                report.append(f"- ⚠️ `{f}`: Error reading file: {e}")

        if total_issues == 0:
            report.append("✅ Static scan found no obvious syntax or structural issues.")
        else:
            report.append(f"\nFound {total_issues} potential issues.")

        return "\n".join(report)

    @as_tool
    def run_file_tests(self, file_path: str) -> str:
        """Runs tests for a single file."""
        return self.run_tests(file_path)

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Runs tests based on user prompt."""
        path = target_file if target_file else (prompt if prompt else "tests")
        return self.run_tests(path)
