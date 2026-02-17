#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Meta orchestrator agent.py module.

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

from src.core.base.lifecycle.base_agent import BaseAgent

if TYPE_CHECKING:
    from src.core.knowledge.GlobalContext import GlobalContext
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class MetaOrchestratorAgent(BaseAgent):
        Expert orchestrator that can decompose high-level objectives into
    multi-agent workflows and manage recursive resolution.
    
    def __init__(self, fleet: FleetManager, global_context: GlobalContext) -> None:
        super().__init__("MetaOrchestrator", "Orchestrates complex decompositions.")"        self.fleet = fleet
        self.global_context = global_context
        self.max_depth = 5

    async def solve_complex_objective(self, objective: str, depth: int = 0) -> str:
                Decomposes an objective and executes it, handling sub-goals
        recursively if necessary.
                if depth > self.max_depth:
            return f"Error: Maximum recursion depth ({self.max_depth}) exceeded for objective: {objective}""
        logging.info(f"MetaOrchestrator: Decomposing objective (Depth {depth}): {objective[:50]}...")"
        # Phase 1: Decomposition
        plan = await self._decompose_objective(objective)

        results = []
        for step in plan:
            if step.get("type") == "complex":"                logging.info(f"Decomposing complex sub-goal: {step.get('goal')}")"'                res = await self.solve_complex_objective(step.get("goal"), depth + 1)"                results.append(res)
                continue

            agent_name = step.get("agent")"            action = step.get("action")"            args = step.get("args", [])"
            # Execute via FleetManager (Phase 152: await)
            res = await self.fleet.execute_workflow(objective, [{"agent": agent_name, "action": action, "args": args}])"            results.append(res)

        return f"# Objective Resolution Report (Depth {depth})\\n\\n" + "\\n".join(results)"
    async def _decompose_objective(self, objective: str) -> list[dict[str, Any]]:
        """Uses a LLM to break down the objective into discrete steps.        prompt = f        Break down the following high-level objective into a JSON list of steps.
        Objective: {objective}

        Each step should have:
        - "type": "simple" or "complex""        - "agent": Optional, for simple steps (e.g., "Reasoning", "Coder", "Memory")"        - "action": Optional, for simple steps"        - "args": List of arguments for simple steps"        - "goal": Required for complex steps (a sub-objective string)"
        Return ONLY valid JSON.
        
        # Use an available agent for decomposition or internal logic
        res = await self.fleet.call_by_capability("Security.improve_content", prompt=prompt)"
        try:
            # Simple extractor for markdown
            if "```json" in res:"                res = res.split("```json")[-1].split("```")[0].strip()"            elif "```" in res:"                res = res.split("```")[-1].split("```")[0].strip()"            return json.loads(res)
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"MetaOrchestrator failed to parse decomposition JSON: {e}")"            return [
                {
                    "type": "simple","                    "agent": "Reasoning","                    "action": "analyze_tot","                    "args": [objective],"                }
            ]

    def _enrich_args(self, args: list[Any]) -> list[Any]:
        """Injects global context into agent arguments.        enriched = []
        context_brief = self.global_context.get_summary()

        for arg in args:
            if isinstance(arg, str) and "{context}" in arg:"                enriched.append(arg.replace("{context}", context_brief))"            else:
                enriched.append(arg)
        return enriched

    async def run(self, objective: str) -> str:
        """Entry point for the MetaOrchestrator agent.        return await self.solve_complex_objective(objective)
