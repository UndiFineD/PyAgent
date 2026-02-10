#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from src.infrastructure.engine.kv_cache.context_sharder import ContextShardManager

def test_distributed_overlap_buffers():
    """Verifies that shards have correct overlap for sliding window attention."""
    # Block size 100, overlap 20
    manager = ContextShardManager(block_size=100)

    shards = manager.shard_context(
        context_id="overlapping_task",
        total_tokens=250,
        available_ranks=[0, 1, 2],
        overlap=20
    )

    # Shard 0: 0 to 100 (no overlap)
    assert shards[0].start_token == 0
    assert shards[0].end_token == 100
    assert shards[0].overlap_size == 0

    # Shard 1: 80 to 200 (20 tokens overlap from previous)
    assert shards[1].start_token == 80  # 100 - 20
    assert shards[1].end_token == 200
    assert shards[1].overlap_size == 20

    # Shard 2: 180 to 250
    assert shards[2].start_token == 180 # 200 - 20
    assert shards[2].end_token == 250

    print("\nPhase 78: Distributed token-shifting (Overlap Buffers) verified.")
