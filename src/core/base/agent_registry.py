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
AgentRegistry: Central registry for all active agent instances.
Provides discovery and cross-agent communication.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from typing import TYPE_CHECKING

__version__ = VERSION

if TYPE_CHECKING:
    from src.core.base.base_agent import BaseAgent


class AgentRegistry:
    """Singleton registry to track all active agents."""

    _instance: AgentRegistry | None = None
    _agents: dict[str, BaseAgent] = {}

    def __new__(cls) -> AgentRegistry:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register(self, agent: BaseAgent) -> None:
        """Register an agent instance."""
        name = getattr(agent, "agent_name", str(id(agent)))
        self._agents[name] = agent
        logging.debug(f"Agent '{name}' registered.")

    def unregister(self, name: str) -> None:
        """Unregister an agent instance."""
        if name in self._agents:
            del self._agents[name]
            logging.debug(f"Agent '{name}' unregistered.")

    def get_agent(self, name: str) -> BaseAgent | None:
        """Retrieve an agent by name."""
        return self._agents.get(name)

    def list_agents(self) -> list[str]:
        """List names of all registered agents."""
        return list(self._agents.keys())

    @property
    def active_count(self) -> int:
        return len(self._agents)
