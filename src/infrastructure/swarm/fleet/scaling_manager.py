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


"""Manager for dynamic scaling of the agent fleet.
Monitors system load and spawns new agent instances as needed.
"""

from __future__ import annotations

import logging
import time

from src.core.base.lifecycle.version import VERSION

from .scaling_core import ScalingCore

__version__ = VERSION


class ScalingManager:
    """
    Shell for ScalingManager.
    Handles fleet orchestration while delegating logic to ScalingCore.
    """

    def __init__(self, fleet_manager) -> None:
        self.fleet = fleet_manager
        self.core = ScalingCore(scale_threshold=5.0, window_size=10, backoff_seconds=60)

    def record_metric(self, agent_name: str, value: float, metric_type: str = "latency") -> None:
        """Records a metric and checks if scaling is required."""
        self.core.add_metric(agent_name, value, metric_type=metric_type)

        if self.core.should_scale(agent_name):
            self._execute_scale_out(agent_name)

    def _execute_scale_out(self, agent_name: str) -> None:
        """Spawns a new instance of an agent if load is too high."""
        load_score = self.core.calculate_weighted_load(agent_name)
        logging.warning(f"SCALING: High load score ({load_score:.2f}) detected for {agent_name}. Spawning replica.")

        # Replica naming logic
        replica_name = f"{agent_name}_replica_{int(time.time())}"
        # Implementation depends on FleetManager dynamic registration
        if hasattr(self.fleet, "register_agent_runtime"):
            self.fleet.register_agent_runtime(replica_name, agent_name)

    def get_scaling_status(self) -> str:
        """Returns the current scaling status."""
        return f"Scaling Manager: Monitoring {len(self.core.load_metrics)} active agent archetypes."
