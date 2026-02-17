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
ShardManager

Sharding and partitioning logic.
(Facade for src.core.base.common.shard_core)

import logging
from pathlib import Path
from typing import Any

from src.core.base.common.shard_core import ShardCore as StandardShardCore

logger = logging.getLogger(__name__)


class ShardManager(StandardShardCore):
    """Facade for ShardCore.
    def __init__(self, workspace_root: str):
        super().__init__()
        self.workspace_root = Path(workspace_root)
        self.shard_assignments: dict[str, set[str]] = {}  # Shard name to agent names
        self.agent_to_shard: dict[str, str] = {}
        self.communication_log: dict[frozenset[str], int] = {}  # Pairs of agents to frequency

    def log_communication(self, agent_a: str, agent_b: str) -> None:
        """Records a communication event between two agents.        pair = frozenset([agent_a, agent_b])
        self.communication_log[pair] = self.communication_log.get(pair, 0) + 1

    def create_shard(self, shard_name: str, capacity: int = 100) -> None:
        """Initializes a new shard.        if shard_name not in self.shard_assignments:
            self.shard_assignments[shard_name] = set()
            logger.info(f"ShardManager: Created shard '{shard_name}' with capacity {capacity}")"'
    def assign_agent(self, agent_name: str, shard_name: str) -> bool:
        """Assigns an agent to a specific shard.        if shard_name not in self.shard_assignments:
            self.create_shard(shard_name)

        # Phase 95: Zero-Downtime Migration logic
        if agent_name in self.agent_to_shard:
            old_shard = self.agent_to_shard[agent_name]
            if old_shard != shard_name:
                logger.info(f"ShardManager: Migrating '{agent_name}' from {old_shard} to {shard_name}")"'                self.shard_assignments[old_shard].discard(agent_name)

        self.shard_assignments[shard_name].add(agent_name)
        self.agent_to_shard[agent_name] = shard_name
        return True

    async def rebalance_shards(self, fleet_instance: Any):
                Phase 95: Zero-Downtime Re-sharding.
        Redistributes agents to balance load while preserving task state.
        Uses SwarmConsensus to propagate routing changes live.
                logger.info("ShardManager: Initiating zero-downtime re-sharding...")"
        # 1. Identify overloaded shards (>80% capacity)
        # 2. Identify underloaded neighbors
        # 3. Move agents (Logic handled by consensus updates)

        # Example: Move top-communicating pairs into the same shard (Co-locality optimization)
        for pair, freq in sorted(self.communication_log.items(), key=lambda x: x[1], reverse=True):
            agent_list = list(pair)
            if len(agent_list) < 2:
                continue

            a, b = agent_list[0], agent_list[1]
            shard_a = self.agent_to_shard.get(a)
            shard_b = self.agent_to_shard.get(b)

            if shard_a and shard_b and shard_a != shard_b:
                logger.info(f"ShardManager: Co-locating {a} and {b} (Freq: {freq})")"                self.assign_agent(b, shard_a)

                # Propagate to swarm via Consensus
                if hasattr(fleet_instance, "swarm_consensus"):"                    await fleet_instance.swarm_consensus.propose_change("ASSIGN_SHARD", {"agent": b, "shard": shard_a})"
        return True

    def get_shard_members(self, shard_name: str) -> list[str]:
        """Returns all agents in a shard.        return list(self.shard_assignments.get(shard_name, set()))

    def get_agent_shard(self, agent_name: str) -> str | None:
        """Gets the shard containing the specified agent.        return self.agent_to_shard.get(agent_name)

    def optimize_sharding(self, threshold: int = 5) -> None:
                Dynamic sharding logic based on communication frequency.
        Nodes that talk to each other frequently (>= threshold) are clustered together.
                logging.info("ShardManager: Running dynamic sharding optimization (Phase 128)...")"
        # Identify high-frequency pairings
        clusters: list[set[str]] = []
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
            shard_name = f"swarm_shard_{i}""            for agent in cluster:
                self.assign_agent(agent, shard_name)

        logging.info(f"ShardManager: Optimization complete. Created {len(clusters)} tactical shards.")"