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

from src.infrastructure.engine.kv_cache.context_sharder import ContextShardManager


def test_shard_mirroring_failover():
    """Verifies that shards can be recovered from mirrors if primary rank fails."""
    # Redundancy factor 2: one primary, one mirror
    manager = ContextShardManager(block_size=512, redundancy_factor=2)

    # Shard across 3 ranks
    available_ranks = [10, 20, 30]
    shards = manager.shard_context("resilient_doc", 1024, available_ranks)

    # Check mirroring: Shard 0 (Rank 10) should have mirror on Rank 20
    assert shards[0].rank_id == 10
    assert 20 in shards[0].replica_ranks

    # Access primary
    assert manager.get_rank_for_token("resilient_doc", 100) == 10

    # KILL Rank 10
    manager.mark_rank_dead(10)

    # Failover access should return Rank 20 (the mirror)
    rank_after_fail = manager.get_rank_for_token("resilient_doc", 100)
    assert rank_after_fail == 20

    # KILL Rank 20 (Double Failure)
    manager.mark_rank_dead(20)
    assert manager.get_rank_for_token("resilient_doc", 100) is None

    print("\nPhase 75: Predictive fault tolerance (Mirror Failover) verified.")
