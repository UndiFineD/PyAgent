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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Agent specializing in Project Management and Multi-Agent Orchestration."""




from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import create_main_function
from src.infrastructure.orchestration.StatusManager import StatusManager
import logging
import os
import json
import importlib
from pathlib import Path
from typing import List

class DirectorAgent(BaseAgent):
    """Orchestrator agent that decomposes complex tasks and delegates to specialists."""
    
    def __init__(self, file_path: str) -> None:
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
            "- SearchAgent: For web research.\n"
            "- TestsAgent: For unit testing.\n"
            "- SecurityAgent: For auditing.\n"
            "- ArchitectAgent: For system design.\n\n"
            "When given a task, break it down into steps. For each step, specify:\n"
            "1. The target file.\n"
            "2. The agent type to use.\n"
            "3. The specific prompt/instruction for that agent.\n\n"
            "You can execute these delegations sequentially to achieve a high-level project goal."
        )

    def _get_default_content(self) -> str:
        return "# Project Orchestration Plan\n\n## Goal\n[Goal here]\n\n## Sequence\n- Pending planning...\n"

    def _get_available_agents(self) -> List[str]:
        """Scans the src/classes directory for available agent classes."""
        agents = []
        classes_path = Path(__file__).parent.parent
        for p in classes_path.rglob("*Agent.py"):
            if p.name != "BaseAgent.py":
                agents.append(p.stem)
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

    def execute_project_plan(self, high_level_goal: str) -> str:
        """Decomposes a goal and executes delegations."""
        available = self._get_available_agents()
        logging.info(f"Director planning for: {high_level_goal}. Available specialists: {available}")
        
        self.status.start_project(high_level_goal, 0)
        
        # Step 1: Ask the LLM to generate a JSON plan
        planning_prompt = (
            f"Given the project goal: '{high_level_goal}'\n"
            f"Available specialized agents in the framework: {', '.join(available)}\n\n"
            "Analyze the workspace and generate a step-by-step execution plan. "
            "Output your plan as a JSON list of objects, each with 'agent', 'file', and 'prompt' keys."
        )
        
        raw_plan = super().improve_content(planning_prompt)
        
        try:
            # Try to extract JSON from the LLM response
            import re
            json_match = re.search(r"\[.*\]", raw_plan, re.DOTALL)
            if not json_match:
                error_msg = f"Plan generation failed. LLM did not provide a valid JSON list. Response: {raw_plan[:200]}"
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
                logging.info(f"Step {i+1}: Delegating {agent_type} -> {target_file}")
                
                try:
                    res = self.delegate_to(agent_type, sub_prompt, target_file)
                    results.append(f"### Step {i+1}: {agent_type} on {target_file}\n{res}\n")
                    self.status.update_step_status(i, "Completed", res[:100] + "...")
                except Exception as step_error:
                    logging.error(f"Step {i+1} failed: {step_error}")
                    results.append(f"### Step {i+1}: {agent_type} FAILED\n{str(step_error)}\n")
                    self.status.update_step_status(i, "Failed", str(step_error))
            
            self.status.finish_project(success=True)
            return "# Plan Execution Results\n\n" + "\n".join(results)

        except Exception as e:
            logging.error(f"Execution failed: {e}")
            self.status.finish_project(success=False)
            return f"Error executing plan: {str(e)}\n\nOriginal Plan Output:\n{raw_plan}"

    def improve_content(self, prompt: str) -> str:
        """Override improve_content to perform the orchestration."""
        return self.execute_project_plan(prompt)

if __name__ == "__main__":
    main = create_main_function(DirectorAgent, "Director Agent", "Goal/Project to orchestrate")
    main()
