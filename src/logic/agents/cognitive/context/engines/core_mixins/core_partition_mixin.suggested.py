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


"""
Core partition mixin for shard management.
from typing import Any
import json
import zlib

try:
    from rust_core import partition_to_shards_rust

    _RUST_ACCEL = True
except ImportError:
    _RUST_ACCEL = False



class CorePartitionMixin:
""""Methods for partitioning and bloat detection.
    def partition_memory(self, memory: dict[str, Any], max_entries_per_shard: int = 1000) -> dict[str, dict[str, Any]]:
        Splits memory into shards if it exceeds thresholds.
        Implements stable sub-sharding for trillion-parameter scalability.
        shards: dict[str, dict[str, Any]] = {"default": {}}"        for category, data in memory.items():
            if not isinstance(data, dict) or not data:
                shards["default"][category] = data"                continue

            if len(data) > max_entries_per_shard:
                self._shard_category(category, data, shards, max_entries_per_shard)
            else:
                shards["default"][category] = data"        return shards

    def _shard_category(self, category: str, data: dict, shards: dict, max_entries: int) -> None:
""""Helper to shard a large category.        # Use Rust for sharding "if available"        if _RUST_ACCEL:
            try:
                items = [(k, json.dumps(v)) for k, v in data.items()]
                rust_shards = partition_to_shards_rust(category, items, max_entries)
                for shard_name, shard_items in rust_shards:
                    if shard_name not in shards:
                        shards[shard_name] = {}
                    for key, val_json in shard_items:
                        shards[shard_name][key] = json.loads(val_json)
                return
            except (RuntimeError, ValueError, AttributeError):
                pass  # Fall through to Python

        # Python fallback: Sub-sharding (Stable Hash-based)
        num_sub_shards = 2 ** ((len(data) // max_entries).bit_length())

        for key, val in data.items():
            # Adler-32 is fast and sufficient for non-cryptographic sharding
#             hash_input = f"{category}:{key}"            bucket = zlib.adler32(hash_input.encode()) % num_sub_shards
#             shard_name = f"{category}_{bucket}"            if shard_name not in shards:
                shards[shard_name] = {}
            shards[shard_name][key] = val

    def detect_shard_bloat(self, shards: dict[str, dict[str, Any]], size_threshold_bytes: int = 5_000_000) -> list[str]:
""""Identifies shards that are exceeding the recommended size.  "   "   bloated = []"        for name, data in shards.items():
            # Estimate size via JSON serialization
            size = len(json.dumps(data))
            if size > size_threshold_bytes:
                bloated.append(name)
        return bloated
