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


"""Agent responsible for merging specialized agent capabilities."""

from __future__ import annotations

import logging
import os
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.base_utilities import as_tool

__version__ = VERSION


# pylint: disable=too-many-ancestors
class SynthesisAgent(BaseAgent):
    """
    Tier 2 (Cognitive Logic) - Synthesis Agent: Responsible for Swarm Synthesis,
    merging specialized agent capabilities into optimized super-agent architectures.
    """

    def __init__(self, workspace_root: str) -> None:
        # Initialize with a dummy path as base_agent needs a file path
        dummy_path = os.path.join(
            workspace_root, r"src\logic\agents\cognitive\synthesis_agent.py"
        )
        super().__init__(dummy_path)
        self.workspace_root = workspace_root
        self._system_prompt = (
            "You are the Synthesis Agent. "
            "Your goal is to merge distinct agent capabilities into high-performance Super-Agents. "
            "You create new Python class files that combine multiple tools into a cohesive whole, "
            "optimizing for reduced inter-agent communication overhead."
        )

    @as_tool
    async def fuse_agents(
        self, agent_names: list[str], new_agent_name: str
    ) -> dict[str, Any]:
        """
        Creates a new agent that combines functionalities of multiple source agents.

        Args:
            agent_names: List of existing agent class names to fuse.
            new_agent_name: The name of the new fused agent class.
        """
        logging.info(f"SynthesisAgent: Fusing {agent_names} into {new_agent_name}")

        # Step 1: Analyze the source agents (simulated)
        # We would normally read their files and extract tools.

        # Step 2: Use LLM to generate fused agent code
        prompt = (
            f"I want to create a new agent named {new_agent_name} that combines the features "
            f"of these source agents: {', '.join(agent_names)}.\n"
            "The new agent should inherit from BaseAgent and use the @as_tool decorator "
            "for all combined capabilities.\n"
            "Generate the full Python code for this new agent class. include all necessary imports.\n"
            "Make sure the class name is exactly " + new_agent_name + "."
        )

        agent_code = await self.think(prompt)

        # Clean up code markup if present
        if "```python" in agent_code:
            agent_code = agent_code.split("```python")[1].split("```")[0].strip()
        elif "```" in agent_code:
            agent_code = agent_code.split("```")[1].split("```")[0].strip()

        # Step 3: Save the new agent file atomically
        target_dir = os.path.join(self.workspace_root, "src/agents")
        os.makedirs(target_dir, exist_ok=True)
        file_path = os.path.join(target_dir, f"{new_agent_name}.py")
        temp_path = file_path + ".tmp"

        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(agent_code)

            # Atomic rename
            os.replace(temp_path, file_path)

            logging.info(f"SynthesisAgent: Successfully created {file_path}")

            return {
                "status": "success",
                "new_agent": new_agent_name,
                "file_path": file_path,
                "components_fused": agent_names,
            }
        except (OSError, IOError) as e:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except (OSError, IOError):
                    pass
            logging.error(f"SynthesisAgent: Failed to save fused agent atomically: {e}")
            return {"status": "error", "message": str(e)}

    @as_tool
    def analyze_fusion_candidates(
        self, fleet_agents: list[str]
    ) -> list[dict[str, Any]]:
        """
        Analyzes the fleet to suggest which agents should be fused based on usage patterns.
        """
        _ = fleet_agents
        logging.info("SynthesisAgent: Analyzing fleet for fusion candidates.")
        # This would typically use telemetry to find agents that frequently call each other.
        # For now, we suggest a logical fusion.
        return [
            {
                "agents": ["ReasoningAgent", "ReflectionAgent"],
                "target": "CognitiveSuperAgent",
                "reason": "High frequency of sequential calling in reasoning loops",
            }
        ]
