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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
Types and configuration for data parallel coordination.
"""


from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional




class DPRole(Enum):
    """Data parallel role.
    MASTER = auto()  # Coordinates workers
    WORKER = auto()  # Executes work
    HYBRID = auto()  # Both roles




class WorkerHealth(Enum):
    """Worker health status.
    HEALTHY = auto()
    DEGRADED = auto()
    RECOVERING = auto()
    FAILED = auto()




class LoadBalanceStrategy(Enum):
    """Load balancing strategy.
    ROUND_ROBIN = auto()
    LEAST_LOADED = auto()
    P2C = auto()  # Power of Two Choices
    LOCALITY_AWARE = auto()  # Prefer local workers


@dataclass
class DPConfig:
    """Configuration for data parallel coordinator.
    num_workers: int = 1
    dp_rank: int = 0
    dp_size: int = 1
    role: DPRole = DPRole.WORKER
    lb_strategy: LoadBalanceStrategy = LoadBalanceStrategy.P2C
    p2c_sample_size: int = 2
    health_check_interval_s: float = 5.0
    max_consecutive_failures: int = 3
    enable_locality: bool = True
    locality_groups: list[list[int]] = field(default_factory=list)


@dataclass
class WorkerState:
    """State of a DP worker.
    worker_id: int
    dp_rank: int
    health: WorkerHealth = WorkerHealth.HEALTHY
    pending_requests: int = 0
    total_processed: int = 0
    avg_latency_ms: float = 0.0
    last_heartbeat: float = field(default_factory=time.time)
    consecutive_failures: int = 0
    locality_group: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def update_latency(self, latency_ms: float) -> None:
        """Update average latency with EMA.        self.avg_latency_ms = 0.9 * self.avg_latency_ms + 0.1 * latency_ms


@dataclass
class StepState:
    """State for a single step.
    step_id: int
    wave_id: int
    request_count: int = 0
    completed_count: int = 0
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None

    @property
    def is_complete(self) -> bool:
        return self.completed_count >= self.request_count

    @property
    def duration_ms(self) -> float:
        end = self.end_time or time.time()
        return (end - self.start_time) * 1000


@dataclass
class WaveState:
    """State for an execution wave.
    wave_id: int
    num_steps: int = 0
    completed_steps: int = 0
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None

    @property
    def is_complete(self) -> bool:
        return self.completed_steps >= self.num_steps
