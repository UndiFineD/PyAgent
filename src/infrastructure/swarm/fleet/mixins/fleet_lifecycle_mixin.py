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
FleetLifecycleMixin
Fleet lifecycle mixin.py module.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.base.lifecycle.base_agent import BaseAgent
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class FleetLifecycleMixin:
    """Mixin for agent lifecycle and biological swarm patterns in FleetManager."""

    lifecycle_manager: FleetManager

    def register_agent(
        self, name: str, agent_class: type[BaseAgent], file_path: str | None = None
    ) -> str:
        """Adds an agent to the fleet."""
        return self.lifecycle_manager.register_agent(name, agent_class, file_path)

    def cell_divide(self, agent_name: str) -> str:
        """Simulates biological mitosis."""
        return self.lifecycle_manager.cell_divide(agent_name)

    def cell_differentiate(self, agent_name: str, specialization: str) -> str:
        """Changes an agent's characteristics."""
        return self.lifecycle_manager.cell_differentiate(agent_name, specialization)

    def cell_apoptosis(self, agent_name: str) -> str:
        """Cleanly shuts down and removes an agent."""
        return self.lifecycle_manager.cell_apoptosis(agent_name)
