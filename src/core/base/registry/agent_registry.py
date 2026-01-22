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
(Re-implemented using RegistryCore)
"""

from __future__ import annotations
import logging
from typing import TYPE_CHECKING
from src.core.base.common.registry_core import RegistryCore
from src.core.base.lifecycle.version import VERSION

if TYPE_CHECKING:
    from src.core.base.lifecycle.base_agent import BaseAgent

__version__ = VERSION


class AgentRegistry(RegistryCore["BaseAgent"]):
    """
    Singleton registry to track all active agents.
    Uses RegistryCore for thread-safe storage and hooks.
    """

    _instance: AgentRegistry | None = None

    def __new__(cls) -> AgentRegistry:
        if cls._instance is None:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
        return cls._instance

    def register(self, agent: BaseAgent) -> None:
        """Register an agent instance."""
        name = getattr(agent, "agent_name", str(id(agent)))
        self.register(name, agent)
        logging.debug(f"Agent '{name}' registered.")

    def unregister(self, name: str) -> None:
        """Unregister an agent instance."""
        if super().unregister(name):
            logging.debug(f"Agent '{name}' unregistered.")

    def get_agent(self, name: str) -> BaseAgent | None:
        """Retrieve an agent by name."""
        return self.get(name)

    def list_agents(self) -> list[str]:
        """List names of all registered agents."""
        return self.list_keys()

    @property
    def active_count(self) -> int:
        return len(self._items)
