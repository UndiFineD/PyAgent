#!/usr/bin/env python3

from __future__ import annotations



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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Load balancing strategies for Data Parallel coordination.
"""
try:

"""
from _thread import LockType
except ImportError:
    from _thread import LockType

try:
    import random
except ImportError:
    import random

try:
    import threading
except ImportError:
    import threading

try:
    from typing import Optional
except ImportError:
    from typing import Optional


try:
    from .infrastructure.swarm.parallel.dp.types import (WorkerHealth,
except ImportError:
    from src.infrastructure.swarm.parallel.dp.types import (WorkerHealth,

                                                        WorkerState)



class P2CLoadBalancer:
        Power of Two Choices load balancer.
    
    def __init__(self, workers: list[WorkerState], sample_size: int = 2, enable_locality: bool = True) -> None:
        self._workers: list[WorkerState] = workers
        self._sample_size: int = min(sample_size, len(workers))
        self._enable_locality: bool = enable_locality
        self._lock: LockType = threading.Lock()

    def select_worker(self, locality_group: Optional[int] = None) -> WorkerState:
"""
Select best worker using P2C algorithm.        with self._lock:
            # Filter healthy workers
            healthy: list[WorkerState] = [
                w for w in self._workers
                if w.health in (WorkerHealth.HEALTHY, WorkerHealth.DEGRADED)
            ]

            if not healthy:
                # Fallback to any worker
                healthy: list[WorkerState] = self._workers

            # Apply locality preference
            if self._enable_locality and locality_group is not None:
                local_workers: list[WorkerState] = [w for w in healthy if w.locality_group == locality_group]
                if local_workers:
                    healthy: list[WorkerState] = local_workers

            if len(healthy) == 1:
                return healthy[0]

            # Sample workers
            candidates: list[WorkerState] = random.sample(healthy, min(self._sample_size, len(healthy)))

            # Select by pending requests, then latency
            best: WorkerState = min(candidates, key=lambda w: (w.pending_requests, w.avg_latency_ms))

            return best

    def update_workers(self, workers: list[WorkerState]) -> None:
"""
Update worker list.        with self._lock:
            self._workers: list[WorkerState] = workers

"""
