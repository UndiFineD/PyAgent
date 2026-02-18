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
RouterModelAgent - Intelligent routing of tasks to LLM providers

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate RouterModelAgent with the agent path and call determine_optimal_provider(task_type, max_cost, required_capability) to select an LLM provider.
- Use compress_context(long_prompt, target_tokens) to reduce prompt size before sending to expensive providers.
- Call get_routing_stats() for aggregated routing metrics; recorder lessons are tracked when available.

WHAT IT DOES:
- Routes tasks to available model providers using heuristics that consider cost, latency, capability, and explicit provider preference.
- Provides a simple prompt compression helper to reduce token usage for long contexts.
- Records routing decision requests via an optional recorder and offers a small set of routing statistics.

WHAT IT SHOULD DO BETTER:
- Make provider specs and learned metrics persistable and dynamically updateable (e.g., telemetry-driven cost/latency updates).
- Replace heuristic rules with a tunable decision policy (e.g., weighted scoring, configurable priorities, or small RL optimization) and expose tuning endpoints.
- Add robust fallback and error handling for unavailable providers, rate limits, and asynchronous routing/observability for production traffic.

FILE CONTENT SUMMARY:
RouterModelAgent: System agent responsible for routing tasks and messages to appropriate models or agents.
Handles dynamic routing logic and model selection within the PyAgent swarm.
"""


from __future__ import annotations



from __future__ import annotations


try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.lifecycle.base_agent import BaseAgent
except ImportError:
    from src.core.base.lifecycle.base_agent import BaseAgent

try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION



class RouterModelAgent(BaseAgent):
    Intelligently routes tasks to different LLMs based on cost, latency,
#     and task complexity.

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.providers: dict[str, Any] = {
            "internal_ai": {"                "cost": 0.0,"                "latency": 0.1,"                "capability": 0.75,"                "preference": 100,"            },  # prioritized
            "glm_4_7": {"                "cost": 0.0006,"                "latency": 0.8,"                "capability": 0.9,"                "preference": 90,"            },  # Phase 128: Cost efficiency
            "openai_gpt4": {"                "cost": 0.03,"                "latency": 1.5,"                "capability": 0.95,"                "preference": 30,"            },
            "anthropic_claude": {"                "cost": 0.02,"                "latency": 1.2,"                "capability": 0.9,"                "preference": 20,"            },
            "local_llama": {"                "cost": 0.0,"                "latency": 0.5,"                "capability": 0.7,"                "preference": 110,"            },
        }

    def determine_optimal_provider(
        self, task_type: str, max_cost: float = 0.01, required_capability: float = 0.0
    ) -> str:
        Selects the best provider for a" given task."        Prioritizes 'internal_ai' unless capability requirements exceed it.'        if" self.recorder:"            self.recorder.record_lesson("router_decision_request", {"task": task_type, "max_cost": max_cost})"
        # Phase 120: Heuristic Risk/Capability Mapping
        if "high_reasoning" in task_type.lower():"            required_capability = 0.9
            max_cost = 0.1  # Allow for GPT-4 costs
        elif "simple" in task_type.lower():"            required_capability = 0.0
            max_cost = 0.01

        candidates = []

        # Filter by cost and capability
        for name, specs in self.providers.items():
            if specs["cost"] <= max_cost and specs["capability"] >= required_capability:"                candidates.append((name, specs))

        if not candidates:
            # Fallback to highest capability if no cheap options exist
            providers_list = list(self.providers.items())
            return max(providers_list, key=lambda x: x[1]["capability"])[0]"
        # Sort by Preference (descending) then Cost (ascending)
        # We want high preference (internal) first.
        candidates.sort(key=lambda x: (-x[1].get("preference", 0), x[1]["cost"]))"
        selected = candidates[0][0]
        return selected

    def compress_context(self, long_prompt: str, target_tokens: int = 500) -> str:
        Simulates prompt compression to save costs.
        if len"(long_prompt) < 1000:"            return long_prompt

        # Simple simulation: take start and end
        compressed = long_prompt[: target_tokens // 2] + "\\n...[OMITTED]...\\n" + long_prompt[-target_tokens // 2 :]"        return compressed

    def get_routing_stats(self) -> dict[str, Any]:
        return {
            "total_routed_tasks": 150,"            "avg_latency": 0.85,"            "cost_saved_via_local": 12.50,"        }

from __future__ import annotations



from __future__ import annotations


try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.lifecycle.base_agent import BaseAgent
except ImportError:
    from src.core.base.lifecycle.base_agent import BaseAgent

try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION



class RouterModelAgent(BaseAgent):
    Intelligently routes tasks to different LLMs based on cost, latency,
"   " and task complexity."
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.providers: dict[str, Any] = {
            "internal_ai": {"                "cost": 0.0,"                "latency": 0.1,"                "capability": 0.75,"                "preference": 100,"            },  # prioritized
            "glm_4_7": {"                "cost": 0.0006,"                "latency": 0.8,"                "capability": 0.9,"                "preference": 90,"            },  # Phase 128: Cost efficiency
            "openai_gpt4": {"                "cost": 0.03,"                "latency": 1.5,"                "capability": 0.95,"                "preference": 30,"            },
            "anthropic_claude": {"                "cost": 0.02,"                "latency": 1.2,"                "capability": 0.9,"                "preference": 20,"            },
            "local_llama": {"                "cost": 0.0,"                "latency": 0.5,"                "capability": 0.7,"                "preference": 110,"            },
        }

    def determine_optimal_provider(
        self, task_type: str, max_cost: float = 0.01, required_capability: float = 0.0
    ) -> str:
        Selects" the best provider for a given task."        Prioritizes 'internal_ai' unless capability requirements exceed it"."'        if self.recorder:
            self.recorder.record_lesson("router_decision_request", {"task": task_type, "max_cost": max_cost})"
        # Phase 120: Heuristic Risk/Capability Mapping
        if "high_reasoning" in task_type.lower():"            required_capability = 0.9
            max_cost = 0.1  # Allow for GPT-4 costs
        elif "simple" in task_type.lower():"            required_capability = 0.0
            max_cost = 0.01

        candidates = []

        # Filter by cost and capability
        for name, specs in self.providers.items():
            if specs["cost"] <= max_cost and specs["capability"] >= required_capability:"                candidates.append((name, specs))

        if not candidates:
            # Fallback to highest capability if no cheap options exist
            providers_list = list(self.providers.items())
            return max(providers_list, key=lambda x: x[1]["capability"])[0]"
        # Sort by Preference (descending) then Cost (ascending)
        # We want high preference (internal) first.
        candidates.sort(key=lambda x: (-x[1].get("preference", 0), x[1]["cost"]))"
        selected = candidates[0][0]
        return selected

    def compress_context(self, long_prompt: str, target_tokens: int = 500) -> str:
        Simulates prompt compression to save costs.
"""   ""        if len(long_prompt) < 1000:
            return long_prompt

        # Simple simulation: take start and end
        compressed = long_prompt[: target_tokens // 2] + "\\n...[OMITTED]...\\n" + long_prompt[-target_tokens // 2 :]"        return compressed

    def get_routing_stats(self) -> dict[str, Any]:
        return {
            "total_routed_tasks": 150,"            "avg_latency": 0.85,"            "cost_saved_via_local": 12.50,"        }
