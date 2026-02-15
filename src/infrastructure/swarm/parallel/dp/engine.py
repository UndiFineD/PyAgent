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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Engine core processor for data parallel coordination.
"""

from __future__ import annotations

from _thread import RLock
import logging
import threading
import time
from collections import deque
from typing import Any, Optional

from src.infrastructure.swarm.parallel.dp.balancer import P2CLoadBalancer
from src.infrastructure.swarm.parallel.dp.types import (DPConfig, StepState,
                                                        WaveState,
                                                        WorkerHealth,
                                                        WorkerState)

logger: logging.Logger = logging.getLogger(__name__)


class DPEngineCoreProc:
    """
    Data Parallel engine core processor.
    """

    def __init__(self, config: DPConfig) -> None:
        self.config: DPConfig = config

        # Step tracking
        self._step_counter = 0
        self._step_request_count = 0
        self._current_step: Optional[StepState] = None

        # Wave tracking
        self._wave_id = 0
        self._current_wave: Optional[WaveState] = None
        self._wave_history: deque[WaveState] = deque(maxlen=100)

        # Workers
        self._workers: dict[int, WorkerState] = {}
        self._init_workers()

        # Load balancer
        self._load_balancer = P2CLoadBalancer(
            list(self._workers.values()), self.config.p2c_sample_size, self.config.enable_locality
        )

        # Barriers for synchronization
        self._step_barrier: Optional[threading.Barrier] = None
        self._wave_barrier: Optional[threading.Barrier] = None

        if self.config.dp_size > 1:
            self._step_barrier = threading.Barrier(self.config.dp_size)
            self._wave_barrier = threading.Barrier(self.config.dp_size)

        self._lock: RLock = threading.RLock()

        logger.info(f"DPEngineCoreProc initialized: rank={config.dp_rank}, size={config.dp_size}")

    def _init_workers(self) -> None:
        """Initialize worker states."""
        for i in range(self.config.num_workers):
            locality_group = 0
            for group_idx, group in enumerate(self.config.locality_groups):
                if i in group:
                    locality_group: int = group_idx
                    break

            self._workers[i] = WorkerState(worker_id=i, dp_rank=i % self.config.dp_size, locality_group=locality_group)

    def begin_step(self, num_requests: int = 0) -> StepState:
        """Begin a new step."""
        with self._lock:
            self._step_counter += 1
            self._step_request_count: int = num_requests

            step = StepState(step_id=self._step_counter, wave_id=self._wave_id, request_count=num_requests)
            self._current_step = step
            return step

    def end_step(self) -> Optional[StepState]:
        """End current step."""
        with self._lock:
            if self._current_step is None:
                return None

            step: StepState = self._current_step
            step.end_time = time.time()
            if self._current_wave:
                self._current_wave.completed_steps += 1
            self._current_step = None
            return step

    def step_sync(self) -> None:
        """Synchronize all DP ranks at step boundary."""
        if self._step_barrier:
            self._step_barrier.wait()

    def begin_wave(self, num_steps: int = 0) -> WaveState:
        """Begin a new execution wave."""
        with self._lock:
            self._wave_id += 1
            wave = WaveState(wave_id=self._wave_id, num_steps=num_steps)
            self._current_wave = wave
            return wave

    def wave_complete(self) -> bool:
        """Check if current wave is complete."""
        with self._lock:
            if self._current_wave is None:
                return True
            return self._current_wave.is_complete

    def end_wave(self) -> Optional[WaveState]:
        """End current wave."""
        with self._lock:
            if self._current_wave is None:
                return None

            wave: WaveState = self._current_wave
            wave.end_time = time.time()
            self._wave_history.append(wave)
            self._current_wave = None
            return wave

    def wave_sync(self) -> None:
        """Synchronize all DP ranks at wave boundary."""
        if self._wave_barrier:
            self._wave_barrier.wait()

    def select_worker(self, locality_group: Optional[int] = None) -> WorkerState:
        """Select worker for request assignment."""
        return self._load_balancer.select_worker(locality_group)

    def assign_request(self, _request_id: str) -> int:
        """Assign request to a worker. Returns worker ID."""
        worker: WorkerState = self.select_worker()
        worker.pending_requests += 1
        return worker.worker_id

    def complete_request(self, worker_id: int, latency_ms: float, success: bool = True) -> None:
        """Mark request as complete on worker."""
        with self._lock:
            if worker_id not in self._workers:
                return

            worker: WorkerState = self._workers[worker_id]
            worker.pending_requests = max(0, worker.pending_requests - 1)
            worker.total_processed += 1
            worker.update_latency(latency_ms)

            if success:
                worker.consecutive_failures = 0
                if worker.health == WorkerHealth.RECOVERING:
                    worker.health = WorkerHealth.HEALTHY
            else:
                worker.consecutive_failures += 1
                if worker.consecutive_failures >= self.config.max_consecutive_failures:
                    worker.health = WorkerHealth.FAILED

            if self._current_step:
                self._current_step.completed_count += 1

    def update_worker_health(self, worker_id: int, health: WorkerHealth) -> None:
        """Update worker health status."""
        with self._lock:
            if worker_id in self._workers:
                self._workers[worker_id].health = health
                self._workers[worker_id].last_heartbeat = time.time()

    def get_step_counter(self) -> int:
        """Get current step counter."""
        return self._step_counter

    def get_wave_id(self) -> int:
        """Get current wave ID."""
        return self._wave_id

    def get_worker_states(self) -> list[WorkerState]:
        """Get all worker states."""
        with self._lock:
            return list(self._workers.values())

    def get_healthy_workers(self) -> list[WorkerState]:
        """Get only healthy workers."""
        with self._lock:
            return [w for w in self._workers.values() if w.health in (WorkerHealth.HEALTHY, WorkerHealth.DEGRADED)]

    def get_metrics(self) -> dict[str, Any]:
        """Get coordinator metrics."""
        with self._lock:
            total_pending: int = sum(w.pending_requests for w in self._workers.values())
            total_processed: int = sum(w.total_processed for w in self._workers.values())
            healthy_count: int = len(self.get_healthy_workers())

            return {
                "dp_rank": self.config.dp_rank,
                "dp_size": self.config.dp_size,
                "step_counter": self._step_counter,
                "wave_id": self._wave_id,
                "num_workers": len(self._workers),
                "healthy_workers": healthy_count,
                "total_pending": total_pending,
                "total_processed": total_processed,
                "waves_completed": len(self._wave_history),
            }
