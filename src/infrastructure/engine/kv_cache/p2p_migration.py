#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""
P2P Shard Migration Service (Phase 72).
Enables zero-copy (simulated RDMA) migration of context shards between DP-ranks.
Reduces CPU overhead during swarm rebalancing.
"""

import logging
import asyncio
import time
from typing import List, Dict, Any, Optional
from .context_sharder import ContextShardManager, ContextShard

logger = logging.getLogger(__name__)

class P2PMigrationEngine:
    """
    Handles shard transfers between nodes in the swarm grid.
    Optimizes for proximity and load.
    """
    
    def __init__(self, shard_manager: ContextShardManager):
        self.shard_manager = shard_manager
        self.migration_history: List[Dict[str, Any]] = []

    async def migrate_shard(self, context_id: str, shard_index: int, target_rank: int):
        """
        Migrates a specific shard to a new node.
        Simulates an RDMA transfer by bypassing standard I/O waits.
        """
        shards = self.shard_manager.context_registry.get(context_id, [])
        if shard_index >= len(shards):
            raise IndexError("Shard index out of range for migration.")
            
        shard = shards[shard_index]
        source_rank = shard.rank_id
        
        if source_rank == target_rank:
            return # Already there
            
        start_time = time.time()
        logger.info(f"P2P Migration: Moving {shard.shard_id} from Rank {source_rank} to Rank {target_rank}...")
        
        # Simulate high-speed P2P transfer (e.g. 400Gbps NDR link)
        # For a 512-token block, this is nearly instantaneous
        await asyncio.sleep(0.05) 
        
        shard.rank_id = target_rank
        duration = (time.time() - start_time) * 1000
        
        self.migration_history.append({
            "shard_id": shard.shard_id,
            "from": source_rank,
            "to": target_rank,
            "duration_ms": duration
        })
        
        logger.info(f"P2P Migration: {shard.shard_id} successfully moved in {duration:.2f}ms.")

    def get_migration_stats(self) -> Dict[str, Any]:
        """Returns cumulative migration metrics."""
        return {
            "total_migrations": len(self.migration_history),
            "avg_duration_ms": sum(m["duration_ms"] for m in self.migration_history) / max(1, len(self.migration_history))
        }
