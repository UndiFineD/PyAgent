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
<<<<<<< HEAD

import logging
from typing import Any

from src.core.base.common.registry_core import RegistryCore
from src.core.base.lifecycle.version import VERSION
=======
import logging
from typing import TYPE_CHECKING
from src.core.base.common.registry_core import RegistryCore
from src.core.base.lifecycle.version import VERSION

if TYPE_CHECKING:
    from src.core.base.lifecycle.base_agent import BaseAgent
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

__version__ = VERSION

<<<<<<< HEAD
__version__: str = VERSION

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

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

<<<<<<< HEAD
    def __init__(self, **_kwargs: Any) -> None:
        if not hasattr(self, "_initialized"):
            super().__init__(name="AgentRegistry")
            self._initialized = True

    def register_instance(self, agent) -> bool:
        """
        Register an agent instance using its internal agent_name.
        Args:
            agent: The agent instance to register.
        Returns:
            bool: True if registration succeeded, False otherwise.
        """
        name: str = getattr(agent, "agent_name", str(id(agent)))
        success: bool = super().register(name, agent)
        if success:
            logging.debug("Agent '%s' registered.", name)
        return success

    def unregister_instance(self, name: str) -> bool:
        """
        Unregister an agent instance by name.
        Args:
            name (str): The name of the agent to unregister.
        Returns:
            bool: True if the agent was unregistered, False otherwise.
        """
        success = super().unregister(name)
        if success:
            logging.debug("Agent '%s' unregistered.", name)
        return bool(success)

    def get_agent(self, name: str) -> Any | None:
        """
        Retrieve an agent by name.
        Args:
            name (str): The name of the agent to retrieve.
        Returns:
            BaseAgent | None: The agent instance if found, else None.
        """
        return self.get(name)

    def list_agents(self) -> list[str]:
        """
        List names of all registered agents.
        Returns:
            list[str]: List of registered agent names.
        """
=======
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
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return self.list_keys()

    @property
    def active_count(self) -> int:
<<<<<<< HEAD
        """
        Return the number of active agents.
        Returns:
            int: Number of active agents.
        """
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return len(self._items)
