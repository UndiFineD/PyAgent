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
Core logic for fleet sharding and partitioning.
"""

from __future__ import annotations
from .base_core import BaseCore

try:
    import rust_core as rc # pylint: disable=import-error
except ImportError:
    rc = None

class ShardCore(BaseCore):
    """
    Authoritative engine for agent and data partitioning.
    Handles shard assignment, rebalancing, and cross-shard routing.
    """
    def calculate_shard_id(self, key: str, shard_count: int) -> int:
        """
        Determines the shard ID for a given key.
        Hot path for Rust acceleration in docs/RUST_MAPPING.md.
        """
        if rc and hasattr(rc, "calculate_shard_id_rust"): # pylint: disable=no-member
            try:
                return rc.calculate_shard_id_rust( # pylint: disable=no-member
                    key, shard_count
                ) # type: ignore
            except Exception: # pylint: disable=broad-exception-caught
                pass

        # Fallback to simple hash-based sharding
        import hashlib # pylint: disable=import-outside-toplevel
        h = hashlib.md5(key.encode()).digest()
        seed = int.from_bytes(h[:8], "big")
        return seed % shard_count
