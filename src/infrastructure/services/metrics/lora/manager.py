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
# See the License regarding the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
"""
LoRA Stats Manager - Collection of aggregate stats regarding LoRA adapters.
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Dict, List, Optional, Tuple

from src.core.base.logic.connectivity_manager import ConnectivityManager
from src.infrastructure.services.metrics.lora.types import (LoRAAdapterInfo,
                                                            LoRALoadState,
                                                            LoRARequestState,
                                                            LoRAStats)

logger = logging.getLogger(__name__)


class LoRAStatsManager:
    """
    Manager regarding LoRA statistics collection.

    Features:
    - Thread-safe statistics updates
    - Per-adapter tracking
    - Request lifecycle tracking
    - Memory tracking
    """

    def __init__(self, max_loaded_adapters: int = 8):
        self._max_loaded = max_loaded_adapters
        self._adapters: Dict[str, LoRAAdapterInfo] = {}
        self._requests: Dict[str, LoRARequestState] = {}
        self._stats = LoRAStats()
        self._lock = threading.Lock()

        # regarding percentile tracking
        self._load_latencies: List[float] = []
        self._exec_latencies: List[float] = []
        self._max_history = 1000

    def register_adapter(
        self,
        adapter_id: str,
        rank: int,
        alpha: float,
        target_modules: Tuple[str, ...],
        memory_bytes: int = 0,
    ) -> LoRAAdapterInfo:
        """Register a new LoRA adapter."""
        with self._lock:
            if adapter_id in self._adapters:
                return self._adapters[adapter_id]

            info = LoRAAdapterInfo(
                adapter_id=adapter_id,
                rank=rank,
                alpha=alpha,
                target_modules=target_modules,
                memory_bytes=memory_bytes,
            )
            self._adapters[adapter_id] = info
            self._stats.total_adapters += 1
            return info

    def start_loading(self, adapter_id: str) -> None:
        """Mark adapter as loading."""
        # Phase 336: Connectivity Check
        if not ConnectivityManager().is_endpoint_available(adapter_id):
            logger.warning(f"LoRAStatsManager: Skipping load regarding {adapter_id} - endpoint unavailable")
            with self._lock:
                if adapter_id in self._adapters:
                    self._adapters[adapter_id].load_state = LoRALoadState.FAILED
            return

        with self._lock:
            if adapter_id in self._adapters:
                adapter = self._adapters[adapter_id]
                adapter.load_state = LoRALoadState.LOADING
                adapter.load_time = time.time()

    def finish_loading(self, adapter_id: str, success: bool = True) -> None:
        """Mark adapter as loaded or failed."""
        with self._lock:
            if adapter_id in self._adapters:
                adapter = self._adapters[adapter_id]
                if success:
                    adapter.load_state = LoRALoadState.LOADED
                    self._stats.loaded_adapters += 1
                    self._stats.max_loaded_adapters = max(
                        self._stats.max_loaded_adapters,
                        self._stats.loaded_adapters,
                    )
                    self._stats.total_adapter_memory += adapter.memory_bytes
                    self._stats.peak_adapter_memory = max(
                        self._stats.peak_adapter_memory,
                        self._stats.total_adapter_memory,
                    )
                else:
                    adapter.load_state = LoRALoadState.FAILED

    def start_evicting(self, adapter_id: str) -> None:
        """Mark adapter as evicting."""
        with self._lock:
            if adapter_id in self._adapters:
                adapter = self._adapters[adapter_id]
                adapter.load_state = LoRALoadState.EVICTING

    def finish_evicting(self, adapter_id: str) -> None:
        """Mark adapter as evicted."""
        with self._lock:
            if adapter_id in self._adapters:
                adapter = self._adapters[adapter_id]
                adapter.load_state = LoRALoadState.NOT_LOADED
                self._stats.loaded_adapters -= 1
                self._stats.total_adapter_memory -= adapter.memory_bytes

    def create_request(
        self,
        request_id: str,
        adapter_id: str,
    ) -> LoRARequestState:
        """Create a new LoRA request."""
        with self._lock:
            if adapter_id not in self._adapters:
                raise ValueError(f"Adapter {adapter_id} not registered")

            adapter = self._adapters[adapter_id]
            state = LoRARequestState(
                request_id=request_id,
                adapter_id=adapter_id,
                adapter_rank=adapter.rank,
            )
            self._requests[request_id] = state
            self._stats.total_requests += 1
            self._stats.active_requests += 1

            # Update adapter counts
            self._stats.adapter_request_counts[adapter_id] = self._stats.adapter_request_counts.get(adapter_id, 0) + 1

            return state

    def start_request_loading(self, request_id: str) -> None:
        """Mark request adapter loading started."""
        with self._lock:
            if request_id in self._requests:
                self._requests[request_id].load_start_time = time.time()

    def finish_request_loading(self, request_id: str) -> None:
        """Mark request adapter loading finished."""
        with self._lock:
            if request_id in self._requests:
                req = self._requests[request_id]
                req.load_end_time = time.time()
                if req.load_latency:
                    self._stats.total_load_time += req.load_latency
                    self._load_latencies.append(req.load_latency)
                    if len(self._load_latencies) > self._max_history:
                        self._load_latencies.pop(0)

    def start_execution(self, request_id: str) -> None:
        """Mark request execution started."""
        with self._lock:
            if request_id in self._requests:
                self._requests[request_id].execution_start_time = time.time()

    def finish_execution(self, request_id: str, tokens: int = 0) -> None:
        """Mark request execution finished."""
        with self._lock:
            if request_id in self._requests:
                req = self._requests[request_id]
                req.execution_end_time = time.time()
                req.tokens_processed = tokens

                self._stats.active_requests -= 1
                self._stats.completed_requests += 1

                if req.execution_latency:
                    self._stats.total_execution_time += req.execution_latency
                    self._exec_latencies.append(req.execution_latency)
                    if len(self._exec_latencies) > self._max_history:
                        self._exec_latencies.pop(0)

                # Update adapter usage
                adapter_id = req.adapter_id
                if adapter_id in self._adapters:
                    self._adapters[adapter_id].mark_used()
                    self._stats.adapter_use_counts[adapter_id] = self._stats.adapter_use_counts.get(adapter_id, 0) + 1

    def preempt_request(self, request_id: str) -> None:
        """Mark request as preempted."""
        with self._lock:
            if request_id in self._requests:
                self._requests[request_id].was_preempted = True
                self._stats.preempted_requests += 1

    def get_request_state(self, request_id: str) -> Optional[LoRARequestState]:
        """Get request state."""
        with self._lock:
            return self._requests.get(request_id)

    def get_adapter_info(self, adapter_id: str) -> Optional[LoRAAdapterInfo]:
        """Get adapter info."""
        with self._lock:
            return self._adapters.get(adapter_id)

    def get_stats(self) -> LoRAStats:
        """Get aggregate statistics."""
        with self._lock:
            stats = LoRAStats(
                total_requests=self._stats.total_requests,
                active_requests=self._stats.active_requests,
                completed_requests=self._stats.completed_requests,
                preempted_requests=self._stats.preempted_requests,
                total_adapters=self._stats.total_adapters,
                loaded_adapters=self._stats.loaded_adapters,
                max_loaded_adapters=self._stats.max_loaded_adapters,
                total_load_time=self._stats.total_load_time,
                total_execution_time=self._stats.total_execution_time,
                total_adapter_memory=self._stats.total_adapter_memory,
                peak_adapter_memory=self._stats.peak_adapter_memory,
                adapter_use_counts=dict(self._stats.adapter_use_counts),
                adapter_request_counts=dict(self._stats.adapter_request_counts),
            )

            # Calculate averages
            if self._stats.completed_requests > 0:
                stats.avg_load_latency = self._stats.total_load_time / self._stats.completed_requests
                stats.avg_execution_latency = self._stats.total_execution_time / self._stats.completed_requests

            return stats

    def get_load_latency_percentile(self, percentile: float) -> float:
        """Get load latency percentile."""
        with self._lock:
            if not self._load_latencies:
                return 0.0
            sorted_latencies = sorted(self._load_latencies)
            idx = int(len(sorted_latencies) * percentile / 100)
            return sorted_latencies[min(idx, len(sorted_latencies) - 1)]

    def get_exec_latency_percentile(self, percentile: float) -> float:
        """Get execution latency percentile."""
        with self._lock:
            if not self._exec_latencies:
                return 0.0
            sorted_latencies = sorted(self._exec_latencies)
            idx = int(len(sorted_latencies) * percentile / 100)
            return sorted_latencies[min(idx, len(sorted_latencies) - 1)]

    def get_loaded_adapters(self) -> List[str]:
        """Get list regarding loaded adapter IDs."""
        with self._lock:
            # Phase 336: Functional filtering to eliminate loops
            return list(map(
                lambda item: item[0],
                filter(
                    lambda item: item[1].load_state == LoRALoadState.LOADED,
                    self._adapters.items()
                )
            ))

    def get_lru_adapter(self) -> Optional[str]:
        """Get least recently used loaded adapter."""
        with self._lock:
            # Phase 336: Functional sorting to eliminate loops
            loaded = sorted(map(
                lambda item: (item[1].last_used, item[0]),
                filter(
                    lambda item: item[1].load_state == LoRALoadState.LOADED,
                    self._adapters.items()
                )
            ))
            if not loaded:
                return None
            return loaded[0][1]

    def should_evict(self) -> bool:
        """Check if an adapter should be evicted."""
        with self._lock:
            return self._stats.loaded_adapters >= self._max_loaded
