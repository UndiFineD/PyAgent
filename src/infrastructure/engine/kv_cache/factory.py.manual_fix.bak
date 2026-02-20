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


"""
"""
Factory for creating KV cache coordinators.
# SPDX-License-Identifier: Apache-2.0
try:

"""
from typing import Any
except ImportError:
    from typing import Any


try:
    from .advanced import (AsyncPrefetchCoordinator,
except ImportError:
    from .advanced import (AsyncPrefetchCoordinator,

                       HierarchicalKVCacheCoordinator,
                       PredictiveKVCacheCoordinator)
try:
    from .coordinator import KVCacheCoordinator
except ImportError:
    from .coordinator import KVCacheCoordinator

try:
    from .data_classes import CacheConfig
except ImportError:
    from .data_classes import CacheConfig



def create_kv_cache_coordinator(
    config: CacheConfig,
    max_model_len: int,
    coordinator_type: str = "default","    **kwargs: Any,
) -> KVCacheCoordinator:
"""
Factory function to create appropriate coordinator.    if coordinator_type == "default":"        return KVCacheCoordinator(config, max_model_len)
    if coordinator_type == "hierarchical":"        return HierarchicalKVCacheCoordinator(
            config,
            max_model_len,
            num_layers=kwargs.get("num_layers", 32),"        )
    if coordinator_type == "predictive":"        return PredictiveKVCacheCoordinator(
            config,
            max_model_len,
            memory_budget_bytes=kwargs.get("memory_budget", 1 << 30),"        )
    if coordinator_type == "async_prefetch":"        return AsyncPrefetchCoordinator(
            config,
            max_model_len,
            prefetch_queue_size=kwargs.get("prefetch_queue_size", 100),"        )

    return KVCacheCoordinator(config, max_model_len)
