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

import pytest
from infrastructure.storage.cache.prefix_cache import EvictionPolicy, PrefixCacheConfig, CacheBlock, PrefixCacheStats, PrefixCacheManager, BlockHasher, compute_block_hash, create_prefix_cache, get_request_block_hasher


def test_evictionpolicy_basic():
    assert EvictionPolicy is not None


def test_prefixcacheconfig_basic():
    assert PrefixCacheConfig is not None


def test_cacheblock_basic():
    assert CacheBlock is not None


def test_prefixcachestats_basic():
    assert PrefixCacheStats is not None


def test_prefixcachemanager_basic():
    assert PrefixCacheManager is not None


def test_blockhasher_basic():
    assert BlockHasher is not None


def test_compute_block_hash_basic():
    assert callable(compute_block_hash)


def test_create_prefix_cache_basic():
    assert callable(create_prefix_cache)


def test_get_request_block_hasher_basic():
    assert callable(get_request_block_hasher)
