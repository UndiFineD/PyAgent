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
from src.core.base.lifecycle.version import VERSION
import logging
from typing import Any
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.base_utilities import as_tool
from src.logic.agents.system.core.morphology_core import MorphologyCore

__version__ = VERSION


class MorphologicalEvolutionAgent(BaseAgent):
    """
    Phase 37: Morphological Code Generation.
    Analyzes API usage patterns and evolves the fleet's class structures.
    Integrated with MorphologyCore for Agent DNA and Splitting/Merging logic.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.capabilities.append("MorphologicalEvolution")
        self.core = MorphologyCore()

    def generate_agent_dna(self, agent_instance: BaseAgent) -> str:
        """
        Generates DNA for an agent instance for persistence and replication.
        """
        return self.core.encode_agent_dna(
            name=agent_instance.__class__.__name__,
            tools=[t["name"] for t in (getattr(agent_instance, "tools", []) or [])],
            prompt=getattr(agent_instance, "_system_prompt", ""),
            model="gpt-4o",  # Default
        )

    def check_for_merge_opportunity(
        self, agent_a_paths: list[str], agent_b_paths: list[str]
    ) -> bool:
        """
        Checks if two agents should merge based on path overlap.
        """
        overlap = self.core.calculate_path_overlap(agent_a_paths, agent_b_paths)
        if overlap > 0.8:
            logging.warning(
                f"MorphologicalEvolution: High overlap ({overlap:.2f}) detected. MERGE recommended."
            )
            return True
        return False

    @as_tool
    def MorphologicalEvolution(self, agent_name: str, call_logs: list[dict[str, Any]]) -> dict[str, Any]:
        """Alias for morphological analysis used by fleet."""
        return self.analyze_api_morphology(agent_name, call_logs)

    @as_tool
    def analyze_api_morphology(
        self, agent_name: str, call_logs: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Analyzes how an agent is being used and proposes a morphological evolution.
        """
        logging.info(
            f"MorphologicalEvolution: Analyzing usage patterns for {agent_name}"
        )

        # Determine if the agent is 'overloaded' or has 'redundant' parameters
        param_usage: dict[Any, Any] = {}
        for log in call_logs:
            for p in log.get("params", []):
                param_usage[p] = param_usage.get(p, 0) + 1

        # Propose a flattened or optimized interface
        proposals = []
        if len(call_logs) > 10:
            proposals.append(
                {
                    "type": "INTERFACE_FLATTENING",
                    "description": f"Convert high-frequency calls in {agent_name} to specialized micro-tools.",
                    "target_file": f"src/logic/agents/specialized/{agent_name}.py",
                }
            )

        return {
            "agent": agent_name,
            "usage_summary": param_usage,
            "morphological_proposals": proposals,
            "evolution_readiness": 0.85,
        }

    def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        # Standard implementation
        return "Morphological Evolution Report: Proposing structural symmetry for fleet interfaces."
