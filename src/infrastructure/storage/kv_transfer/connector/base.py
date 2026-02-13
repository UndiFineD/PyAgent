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

"""
Phase 45: KV Transfer Connector Base
Abstract base class for all KV transfer connectors.
"""

from __future__ import annotations

import logging
import threading
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

if TYPE_CHECKING:
    from src.infrastructure.storage.kv_transfer.connector.types import (
        ForwardContext, KVCacheBlocks, KVConnectorMetadata, KVTransferConfig,
        Request)

logger = logging.getLogger(__name__)


class KVConnectorBase(ABC):
    """Abstract base class for KV transfer connectors."""

    def __init__(
        self,
        config: KVTransferConfig,
        kv_cache_config: Optional[Any] = None,
    ):
        self.config = config
        self.kv_cache_config = kv_cache_config
        self._kv_caches: Dict[str, Any] = {}  # layer_name -> kv_cache tensor
        self._lock = threading.RLock()
        self._initialized = False

        # Health tracking
        self._last_health_check = 0.0
        self._health_status = True
        self._error_count = 0

    # Worker-side methods

    def register_kv_caches(self, kv_caches: Dict[str, Any]) -> None:
        """Register KV caches for transfer operations."""
        with self._lock:
            self._kv_caches = kv_caches
            self._initialized = True
            logger.debug("Registered %d KV cache layers for transfer", len(kv_caches))

    @abstractmethod
    def start_load_kv(self, forward_context: ForwardContext, **kwargs: Any) -> None:
        """Start asynchronous KV cache loading."""
        ...

    @abstractmethod
    def wait_for_layer_load(self, layer_name: str) -> None:
        """Wait for a specific layer's KV cache to finish loading."""
        ...

    @abstractmethod
    def save_kv_layer(self, layer_name: str, kv_layer: Any, attn_metadata: Any, **kwargs: Any) -> None:
        """Save a layer's KV cache for transfer."""
        ...

    def wait_for_save(self) -> None:
        """Wait for all KV cache saves to complete."""
        pass

    # Scheduler-side methods

    @abstractmethod
    def get_num_new_matched_tokens(self, request: Request, num_computed_tokens: int) -> Tuple[int, bool]:
        """Get number of tokens that can be loaded from external KV cache."""
        ...

    @abstractmethod
    def update_state_after_alloc(self, request: Request, blocks: KVCacheBlocks, num_external_tokens: int) -> None:
        """Update connector state after block allocation."""
        ...

    @abstractmethod
    def build_connector_meta(self, scheduler_output: Any) -> KVConnectorMetadata:
        """Build metadata for worker-side operations."""
        ...

    @abstractmethod
    def request_finished(self, request: Request, block_ids: List[int]) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Handle request completion."""
        ...

    # Health and lifecycle

    def health_check(self) -> bool:
        """Check connector health."""
        return self._health_status and self._initialized

    def reset_error_count(self) -> None:
        """Reset error count after successful operation."""
        self._error_count = 0

    def record_error(self) -> None:
        """Record an error occurrence."""
        self._error_count += 1
        if self._error_count > self.config.retry_attempts:
            self._health_status = False
            logger.warning("KV connector marked unhealthy after %d errors", self._error_count)

    def close(self) -> None:
        """Close the connector and release resources."""
        with self._lock:
            self._kv_caches.clear()
            self._initialized = False
