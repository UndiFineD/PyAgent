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
import logging
from typing import Dict, List, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..fleet.FleetManager import FleetManager

class PhaseOrchestrator:
    """High-reliability task orchestrator using a 7-phase scientific method loop."""
    
    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet
        self.current_context: Dict[str, Any] = {}

    async def execute_task(self, task: str) -> str:
        """Runs the 7-phase cycle for a given task."""
        logging.info(f"PhaseOrchestrator: Starting 7-phase cycle for task: {task}")
        
        report = [f"# Phase Execution Report: {task}\n"]
        
        # Phase 1: OBSERVE
        observe_res = await self._phase_observe(task)
        report.append(f"## Phase 1: OBSERVE\n{observe_res}\n")
        
        # Phase 2: THINK
        think_res = await self._phase_think(task, observe_res)
        report.append(f"## Phase 2: THINK\n{think_res}\n")
        
        # Phase 3: DEFINE
        criteria = await self._phase_define(task)
        report.append(f"## Phase 3: DEFINE\n{criteria}\n")
        
        # Phase 4: PLAN
        plan = await self._phase_plan(task, think_res)
        report.append(f"## Phase 4: PLAN\n{plan}\n")
        
        # Phase 5: EXECUTE
        exec_res = await self._phase_execute(plan)
        report.append(f"## Phase 5: EXECUTE\n{exec_res}\n")
        
        # Phase 6: VERIFY
        verify_res = await self._phase_verify(exec_res, criteria)
        report.append(f"## Phase 6: VERIFY\n{verify_res}\n")
        
        # Phase 7: LEARN
        learn_res = await self._phase_learn(task, verify_res)
        report.append(f"## Phase 7: LEARN\n{learn_res}\n")
        
        return "\n".join(report)

    async def _phase_observe(self, task: str) -> str:
        """Gather initial facts."""
        return await self.fleet.call_by_capability("Security.improve_content", prompt=f"Observe the environment for task: {task}. What are the constraints and available tools?")

    async def _phase_think(self, task: str, observation: str) -> str:
        """Formulate a working hypothesis."""
        return await self.fleet.call_by_capability("Security.improve_content", prompt=f"Think about the task: {task}\nObservation: {observation}\nWhat is the hypothesis for success?")

    async def _phase_define(self, task: str) -> str:
        """Define verification criteria."""
        return await self.fleet.call_by_capability("Security.improve_content", prompt=f"Define verification criteria for: {task}")

    async def _phase_plan(self, task: str, thought: str) -> List[Dict[str, Any]]:
        """Synthesize steps."""
        prompt = f"Plan a PyAgent workflow for: {task}\nThought: {thought}\nOutput ONLY a JSON list of steps."
        res = await self.fleet.call_by_capability("Security.improve_content", prompt=prompt)
        # Parse JSON from result
        import json
        try:
            # Simple extractor for markdown
            if "```json" in res:
                res = res.split("```json")[-1].split("```")[0].strip()
            elif "```" in res:
                res = res.split("```")[-1].split("```")[0].strip()
            return json.loads(res)
        except Exception:
            logging.warning("Failed to parse JSON plan, using default reasoning step.")
            return [{"agent": "Reasoning", "action": "analyze_tot", "args": [task]}]

    async def _phase_execute(self, plan: List[Dict[str, Any]]) -> str:
        """Run the planned steps."""
        if not plan:
            return "Error: No plan generated in Phase 3."
        return await self.fleet.execute_workflow("7-Phase Execution", plan)

    async def _phase_verify(self, execution_result: str, criteria: str) -> str:
        """Compare execution results against build criteria."""
        return await self.fleet.call_by_capability("Security.improve_content", prompt=f"Verify if the result matches criteria.\nResult: {execution_result}\nCriteria: {criteria}")

    async def _phase_learn(self, task: str, verification: str) -> str:
        """Extract insights and update global context."""
        return await self.fleet.global_context.record_lesson(
            failure_context=task,
            error_msg="No error detected.",
            lesson=f"Verification results: {verification}"
        )