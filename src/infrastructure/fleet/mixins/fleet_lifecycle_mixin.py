# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.infrastructure.fleet.fleet_manager import FleetManager
    from src.core.base.base_agent import BaseAgent

class FleetLifecycleMixin:
    """Mixin for agent lifecycle and biological swarm patterns in FleetManager."""

    def register_agent(
        self: FleetManager, name: str, agent_class: type[BaseAgent], file_path: str | None = None
    ) -> str:
        """Adds an agent to the fleet."""
        return self.lifecycle_manager.register_agent(name, agent_class, file_path)

    def cell_divide(self: FleetManager, agent_name: str) -> str:
        """Simulates biological mitosis."""
        return self.lifecycle_manager.cell_divide(agent_name)

    def cell_differentiate(self: FleetManager, agent_name: str, specialization: str) -> str:
        """Changes an agent's characteristics."""
        return self.lifecycle_manager.cell_differentiate(agent_name, specialization)

    def cell_apoptosis(self: FleetManager, agent_name: str) -> str:
        """Cleanly shuts down and removes an agent."""
        return self.lifecycle_manager.cell_apoptosis(agent_name)
