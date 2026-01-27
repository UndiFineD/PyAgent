#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import pytest
import asyncio
from src.infrastructure.engine.kv_cache.context_sharder import ContextShardManager
from src.infrastructure.engine.kv_cache.compression import AdaptiveSwarmCompressor

@pytest.mark.asyncio
async def test_dynamic_bit_scaling():
    """Verifies that shards downscale precision when VRAM pressure is high."""
    manager = ContextShardManager(block_size=512)
    compressor = AdaptiveSwarmCompressor(manager)

    # Create some float16 shards
    manager.shard_context("heavy_task", 10000, [0, 1])
    shard = manager.context_registry["heavy_task"][0]
    assert shard.precision == "float16"

    # 1. Moderate pressure (55%) -> FP8
    await compressor.apply_pressure_quantization(0.55)
    assert shard.precision == "fp8"

    # 2. High pressure (75%) -> INT4
    await compressor.apply_pressure_quantization(0.75)
    assert shard.precision == "int4"

    # 3. Extreme pressure (95%) -> INT2
    await compressor.apply_pressure_quantization(0.95)
    assert shard.precision == "int2"

    # 4. Low pressure (10%) -> No change (does not automatically upscale here, handled by touch_shard)
    await compressor.apply_pressure_quantization(0.10)
    assert shard.precision == "int2"

    print("\nPhase 76: Dynamic bit-scaling (on-the-fly quantization) verified.")
