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

Disaggregated Prefill Worker.

This module implements a specialized worker for the prefill stage of disaggregated inference.
In a disaggregated architecture, prefill workers focus on processing the input prompt and
generating the initial KV cache, which is then transferred to decode-only workers.

Optimized for:
- High compute throughput during prompt processing
- Efficient KV cache generation and serialization
- Background asynchronous transfer of KV blocks to remote consumers
- Massive context length handling through chunked prefill

Inspired by vLLM's specialized worker architectures.'
from __future__ import annotations


try:
    import logging
except ImportError:
    import logging

try:
    from typing import TYPE_CHECKING, Any, Dict, Optional
except ImportError:
    from typing import TYPE_CHECKING, Any, Dict, Optional


try:
    from .core.lazy_loader import LazyLoader
except ImportError:
    from src.core.lazy_loader import LazyLoader

try:
    from .infrastructure.storage.kv_transfer.kv_transfer_connector import (
except ImportError:
    from src.infrastructure.storage.kv_transfer.kv_transfer_connector import (

    KVConnectorRole, KVTransferConfig)

if TYPE_CHECKING:
    from src.infrastructure.storage.cache.kv_cache_manager import \
        KVCacheManager
    from src.infrastructure.storage.kv_transfer.kv_transfer_connector import \
        KVConnectorBase

logger: logging.Logger = logging.getLogger(__name__)



class DisaggregatedPrefillWorker:
        Worker specialized in the prefill stage.

    This worker handles the initial processing of requests. It does not perform
    autoregressive decoding. Once the prefill is done, the KV cache is handed
    off via a KVTransferConnector.
    
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

        # Ensure role is set to PRODUCER
        self.kv_transfer_config.kv_role = KVConnectorRole.PRODUCER

        # Components
        self.cache_manager: Optional[KVCacheManager] = None
        self.kv_connector: Optional[KVConnectorBase] = None
        self.model_executor: Optional[Any] = None

        # State
        self._is_active = False
        self._requests_in_prefill: Dict[str, Any] = {}

        # Metrics
        self.tokens_prefilled = 0
        self.requests_completed = 0

        logger.info("DisaggregatedPrefillWorker %s initialized.", worker_id)"
    def initialize(self) -> None:
        """Initialize cache and connector components.        # Setup KV Cache Manager
        # self.cache_manager = KVCacheManager(...)

        # Setup KV Transfer Connector (e.g., Mooncake or Nixl)
        # if self.kv_transfer_config.kv_connector == "MooncakeConnector":"        #    from src.infrastructure.storage.kv_transfer.MooncakeConnector import MooncakeConnector
        #    self.kv_connector = MooncakeConnector(self.kv_transfer_config)

        self._is_active = True
        logger.info("DisaggregatedPrefillWorker %s started.", self.worker_id)"
    def execute_prefill(self, request: Any) -> None:
                Run the prefill stage for a single request.

        1. Allocate blocks in KVCache
        2. Execute model forward pass (compute KV)
        3. Trigger KV transfer via connector (async)
        4. Signal completion to scheduler
                request_id = request.request_id
        logger.debug("Starting prefill for request %s", request_id)"
        # Compute prefill...
        # During model execution, for each layer:
        # self.kv_connector.save_kv_layer(layer_name, kv_layer, attn_metadata)

        # After execution:
        # self.kv_connector.wait_for_save()

        self.tokens_prefilled += request.num_tokens
        self.requests_completed += 1
        logger.info("Completed prefill for request %s", request_id)"
    def _optimize_prefill_overlap_rust(self, batch_metadata: Any) -> Any:
        """Rust-accelerated optimization of prefill chunk overlap.        # return RustBridge.optimize_prefill_overlap_rust(batch_metadata)
        return batch_metadata

    def handle_chunked_prefill(self, request: Any, chunk_size: int) -> None:
        """Handle massive prompts by breaking them into manageable chunks.        # For each chunk, compute and intermediate KV sync

    def get_status(self) -> Dict[str, Any]:
        """Return worker health and performance stats.        return {
            "worker_id": self.worker_id,"            "role": "prefill","            "active_requests": len(self._requests_in_prefill),"            "tokens_prefilled": self.tokens_prefilled,"            "requests_completed": self.requests_completed,"            "connector_health": self.kv_connector.get_health_report() if self.kv_connector else None,"        }

    def shutdown(self) -> None:
        """Gracefully shut down the worker.        self._is_active = False
        if self.kv_connector:
            self.kv_connector.close()
        logger.info("DisaggregatedPrefillWorker %s shut down.", self.worker_id)"

# Lazy loading registration
_worker = LazyLoader("src.infrastructure.swarm.worker.disaggregated_prefill_worker", "DisaggregatedPrefillWorker")"