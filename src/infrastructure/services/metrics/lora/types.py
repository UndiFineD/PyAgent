#!/usr/bin/env python3
# Refactored by copilot-placeholder
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
"""
LoRA Stats Types - Enums and DataClasses for LoRA adapter tracking.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, Optional, Tuple


class LoRALoadState(Enum):
    """State of a LoRA adapter."""

    NOT_LOADED = auto()
    LOADING = auto()
    LOADED = auto()
    EVICTING = auto()
    FAILED = auto()


class RequestStatus(Enum):
    """Status of a request in the system."""

    WAITING = auto()
    RUNNING = auto()
    PREEMPTED = auto()
    FINISHED_STOPPED = auto()
    FINISHED_LENGTH_CAPPED = auto()
    FINISHED_ABORTED = auto()


@dataclass
class LoRAAdapterInfo:
    """Information about a LoRA adapter."""

    adapter_id: str
    rank: int
    alpha: float
    target_modules: Tuple[str, ...]
    memory_bytes: int = 0
    load_state: LoRALoadState = LoRALoadState.NOT_LOADED
    load_time: float = 0.0
    last_used: float = 0.0
    use_count: int = 0

    def mark_used(self) -> None:
        """Mark adapter as used."""
        self.last_used = time.time()
        self.use_count += 1


@dataclass
class LoRARequestState:
    """
    State of a LoRA request.

    Tracks per-request LoRA adapter usage and timing.
    """

    request_id: str
    adapter_id: str
    adapter_rank: int
    queued_time: float = field(default_factory=time.time)
    load_start_time: Optional[float] = None
    load_end_time: Optional[float] = None
    execution_start_time: Optional[float] = None
    execution_end_time: Optional[float] = None
    tokens_processed: int = 0
    was_preempted: bool = False

    @property
    def load_latency(self) -> Optional[float]:
        """Time spent loading the adapter."""
        if self.load_start_time and self.load_end_time:
            return self.load_end_time - self.load_start_time
        return None

    @property
    def queue_latency(self) -> Optional[float]:
        """Time spent waiting in queue."""
        if self.execution_start_time:
            return self.execution_start_time - self.queued_time
        return None

    @property
    def execution_latency(self) -> Optional[float]:
        """Time spent executing."""
        if self.execution_start_time and self.execution_end_time:
            return self.execution_end_time - self.execution_start_time
        return None

    @property
    def total_latency(self) -> Optional[float]:
        """Total request latency."""
        if self.execution_end_time:
            return self.execution_end_time - self.queued_time
        return None


@dataclass
class LoRAStats:
    """
    Aggregate statistics for LoRA operations.
    """

    # Request counts
    total_requests: int = 0
    active_requests: int = 0
    completed_requests: int = 0
    preempted_requests: int = 0

    # Adapter counts
    total_adapters: int = 0
    loaded_adapters: int = 0
    max_loaded_adapters: int = 0

    # Timing stats (in seconds)
    total_load_time: float = 0.0
    total_execution_time: float = 0.0
    avg_load_latency: float = 0.0
    avg_execution_latency: float = 0.0

    # Memory stats
    total_adapter_memory: int = 0
    peak_adapter_memory: int = 0

    # Per-adapter stats
    adapter_use_counts: Dict[str, int] = field(default_factory=dict)
    adapter_request_counts: Dict[str, int] = field(default_factory=dict)
