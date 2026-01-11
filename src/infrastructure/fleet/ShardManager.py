#!/usr/bin/env python3

from __future__ import annotations

import logging
from typing import Dict, List, Any, Optional, Set
from pathlib import Path

class ShardManager:
    """
    Manages partitioning of large fleets into semi-autonomous clusters (shards).
    This reduces broadcast noise and improves scalability for trillion-parameter systems.
    """
    
    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.shards: Dict[str, Set[str]] = {} # Shard name to agent names
        self.agent_to_shard: Dict[str, str] = {}
        self.communication_log: Dict[frozenset[str], int] = {} # Pairs of agents to frequency

    def log_communication(self, agent_a: str, agent_b: str) -> None:
        """Records a communication event between two agents."""
        pair = frozenset([agent_a, agent_b])
        self.communication_log[pair] = self.communication_log.get(pair, 0) + 1

    def create_shard(self, shard_name: str, capacity: int = 100) -> None:
        """Initializes a new shard."""
        if shard_name not in self.shards:
            self.shards[shard_name] = set()
            logging.info(f"ShardManager: Created shard '{shard_name}' with capacity {capacity}")

    def assign_agent(self, agent_name: str, shard_name: str) -> bool:
        """Assigns an agent to a specific shard."""
        if shard_name not in self.shards:
            self.create_shard(shard_name)
        
        # Remove from old shard if exists
        if agent_name in self.agent_to_shard:
            old_shard = self.agent_to_shard[agent_name]
            self.shards[old_shard].discard(agent_name)
            
        self.shards[shard_name].add(agent_name)
        self.agent_to_shard[agent_name] = shard_name
        logging.info(f"ShardManager: Assigned agent {agent_name} to shard {shard_name}")
        return True

    def get_shard_members(self, shard_name: str) -> List[str]:
        """Returns all agents in a shard."""
        return list(self.shards.get(shard_name, set()))

    def get_agent_shard(self, agent_name: str) -> Optional[str]:
        """Gets the shard containing the specified agent."""
        return self.agent_to_shard.get(agent_name)

    def optimize_sharding(self, threshold: int = 5) -> None:
        """
        Dynamic sharding logic based on communication frequency.
        Nodes that talk to each other frequently (>= threshold) are clustered together.
        """
        logging.info("ShardManager: Running dynamic sharding optimization (Phase 128)...")
        
        # Identify high-frequency pairings
        clusters: List[Set[str]] = []
        for pair, count in self.communication_log.items():
            if count >= threshold:
                agent_list = list(pair)
                found = False
                for cluster in clusters:
                    if any(a in cluster for a in agent_list):
                        cluster.update(agent_list)
                        found = True
                        break
                if not found:
                    clusters.append(set(agent_list))

        # Reassign agents based on discovered clusters
        for i, cluster in enumerate(clusters):
            shard_name = f"swarm_shard_{i}"
            for agent in cluster:
                self.assign_agent(agent, shard_name)
        
        logging.info(f"ShardManager: Optimization complete. Created {len(clusters)} tactical shards.")
