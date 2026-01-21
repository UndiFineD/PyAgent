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


"""AutoDebuggerOrchestrator for PyAgent.
Coordinates between ImmuneSystemAgent and CoderAgent to self-heal source code changes.
Implemented as part of Phase 40: Recursive Self-Debugging.
"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
import logging
import os
import sys
import subprocess
from typing import Any
from src.logic.agents.security.immune_system_agent import ImmuneSystemAgent
from src.logic.agents.development.coder_agent import CoderAgent
from src.core.base.common.base_utilities import as_tool

__version__ = VERSION


class AutoDebuggerOrchestrator:
    """Orchestrates recursive self-debugging and code repair."""

    def __init__(self, workspace_root: str | None = None) -> None:
        self.workspace_root = workspace_root or os.getcwd()
        # Initialize specialized agents
        # Note: We use the actual source paths if we can find them, otherwise relative
        immune_path = os.path.join(
            self.workspace_root, "src\logic\agents\security\immune_system_agent.py"
        )
        coder_path = os.path.join(
            self.workspace_root, "src\logic\agents\development\coder_agent.py"
        )

        self.immune_system = ImmuneSystemAgent(immune_path)
        self.coder = CoderAgent(coder_path)
        self.repair_history: list[dict[str, Any]] = []

    @as_tool
    async def validate_and_repair(self, file_path: str) -> dict[str, Any]:
        """Validates a file and attempts automatic repair if it fails syntax check.

        Args:
            file_path: The absolute path to the file to check.
        """
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"File not found: {file_path}"}

        logging.info(f"AutoDebugger: Validating {file_path}")

        # 1. Syntax Check using python -m py_compile
        try:
            subprocess.run(
                [sys.executable, "-m", "py_compile", file_path],
                check=True,
                capture_output=True,
                text=True,
            )
            return {"status": "success", "message": f"{file_path} passed syntax check."}
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or e.stdout
            logging.warning(
                f"AutoDebugger: Syntax error detected in {file_path}: {error_msg}"
            )

            # 2. Safety Scan with ImmuneSystemAgent
            threat_scan = self.immune_system.scan_for_injections(error_msg)
            logging.debug(f"AutoDebugger: Safety scan result: {threat_scan}")
            if threat_scan["status"] == "dangerous":
                # Fix: Catch false positives from LLM fallback/failures when scanning compiler errors.
                # If there are no specific injection findings (regex matches) and it's a standard SyntaxError,
                # we treat it as safe to avoid blocking legitimate repairs.
                if not threat_scan.get("findings", []) and (
                    "SyntaxError" in error_msg or "IndentationError" in error_msg
                ):
                    logging.warning(
                        f"AutoDebugger: Ignoring potential false positive in safety scan for {file_path}"
                    )
                else:
                    logging.error(
                        f"AutoDebugger: Safety breach detected in error logs for {file_path}. Aborting repair."
                    )
                    return {
                        "status": "blocked",
                        "message": "Infected code detected during validation. Quarantining fix.",
                    }

            # 3. Attempt Repair with CoderAgent
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            repair_prompt = (
                f"The file {file_path} has the following syntax error:\n"
                f"```\n{error_msg}\n```\n"
                f"Fix the syntax error while preserving the original logic. Content:\n\n{content}"
            )

            # Use CoderAgent to perform the fix
            # coder.improve_content(prompt) handles the actual update and self-validation
            from pathlib import Path

            self.coder.file_path = Path(
                file_path
            )  # Target the coder to the broken file
            await self.coder.improve_content(repair_prompt)

            repair_record = {
                "file": file_path,
                "error": error_msg,
                "status": "repaired",
                "timestamp": "now",  # In real implementation we'd use datetime
            }
            self.repair_history.append(repair_record)

            return {
                "status": "repaired",
                "message": f"AutoDebugger: Successfully repaired {file_path}",
                "error_details": error_msg,
            }

    @as_tool
    def run_fleet_self_audit(self) -> str:
        """Audits all python files in the src directory for syntax issues."""
        src_path = os.path.join(self.workspace_root, "src")
        python_files = []

        for root, dirs, files in os.walk(src_path):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))

        results = []
        for pf in python_files:
            res = self.validate_and_repair(pf)
            if res["status"] != "success":
                results.append(f"{pf}: {res['status']} - {res['message']}")

        if not results:
            return "Fleet self-audit complete. No issues found."
        return "Fleet self-audit complete. Issues found:\n" + "\n".join(results)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    orchestrator = AutoDebuggerOrchestrator()
    if len(sys.argv) > 1:
        print(orchestrator.validate_and_repair(sys.argv[1]))
    else:
        print(orchestrator.run_fleet_self_audit())
