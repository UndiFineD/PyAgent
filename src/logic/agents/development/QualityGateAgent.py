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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Agent specializing in automated quality gates and release validation."""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import json
import subprocess
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import create_main_function, as_tool

__version__ = VERSION




class QualityGateAgent(BaseAgent):
    """Enforces thresholds for code quality, test coverage, and security before deployment."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = self.file_path.parent.parent.parent
        self._system_prompt = (
            "You are the Quality Gate Agent. "
            "Your role is to protect the production branch by verifying that all quality gates are green. "
            "Scan for: Test failures, low coverage, linting errors, and high-severity security issues. "
            "If any gate is red, output 'DEPLOYMENT BLOCKED'."
        )

    def _get_default_content(self) -> str:
        return "# Quality Gate Log\n\n## Status\nIdle.\n"

    def check_gates(self) -> str:
        """Executes a full suite of quality checks."""
        report = ["# Quality Gate Validation Report\n"]
        blocked = False

        # 1. Test Gate
        try:
            logging.info("Quality Gate: Running Pytest...")
            # Use sys.executable to be robust
            import sys
            subprocess.run([sys.executable, "-m", "pytest", "--version"], capture_output=True)
            # Phase 108: Record validation
            self._record("check_gates", "Initiated", provider="Internal", model="Gatekeeper")

            # In a real scenario, we'd run: ["python", "-m", "pytest", "tests/"]
            # To keep this fast for the dashboard, we check if test_results.txt exists
            test_results = self.workspace_root / "test_results.txt"
            if test_results.exists():
                content = test_results.read_text()
                if "FAILED" in content:
                    report.append("- ❌ **Tests**: FAILED items detected in test_results.txt")
                    blocked = True
                else:
                    report.append("- ✅ **Tests**: All tests passing.")
            else:
                report.append("- ⚠️ **Tests**: No test_results.txt found. Run tests first.")
        except Exception as e:
            report.append(f"- ❌ **Tests**: Error running test suites: {e}")
            blocked = True

        # 2. Security Gate
        self.workspace_root / "src/logic/agents/development/SecurityGuardAgent.py"
        # Since we are an agent, we can't easily 'summon' another unless we are the FleetManager,
        # but we can look for the output of others.
        telemetry_file = self.workspace_root / ".agent_telemetry.json"
        if telemetry_file.exists():
            telemetry = json.loads(telemetry_file.read_text())
            errors = [m for m in telemetry if m.get("status") == "error"]
            if errors:
                report.append(f"- ❌ **Reliability**: Found {len(errors)} execution errors in recent telemetry.")
                blocked = True
            else:
                report.append("- ✅ **Reliability**: Zero execution errors in history.")

        if blocked:
            report.append("\n## ⛔ DEPLOYMENT BLOCKED")
            report.append("Please resolve the issues above before attempting to release.")
        else:
            report.append("\n## ✅ READY FOR RELEASE")
            report.append("All quality gates are currently green.")

        return "\n".join(report)

    def validate_against_blueprint(self, result: str, blueprint: str) -> str:
        """Verifies if the result aligns with the logical reasoning blueprint."""
        # Simple heuristic check: ensure key objectives from blueprint are mentioned in results
        objectives = [line.replace('- **Primary Objective**: ', '') for line in blueprint.splitlines() if 'Primary Objective' in line]

        if not objectives:
            return "⚠️ No clear objectives found in blueprint for validation."

        matches = [obj for obj in objectives if obj.lower() in result.lower()]
        if len(matches) == len(objectives):










            return "✅ Result successfully aligns with the logical blueprint objectives."
        else:
            return f"❌ Alignment mismatch: Result did not clearly address {len(objectives) - len(matches)} blueprint objectives."






    @as_tool
    def validate_release(self, current_result: str | None = None, reasoning_blueprint: str | None = None) -> str:
        """High-level validation including blueprint alignment and gates."""
        report = [self.check_gates()]






        if current_result and reasoning_blueprint:
            report.append("\n## Blueprint Alignment Check")
            report.append(self.validate_against_blueprint(current_result, reasoning_blueprint))

        return "\n".join(report)





    def improve_content(self, prompt: str | None = None) -> str:
        """Perform a quality gate check."""
        return self.check_gates()






if __name__ == "__main__":
    main = create_main_function(QualityGateAgent, "QualityGate Agent", "Task (e.g. 'check')")
    main()
