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
Logic for distributing model shards, fleet agents, and workload across the swarm.
Integrates with Project Voyager and Rust-accelerated distributed benchmarks.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import numpy as np

from src.core.rust_bridge import RustBridge
from .base_core import BaseCore


class ShardingCore(BaseCore):
    """
    Manages Tensor Down-sharding, fleet partitioning, and Pipeline Parallelism.
    Authoritative engine for agent and data partitioning across the swarm.
    """

    def __init__(self, cluster_size: int = 4) -> None:
        super().__init__(name="ShardingCore")
        self.cluster_size = cluster_size
        self.shards: Dict[int, Dict[str, Any]] = {}
        self.replication_factor = 2

    def calculate_shard_id(self, key: str, shard_count: Optional[int] = None) -> int:
        """
        Determines the shard ID for a given key (Fleet Partitioning).
        Uses high-speed MD5 Rust acceleration if available.
        """
        count = shard_count or self.cluster_size
        return RustBridge.calculate_shard_id(key, count)

    def get_replica_shards(self, key: str, shard_count: Optional[int] = None) -> List[int]:
        """Returns a list of primary and replica shard IDs for high availability."""
        primary = self.calculate_shard_id(key, shard_count)
        count = shard_count or self.cluster_size

        replicas = [primary]
        for i in range(1, self.replication_factor):
            replicas.append((primary + i) % count)
        return replicas

    def calculate_splits(self, tensor_shape: List[int], num_nodes: int) -> Dict[int, List[int]]:
        """
        Determines how to split a large tensor across multiple nodes.
        Uses Rust multi_node_coordinate_rust if available.
        """
        if RustBridge.is_rust_active():
            # node_id, total_nodes, shape
            res = RustBridge._try_rust_call("multi_node_coordinate_rust", 0, num_nodes, tensor_shape)
            if res:
                return res

        # Python fallback: Split along the last dimension
        splits = {}
        last_dim = tensor_shape[-1]
        chunk = last_dim // num_nodes

        for i in range(num_nodes):
            new_shape = list(tensor_shape)
            start = i * chunk
            end = last_dim if i == num_nodes - 1 else (i + 1) * chunk
            new_shape[-1] = end - start
            splits[i] = new_shape

        return splits

    def assign_workload(self, node_loads: List[float]) -> int:
        """
        Selects the best node for new work using Power of Two Choices (P2C).
        """
        if not node_loads:
            return 0

        ranks = list(range(len(node_loads)))
        if RustBridge.is_rust_active():
            res = RustBridge._try_rust_call("load_balance_select_rust", ranks, node_loads)
            if res is not None:
                return int(res)

        # Python fallback: pick minimum load
        return int(np.argmin(node_loads))

    def verify_sync(self, ready_node_flags: List[bool]) -> bool:
        """
        Checks if all nodes in a pipeline stage are ready for sync.
        Uses SIMD-accelerated Rust wave_sync_check_rust.
        """
        if RustBridge.is_rust_active():
            return RustBridge._try_rust_call("wave_sync_check_rust", ready_node_flags)

        return all(ready_node_flags)

    def aggregate_swarm_metrics(self, node_stats: Dict[int, Dict[str, float]]) -> Dict[str, float]:
        """
        Aggregates performance metrics from all nodes in the shard.
        """
        if RustBridge.is_rust_active():
            return RustBridge._try_rust_call("dp_stats_aggregate_rust", node_stats)

        # Python fallback
        if not node_stats:
            return {}

        avg_lat = sum(s.get("latency", 0.0) for s in node_stats.values()) / len(node_stats)
        total_thr = sum(s.get("throughput", 0.0) for s in node_stats.values())

        return {"avg_latency": avg_lat, "total_throughput": total_thr}
