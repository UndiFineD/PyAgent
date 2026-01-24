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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Core logic for multi-agent orchestration and workflow management.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable, Dict, List

from .base_core import BaseCore
from .models import ComposedAgent

if TYPE_CHECKING:
    pass


class OrchestrationCore(BaseCore):
    """
    Authoritative engine for multi-agent workflows.
    """

    def __init__(self) -> None:
        super().__init__()
        self.agents: List[ComposedAgent] = []
        self.results: Dict[str, str] = {}
        self.execution_order: List[str] = []

    def add_agent(self, agent: ComposedAgent) -> None:
        """
        Adds an agent to the orchestration registry.
        """
        self.agents.append(agent)
        self._calculate_execution_order()

    def _calculate_execution_order(self) -> None:
        """
        Computes the topological sort of agents based on dependencies.
        """
        sorted_agents: List[str] = []
        visited: set[str] = set()
        temp: set[str] = set()

        def visit(agent_type: str) -> None:
            if agent_type in temp:
                raise ValueError(f"Circular dependency for {agent_type}")
            if agent_type in visited:
                return
            temp.add(agent_type)
            agent = next((a for a in self.agents if a.agent_type == agent_type), None)
            if agent:
                for dep in agent.depends_on:
                    visit(dep)
            temp.remove(agent_type)
            visited.add(agent_type)
            sorted_agents.append(agent_type)

        for agent in sorted(self.agents, key=lambda a: a.order):
            if agent.agent_type not in visited:
                visit(agent.agent_type)
        self.execution_order = sorted_agents

    def execute_workflow(
        self,
        file_path: str,
        prompt: str,
        agent_factory: Callable[[str, str], Any],
    ) -> Dict[str, str]:
        """
        Executes the registered agents in the calculated order.
        """
        self.results.clear()
        current_content = ""
        for agent_type in self.execution_order:
            agent_config = next((a for a in self.agents if a.agent_type == agent_type), None)
            if not agent_config:
                continue
            agent = agent_factory(agent_type, file_path)
            enhanced_prompt = prompt
            for dep in agent_config.depends_on:
                if dep in self.results:
                    enhanced_prompt += f"\n\nPrevious {dep} result:\n{self.results[dep][:500]}"
            if current_content and hasattr(agent, "previous_content"):
                agent.previous_content = current_content
            result = agent.improve_content(enhanced_prompt)
            self.results[agent_type] = result
            current_content = result
        return self.results


@dataclass
class QualityScorer:
    """
    Evaluates text quality based on weighted criteria.
    """

    criteria: Dict[str, tuple[Callable[[str], float], float]] = field(default_factory=dict)

    def add_criterion(self, name: str, func: Callable[[str], float], weight: float = 1.0) -> None:
        """
        Adds a single scoring criterion.
        """
        self.criteria[name] = (func, weight)

    def score(self, text: str) -> float:
        """
        Calculates the weighted average score for a given text.
        """
        if not self.criteria:
            return min(1.0, len(text) / 200.0)
        total_weight, total_score = 0.0, 0.0
        for func, weight in self.criteria.values():
            total_score += func(text) * weight
            total_weight += weight
        return total_score / total_weight if total_weight > 0 else 0.0


@dataclass
class ABTest:
    """
    Simple A/B testing harness for variants.
    """

    name: str
    variants: List[str]
    weights: List[float] = field(default_factory=list)
    variant_counts: Dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for v in self.variants:
            self.variant_counts[v] = 0
        if not self.weights:
            self.weights = [1.0 / len(self.variants)] * len(self.variants)

    def select_variant(self) -> str:
        """
        Selects a variant based on defined weights.
        """
        return random.choices(self.variants, weights=self.weights, k=1)[0]
