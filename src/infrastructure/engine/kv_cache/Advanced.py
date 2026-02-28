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

"""Advanced KV cache coordinators for complex use cases."""

# SPDX-License-Identifier: Apache-2.0
import threading
from collections import defaultdict
from typing import Dict, List, Tuple

from .coordinator import KVCacheCoordinator
from .data_classes import CacheConfig, KVCacheBlocks


class HierarchicalKVCacheCoordinator(KVCacheCoordinator):
    """Hierarchical coordinator for complex model architectures."""

    def __init__(self, config: CacheConfig, max_model_len: int, num_layers: int) -> None:
        super().__init__(config, max_model_len)
        self.num_layers = num_layers
        self.layer_stats: Dict[int, Dict[str, int]] = defaultdict(lambda: {"allocations": 0, "hits": 0})

    def allocate_for_layer(self, request_id: str, num_tokens: int, layer_idx: int) -> KVCacheBlocks:
        """Allocate KV cache specifically for a specific model layer."""
        blocks = self.allocate(request_id, num_tokens)
        self.layer_stats[layer_idx]["allocations"] += 1
        return blocks


class PredictiveKVCacheCoordinator(KVCacheCoordinator):
    """Coordinator with predictive allocation based on request patterns."""

    def __init__(self, config: CacheConfig, max_model_len: int, memory_budget_bytes: int) -> None:
        super().__init__(config, max_model_len)
        self.memory_budget = memory_budget_bytes
        self._length_history: List[int] = []
        self._avg_length: float = 256.0

    def predict_length(self, prompt_length: int) -> int:
        """Predict the total sequence length for a given prompt."""
        if not self._length_history:
            return int(self._avg_length)
        return int(self._avg_length * 0.9 + prompt_length * 0.1)

    def record_completion_length(self, length: int) -> None:
        """Record the actual completion length to improve future predictions."""
        self._length_history.append(length)
        if len(self._length_history) > 1000:
            self._length_history = self._length_history[-500:]
        self._avg_length = sum(self._length_history) / len(self._length_history)

    def allocate_predictive(self, request_id: str, current_tokens: int, prompt_length: int) -> KVCacheBlocks:
        """Allocate KV cache based on predicted future demand."""
        predicted = self.predict_length(prompt_length)
        target_tokens = max(current_tokens, predicted)
        return self.allocate(request_id, target_tokens)


class AsyncPrefetchCoordinator(KVCacheCoordinator):
    """Coordinator with async prefetch support."""

    def __init__(self, config: CacheConfig, max_model_len: int, prefetch_queue_size: int = 100) -> None:
        super().__init__(config, max_model_len)
        self.prefetch_queue_size = prefetch_queue_size
        self._prefetch_requests: List[Tuple[str, int]] = []
        self._prefetch_lock = threading.Lock()

    def queue_prefetch(self, request_id: str, expected_tokens: int, priority: int = 0) -> None:
        """Queue a prefetch request for future allocation."""
        _ = priority  # Unused argument
        with self._prefetch_lock:
            if len(self._prefetch_requests) < self.prefetch_queue_size:
                self._prefetch_requests.append((request_id, expected_tokens))

    def process_prefetch_queue(self, max_blocks: int = 10) -> int:
        """Process pending prefetch requests from the queue."""
        processed = 0
        with self._prefetch_lock:
            while self._prefetch_requests and processed < max_blocks:
                request_id, tokens = self._prefetch_requests.pop(0)
                try:
                    self.allocate(request_id, tokens)
                    processed += 1
                except MemoryError:
                    self._prefetch_requests.insert(0, (request_id, tokens))
                    break
        return processed
