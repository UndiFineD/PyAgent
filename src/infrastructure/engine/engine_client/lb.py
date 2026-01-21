"""
Phase 45: P2C Load Balancer
Power of Two Choices algorithm for engine client selection.
"""

from __future__ import annotations
import threading
import random
from typing import Optional, TYPE_CHECKING
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

    def __init__(self, workers: list[WorkerInfo], sample_size: int = 2):
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
