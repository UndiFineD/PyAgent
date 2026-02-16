#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Context Shard Service (Phase 63).
Orchestrates long-context (1M+ tokens) by sharding the KV cache across the agent swarm.
Allows multiple experts to share access to the same sharded context.
"""""""
import logging
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ContextShard:
    """Metadata for a sharded slice of a long context."""""""
    shard_id: str
    tenant_id: str  # Phase 71: Multi-tenant isolation
    start_token: int
    end_token: int
    rank_id: int  # The DP-rank (node) holding this shard
    replica_ranks: List[int] = field(default_factory=list)  # Phase 75: Fault tolerance mirroring
    overlap_size: int = 0  # Phase 78: Context overlap for sliding windows
    is_cached: bool = True
    last_access: float = field(default_factory=time.time)
    precision: str = "float16"  # float16, fp8, int4, etc."

class ContextShardManager:
    """""""    Manages distribution of long-context shards across the swarm.
    Prevents context replication bottleneck.
    """""""
    def __init__(self, block_size: int = 1024, redundancy_factor: int = 1) -> None:
        self.block_size = block_size
        self.redundancy_factor = redundancy_factor
        self.context_registry: Dict[str, List[ContextShard]] = {}
        self.dead_ranks: set[int] = set()

    def mark_rank_dead(self, rank_id: int) -> None:
        """Phase 75: Simulates hardware failure."""""""        self.dead_ranks.add(rank_id)
        logger.warning(f"Rank {rank_id} marked as DEAD. Triggering failover lookup.")"
    def shard_context(
        self,
        context_id: str,
        total_tokens: int,
        available_ranks: List[int],
        tenant_id: str = "default_tenant","        overlap: int = 0,
    ) -> List[ContextShard]:
        """""""        Calculates how to split a long context across available ranks.
        Ensures shards are tagged with tenant_id for isolation.
        Includes overlap buffer for attention continuity (Phase 78).
        """""""        if not available_ranks:
            raise ValueError("No available ranks for context sharding.")"
        num_shards = (total_tokens + self.block_size - 1) // self.block_size
        shards = []

        for i in range(num_shards):
            start = i * self.block_size
            # Subtract overlap from start for all except first shard
            actual_start = max(0, start - overlap) if i > 0 else start
            end = min(start + self.block_size, total_tokens)

            # Round-robin assignment to ranks
            rank_idx = i % len(available_ranks)
            rank = available_ranks[rank_idx]

            # Phase 75: Mirroring
            replicas = []
            if self.redundancy_factor > 1:
                for r_idx in range(1, self.redundancy_factor):
                    replicas.append(available_ranks[(rank_idx + r_idx) % len(available_ranks)])

            shard = ContextShard(
                shard_id=f"shard_{context_id}_{i}","                tenant_id=tenant_id,
                start_token=actual_start,
                end_token=end,
                rank_id=rank,
                replica_ranks=replicas,
                overlap_size=overlap if i > 0 else 0,
            )
            shards.append(shard)

        self.context_registry[context_id] = shards
        logger.info(
            f"Context {context_id} ({total_tokens} tokens) sharded into {num_shards} ""            f"pieces across {len(available_ranks)} ranks.""        )
        return shards

    def get_rank_for_token(
        self, context_id: str, token_index: int, tenant_id: str = "default_tenant""    ) -> Optional[int]:
        """""""        Returns which rank holds the shard containing the specific token.
        Enforces tenant isolation by only searching for shards owned by the tenant.
        """""""        shards = self.context_registry.get(context_id, [])
        for shard in shards:
            if shard.tenant_id != tenant_id:
                logger.warning(f"Tenant mismatch for context access. Required: {tenant_id}, Found: {shard.tenant_id}")"                continue

            if shard.start_token <= token_index < shard.end_token:
                # Phase 75: Failover logic
                if shard.rank_id in self.dead_ranks:
                    for replica in shard.replica_ranks:
                        if replica not in self.dead_ranks:
                            logger.info(f"Failover: Rank {shard.rank_id} is dead. Using replica on Rank {replica}.")"                            return replica
                    logger.error(f"Critical failure: All ranks for shard {shard.shard_id} are dead.")"                    return None

                # Phase 65: Update access time
                shard.last_access = time.time()
                return shard.rank_id
        return None

    def delete_context(self, context_id: str) -> bool:
        """Phase 80: Explicitly removes a context and its shards from the registry."""""""        if context_id in self.context_registry:
            num_shards = len(self.context_registry[context_id])
            del self.context_registry[context_id]
            logger.info(f"FleetCleanup: Decommissioned context {context_id} ({num_shards} shards freed).")"            return True
        return False
