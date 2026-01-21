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
from src.core.base.version import VERSION
import time
import contextlib
from dataclasses import dataclass

try:
    import rust_core as rc
    HAS_RUST = True
except ImportError:
    HAS_RUST = False

__version__ = VERSION


@dataclass
class HealthStatus:
    """Status tracking for individual agents in the self-healing system."""

    agent_name: str
    is_alive: bool

    last_seen: float
    error_count: int = 0
    latency_ms: float = 0.0
    status_msg: str = "ok"


class SelfHealingCore:
    """Pure logic core for the SelfHealing orchestrator."""

    def __init__(self, timeout_seconds: float = 30.0, max_errors: int = 5) -> None:
        self.timeout_seconds = timeout_seconds
        self.max_errors = max_errors
        self.health_registry: dict[str, HealthStatus] = {}

    def update_health(
        self, agent_name: str, latency: float = 0.0, error: bool = False
    ) -> bool:
        """Updates internal status for an agent."""
        now = time.time()
        if agent_name not in self.health_registry:
            self.health_registry[agent_name] = HealthStatus(agent_name, True, now)

        status = self.health_registry[agent_name]
        status.last_seen = now
        status.latency_ms = latency
        if error:
            status.error_count += 1
        else:
            # Gradually decay error count on success
            status.error_count = max(0, status.error_count - 1)

        status.is_alive = status.error_count < self.max_errors
        return status.is_alive

    def detect_failures(self) -> list[str]:
        """Returns a list of agent names that are considered failed."""
        now = time.time()
        # Rust-accelerated failure detection
        if HAS_RUST:
            with contextlib.suppress(Exception):
                agent_data = [
                    (name, status.last_seen, status.error_count, self.max_errors)
                    for name, status in self.health_registry.items()
                ]
                failures = rc.detect_failed_agents_rust(agent_data, now, self.timeout_seconds)  # type: ignore[attr-defined]
                # Update statuses
                for name, reason in failures:
                    if name in self.health_registry:
                        self.health_registry[name].is_alive = False
                        self.health_registry[name].status_msg = reason
                return [name for name, _ in failures]

        failed = []
        for name, status in self.health_registry.items():
            # Time-based failure
            if now - status.last_seen > self.timeout_seconds:
                status.is_alive = False
                status.status_msg = "timeout"
                failed.append(name)
            # Error-based failure
            elif status.error_count >= self.max_errors:
                status.is_alive = False
                status.status_msg = "error_threshold_exceeded"
                failed.append(name)
        return failed

    def get_recovery_action(self, agent_name: str) -> str:
        """Determines the best strategy for a failed agent."""
        status = self.health_registry.get(agent_name)
        if not status:
            return "reinitialize"

        if status.status_msg == "timeout":
            return "restart_process"
        if status.error_count > self.max_errors * 2:
            return "apoptosis"  # Clean kill if beyond help

        return "reinitialize"

    def validate_plugin_version(
        self, plugin_version: str, required_version: str
    ) -> bool:
        """
        Semantic version comparison logic.
        v1.2.3 vs v1.2.0
        """
        # Rust-accelerated semver validation
        if HAS_RUST:
            with contextlib.suppress(Exception):
                return rc.validate_semver_rust(plugin_version, required_version)  # type: ignore[attr-defined]

        try:
            p_parts = [int(x) for x in plugin_version.lstrip("v").split(".")]
            r_parts = [int(x) for x in required_version.lstrip("v").split(".")]

            # Pad with zeros if necessary
            p_parts += [0] * (3 - len(p_parts))
            r_parts += [0] * (3 - len(r_parts))

            # Major must match exactly, Minor must be >=, Patch ignored for now
            if p_parts[0] != r_parts[0]:
                return False
            if p_parts[1] < r_parts[1]:
                return False
            return True
        except (ValueError, AttributeError):
            return False
