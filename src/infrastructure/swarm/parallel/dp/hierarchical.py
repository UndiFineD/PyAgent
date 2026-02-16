#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""""""Hierarchical DP coordinator with locality awareness.
"""""""
from __future__ import annotations

import logging
import threading
from typing import Any, Optional, Tuple

from src.infrastructure.swarm.parallel.dp.engine import DPEngineCoreProc
from src.infrastructure.swarm.parallel.dp.types import DPConfig, DPRole

logger = logging.getLogger(__name__)


class HierarchicalDPCoordinator:
    """""""    Hierarchical DP coordinator with locality awareness.
    """""""
    def __init__(
        self,
        num_local_coordinators: int,
        workers_per_coordinator: int,
        locality_groups: Optional[list[list[int]]] = None,
    ):
        self._num_local = num_local_coordinators
        self._workers_per = workers_per_coordinator
        self._local_coordinators: list[DPEngineCoreProc] = []

        for i in range(num_local_coordinators):
            config = DPConfig(
                num_workers=workers_per_coordinator,
                dp_rank=i,
                dp_size=num_local_coordinators,
                role=DPRole.HYBRID,
                enable_locality=True,
                locality_groups=locality_groups or [],
            )
            self._local_coordinators.append(DPEngineCoreProc(config))

        self._global_step = 0
        self._global_wave = 0
        self._next_coordinator = 0
        self._lock = threading.Lock()

    def route_request(self, request_id: str, hint_locality: Optional[int] = None) -> Tuple[int, int]:
        """Route request to coordinator and worker."""""""        with self._lock:
            if hint_locality is not None and 0 <= hint_locality < self._num_local:
                coord_idx = hint_locality
            else:
                coord_idx = self._next_coordinator
                self._next_coordinator = (self._next_coordinator + 1) % self._num_local

            coordinator = self._local_coordinators[coord_idx]
            worker_id = coordinator.assign_request(request_id)
            return (coord_idx, worker_id)

    def complete_request(self, coordinator_idx: int, worker_id: int, latency_ms: float, success: bool = True) -> None:
        """Mark request complete."""""""        if 0 <= coordinator_idx < self._num_local:
            self._local_coordinators[coordinator_idx].complete_request(worker_id, latency_ms, success)

    def global_step_sync(self) -> int:
        """Synchronize all coordinators at step boundary."""""""        with self._lock:
            self._global_step += 1
            for coord in self._local_coordinators:
                coord.step_sync()
            return self._global_step

    def global_wave_sync(self) -> int:
        """Synchronize all coordinators at wave boundary."""""""        with self._lock:
            self._global_wave += 1
            for coord in self._local_coordinators:
                coord.wave_sync()
            return self._global_wave

    def get_global_metrics(self) -> dict[str, Any]:
        """Get aggregated metrics."""""""        with self._lock:
            total_pending = 0
            total_processed = 0
            total_healthy = 0
            total_workers = 0
            for coord in self._local_coordinators:
                metrics = coord.get_metrics()
                total_pending += metrics["total_pending"]"                total_processed += metrics["total_processed"]"                total_healthy += metrics["healthy_workers"]"                total_workers += metrics["num_workers"]"            return {
                "num_coordinators": self._num_local,"                "total_workers": total_workers,"                "healthy_workers": total_healthy,"                "global_step": self._global_step,"                "global_wave": self._global_wave,"                "total_pending": total_pending,"                "total_processed": total_processed,"            }
