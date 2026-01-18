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


"""Engine for autonomous agent creation.
Allows agents to generate new, specialized agent files to expand fleet capabilities.
"""

from __future__ import annotations
from src.core.base.Version import VERSION
import logging
from pathlib import Path
from typing import Any
from .EvolutionCore import EvolutionCore

__version__ = VERSION


class EvolutionEngine:
    """
    Manages the autonomous generation of new agent types.
    Shell for EvolutionCore.
    """

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.output_dir = self.workspace_root / "src/generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.core = EvolutionCore()

    def generate_agent(
        self, name: str, capabilities: str, base_type: str = "BaseAgent"
    ) -> str:
        """Generates a new agent class file based on a name and capabilities description."""
        agent_filename = f"{name.lower()}_agent.py"
        target_path = self.output_dir / agent_filename

        template = self.core.generate_agent_template(name, capabilities, base_type)

        with open(target_path, "w") as f:
            f.write(template)

        logging.info(f"Evolution: Generated new agent {name} at {target_path}")
        return str(target_path)

    def optimize_hyperparameters(self, fleet_stats: dict[str, Any]) -> dict[str, Any]:
        """
        Phase 52: Evolutionary Neuro-Optimization.
        Delegates strategy to EvolutionCore.
        """
        return self.core.compute_mutations(fleet_stats)

    def register_generated_agent(self, fleet_manager: Any, name: str, path: str) -> str:
        """Dynamically loads and registers the generated agent into the fleet."""
        # For simulation, we'll just mock the dynamic import or use standard registration
        # In a real system, we'd use importlib.util.spec_from_file_location
        logging.info(f"Evolution: Registering generated agent {name} from {path}")
        # Note: FleetManager already has a register_agent method
        return f"Agent {name} registered."
