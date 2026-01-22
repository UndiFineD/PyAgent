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

<<<<<<< HEAD
<<<<<<< HEAD
"""
Load balancer.py module.
"""

import asyncio
import logging
from typing import Any, Dict, List

from src.infrastructure.engine.kv_cache.context_sharder import \
    ContextShardManager
from src.infrastructure.engine.kv_cache.p2p_migration import P2PMigrationEngine
from src.infrastructure.swarm.orchestration.swarm.telemetry import \
    SwarmTelemetryService

logger: logging.Logger = logging.getLogger(__name__)

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
import asyncio
import logging
from typing import List, Dict, Any, Optional
from src.infrastructure.swarm.orchestration.swarm.telemetry import SwarmTelemetryService
from src.infrastructure.engine.kv_cache.context_sharder import ContextShardManager
from src.infrastructure.engine.kv_cache.p2p_migration import P2PMigrationEngine

logger = logging.getLogger(__name__)
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

class SwarmLoadBalancer:
    """
    Automated resource reallocation service.
    Monitors telemetry and re-shards context across ranks to prevent hotspots (Phase 81).
    """

    def __init__(
<<<<<<< HEAD
<<<<<<< HEAD
        self,
        telemetry: SwarmTelemetryService,
        shard_manager: ContextShardManager,
        migration_engine: P2PMigrationEngine,
        hot_threshold: float = 0.85,
        cool_threshold: float = 0.40,
    ) -> None:
        self.telemetry: SwarmTelemetryService = telemetry
        self.shard_manager: ContextShardManager = shard_manager
        self.migration_engine: P2PMigrationEngine = migration_engine
        self.hot_threshold: float = hot_threshold
        self.cool_threshold: float = cool_threshold
        self.balancing_active = True

    async def run_balancing_cycle(self) -> None:
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self, 
        telemetry: SwarmTelemetryService, 
        shard_manager: ContextShardManager,
        migration_engine: P2PMigrationEngine,
        hot_threshold: float = 0.85,
        cool_threshold: float = 0.40
    ):
        self.telemetry = telemetry
        self.shard_manager = shard_manager
        self.migration_engine = migration_engine
        self.hot_threshold = hot_threshold
        self.cool_threshold = cool_threshold
        self.balancing_active = True

    async def run_balancing_cycle(self):
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        """
        Executed periodically to check for imbalances and trigger P2P migrations.
        """
        if not self.balancing_active:
            return

<<<<<<< HEAD
<<<<<<< HEAD
        metrics: Dict[str, Any] = self.telemetry.get_grid_metrics()

=======
        metrics = self.telemetry.get_grid_metrics()
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        metrics = self.telemetry.get_grid_metrics()
        
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        hot_ranks: List[int] = []
        cool_ranks: List[int] = []

        # Identify hot and cool nodes based on grid metrics
        for key, val in metrics.items():
            if key.startswith("rank_") and key.endswith("_util"):
                try:
                    rank_id = int(key.split("_")[1])
                    if val > self.hot_threshold:
                        hot_ranks.append(rank_id)
                    elif val < self.cool_threshold:
                        cool_ranks.append(rank_id)
                except (ValueError, IndexError):
                    continue

        if not hot_ranks or not cool_ranks:
            return

        # Sort cool ranks by utilization (ascending) to pick the most empty one first
        cool_ranks.sort(key=lambda r: metrics.get(f"rank_{r}_util", 1.0))

        for hot_rank in hot_ranks:
            # Find shards currently on this rank
            shards_on_hot_rank = self._get_shards_on_rank(hot_rank)
<<<<<<< HEAD
<<<<<<< HEAD

=======
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            if not shards_on_hot_rank:
                continue

            # Pick the first available cool rank
<<<<<<< HEAD
<<<<<<< HEAD
            target_rank: int = cool_ranks[0]

            # Pick a shard to move (e.g., the first one)
            context_id, shard_idx = shards_on_hot_rank[0]

            logger.info(
                "[Phase 81] LoadBalancer: Hot spot detected on Rank %s (%s). "
                "Migrating %s shard %s to Rank %s.",
                hot_rank,
                f"{metrics[f'rank_{hot_rank}_util']:.2f}",
                context_id,
                shard_idx,
                target_rank,
            )

            try:
                await self.migration_engine.migrate_shard(context_id, shard_idx, target_rank)
                # After one migration, re-sort or break to avoid over-filling a cool rank in one pass
                break
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            target_rank = cool_ranks[0]
            
            # Pick a shard to move (e.g., the first one)
            context_id, shard_idx = shards_on_hot_rank[0]
            
            logger.info(f"[Phase 81] LoadBalancer: Hot spot detected on Rank {hot_rank} ({metrics[f'rank_{hot_rank}_util']:.2f}). "
                        f"Migrating {context_id} shard {shard_idx} to Rank {target_rank}.")
            
            try:
                await self.migration_engine.migrate_shard(context_id, shard_idx, target_rank)
                # After one migration, re-sort or break to avoid over-filling a cool rank in one pass
                break 
            except Exception as e:
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                logger.error(f"Failed to migrate shard during load balancing: {e}")

    def _get_shards_on_rank(self, rank_id: int) -> List[tuple]:
        """Scans the shard manager for shards hosted on a specific rank."""
        res = []
        # Accessing the internal registry of the shard manager
        for ctx_id, shards in self.shard_manager.context_registry.items():
            for i, shard in enumerate(shards):
                if shard.rank_id == rank_id:
                    res.append((ctx_id, i))
        return res

<<<<<<< HEAD
<<<<<<< HEAD
    async def start_loop(self, interval: float = 5.0) -> None:
=======
    async def start_loop(self, interval: float = 5.0):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    async def start_loop(self, interval: float = 5.0):
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        """Starts a background balancing loop."""
        while self.balancing_active:
            await self.run_balancing_cycle()
            await asyncio.sleep(interval)

<<<<<<< HEAD
<<<<<<< HEAD
    def stop(self) -> None:
=======
    def stop(self):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    def stop(self):
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        """Stops the balancing service."""
        self.balancing_active = False
