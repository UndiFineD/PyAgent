
"""
Test Phase65 Compression module.
"""
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Tests for Phase 65: Adaptive Swarm Compression

import pytest
import time
from src.infrastructure.engine.kv_cache.context_sharder import ContextShardManager
from src.infrastructure.engine.kv_cache.compression import AdaptiveSwarmCompressor

@pytest.mark.asyncio
async def test_adaptive_compression_cycle():
    manager = ContextShardManager(block_size=100)
    # Set high threshold for eviction so we can test compression first
    compressor = AdaptiveSwarmCompressor(manager, idle_threshold_sec=60.0)

    # 1. Create shards
    manager.shard_context("doc", 200, [0]) # 2 shards

    # Check initial state
    shards = manager.context_registry["doc"]
    assert all(s.precision == "float16" for s in shards)

    # 2. Trigger idle (simulated)
    # Manually backdate one shard to 15s (between 10s and 60s)
    shards[0].last_access = time.time() - 15.0
    shards[1].last_access = time.time() - 0.1

    stats = await compressor.run_optimization_cycle()
    assert stats["compressed"] == 1
    assert shards[0].precision == "fp8"
    assert shards[1].precision == "float16"

    # 3. Trigger eviction (simulated)
    compressor.idle_threshold_sec = 0.5 # Lower threshold now
    shards[0].last_access = time.time() - 15.0 # Now 15.0 > 0.5
    stats = await compressor.run_optimization_cycle()
    assert stats["evicted"] >= 1
    assert shards[0].is_cached is False

    # 4. Touch to restore
    compressor.touch_shard("doc", 50)
    assert shards[0].is_cached is True
    assert shards[0].precision == "float16"
