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


"""Core logic for fleet stability, health monitoring, and anomaly detection."""


from __future__ import annotations

import contextlib
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

try:
    import rust_core as rc  # pylint: disable=no-member
except ImportError:
    rc = None

from .base_core import BaseCore


@dataclass
class HealthStatus:
    """Status tracking for individual agents or components."""
    component_id: str
    is_alive: bool = True
    last_seen: float = field(default_factory=time.time)
    error_count: int = 0
    latency_ms: float = 0.0
    status_msg: str = "ok"
    metrics: Dict[str, Any] = field(default_factory=dict)


class StabilityCore(BaseCore):
    """Standardized logic for fleet stability, health monitoring, and anomaly detection.
    Inherits from BaseCore for lifecycle and persistence.
    """

    def __init__(self, name: str = "StabilityCore", repo_root: Optional[str] = None) -> None:
        super().__init__(name=name, repo_root=repo_root)
        self.timeout_seconds: float = 30.0
        self.max_errors: int = 5
        self.health_registry: Dict[str, HealthStatus] = {}

    def update_status(self, component_id: str, latency: float = 0.0, error: bool = False, **metrics) -> bool:
        """Updates internal status for a component."""
        now = time.time()
        if component_id not in self.health_registry:
            self.health_registry[component_id] = HealthStatus(component_id)

        status = self.health_registry[component_id]
        status.last_seen = now
        status.latency_ms = latency
        status.metrics.update(metrics)

        if error:
            status.error_count += 1
        else:
            status.error_count = max(0, status.error_count - 1)

        status.is_alive = status.error_count < self.max_errors
        return status.is_alive


    def detect_failures(self) -> List[str]:
        """Returns a list of IDs that are considered failed."""
        now = time.time()

        if rc and hasattr(rc, "detect_failed_agents_rust"):
            with contextlib.suppress(Exception):
                agent_data = [
                    (name, status.last_seen, status.error_count, self.max_errors)
                    for name, status in self.health_registry.items()
                ]
                failures = rc.detect_failed_agents_rust(  # pylint: disable=no-member
                    agent_data, now, self.timeout_seconds
                )
                for name, reason in failures:
                    if name in self.health_registry:
                        self.health_registry[name].is_alive = False
                        self.health_registry[name].status_msg = reason
                return [name for name, _ in failures]

        failed = []
        for name, status in self.health_registry.items():
            if now - status.last_seen > self.timeout_seconds:
                status.is_alive = False
                status.status_msg = "timeout"
                failed.append(name)
            elif not status.is_alive:
                failed.append(name)
        return failed


    def get_fleet_health_score(self) -> float:
        """Returns a normalized score (0.0 to 1.0) of system health."""
        if not self.health_registry:
            return 1.0
        alive_count = sum(1 for s in self.health_registry.values() if s.is_alive)
        return alive_count / len(self.health_registry)
