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
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.Version import VERSION
import logging
import time
from typing import TYPE_CHECKING
from src.core.base.BaseAgent import BaseAgent

__version__ = VERSION

if TYPE_CHECKING:
    from .FleetManager import FleetManager


class FleetLifecycleManager:
    """Handles agent lifecycle operations (mitosis, differentiation, apoptosis) for the Fleet."""

    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet

    def cell_divide(self, agent_name: str) -> str:
        """Simulates biological mitosis by creating a clone of an existing agent."""
        if agent_name not in self.fleet.agents:
            return f"Error: Agent {agent_name} not found for division."

        base_agent = self.fleet.agents[agent_name]
        clone_name = f"{agent_name}_clone_{int(time.time())}"
        self.fleet.agents[clone_name] = base_agent

        logging.info(f"Mitosis: {agent_name} divided into {clone_name}")
        self.fleet.signals.emit(
            "CELL_DIVIDED",
            {"parent": agent_name, "child": clone_name},
            sender="FleetManager",
        )
        return f"Agent {agent_name} successfully divided into {clone_name}."

    def cell_differentiate(self, agent_name: str, specialization: str) -> str:
        """Changes an agent's characteristics or 'role' based on environmental signals."""
        if agent_name not in self.fleet.agents:
            return f"Error: Agent {agent_name} not found for differentiation."

        logging.info(f"Differentiation: {agent_name} specialized into {specialization}")
        self.fleet.signals.emit(
            "CELL_DIFFERENTIATED",
            {"agent": agent_name, "specialization": specialization},
            sender="FleetManager",
        )
        return f"Agent {agent_name} successfully differentiated into {specialization}."

    def cell_apoptosis(self, agent_name: str) -> str:
        """Cleanly shuts down and removes an agent from the fleet (programmed cell death)."""
        if agent_name not in self.fleet.agents:
            return f"Error: Agent {agent_name} not found for apoptosis."

        del self.fleet.agents[agent_name]
        logging.info(f"Apoptosis: {agent_name} has been recycled.")
        self.fleet.signals.emit(
            "CELL_APOPTOSIS", {"agent": agent_name}, sender="FleetManager"
        )
        return f"Agent {agent_name} successfully removed from the fleet."

    def register_agent(
        self, name: str, agent_class: type[BaseAgent], file_path: str | None = None
    ) -> str:
        """Adds an agent to the fleet."""
        path = file_path or str(self.fleet.workspace_root / f"agent_{name.lower()}.py")
        agent = agent_class(path)
        # Inject fleet reference (Phase 123)
        if hasattr(agent, "fleet"):
            agent.fleet = self.fleet

        # Register tools with the fleet registry (Phase 123 Integration)
        if (
            hasattr(agent, "register_tools")
            and hasattr(self.fleet, "registry")
            and self.fleet.registry
        ):
            try:
                agent.register_tools(self.fleet.registry)
                logging.debug(f"Fleet: Registered tools for agent '{name}'")
            except Exception as e:
                logging.error(
                    f"Fleet: Failed to register tools for agent '{name}': {e}"
                )

        self.fleet.agents[name] = agent
        logging.info(f"Registered agent: {name}")
        return f"Agent {name} registered."
