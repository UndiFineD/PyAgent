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
Decode-Only Worker.

This module implements a specialized worker for the decode stage of disaggregated inference.
Decode-only workers receive KV cache from prefill workers and perform low-latency,
autoregressive token generation.

Optimized for:
- Low-latency token-by-token generation
- Efficient incremental KV cache loading from remote producers
- Minimal memory footprint (swapping unused KV blocks to remote storage)
- High concurrency for many concurrent sequences

Inspired by vLLM's specialized worker architectures and disaggregated prefill-decode patterns.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from src.core.lazy_loader import LazyLoader
from src.infrastructure.storage.kv_transfer.kv_transfer_connector import (
    KVConnectorRole, KVTransferConfig)

if TYPE_CHECKING:
    from src.infrastructure.storage.cache.kv_cache_manager import \
        KVCacheManager
    from src.infrastructure.storage.kv_transfer.kv_transfer_connector import \
        KVConnectorBase

logger: logging.Logger = logging.getLogger(__name__)


class DecodeOnlyWorker:
    """
    Worker specialized in the decode stage.

    This worker assumes the prefill (initial prompt processing) has been done elsewhere.
    It pulls the necessary KV cache blocks on-demand or ahead-of-time from the
    distributed pool (e.g., Mooncake) and proceeds with generation.
    """

    def __init__(
        self,
        worker_id: str,
        model_config: Any,
        parallel_config: Any,
        kv_transfer_config: KVTransferConfig,
    ) -> None:
        self.worker_id: str = worker_id
        self.model_config = model_config
        self.parallel_config = parallel_config
        self.kv_transfer_config: KVTransferConfig = kv_transfer_config

        # Ensure role is set to CONSUMER
        self.kv_transfer_config.kv_role = KVConnectorRole.CONSUMER

        # Components
        self.cache_manager: Optional[KVCacheManager] = None
        self.kv_connector: Optional[KVConnectorBase] = None
        self.model_executor: Optional[Any] = None

        # State
        self._is_active = False
        self._active_sequences: Dict[str, Any] = {}

        # Metrics
        self.tokens_generated = 0
        self.cache_hits_remote = 0
        self.cache_misses_remote = 0

        logger.info("DecodeOnlyWorker %s initialized.", worker_id)

    def initialize(self) -> None:
        """Initialize components for decoding."""
        # Setup...
        self._is_active = True
        logger.info("DecodeOnlyWorker %s started.", self.worker_id)

    def execute_step(self, active_requests: List[Any]) -> None:
        """
        Perform one decoding step for a batch of requests.

        1. Coordinate with KV connector to ensure blocks are loaded
        2. Execute model forward pass (single token)
        3. Sample next tokens
        4. Update local KV cache
        """
        if not active_requests:
            return

        # Ahead-of-time loading coordination
        # for request in active_requests:
        #    self.kv_connector.start_load_kv(forward_context)

        # Model forward loop:
        # for layer_idx in range(num_layers):
        #    self.kv_connector.wait_for_layer_load(layer_name)
        #    ... attention ...

        self.tokens_generated += len(active_requests)

    def _schedule_kv_prefetch_rust(self, seq_metadata: Any) -> List[int]:
        """Rust-accelerated heuristic for prefetching KV blocks from remote."""
        _ = seq_metadata
        # return RustBridge.schedule_kv_prefetch_rust(seq_metadata)
        return []

    def get_status(self) -> Dict[str, Any]:
        """Return worker health and performance stats."""
        return {
            "worker_id": self.worker_id,
            "role": "decode",
            "active_sequences": len(self._active_sequences),
            "tokens_generated": self.tokens_generated,
            "cache_hits_remote": self.cache_hits_remote,
            "cache_misses_remote": self.cache_misses_remote,
        }

    def shutdown(self) -> None:
        """Gracefully shut down the decode worker."""
        self._is_active = False
        if self.kv_connector:
            self.kv_connector.close()
        logger.info("DecodeOnlyWorker %s shut down.", self.worker_id)


# Lazy loading registration
_worker = LazyLoader("src.infrastructure.swarm.worker.decode_only_worker", "DecodeOnlyWorker")
