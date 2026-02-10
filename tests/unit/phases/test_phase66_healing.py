
"""
Test Phase66 Healing module.
"""
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Tests for Phase 66: Swarm Self-Healing

import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from src.infrastructure.swarm.orchestration.swarm.cross_model_moe_orchestrator import CrossModelMoEOrchestrator
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import MoEGatekeeper
from src.infrastructure.engine.models.similarity import EmbeddingSimilarityService
from src.core.base.common.models.communication_models import ExpertProfile

@pytest.mark.asyncio
async def test_self_healing_rerouting():
    sim_service = EmbeddingSimilarityService()
    gatekeeper = MoEGatekeeper(sim_service)
    orchestrator = CrossModelMoEOrchestrator(gatekeeper)
    orchestrator.timeout_sec = 0.1 # Short timeout for test

    # Setup two experts
    gatekeeper.register_expert(ExpertProfile(agent_id="e1", domains=["fail"], performance_score=1.0))
    gatekeeper.register_expert(ExpertProfile(agent_id="e2", domains=["fail"], performance_score=0.8))

    # Expert 1: Fails (Timeout or Exception)
    mock_e1 = MagicMock()
    mock_e1.process_request = AsyncMock(side_effect=asyncio.TimeoutError())

    # Expert 2: Succeeds
    mock_e2 = MagicMock()
    mock_e2.process_request = AsyncMock(return_value="Success after failover")

    orchestrator.register_agent_instance("e1", mock_e1)
    orchestrator.register_agent_instance("e2", mock_e2)

    # Run task: e1 should fail and e2 should be picked
    result = await orchestrator.execute_moe_task("Test healing", mode="best_expert")

    assert result == "Success after failover"
    assert orchestrator.expert_health["e1"] is False
    assert orchestrator.expert_health["e2"] is True

@pytest.mark.asyncio
async def test_self_healing_mixture_partial_failure():
    sim_service = EmbeddingSimilarityService()
    gatekeeper = MoEGatekeeper(sim_service)
    orchestrator = CrossModelMoEOrchestrator(gatekeeper)
    orchestrator.timeout_sec = 0.1

    gatekeeper.register_expert(ExpertProfile(agent_id="e1", domains=["general"], performance_score=1.0))
    gatekeeper.register_expert(ExpertProfile(agent_id="e2", domains=["general"], performance_score=0.9))

    # e1 fails, e2 succeeds
    mock_e1 = MagicMock()
    mock_e1.process_request = AsyncMock(side_effect=RuntimeError("Crash"))
    mock_e2 = MagicMock()
    mock_e2.process_request = AsyncMock(return_value="Safe result")

    orchestrator.register_agent_instance("e1", mock_e1)
    orchestrator.register_agent_instance("e2", mock_e2)

    # Mixture should still work if at least one expert succeeds
    result = await orchestrator.execute_moe_task("Test mixture healing", mode="mixture")

    assert result == "Safe result"
    assert orchestrator.expert_health["e1"] is False
    assert orchestrator.expert_health["e2"] is True
