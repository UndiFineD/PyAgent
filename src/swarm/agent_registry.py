#!/usr/bin/env python3
"""Registry to manage agent registrations and heartbeats."""
# Copyright 2026 PyAgent Authors
#
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

import time
from typing import Any


class AgentRegistry:
    """Registry to manage agent registrations and heartbeats."""

    def __init__(self, heartbeat_interval: float = 30.0) -> None:
        """Initialize the agent registry with a heartbeat interval for health checks."""
        self.heartbeat_interval = heartbeat_interval
        self._agents: dict[str, dict[str, Any]] = {}

    def register(self, agent_type: str, capabilities: list[str]) -> str:
        """Register a new agent and return its ID."""
        aid = f"agent-{len(self._agents) + 1}"
        self._agents[aid] = {
            "type": agent_type,
            "capabilities": capabilities,
            "last_seen": time.time(),
        }
        return aid

    def heartbeat(self, agent_id: str) -> None:
        """Update the last seen time for the given agent ID."""
        self._agents[agent_id]["last_seen"] = time.time()

    def get(self, agent_id: str) -> dict[str, Any]:
        """Get the agent info for the given agent ID."""
        return self._agents[agent_id]

    def is_healthy(self, agent_id: str) -> bool:
        """Check if the agent is healthy based on its last heartbeat."""
        # cast stored timestamp to float so mypy can reason correctly
        from typing import cast

        last = cast(float, self._agents[agent_id]["last_seen"])
        return (time.time() - last) < self.heartbeat_interval

    def metrics(self) -> str:
        """Return a string in Prometheus text format with metrics about the agents."""
        now = time.time()
        healthy_agents = sum(
            1 for info in self._agents.values() if (now - float(info.get("last_seen", 0.0))) < self.heartbeat_interval
        )

        lines = [
            f"agent_registered_total {len(self._agents)}",
            f"agent_healthy_total {healthy_agents}",
            f"agent_unhealthy_total {len(self._agents) - healthy_agents}",
            f"agent_heartbeat_interval_seconds {self.heartbeat_interval}",
        ]
        return "\n".join(lines)
