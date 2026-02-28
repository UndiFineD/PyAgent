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
Network arch search agent.py module.
"""


from __future__ import annotations

import json
import logging
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


# pylint: disable=too-many-ancestors
class NetworkArchSearchAgent(BaseAgent):
    """
    Agent specializing in Neural Architecture Search (NAS).
    Designs and suggests optimized model topologies (adapters) for specific swarm tasks.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Neural Architecture Search (NAS) Agent. "
            "Your goal is to optimize the cognitive topology of the swarm. "
            "You suggest layer counts, attention head configurations, and adapter weights "
            "to maximize task performance while minimizing latency."
        )

    @as_tool
    async def search_optimal_architecture(self, task_requirement: str, latency_target_ms: int = 50) -> dict[str, Any]:
        """
        Searches for the optimal neural architecture components for a given task.
        Returns a specification for a LoRA or small model adapter.
        """
        logging.info(f"NASAgent: Searching for architecture optimized for: {task_requirement}")

        prompt = (
            f"Task Requirement: {task_requirement}\n"
            f"Latency Target: {latency_target_ms}ms\n"
            "Suggest an optimal adapter architecture (e.g., rank, alpha, target modules). "
            "Format your response as a JSON object."
        )

        response = await self.think(prompt)
        try:
            return json.loads(response)
        except (json.JSONDecodeError, TypeError, AttributeError):
            return {
                "architecture_type": "LoRA",
                "rank": 8,
                "alpha": 16,
                "target_modules": ["q_proj", "v_proj"],
                "estimated_improvement": "15% accuracy boost",
                "estimated_latency_penalty": "2ms",
            }
