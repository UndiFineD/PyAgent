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
Routing engine for task distribution.
(Facade for src.core.base.common.routing_core)
"""

import os
from typing import Any

from src.core.base.common.routing_core import \
    RoutingCore as StandardRoutingCore

# Assuming BackendHandlers should be imported or mocked if not found
from .backend_handlers import BackendHandlers


class RoutingEngine(StandardRoutingCore):
    """Facade for RoutingCore."""

    def select_provider(self, task_type="general", priority="balanced", federated=False):
        """Legacy compatibility wrapper."""
        if federated:
            return "federated_cluster"

        report = BackendHandlers.get_performance_report()
        preferred = os.environ.get("DV_AGENT_BACKEND", "github_models")

        if priority == "latency":
            # Select provider with lowest TTFT or highest TPS
            best_provider = preferred
            min_ttft = float("inf")
            for p, metrics in report.items():
                if metrics["ttft"] < min_ttft:
                    min_ttft = metrics["ttft"]
                    best_provider = p
            return best_provider

        if task_type == "classification" and not os.environ.get("DV_AGENT_BACKEND"):
            # Classification is often better on fast small models
            if "openai" in report and report["openai"]["ttft"] < 1.0:
                return "openai"

        if task_type == "reasoning":
            # Reasoning usually requires frontier models, prefer GitHub Models (defaulting to gpt-4o)
            return "github_models"

        return preferred

    @staticmethod
    def get_routing_stats() -> dict[str, Any]:
        """Returns statistics on routing decisions and provider health."""
        return {
            "active_metrics": BackendHandlers.get_performance_report(),
            "default_backend": os.environ.get("DV_AGENT_BACKEND", "github_models"),
        }
