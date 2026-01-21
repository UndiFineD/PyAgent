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


from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
import logging
from typing import Any
from src.infrastructure.services.api.core.gateway_core import GatewayCore
from src.infrastructure.swarm.fleet.core.load_balancer_core import (
    LoadBalancerCore,
    AgentMetrics,
)

__version__ = VERSION


class FleetLoadBalancer:
    """
    GUI Improvements: Load Balancer for multi-interface traffic.
    Integrated with LoadBalancerCore for cognitive pressure distribution.
    """

    def __init__(self, fleet) -> None:
        self.fleet = fleet
        self.gateway_core = GatewayCore()
        self.lb_core = LoadBalancerCore()
        self.request_queue: list[dict[str, Any]] = []
        self.agent_metrics: dict[str, AgentMetrics] = {}

    def balance_request(self, interface: str, command: str) -> dict[str, Any]:
        """
        Routes the request to the most available resource or queues it.
        Assigns model based on Interface Affinity.
        """
        logging.info(
            f"LoadBalancer: Incoming request from {interface}: {command[:30]}..."
        )

        assigned_model = self.gateway_core.resolve_model_by_affinity(interface)

        # Simple simulation: If queue is large, increase latency or reject
        if len(self.request_queue) > 100:
            return {"status": "REJECTED", "reason": "High Traffic Load"}

        self.request_queue.append(
            {"interface": interface, "command": command, "model": assigned_model}
        )

        return {
            "status": "ACCEPTED",
            "interface": interface,
            "assigned_model": assigned_model,
            "estimated_wait_ms": len(self.request_queue) * 10,
        }

    def get_stats(self) -> dict[str, Any]:
        return {
            "queue_depth": len(self.request_queue),
            "interface_diversity": list(
                set(r["interface"] for r in self.request_queue)
            ),
        }
