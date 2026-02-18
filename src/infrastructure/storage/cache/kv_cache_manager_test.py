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

try:
    import pytest
except ImportError:
    import pytest

try:
    from infrastructure.storage.cache.kv_cache_manager import DeviceType, DType, KVCacheConfig, KVCacheBlock, KVCacheBlocks, KVCacheAllocator, PagedKVCache, KVCacheTransfer, KVCacheManager, create_kv_cache_manager
except ImportError:
    from infrastructure.storage.cache.kv_cache_manager import DeviceType, DType, KVCacheConfig, KVCacheBlock, KVCacheBlocks, KVCacheAllocator, PagedKVCache, KVCacheTransfer, KVCacheManager, create_kv_cache_manager



def test_devicetype_basic():
    assert DeviceType is not None


def test_dtype_basic():
    assert DType is not None


def test_kvcacheconfig_basic():
    assert KVCacheConfig is not None


def test_kvcacheblock_basic():
    assert KVCacheBlock is not None


def test_kvcacheblocks_basic():
    assert KVCacheBlocks is not None


def test_kvcacheallocator_basic():
    assert KVCacheAllocator is not None


def test_pagedkvcache_basic():
    assert PagedKVCache is not None


def test_kvcachetransfer_basic():
    assert KVCacheTransfer is not None


def test_kvcachemanager_basic():
    assert KVCacheManager is not None


def test_create_kv_cache_manager_basic():
    assert callable(create_kv_cache_manager)
