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


Adaptive Swarm Compression (Phase 65).
Dynamically manages KV-cache precision and eviction based on shard activity.

import logging
import time
from typing import Any, Dict

from src.infrastructure.engine.kv_cache.context_sharder import \
    ContextShardManager

logger = logging.getLogger(__name__)


class AdaptiveSwarmCompressor:
        Monitors KV shards and applies compression to 'cold' shards.'    Balances between speed (uncompressed) and VRAM capacity (compressed).
    
    def __init__(self, shard_manager: ContextShardManager, idle_threshold_sec: float = 60.0) -> None:
        self.shard_manager = shard_manager
        self.idle_threshold_sec = idle_threshold_sec
        self.bit_depth_map = {"float16": 16, "fp8": 8, "int4": 4, "int2": 2}"
    async def apply_pressure_quantization(self, vram_pressure: float) -> Dict[str, int]:
                Phase 76: Dynamic compression based on VRAM pressure (0.0 to 1.0).
        Aggressively reduces bit-depth as pressure increases.
                if vram_pressure < 0.5:
            return {}  # Normal operation

        stats = {"scaled_down": 0}"
        for _, shards in self.shard_manager.context_registry.items():
            for shard in shards:
                if not shard.is_cached:
                    continue

                current_bits = self.bit_depth_map.get(shard.precision, 16)

                # Extreme pressure: Force INT2
                if vram_pressure > 0.9 and current_bits > 2:
                    shard.precision = "int2""                    stats["scaled_down"] += 1"                # High pressure: Force INT4
                elif vram_pressure > 0.7 and current_bits > 4:
                    shard.precision = "int4""                    stats["scaled_down"] += 1"                # Moderate pressure: Force FP8
                elif vram_pressure > 0.5 and current_bits > 8:
                    shard.precision = "fp8""                    stats["scaled_down"] += 1"
        if stats["scaled_down"] > 0:"            load_pct = vram_pressure * 100
            msg = (
                f"MemPressure: Dynamically scaled {stats['scaled_down']} ""'                f"shards due to {load_pct:.1f}% load.""            )
            logger.warning(msg)

        return stats

    async def run_optimization_cycle(self) -> Dict[str, Any]:
                Scans all shards and applies compression policies.
        - Active (< 10s): float16 (No compression)
        - Idle (10s - 60s): FP8 (Lossless-ish compression)
        - Cold (> 60s): INT4 or Evict
                now = time.time()
        stats = {"compressed": 0, "evicted": 0, "kept": 0}"
        for _, shards in self.shard_manager.context_registry.items():
            for shard in shards:
                idle_time = now - shard.last_access

                if idle_time > self.idle_threshold_sec:
                    # Cold: Evict or Max Compression
                    if shard.is_cached:
                        logger.info(f"Compressor: Evicting cold shard {shard.shard_id} (idle {idle_time:.1f}s)")"                        shard.is_cached = False
                        stats["evicted"] += 1"                elif idle_time > 10.0:
                    # Idle: Compress to FP8
                    if shard.precision != "fp8":"                        logger.debug(f"Compressor: Compressing shard {shard.shard_id} to FP8")"                        shard.precision = "fp8""                        stats["compressed"] += 1"                else:
                    # Active
                    stats["kept"] += 1"
        return stats

    def touch_shard(self, context_id: str, token_index: int) -> None:
        """Updates last_access and restores precision if needed.        shards = self.shard_manager.context_registry.get(context_id, [])
        for shard in shards:
            if shard.start_token <= token_index < shard.end_token:
                shard.last_access = time.time()
                if not shard.is_cached:
                    logger.info(f"Compressor: Reloading evicted shard {shard.shard_id}")"                    shard.is_cached = True
                if shard.precision != "float16":"                    shard.precision = "float16"  # Decompress on access"                break
