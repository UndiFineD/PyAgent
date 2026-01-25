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
Test Phase81 Load Balancer module.
"""

import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from src.infrastructure.swarm.orchestration.swarm.load_balancer import SwarmLoadBalancer
from src.infrastructure.engine.kv_cache.context_sharder import ContextShardManager, ContextShard
from src.infrastructure.engine.kv_cache.p2p_migration import P2PMigrationEngine

@pytest.mark.asyncio
async def test_swarm_load_balancing():
    # 1. Setup Mock Telemetry
    mock_telemetry = MagicMock()
    # Rank 0 is hot (95%), Rank 1 is cool (10%)
    mock_telemetry.get_grid_metrics.return_value = {
        "rank_0_util": 0.95,
        "rank_1_util": 0.10,
        "fleet_size": 2
    }

    # 2. Setup Shard Manager with a shard on Rank 0
    shard_manager = ContextShardManager(block_size=1024)
    shard_manager.context_registry["ctx_test"] = [
        ContextShard(shard_id="s1", tenant_id="t1", start_token=0, end_token=1024, rank_id=0)
    ]

    # 3. Setup Migration Engine Mock
    migration_engine = MagicMock(spec=P2PMigrationEngine)
    migration_engine.migrate_shard = AsyncMock()

    # 4. Initialize Load Balancer
    balancer = SwarmLoadBalancer(
        telemetry=mock_telemetry,
        shard_manager=shard_manager,
        migration_engine=migration_engine,
        hot_threshold=0.80,
        cool_threshold=0.30
    )

    # 5. Run one cycle
    await balancer.run_balancing_cycle()

    # 6. Verify migration was triggered from Rank 0 to Rank 1
    migration_engine.migrate_shard.assert_called_once_with("ctx_test", 0, 1)
    print("\n[Phase 81] Load balancer successfully triggered migration from hot Rank 0 to cool Rank 1.")

@pytest.mark.asyncio
async def test_no_balancing_when_stable():
    mock_telemetry = MagicMock()
    # Both ranks are within normal bounds
    mock_telemetry.get_grid_metrics.return_value = {
        "rank_0_util": 0.50,
        "rank_1_util": 0.50
    }

    shard_manager = ContextShardManager()
    migration_engine = MagicMock(spec=P2PMigrationEngine)
    migration_engine.migrate_shard = AsyncMock()

    balancer = SwarmLoadBalancer(mock_telemetry, shard_manager, migration_engine)

    await balancer.run_balancing_cycle()

    migration_engine.migrate_shard.assert_not_called()
    print("[Phase 81] Load balancer correctly remained idle during stable utilization.")