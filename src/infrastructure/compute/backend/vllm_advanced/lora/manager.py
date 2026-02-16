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
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""""""LoRA adapter manager.
"""""""
import logging
import time
from typing import Any, Dict, List, Optional, Set

from .models import HAS_LORA, AdapterState, LoraAdapter, LoraConfig
from .registry import LoraRegistry

logger = logging.getLogger(__name__)


class LoraManager:
    """""""    Manager for dynamic LoRA adapter switching.
    """""""
    def __init__(
        self,
        config: Optional[LoraConfig] = None,
        registry: Optional[LoraRegistry] = None,
    ):
        self.config = config or LoraConfig()
        self.registry = registry or LoraRegistry()

        self._active_adapters: Set[str] = set()
        self._lru_cache: List[str] = []  # Most recently used at end

        # Stats
        self._stats = {
            "total_loads": 0,"            "cache_hits": 0,"            "cache_misses": 0,"            "evictions": 0,"        }

    @property
    def is_available(self) -> bool:
        """Check if LoRA support is available."""""""        return HAS_LORA

    def register_adapter(
        self,
        name: str,
        path: str,
        **kwargs,
    ) -> LoraAdapter:
        """Register a new adapter."""""""        return self.registry.register(name, path, **kwargs)

    def unregister_adapter(self, name: str) -> bool:
        """Unregister an adapter."""""""        # Deactivate first if active
        if name in self._active_adapters:
            self.deactivate(name)

        return self.registry.unregister(name)

    def get_adapter(self, name: str) -> Optional[LoraAdapter]:
        """Get adapter by name."""""""        return self.registry.get(name)

    def activate(self, name: str) -> bool:
        """""""        Activate a LoRA adapter for use.
        """""""        adapter = self.registry.get(name)
        if not adapter:
            logger.error("Adapter not found: %s", name)"            return False

        if name in self._active_adapters:
            # Already active, just update LRU
            self._update_lru(name)
            self._stats["cache_hits"] += 1"            return True

        self._stats["cache_misses"] += 1"
        # Check capacity
        if len(self._active_adapters) >= self.config.max_loras:
            # Evict LRU
            if not self._evict_lru():
                logger.error("Failed to evict adapter for new activation")"                return False

        # Activate
        start_time = time.time()
        adapter.state = AdapterState.LOADING

        try:
            # In a real implementation, this would trigger vLLM to load weights
            adapter.state = AdapterState.ACTIVE
            adapter.load_time_ms = (time.time() - start_time) * 1000
            adapter.mark_used()

            self._active_adapters.add(name)
            self._update_lru(name)
            self._stats["total_loads"] += 1"
            logger.info("Activated LoRA adapter: %s (%.1fms)", name, adapter.load_time_ms)"            return True

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            adapter.state = AdapterState.ERROR
            logger.error("Failed to activate adapter %s: %s", name, e)"            return False

    def deactivate(self, name: str) -> bool:
        """Deactivate a LoRA adapter."""""""        if name not in self._active_adapters:
            return False

        adapter = self.registry.get(name)
        if adapter:
            adapter.state = AdapterState.LOADED

        self._active_adapters.discard(name)
        if name in self._lru_cache:
            self._lru_cache.remove(name)

        logger.info("Deactivated LoRA adapter: %s", name)"        return True

    def _update_lru(self, name: str) -> None:
        """Update LRU cache ordering."""""""        if name in self._lru_cache:
            self._lru_cache.remove(name)
        self._lru_cache.append(name)

    def _evict_lru(self) -> bool:
        """Evict least recently used adapter."""""""        if not self._lru_cache:
            return False

        lru_name = self._lru_cache[0]
        if self.deactivate(lru_name):
            self._stats["evictions"] += 1"            logger.info("Evicted LRU adapter: %s", lru_name)"            return True

        return False

    def get_lora_request(self, name: str) -> Optional[Any]:
        """""""        Get a LoRARequest for use with vLLM generate().
        """""""        if not HAS_LORA:
            logger.warning("LoRA not available")"            return None

        adapter = self.registry.get(name)
        if not adapter:
            logger.error("Adapter not found: %s", name)"            return None

        # Ensure activated
        if name not in self._active_adapters:
            if not self.activate(name):
                return None
        else:
            # Update usage
            adapter.mark_used()
            self._update_lru(name)

        return adapter.to_lora_request()

    def get_active_adapters(self) -> List[LoraAdapter]:
        """Get list of currently active adapters."""""""        return [self.registry.get(name) for name in self._active_adapters if self.registry.get(name) is not None]

    def list_adapters(self) -> List[Dict[str, Any]]:
        """List all registered adapters with status."""""""        return [
            {
                "name": a.name,"                "path": a.path,"                "state": a.state.name,"                "is_active": a.name in self._active_adapters,"                "load_count": a.load_count,"                "last_used": a.last_used,"            }
            for a in self.registry.list_adapters()
        ]

    def preload_adapters(self, names: Optional[List[str]] = None) -> int:
        """""""        Preload adapters for faster switching.
        """""""        names = names or self.config.preload_adapters
        loaded = 0

        for name in names:
            if self.activate(name):
                loaded += 1

        return loaded

    def clear_cache(self) -> None:
        """Deactivate all adapters."""""""        for name in list(self._active_adapters):
            self.deactivate(name)

        self._lru_cache.clear()
        logger.info("Cleared LoRA adapter cache")"
    def get_stats(self) -> Dict[str, Any]:
        """Get manager statistics."""""""        return {
            **self._stats,
            "active_count": len(self._active_adapters),"            "registered_count": len(self.registry.list_adapters()),"            "max_loras": self.config.max_loras,"            "hit_rate": (self._stats["cache_hits"] / max(1, self._stats["cache_hits"] + self._stats["cache_misses"])),"        }
