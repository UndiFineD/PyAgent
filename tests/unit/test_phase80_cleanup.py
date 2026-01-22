#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import pytest
import asyncio
import time
from src.infrastructure.swarm.orchestration.swarm.fleet_cleanup import FleetDecommissioner
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import MoEGatekeeper
from src.infrastructure.engine.kv_cache.context_sharder import ContextShardManager
from src.core.base.common.models.communication_models import ExpertProfile

@pytest.mark.asyncio
async def test_fleet_decommissioning():
    """Verifies that idle contexts and failed agents are cleaned up."""
    gatekeeper = MoEGatekeeper(similarity_service=None)
    shard_manager = ContextShardManager()
    
    # 1. Setup stale state
    # Failed agent (0.05 score)
    gatekeeper.register_expert(ExpertProfile(agent_id="failed_agent", domains=["none"], performance_score=0.05))
    # Healthy agent
    gatekeeper.register_expert(ExpertProfile(agent_id="good_agent", domains=["all"], performance_score=0.9))
    
    # Idle context
    shard_manager.shard_context("idle_doc", 100, [0])
    # Manually backdate the access time to 2 hours ago
    shard_manager.context_registry["idle_doc"][0].last_access = time.time() - 7200
    
    # 2. Run cleanup
    cleaner = FleetDecommissioner(gatekeeper, shard_manager, idle_timeout=3600)
    stats = await cleaner.run_cleanup_audit()
    
    # 3. Verify results
    assert stats["agents_pruned"] == 1
    assert stats["contexts_purged"] == 1
    assert "failed_agent" not in gatekeeper.experts
    assert "good_agent" in gatekeeper.experts
    assert "idle_doc" not in shard_manager.context_registry
    
    print(f"\nPhase 80: Autonomous fleet decommissioning verified. Stats: {stats}")
