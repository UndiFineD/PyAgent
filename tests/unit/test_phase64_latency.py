#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Tests for Phase 64: MoE Routing Latency Optimization

import pytest
import asyncio
import time
from unittest.mock import MagicMock, AsyncMock
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import MoEGatekeeper
from src.infrastructure.engine.models.similarity import EmbeddingSimilarityService
from src.core.base.common.models.communication_models import ExpertProfile

@pytest.mark.asyncio
async def test_gatekeeper_caching():
    sim_service = EmbeddingSimilarityService()
    # Mock embedding with a small delay to simulate model latency
    original_get = sim_service.get_embedding
    
    call_count = 0
    async def slow_get(text):
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.05)
        return await original_get(text)
    
    sim_service.get_embedding = slow_get
    
    gatekeeper = MoEGatekeeper(sim_service)
    gatekeeper.register_expert(ExpertProfile(agent_id="e1", domains=["test"]))

    task = "Find the bug in this rust code"
    
    # First call: should be slow and increment call_count
    start = time.time()
    await gatekeeper.route_task(task)
    duration1 = time.time() - start
    assert call_count == 1
    
    # Second call: should be fast (cache hit) and NOT increment call_count
    start = time.time()
    await gatekeeper.route_task(task)
    duration2 = time.time() - start
    assert call_count == 1 # Still 1!
    assert duration2 < duration1

@pytest.mark.asyncio
async def test_gatekeeper_batch_routing():
    sim_service = EmbeddingSimilarityService()
    gatekeeper = MoEGatekeeper(sim_service)
    gatekeeper.register_expert(ExpertProfile(agent_id="e1", domains=["test"]))
    
    prompts = ["Task 1", "Task 2", "Task 3"]
    decisions = await gatekeeper.batch_route_tasks(prompts)
    
    assert len(decisions) == 3
    assert all(hasattr(d, "selected_experts") for d in decisions)
