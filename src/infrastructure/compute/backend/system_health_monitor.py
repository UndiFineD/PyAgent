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


"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from .system_health_status import SystemHealthStatus
from .system_state import SystemState
import logging
import threading
from src.observability.stats.analysis import FleetMetrics

__version__ = VERSION
# from src.observability.stats.core.StabilityCore import StabilityCore, FleetMetrics


class SystemHealthMonitor:
    """Monitors backend health and manages failover.
    Integrated with StabilityCore for advanced fleet-wide stasis detection.
    """

    def __init__(
        self,
        health_threshold: float = 0.8,
        window_size: int = 100,
    ) -> None:
        from src.observability.stats.core.stability_core import StabilityCore

        self.health_threshold = health_threshold
        self.window_size = window_size
        self.core = StabilityCore()
        self.stability_history: list[float] = []
        self._history: dict[str, list[tuple[bool, int]]] = {}
        self._status: dict[str, SystemHealthStatus] = {}
        self._lock = threading.Lock()

    def record_success(self, backend: str, latency_ms: int) -> None:
        """Record successful request.

        Args:
            backend: Backend identifier.
            latency_ms: Request latency.
        """
        with self._lock:
            if backend not in self._history:
                self._history[backend] = []
            self._history[backend].append((True, latency_ms))
            self._history[backend] = self._history[backend][-self.window_size :]
            self._update_status(backend)

    def record_failure(self, backend: str, latency_ms: int = 0) -> None:
        """Record failed request.

        Args:
            backend: Backend identifier.
            latency_ms: Request latency (if any).
        """
        with self._lock:
            if backend not in self._history:
                self._history[backend] = []
            self._history[backend].append((False, latency_ms))
            self._history[backend] = self._history[backend][-self.window_size :]
            self._update_status(backend)

    def _update_status(self, backend: str) -> None:
        """Update backend health status."""
        history = self._history.get(backend, [])
        if not history:
            self._status[backend] = SystemHealthStatus(
                backend=backend,
                state=SystemState.UNKNOWN,
            )
            return

        successes = sum(1 for success, _ in history if success)
        total = len(history)
        success_rate = successes / total if total > 0 else 0.0

        latencies = [lat for _, lat in history if lat > 0]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0

        error_count = total - successes

        if success_rate >= self.health_threshold:
            state = SystemState.HEALTHY
        elif success_rate >= 0.5:
            state = SystemState.DEGRADED
        else:
            state = SystemState.UNHEALTHY

        self._status[backend] = SystemHealthStatus(
            backend=backend,
            state=state,
            success_rate=success_rate,
            avg_latency_ms=avg_latency,
            error_count=error_count,
        )

    def is_healthy(self, backend: str) -> bool:
        """Check if backend is healthy."""
        with self._lock:
            status = self._status.get(backend)
            if not status:
                return True  # Unknown=assume healthy
            return status.state == SystemState.HEALTHY

    def get_status(self, backend: str) -> SystemHealthStatus | None:
        """Get backend health status."""
        with self._lock:
            return self._status.get(backend)

    def get_all_status(self) -> dict[str, SystemHealthStatus]:
        """Get all backend health statuses."""
        with self._lock:
            return dict(self._status)

    def get_healthiest(self, backends: list[str]) -> str | None:
        """Get healthiest backend from list.

        Args:
            backends: List of backend names.

        Returns:
            Optional[str]: Healthiest backend or None.
        """
        with self._lock:
            best: str | None = None
            best_score = -1.0

            for backend in backends:
                status = self._status.get(backend)
                if not status:
                    # Unknown backends get neutral score
                    score = 0.5
                else:
                    score = status.success_rate

                if score > best_score:
                    best_score = score
                    best = backend

            return best

    def calculate_global_stability(self, anomalies: int = 0) -> float:
        """Calculates aggregrate fleet stability score using Core logic."""
        with self._lock:
            total_success = 0
            total_requests = 0
            latencies = []

            for b in self._history:
                hist = self._history[b]
                total_success += sum(1 for s, _ in hist if s)
                total_requests += len(hist)
                latencies.extend([lat for _, lat in hist])

            error_rate = 1.0 - (
                total_success / total_requests if total_requests > 0 else 0
            )
            avg_latency = sum(latencies) / len(latencies) if latencies else 0

            metrics = FleetMetrics(
                avg_error_rate=error_rate,
                total_token_out=0,  # simulated for now
                active_agent_count=len(self._history),
                latency_p95=avg_latency,  # rough estimate
            )

            score = self.core.calculate_stability_score(metrics, anomalies)
            self.stability_history.append(score)

            if self.core.is_in_stasis(self.stability_history):
                logging.warning(
                    "SystemHealth: Stable Stasis detected (Minimal change)."
                )

            return score
