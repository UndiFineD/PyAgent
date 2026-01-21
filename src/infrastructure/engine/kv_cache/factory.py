"""Factory for creating KV cache coordinators."""
# SPDX-License-Identifier: Apache-2.0
from typing import Any
from .data_classes import CacheConfig
from .coordinator import KVCacheCoordinator
from .advanced import (
    HierarchicalKVCacheCoordinator, PredictiveKVCacheCoordinator, AsyncPrefetchCoordinator
)

def create_kv_cache_coordinator(
    config: CacheConfig,
    max_model_len: int,
    coordinator_type: str = 'default',
    **kwargs: Any,
) -> KVCacheCoordinator:
    """Factory function to create appropriate coordinator."""
    if coordinator_type == 'default':
        return KVCacheCoordinator(config, max_model_len)
    if coordinator_type == 'hierarchical':
        return HierarchicalKVCacheCoordinator(
            config, max_model_len,
            num_layers=kwargs.get('num_layers', 32),
        )
    if coordinator_type == 'predictive':
        return PredictiveKVCacheCoordinator(
            config, max_model_len,
            memory_budget_bytes=kwargs.get('memory_budget', 1 << 30),
        )
    if coordinator_type == 'async_prefetch':
        return AsyncPrefetchCoordinator(
            config, max_model_len,
            prefetch_queue_size=kwargs.get('prefetch_queue_size', 100),
        )
    return KVCacheCoordinator(config, max_model_len)

    else:
        raise ValueError(f"Unknown coordinator type: {coordinator_type}")
