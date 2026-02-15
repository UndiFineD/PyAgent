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

# Licensed under the Apache License, Version 2.0 (the "License");

import pytest
from src.infrastructure.engine.kv_cache.context_sharder import ContextShardManager
from src.infrastructure.engine.kv_cache.p2p_migration import P2PMigrationEngine


@pytest.mark.asyncio
async def test_shard_migration_flow():
    """Verifies that shards can be moved between ranks successfully."""
    manager = ContextShardManager(block_size=1024)
    migration_engine = P2PMigrationEngine(manager)

    # Setup context on Rank 0
    manager.shard_context("long_doc", 2048, [0])
    assert manager.context_registry["long_doc"][0].rank_id == 0
    assert manager.context_registry["long_doc"][1].rank_id == 0

    # Migrate Shard 1 to Rank 5
    await migration_engine.migrate_shard("long_doc", 1, 5)

    assert manager.context_registry["long_doc"][0].rank_id == 0
    assert manager.context_registry["long_doc"][1].rank_id == 5

    stats = migration_engine.get_migration_stats()
    assert stats["total_migrations"] == 1
    assert stats["avg_duration_ms"] > 0

    print(f"\nPhase 72: P2P Shard Migration verified. Stats: {stats}")
