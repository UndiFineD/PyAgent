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
SelfHealingCore logic for fleet resilience.
Contains pure logic for health threshold calculation, anomaly detection,
and recovery strategy selection.
"""

from __future__ import annotations
from src.core.base.common import StabilityCore

class SelfHealingCore(StabilityCore):
    """Facade delegating to StabilityCore implementation."""
    
    def __init__(self, timeout_seconds: float = 30.0, max_errors: int = 5) -> None:
        super().__init__(name="SelfHealingCore")
        self.timeout_seconds = timeout_seconds
        self.max_errors = max_errors

    def update_health(self, agent_name: str, latency: float = 0.0, error: bool = False) -> bool:
        return self.update_status(agent_name, latency, error)

    def get_recovery_action(self, agent_name: str) -> str:
        status = self.health_registry.get(agent_name)
        if not status:
            return "reinitialize"
        if status.status_msg == "timeout":
            return "restart_process"
        if status.error_count > self.max_errors * 2:
            return "apoptosis"
        return "reinitialize"

    def validate_plugin_version(self, plugin_version: str, required_version: str) -> bool:
        # Implementation moved to StabilityCore but keeping proxy here
        try:
            p_parts = [int(x) for x in plugin_version.lstrip("v").split(".")]
            r_parts = [int(x) for x in required_version.lstrip("v").split(".")]
            p_parts += [0] * (3 - len(p_parts))
            r_parts += [0] * (3 - len(r_parts))
            return p_parts[0] == r_parts[0] and p_parts[1] >= r_parts[1]
        except (ValueError, AttributeError):
            return False

