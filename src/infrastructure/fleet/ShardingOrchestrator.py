#!/usr/bin/env python3

"""Dynamic Communication Sharding Orchestrator (Phase 128).
Optimizes swarm latency by clustering frequently interacting agents.
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Set
from collections import Counter

class ShardingOrchestrator:
    """Analyzes agent interactions and suggests/implements logical grouping."""

    def __init__(self, workspace_root: Path, interaction_threshold: int = 1000) -> None:
        self.workspace_root = workspace_root
        self.threshold = interaction_threshold
        self.interaction_log = workspace_root / "data/logs/interaction_matrix.json"
        self.shard_mapping_path = workspace_root / "config/shard_mapping.json"
        self._counts: Counter = Counter()
        self._total_interactions = 0

    def record_interaction(self, agent_a: str, agent_b: str) -> None:
        """Records a communication event between two agents."""
        pair = tuple(sorted([agent_a, agent_b]))
        self._counts[pair] += 1
        self._total_interactions += 1
        
        if self._total_interactions >= self.threshold:
            self.rebalance_shards()
            self._total_interactions = 0

    def rebalance_shards(self) -> None:
        """Clusters agents into logical shards based on interaction frequency."""
        logging.info("ShardingOrchestrator: Rebalancing logical shards...")
        
        # Simple Clustering: Agents with > 10% of total interactions go in the same shard
        clusters: List[Set[str]] = []
        for (a, b), count in self._counts.most_common():
            if count < (self.threshold * 0.05): # 5% threshold
                break
            
            # Find if either agent is already in a cluster
            found_a = next((c for c in clusters if a in c), None)
            found_b = next((c for c in clusters if b in c), None)
            
            if found_a and found_b:
                if found_a is not found_b:
                    found_a.update(found_b)
                    clusters.remove(found_b)
            elif found_a:
                found_a.add(b)
            elif found_b:
                found_b.add(a)
            else:
                clusters.append({a, b})
        
        # Persist mapping
        mapping = {f"shard_{i}": list(c) for i, c in enumerate(clusters)}
        self._save_mapping(mapping)
        logging.info(f"ShardingOrchestrator: Created {len(mapping)} logical clusters.")

    def _save_mapping(self, mapping: Dict[str, List[str]]) -> None:
        self.shard_mapping_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.shard_mapping_path, "w") as f:
            json.dump(mapping, f, indent=4)

    def load_mapping(self) -> Dict[str, List[str]]:
        if self.shard_mapping_path.exists():
            with open(self.shard_mapping_path, "r") as f:
                return json.load(f)
        return {}

if __name__ == "__main__":
    # Test stub
    orch = ShardingOrchestrator(Path("."))
    orch.record_interaction("CoderAgent", "ReviewAgent")
    orch.record_interaction("CoderAgent", "ReviewAgent")
    orch.rebalance_shards()
