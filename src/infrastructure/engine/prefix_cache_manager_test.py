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

import pytest
from infrastructure.engine.prefix_cache_manager import HashAlgorithm, BlockHash, CacheBlock, PrefixCacheManager, get_hash_function, hash_block_tokens, hash_block_tokens_rust, init_none_hash, compute_prefix_match, compute_prefix_match_rust, compute_cache_keys, compute_cache_keys_rust


def test_hashalgorithm_basic():
    assert HashAlgorithm is not None


def test_blockhash_basic():
    assert BlockHash is not None


def test_cacheblock_basic():
    assert CacheBlock is not None


def test_prefixcachemanager_basic():
    assert PrefixCacheManager is not None


def test_get_hash_function_basic():
    assert callable(get_hash_function)


def test_hash_block_tokens_basic():
    assert callable(hash_block_tokens)


def test_hash_block_tokens_rust_basic():
    assert callable(hash_block_tokens_rust)


def test_init_none_hash_basic():
    assert callable(init_none_hash)


def test_compute_prefix_match_basic():
    assert callable(compute_prefix_match)


def test_compute_prefix_match_rust_basic():
    assert callable(compute_prefix_match_rust)


def test_compute_cache_keys_basic():
    assert callable(compute_cache_keys)


def test_compute_cache_keys_rust_basic():
    assert callable(compute_cache_keys_rust)
