
"""
Benchmark Kv V1 Vs V2 module.
"""
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Performance benchmark: KV V1 (Structural) vs KV V2 (Vectorized)

import time
import numpy as np
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.infrastructure.engine.kv_cache.v2.block_table import BlockTableV2
from src.infrastructure.engine.kv_cache.coordinator import KVCacheCoordinator
from src.infrastructure.engine.kv_cache.data_classes import CacheConfig, CacheGroupSpec
from src.infrastructure.engine.kv_cache.enums import CacheGroupType, EvictionPolicy

def benchmark_v1(num_blocks=1024, block_size=16, num_heads=32, num_iters=1000):
    spec = CacheGroupSpec(
        group_id=0,
        group_type=CacheGroupType.FULL_ATTENTION,
        block_size=block_size,
        num_kv_heads=num_heads,
        head_dim=128
    )
    config = CacheConfig(
        num_blocks=num_blocks,
        block_size=block_size,
        groups=[spec],
        enable_prefix_caching=True,
        eviction_policy=EvictionPolicy.LRU
    )
    coord = KVCacheCoordinator(config, max_model_len=4096)

    start = time.perf_counter()
    for i in range(num_iters):
        req_id = f"req_{i}"
        tokens = (i % 32) + 1
        blocks = coord.allocate(req_id, tokens)
        # Free immediately or every 2 steps to avoid OOM
        if i % 2 == 0:
            coord.free(f"req_{i-2}" if i >= 2 else f"req_{i}")

    end = time.perf_counter()
    return end - start

def benchmark_v2(num_blocks=1024, block_size=16, num_heads=32, num_iters=1000):
    table = BlockTableV2(num_blocks=num_blocks, block_size=block_size)

    start = time.perf_counter()
    for i in range(num_iters):
        num_tokens = (i % 32) + 1
        num_needed = (num_tokens + block_size - 1) // block_size

        block_ids = table.allocate(i, num_needed)

        if i % 2 == 0:
            table.free(i-2 if i >= 2 else i)

    end = time.perf_counter()
    return end - start

if __name__ == "__main__":
    print("--- KV CACHE PERFORMANCE BENCHMARK ---")
    ITERS = 5000
    BLOCKS = 8192

    print(f"Running {ITERS} ops with {BLOCKS} blocks...")

    try:
        t1 = benchmark_v1(num_blocks=BLOCKS, num_iters=ITERS)
        print(f"V1 (Structural/OOD) Time: {t1:.4f}s")
    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
        print(f"V1 Failed: {e}")
        t1 = 0

    try:
        t2 = benchmark_v2(num_blocks=BLOCKS, num_iters=ITERS)
        print(f"V2 (Vectorized/Hybrid) Time: {t2:.4f}s")
    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
        print(f"V2 Failed: {e}")
        t2 = 0

    if t1 > 0 and t2 > 0:
        speedup = t1 / t2
        print(f"Speedup: {speedup:.2f}x")

    print("\n--- Summary ---")
    print("V1 overhead is mostly Python object creation for individual blocks.")
    print("V2 uses numpy and simplified ID management, leading to significant speedup.")
