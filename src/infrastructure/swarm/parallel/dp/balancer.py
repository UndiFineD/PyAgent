# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Load balancing strategies for Data Parallel coordination.
"""

from __future__ import annotations

import random
import threading
from typing import List, Optional

from src.infrastructure.swarm.parallel.dp.types import WorkerState, WorkerHealth

class P2CLoadBalancer:
    """
    Power of Two Choices load balancer.
    """

    def __init__(
        self,
        workers: list[WorkerState],
        sample_size: int = 2,
        enable_locality: bool = True
    ):
        self._workers = workers
        self._sample_size = min(sample_size, len(workers))
        self._enable_locality = enable_locality
        self._lock = threading.Lock()

    def select_worker(self, locality_group: Optional[int] = None) -> WorkerState:
        """Select best worker using P2C algorithm."""
        with self._lock:
            # Filter healthy workers
            healthy = [
                w for w in self._workers
                if w.health in (WorkerHealth.HEALTHY, WorkerHealth.DEGRADED)
            ]

            if not healthy:
                # Fallback to any worker
                healthy = self._workers

            # Apply locality preference
            if self._enable_locality and locality_group is not None:
                local_workers = [w for w in healthy if w.locality_group == locality_group]
                if local_workers:
                    healthy = local_workers

            if len(healthy) == 1:
                return healthy[0]

            # Sample workers
            candidates = random.sample(healthy, min(self._sample_size, len(healthy)))

            # Select by pending requests, then latency
            best = min(candidates, key=lambda w: (w.pending_requests, w.avg_latency_ms))

            return best

    def update_workers(self, workers: list[WorkerState]) -> None:
        """Update worker list."""
        with self._lock:
            self._workers = workers
