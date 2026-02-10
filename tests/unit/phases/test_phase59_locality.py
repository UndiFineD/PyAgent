
"""
Test Phase59 Locality module.
"""
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Tests for Phase 59: Locality-aware DP

import pytest
from src.infrastructure.swarm.distributed.v2.dp_coordinator import DPCoordinatorV2
from src.infrastructure.swarm.distributed.v2.locality_manager import LocalityManager

def test_locality_manager_clustering():
    mgr = LocalityManager()

    # Register ranks in different localities
    mgr.register_rank(0, "rack-A")
    mgr.register_rank(1, "rack-A")
    mgr.register_rank(2, "rack-B")

    peers_0 = mgr.get_peers_in_same_locality(0)
    assert 1 in peers_0
    assert 2 not in peers_0

    meta_shards = mgr.optimize_sharding(4)
    # 4 shards over 2 groups: 2 shards per group
    assert len(meta_shards["rack-A"]) == 2
    assert len(meta_shards["rack-B"]) == 2

@pytest.mark.asyncio
async def test_coordinator_locality_publish():
    # Master
    master = DPCoordinatorV2(port=5560, is_master=True)
    await master.connect()

    # This shouldn't crash
    await master.publish_wave_to_locality([101, 102], "rack-X")

    assert master.current_wave == 1
    await master.close()

def test_suggested_aggregators():
    mgr = LocalityManager()
    mgr.register_rank(5, "DC1")
    mgr.register_rank(3, "DC1")
    mgr.register_rank(10, "DC2")

    # DC1 aggregator should be 3 (lowest)
    assert mgr.suggest_coordinator_rank("DC1") == 3
    assert mgr.suggest_coordinator_rank("DC2") == 10
