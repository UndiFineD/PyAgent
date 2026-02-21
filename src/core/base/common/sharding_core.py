#!/usr/bin/env python3
"""Sharding core - minimal parser-safe implementation."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    from .base_core import BaseCore
except Exception:
    class BaseCore:  # pragma: no cover - fallback for tests
        def __init__(self, name: str = "Base") -> None:
            self.name = name


class ShardingCore(BaseCore):
    """Simple sharding helper used for tests and to avoid import errors."""

    def __init__(self, cluster_size: int = 4) -> None:
        super().__init__(name="ShardingCore")
        self.cluster_size = cluster_size
        self.replication_factor = 2

    def calculate_shard_id(self, key: str, shard_count: Optional[int] = None) -> int:
        count = shard_count or self.cluster_size
        # Simple stable hash fallback
        return abs(hash(key)) % max(1, count)

    def get_replica_shards(self, key: str, shard_count: Optional[int] = None) -> List[int]:
        primary = self.calculate_shard_id(key, shard_count)
        count = shard_count or self.cluster_size
        replicas = [primary]
        for i in range(1, self.replication_factor):
            replicas.append((primary + i) % max(1, count))
        return replicas

    def calculate_splits(self, tensor_shape: List[int], num_nodes: int) -> Dict[int, List[int]]:
        # Naive split along last dimension
        splits: Dict[int, List[int]] = {}
        if not tensor_shape:
            return splits
        last_dim = tensor_shape[-1]
        chunk = max(1, last_dim // max(1, num_nodes))
        for i in range(num_nodes):
            new_shape = list(tensor_shape)
            start = i * chunk
            end = last_dim if i == num_nodes - 1 else (i + 1) * chunk
            new_shape[-1] = max(1, end - start)
            splits[i] = new_shape
        return splits

    def assign_workload(self, node_loads: List[float]) -> int:
        if not node_loads:
            return 0
        # pick the node with minimum load
        return int(min(range(len(node_loads)), key=lambda i: node_loads[i]))

    def verify_sync(self, ready_node_flags: List[bool]) -> bool:
        return all(ready_node_flags)

    def aggregate_swarm_metrics(self, node_stats: Dict[int, Dict[str, float]]) -> Dict[str, float]:
        if not node_stats:
            return {}
        avg_lat = sum(s.get("latency", 0.0) for s in node_stats.values()) / len(node_stats)
        total_thr = sum(s.get("throughput", 0.0) for s in node_stats.values())
        return {"avg_latency": avg_lat, "total_throughput": total_thr}

