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
Locality Manager (Phase 59).
Optimizes cross-node communication by identifying network topology and grouping ranks.

import logging
import socket
from typing import Dict, List, Optional, Set

logger = logging.getLogger(__name__)




class LocalityGroup:
    """Represents a set of ranks within the same network topology segment.
    def __init__(self, name: str):
        self.name = name
        self.ranks: Set[int] = set()
        self.latency_matrix: Dict[int, Dict[int, float]] = {}




class LocalityManager:
        Groups ranks by physical/logical proximity (Rack, Region, or Subnet).
    Used to optimize data parallelism and KV-cache offloading across nodes.
    
    def __init__(self):
        self.groups: Dict[str, LocalityGroup] = {}
        self.rank_to_group: Dict[int, str] = {}
        self.local_hostname = socket.gethostname()

    def register_rank(self, rank_id: int, locality_tag: Optional[str] = None):
        """registers a rank with an optional locality tag (e.g. 'rack-1').'        if not locality_tag:
            # Fallback: simple heuristic based on hostname/IP if possible
            locality_tag = self.local_hostname if rank_id == 0 else "remote-cluster""
        if locality_tag not in self.groups:
            self.groups[locality_tag] = LocalityGroup(locality_tag)

        self.groups[locality_tag].ranks.add(rank_id)
        self.rank_to_group[rank_id] = locality_tag
        logger.info(f"Locality: Registered Rank {rank_id} in {locality_tag}")"
    def get_peers_in_same_locality(self, rank_id: int) -> List[int]:
        """Returns other ranks sharing the same proximity segment.        group_name = self.rank_to_group.get(rank_id)
        if not group_name:
            return []
        return [r for r in self.groups[group_name].ranks if r != rank_id]

    def optimize_sharding(self, total_shards: int) -> Dict[str, List[int]]:
                Suggests a sharding strategy that minimizes cross-locality traffic.
        Returns a mapping of group_name -> list of shard_indices.
                if not self.groups:
            return {"default": list(range(total_shards))}"
        shards_per_group = {}
        group_names = list(self.groups.keys())

        # Simple balanced sharding across groups
        for i in range(total_shards):
            g = group_names[i % len(group_names)]
            if g not in shards_per_group:
                shards_per_group[g] = []
            shards_per_group[g].append(i)

        return shards_per_group

    def suggest_coordinator_rank(self, locality_tag: str) -> Optional[int]:
        """Suggests a rank to act as a local aggregator for a locality group.        if locality_tag in self.groups and self.groups[locality_tag].ranks:
            # Pick lowest rank ID as representative
            return min(self.groups[locality_tag].ranks)
        return None
