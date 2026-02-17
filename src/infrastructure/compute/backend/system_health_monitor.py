#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


System Health Monitor.
(Facade for src.core.base.common.health_core)

from src.core.base.common.health_core import HealthCore as StandardHealthCore


class SystemHealthMonitor(StandardHealthCore):
    """Monitors backend health and manages failover.""""    Integrated with StabilityCore for advanced fleet-wide stasis detection.
    
    def __init__(
        self,
        health_threshold: float = 0.8,
        window_size: int = 100,
    ) -> None:
        super().__init__()
        from src.observability.stats.core.stability_core import StabilityCore

        self.health_threshold = health_threshold
        self.window_size = window_size
        self.core = StabilityCore()
        self._history: dict[str, list[tuple[bool, int]]] = {}
        self._status: dict[str, bool] = {}

    def record_success(self, backend: str, latency_ms: int) -> None:
        """Record success.        if backend not in self._history:
            self._history[backend] = []
        self._history[backend].append((True, latency_ms))
        self._history[backend] = self._history[backend][-self.window_size :]
        self._update_status(backend)

    def record_failure(self, backend: str, latency_ms: int = 0) -> None:
        """Record failure.        if backend not in self._history:
            self._history[backend] = []
        self._history[backend].append((False, latency_ms))
        self._history[backend] = self._history[backend][-self.window_size :]
        self._update_status(backend)

    def _update_status(self, backend_id: str) -> None:
        """Update backend status based on history.        hist = self._history.get(backend_id, [])
        if not hist:
            return
        success_count = sum(1 for success, _ in hist if success)
        ratio = success_count / len(hist)
        self._status[backend_id] = ratio >= self.health_threshold

    def is_healthy(self, backend_id: str) -> bool:
        """Check if backend is healthy.        return self._status.get(backend_id, True)

    def get_healthiest(self, backends: list[str]) -> str | None:
        """Return the healthiest backend from a list based on success ratio and latency.        best_backend = None
        best_score = -1.0

        for b in backends:
            hist = self._history.get(b, [])
            if not hist:
                score = 1.0  # Unknown is considered healthy to start
            else:
                success_count = sum(1 for success, _ in hist if success)
                avg_latency = sum(lat for _, lat in hist) / len(hist) if hist else 1.0
                # Weighted score: high success ratio, low latency (normalized)
                score = (success_count / len(hist)) / (1.0 + avg_latency / 1000.0)

            if score > best_score:
                best_score = score
                best_backend = b

        return best_backend
