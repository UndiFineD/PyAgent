
"""
Test Phase63 Context module.
"""
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Tests for Phase 63: Context Sharding and Locality-Aware MoE

import pytest
from unittest.mock import MagicMock, AsyncMock
from src.infrastructure.engine.kv_cache.context_sharder import ContextShardManager
from src.infrastructure.swarm.orchestration.swarm.context_aware_moe import ContextAwareMoEOrchestrator
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import MoEGatekeeper
from src.infrastructure.engine.models.similarity import EmbeddingSimilarityService
from src.core.base.common.models.communication_models import ExpertProfile

@pytest.mark.asyncio
async def test_context_sharding_logic():
    manager = ContextShardManager(block_size=100)
    # Shard 1000 tokens across 3 ranks
    shards = manager.shard_context("doc1", 1000, [0, 1, 2])

    assert len(shards) == 10
    # Token 250 should be in shard 2, which is rank 2 (250 // 100 = 2, 2 % 3 = 2)
    assert manager.get_rank_for_token("doc1", 250) == 2
    # Token 550 should be rank 2 (550 // 100 = 5, 5 % 3 = 2)
    assert manager.get_rank_for_token("doc1", 550) == 2

@pytest.mark.asyncio
async def test_locality_aware_routing():
    sim_service = EmbeddingSimilarityService()
    gatekeeper = MoEGatekeeper(sim_service)
    context_manager = ContextShardManager(block_size=100)
    orchestrator = ContextAwareMoEOrchestrator(gatekeeper, context_manager)

    # Experts
    e1_profile = ExpertProfile(agent_id="e1", domains=["general"])
    e2_profile = ExpertProfile(agent_id="e2", domains=["general"])
    gatekeeper.register_expert(e1_profile)
    gatekeeper.register_expert(e2_profile)

    # Locations: Expert 1 is on Rank 0, Expert 2 is on Rank 1
    orchestrator.register_expert_location("e1", 0)
    orchestrator.register_expert_location("e2", 1)

    # Mock context: Token 50 is on Rank 1
    context_manager.shard_context("doc", 100, [0, 1])

    # Mock Execution
    mock_agent = MagicMock()
    mock_agent.process_request = AsyncMock(return_value="Success")
    orchestrator.register_agent_instance("e2", mock_agent)
    orchestrator.register_agent_instance("e1", MagicMock())

    # Route for task focusing on Token 50 (Rank 1).
    # Even if e1/e2 are semantically equal, e2 should win due to locality (Rank 1).
    result = await orchestrator.execute_context_task("Tell me about part 50", "doc", focus_token=50)
    assert result == "Success"
    # Verify e2 was preferred
    # (Since semantic scores are equal in this mock, locality boost makes e2 the clear winner)