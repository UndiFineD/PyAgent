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

"""Agent specializing in Project Management and Multi-Agent Orchestration."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path

from src.core.base.common.base_utilities import create_main_function
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.infrastructure.swarm.orchestration.state.status_manager import \
    StatusManager

__version__ = VERSION


class DirectorAgent(BaseAgent):
    """Orchestrator agent that decomposes complex tasks and delegates to specialists."""

    def __init__(self, file_path: str) -> None:
        """Initializes the DirectorAgent."""
        super().__init__(file_path)
        self.status = StatusManager()

        # Subscribe to signals to adjust coordination
        if self.registry:
            self.registry.subscribe("agent_fail", self._handle_agent_failure)
            self.registry.subscribe("improvement_ready", self._handle_agent_success)

        self._system_prompt = (
            "You are the Director Agent (Orchestrator). "
            "Your goal is to manage complex multi-file projects. "
            "You have the authority to delegate tasks to other specialized agents:\n"
            "- CoderAgent: For implementation/refactoring.\n"
            "- WebIntelligenceAgent: For deep web research, Arxiv synthesis, and navigation.\n"
            "- TestsAgent: For unit testing and verification.\n"
            "- SecurityAgent: For auditing and safety scanning.\n"
            "- ArchitectAgent: For system design and IA³ configuration.\n\n"
            "RESEARCH WORKFLOW:\n"
            "If a task requires modern research (Phase 51+), follow this workflow:\n"
            "1. Search: Use WebIntelligenceAgent's search_arxiv tools.\n"
            "2. Data: Download papers/summaries to data/research/.\n"
            "3. Map: Use ArchitectAgent to map findings to Agent Logic (e.g., IA³ layers).\n"
            "4. Implement: Use CoderAgent to apply changes.\n"
            "5. Track: Update docs/improvements.md and .improvements.md files.\n\n"
            "When given a task, break it down into steps. For each step, specify:\n"
            "1. The target file.\n"
            "2. The agent type to use.\n"
            "3. The specific prompt/instruction for that agent.\n\n"
            "You can execute these delegations sequentially to achieve a high-level project goal."
        )

    def _get_default_content(self) -> str:
        """Provides the default content for the DirectorAgent's log."""
        return "# Project Orchestration Plan\n\n## Goal\n[Goal here]\n\n## Sequence\n- Pending planning...\n"

    def _get_available_agents(self) -> list[str]:
        """Scans the repository for available specialized agent classes."""
        agents = []
        # Target the core agent source directories
        ws_root = getattr(self, "_workspace_root", None) or Path.cwd()
        src_path = Path(ws_root) / "src"

        # Scan src/data/agents, src/logic/agents, and orchestration folders
        for p in src_path.rglob("*_agent.py"):
            if p.name not in ["base_agent.py", "director_agent.py"]:
                # Convert snake_case to PascalCase for easier LLM identification
                name = "".join(part.capitalize() for part in p.stem.split("_"))
                agents.append(name)

        # Ensure we unique and sort
        return sorted(list(set(agents)))

    def _handle_agent_failure(self, event: dict) -> str:
        """React to agent failures broadcast on the signal registry."""
        sender = event.get("sender")
        data = event.get("data", {})
        logging.warning(f"Director received FAILURE signal from {sender}: {data}")
        # In the future, this could trigger a retry with a different agent or strategy

    def _handle_agent_success(self, event: dict) -> str:
        """React to agent successes broadcast on the signal registry."""
        sender = event.get("sender")
        data = event.get("data", {})
        logging.info(f"Director received SUCCESS signal from {sender}: {data}")

    async def think(self, prompt: str) -> str:
        """Entry point for the DirectorAgent to handle tasks."""
        # Prevent recursive planning cycles
        if getattr(self, "_is_planning", False):
            return await super().think(prompt)

        # If the prompt suggests a new project, trigger the planner
        if "Improvement Task:" in prompt or "Project Goal:" in prompt:
            self._is_planning = True
            try:
                return await self.execute_project_plan(prompt)
            finally:
                self._is_planning = False

        # Otherwise, fall back to standard thinking/planning
        return await super().think(prompt)

    async def execute_project_plan(self, high_level_goal: str) -> str:
        """Decomposes a goal and executes delegations."""
        available = self._get_available_agents()
        logging.info(f"Director planning for: {high_level_goal}. Available specialists: {available}")

        improvement_title = None
        if "Improvement Task:" in high_level_goal:
            improvement_title = high_level_goal.replace("Improvement Task:", "").strip()

        self.status.start_project(high_level_goal, 0)

        # Step 1: Ask the LLM to generate a JSON plan
        # We use super().think() directly to avoid the project-triggering logic in self.think()
        planning_prompt = (
            f"Given the project goal: '{high_level_goal}'\n"
            f"Available specialized agents in the framework: {', '.join(available)}\n\n"
            "Analyze the workspace and generate a step-by-step execution plan. "
            "Output your plan as a JSON list of objects, each with 'agent', 'file', and 'prompt' keys."
        )

        raw_plan = await super().think(planning_prompt)

        try:
            # Try to extract JSON from the LLM response
            json_match = re.search(r"\[.*\]", raw_plan, re.DOTALL)
            if not json_match:
                error_prefix = "Plan generation failed. LLM did not provide a valid JSON list."
                error_msg = f"{error_prefix} Response: {raw_plan[:200]}"
                self.status.finish_project(success=False)
                return error_msg

            plan = json.loads(json_match.group(0))
            results = []

            # Record all steps first
            for step in plan:
                self.status.add_step(step.get("agent"), step.get("file"), step.get("prompt"))

            for i, step in enumerate(plan):
                agent_type = step.get("agent")
                target_file = step.get("file")
                sub_prompt = step.get("prompt")

                self.status.update_step_status(i, "Running")
                logging.info(f"Step {i + 1}: Delegating {agent_type} -> {target_file}")

                try:
                    res = await self.delegate_to(agent_type, sub_prompt, target_file)

                    results.append(f"### Step {i + 1}: {agent_type} on {target_file}\n{res}\n")
                    self.status.update_step_status(i, "Completed", res[:100] + "...")
                except Exception as step_error:  # pylint: disable=broad-exception-caught
                    logging.error(f"Step {i + 1} failed: {step_error}")

                    results.append(f"### Step {i + 1}: {agent_type} FAILED\n{str(step_error)}\n")
                    self.status.update_step_status(i, "Failed", str(step_error))

            self.status.finish_project(success=True)

            if improvement_title:
                self._update_improvement_status(improvement_title, "COMPLETED")

            return "# Plan Execution Results\n\n" + "\n".join(results)

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"Execution failed: {e}")
            self.status.finish_project(success=False)
            return f"Error executing plan: {str(e)}\n\nOriginal Plan Output:\n{raw_plan}"

    def _update_improvement_status(self, title: str, status: str) -> None:
        """Updates the status of an improvement in the tracking file."""
        if not self.file_path.exists():
            return

        try:
            content = self.file_path.read_text(encoding="utf-8")
            # Look for the title and the status line following it
            # Format: **Title**\n   - Status: OLD_STATUS
            pattern = re.compile(rf"\*\*{re.escape(title)}\*\*\n\s+-\s+Status:\s+([A-Z/ ()\w]+)", re.MULTILINE)

            match = pattern.search(content)
            if match:
                old_status_line = match.group(0)
                new_status_line = old_status_line.replace(match.group(1), status)
                new_content = content.replace(old_status_line, new_status_line)
                self.file_path.write_text(new_content, encoding="utf-8")
                logging.info(f"Updated status for '{title}' to {status} in {self.file_path.name}")
            else:
                logging.warning(f"Could not find improvement '{title}' in {self.file_path.name}")
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"Failed to update improvement status: {e}")

    async def improve_content(self, prompt: str) -> str:
        """Override improve_content to perform the orchestration."""
        return await self.execute_project_plan(prompt)


if __name__ == "__main__":
    main = create_main_function(DirectorAgent, "Director Agent", "Goal/Project to orchestrate")
    main()
