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


"""Auto-extracted class from agent.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from typing import Any
import logging

__version__ = VERSION


class AgentPriorityQueue:
    """Priority queue for ordered agent execution.

    Executes agents in priority order with support for dependencies.

    Example:
        queue=AgentPriorityQueue()
        queue.add_agent("critical_fix", priority=1)
        queue.add_agent("tests", priority=5, depends_on=["critical_fix"])
        queue.add_agent("docs", priority=10)

        for agent in queue.get_execution_order():
            execute(agent)
    """

    def __init__(self) -> None:
        """Initialize priority queue."""
        self._agents: dict[str, dict[str, Any]] = {}

    def add_agent(
        self,
        name: str,
        priority: int = 5,
        depends_on: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Add agent to queue.

        Args:
            name: Agent name.
            priority: Priority (lower=higher priority).
            depends_on: List of agents this depends on.
            metadata: Optional metadata.
        """
        self._agents[name] = {
            "priority": priority,
            "depends_on": depends_on or [],
            "metadata": metadata or {},
        }

    def remove_agent(self, name: str) -> bool:
        """Remove agent from queue.

        Args:
            name: Agent name.

        Returns:
            True if removed, False if not found.
        """
        if name in self._agents:
            del self._agents[name]
            return True
        return False

    def get_execution_order(self) -> list[str]:
        """Get agents in execution order.

        Returns:
            List of agent names in order.
        """
        # Topological sort with priority
        executed: set[str] = set()
        order: list[str] = []

        while len(order) < len(self._agents):
            available: list[tuple[int, str]] = []

            for name, info in self._agents.items():
                if name in executed:
                    continue

                # Check if all dependencies are met
                deps_met = all(d in executed for d in info["depends_on"])
                if deps_met:
                    available.append((info["priority"], name))

            if not available:
                # Cycle detected or error
                remaining = [n for n in self._agents if n not in executed]
                logging.warning(
                    f"Dependency cycle detected, adding remaining: {remaining}"
                )
                order.extend(sorted(remaining))
                break

            # Sort by priority and take the highest priority
            available.sort()
            _, next_agent = available[0]
            order.append(next_agent)
            executed.add(next_agent)

        return order
