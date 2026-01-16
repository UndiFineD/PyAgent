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

"""Agent specializing in breaking down complex tasks into executable workflows."""

from __future__ import annotations
from src.core.base.Version import VERSION
import json
import logging
from typing import Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import create_main_function, as_tool

__version__ = VERSION


class TaskPlannerAgent(BaseAgent):
    """Orchestrator that plans multi-agent workflows."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Task Planner Agent. "
            "Your role is to take a high-level user request and break it down into a sequence of steps "
            "that specialized agents (Knowledge, Coder, Security, Linting, Tester) can execute. "
            "Output your plan as a JSON-compatible list of steps."
        )

    @as_tool
    def generate_shared_dependencies(self, prompt: str) -> str:
        """Generates a contract file (SHARED_DEPS.md) for cross-agent coordination."""
        logging.info("Generating SHARED_DEPS.md contract...")
        contract = (
            f"# Shared Dependencies for: {prompt}\n\n"
            "## Data Flow\n"
            "1. KnowledgeAgent -> Global Context\n"
            "2. CoderAgent -> Sandbox Execution\n\n"
            "## Constraints\n"
            "- No side effects on host\n"
            "- All changes must be verified by SecurityAgent\n"
        )
        deps_file = self.file_path.parent.parent.parent / "SHARED_DEPS.md"
        deps_file.write_text(contract)
        return "Contract SHARED_DEPS.md generated successfully."

    def _get_default_content(self) -> str:
        return "# Workspace Planning Log\n\n## Active Plans\nNone.\n"

    def create_plan(self, user_request: str) -> list[dict[str, Any]]:
        """Generates a structured plan for the FleetManager following the scientific method."""
        plan = []
        req = user_request.lower()

        # 0. Generate Contract (Shared Dependencies) - Pattern from smol-ai
        plan.append(
            {
                "agent": "TaskPlanner",
                "action": "generate_shared_dependencies",
                "args": [user_request],
            }
        )

        # 1. Verification of state (OBSERVE)
        plan.append(
            {"agent": "Knowledge", "action": "query_knowledge", "args": [user_request]}
        )

        # 2. Logic Step (THINK)
        # 3. Work Step (EXECUTE)
        if any(w in req for w in ["fix", "bug", "error", "refactor"]):
            plan.append(
                {
                    "agent": "Coder",
                    "action": "improve_content",
                    "args": [f"Follow scientific iteration to fix: {user_request}"],
                }
            )

        # 4. Critical Gate (VERIFY)
        plan.append(
            {
                "agent": "Security",
                "action": "improve_content",
                "args": ["Verify the code changes for hallucinations or injections."],
            }
        )

        return plan

    def improve_content(self, prompt: str) -> str:
        """Analyze a request and output the planning report."""
        plan = self.create_plan(prompt)
        report = [
            f"# Execution Plan for: {prompt}",
            "",
            "## Assigned Agents and Actions",
            "| Step | Agent | Action |",
            "| :--- | :--- | :--- |",
        ]

        for i, step in enumerate(plan, 1):
            report.append(f"| {i} | {step['agent']} | {step['action']} |")

        report.append("\n## JSON Payload (for FleetManager)")
        report.append(f"```json\n{json.dumps(plan, indent=2)}\n```")

        return "\n".join(report)


if __name__ == "__main__":
    main = create_main_function(
        TaskPlannerAgent, "TaskPlanner Agent", "User request to plan for"
    )
    main()
