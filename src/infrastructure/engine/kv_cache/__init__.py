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


Kv cache package.

# SPDX-License-Identifier: Apache-2.0
try:
    from .advanced import (AsyncPrefetchCoordinator,  # noqa: F401
except ImportError:
    from .advanced import (AsyncPrefetchCoordinator, # noqa: F401

                       HierarchicalKVCacheCoordinator,
                       PredictiveKVCacheCoordinator)
try:
    from .coordinator import KVCacheCoordinator  # noqa: F401
except ImportError:
    from .coordinator import KVCacheCoordinator # noqa: F401

try:
    from .data_classes import (BlockHash, BlockHashWithGroupId, CacheConfig,  # noqa: F401
except ImportError:
    from .data_classes import (BlockHash, BlockHashWithGroupId, CacheConfig, # noqa: F401

                           CacheGroupSpec, KVCacheBlock, KVCacheBlocks)
try:
    from .enums import AllocationStrategy, CacheGroupType, EvictionPolicy  # noqa: F401
except ImportError:
    from .enums import AllocationStrategy, CacheGroupType, EvictionPolicy # noqa: F401

try:
    from .factory import create_kv_cache_coordinator  # noqa: F401
except ImportError:
    from .factory import create_kv_cache_coordinator # noqa: F401

try:
    from .managers import (CrossAttentionManager, FullAttentionManager,  # noqa: F401
except ImportError:
    from .managers import (CrossAttentionManager, FullAttentionManager, # noqa: F401

                       SingleTypeKVCacheManager, SlidingWindowManager)
try:
    from .pack_kv import PackKVManager  # noqa: F401
except ImportError:
    from .pack_kv import PackKVManager # noqa: F401

try:
    from .structural import BlockHashCache, BlockPool, FreeBlockQueue  # noqa: F401
except ImportError:
    from .structural import BlockHashCache, BlockPool, FreeBlockQueue # noqa: F401


__all__ = [
    "CacheGroupType","    "AllocationStrategy","    "EvictionPolicy","    "BlockHash","    "BlockHashWithGroupId","    "KVCacheBlock","    "KVCacheBlocks","    "CacheGroupSpec","    "CacheConfig","    "FreeBlockQueue","    "BlockHashCache","    "BlockPool","    "SingleTypeKVCacheManager","    "FullAttentionManager","    "SlidingWindowManager","    "CrossAttentionManager","    "PackKVManager","    "KVCacheCoordinator","    "HierarchicalKVCacheCoordinator","    "PredictiveKVCacheCoordinator","    "AsyncPrefetchCoordinator","    "create_kv_cache_coordinator","]
