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

"""
Test Phase67 Prefetch module.
"""
# Tests for Phase 67: Predictive Context Prefetching

import pytest
from src.infrastructure.engine.kv_cache.context_sharder import ContextShardManager
from src.infrastructure.engine.kv_cache.compression import AdaptiveSwarmCompressor
from src.infrastructure.engine.kv_cache.prefetcher import ContextPrefetcher


@pytest.mark.asyncio
async def test_predictive_prefetching_success():
    # 1. Setup Stack
    block_size = 100
    manager = ContextShardManager(block_size=block_size)
    compressor = AdaptiveSwarmCompressor(manager, idle_threshold_sec=60.0)
    prefetcher = ContextPrefetcher(manager, compressor, lookahead_shards=1)

    # doc1, 300 tokens (3 shards: 0-99, 100-199, 200-299)
    manager.shard_context("doc1", 300, [0])
    shards = manager.context_registry["doc1"]

    # 2. Simulate Cold/Compress State for future shards
    shards[1].precision = "fp8"
    shards[2].precision = "fp8"
    shards[2].is_cached = False  # Evicted

    # 3. Access sequence
    # Access shard 0 (token 0)
    prefetcher.record_access("doc1", 0)
    # Access shard 0 again (token 10) -> Detection of sequential movement
    prefetcher.record_access("doc1", 10)

    # 4. Verification
    # Prefetcher should have predicted tokens in the next shard (e.g. 100)
    # and "touched" it, which restores precision to float16 and is_cached to True
    assert shards[1].precision == "float16", "Shard 1 (100-199) should have been prefetched to float16"

    # Let's move deeper to trigger shard 2 prefetch
    prefetcher.record_access("doc1", 110)
    assert shards[2].is_cached, "Shard 2 (200-299) should have been prefetched/reloaded"
    assert shards[2].precision == "float16"
