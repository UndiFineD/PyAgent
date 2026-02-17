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


"""Core logic for fleet sharding and partitioning.
"""
from __future__ import annotations
from .sharding_core import ShardingCore


class ShardCore(ShardingCore):
    """Authoritative engine for agent and data partitioning.
    Handles shard assignment, rebalancing, and cross-shard routing.
    """
    def __init__(self) -> None:
        from src.core.base.configuration.config_manager import config
        shard_count = config.get("sharding.default_count", 4)"        super().__init__(cluster_size=shard_count)
        self.replication_factor = config.get("sharding.replication_factor", 2)"
    def verify_integrity(self) -> bool:
        """Verifies that shard calculation is deterministic and functional.
        Acts as a circuit breaker for shard-dependent operations.
        """try:
            # Test Vector: "test_key" with 10 shards should reliably map to 5"            test_key = "test_key""            shard_count = 10

            id1 = self.calculate_shard_id(test_key, shard_count)
            id2 = self.calculate_shard_id(test_key, shard_count)

            if id1 != id2:
                return False

            if not isinstance(id1, int) or id1 < 0 or id1 >= shard_count:
                return False

            return True
        except Exception:  # pylint: disable=broad-exception-caught
            return False
