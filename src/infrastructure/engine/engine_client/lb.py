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
Phase 45: P2C Load Balancer
Power of Two Choices algorithm for engine client selection.
"""

from __future__ import annotations

import random
import threading
from typing import TYPE_CHECKING, Optional

from src.infrastructure.engine.engine_client.types import WorkerState

if TYPE_CHECKING:
    from src.infrastructure.engine.engine_client.types import WorkerInfo


class P2CLoadBalancer:
    """
    Power of Two Choices load balancer.

    vLLM Pattern: DPLBAsyncMPClient worker selection

    Algorithm:
    1. Randomly sample 2 workers
    2. Select the one with fewer pending requests
    3. Tie-break by latency
    """

    def __init__(self, workers: list[WorkerInfo], sample_size: int = 2) -> None:
        self.workers = workers
        self.sample_size = min(sample_size, len(workers))
        self._lock = threading.Lock()

    def select_worker(self) -> WorkerInfo:
        """Select best worker using P2C algorithm."""
        with self._lock:
            # Filter healthy workers
            healthy = [w for w in self.workers if w.state in (WorkerState.HEALTHY, WorkerState.DEGRADED)]

            if not healthy:
                # Fallback to any worker
                healthy = self.workers

            if len(healthy) == 1:
                return healthy[0]

            # Sample workers
            candidates = random.sample(healthy, min(self.sample_size, len(healthy)))

            # Select by pending requests, then latency
            best = min(candidates, key=lambda w: (w.pending_requests, w.avg_latency_ms))

            return best

    def update_worker(self, worker_id: int, pending_delta: int = 0, latency_ms: Optional[float] = None) -> None:
        """Update worker statistics."""
        with self._lock:
            for worker in self.workers:
                if worker.worker_id == worker_id:
                    worker.pending_requests = max(0, worker.pending_requests + pending_delta)
                    if latency_ms is not None:
                        # Exponential moving average
                        worker.avg_latency_ms = 0.9 * worker.avg_latency_ms + 0.1 * latency_ms
                    break
