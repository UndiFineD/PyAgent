
"""
Test Phase61 Moe module.
"""
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Tests for Phase 61: Cross-Model MoE Orchestration

import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import MoEGatekeeper
from src.infrastructure.swarm.orchestration.swarm.cross_model_moe_orchestrator import CrossModelMoEOrchestrator
from src.infrastructure.engine.models.similarity import EmbeddingSimilarityService
from src.core.base.common.models.communication_models import ExpertProfile

@pytest.mark.asyncio
async def test_moe_routing_accuracy():
    sim_service = EmbeddingSimilarityService()
    gatekeeper = MoEGatekeeper(sim_service)

    # Register a Coding Expert
    coder_profile = ExpertProfile(
        agent_id="agent_coder",
        domains=["python", "rust", "debugging", "coding"],
        performance_score=1.0
    )
    # Register a Poetry Expert
    poet_profile = ExpertProfile(
        agent_id="agent_poet",
        domains=["poetry", "creative writing", "literature"],
        performance_score=0.9
    )

    gatekeeper.register_expert(coder_profile)
    gatekeeper.register_expert(poet_profile)

    # Test routing for a code task
    decision_code = await gatekeeper.route_task("Write a fast rust function for matrix multiplication")
    assert decision_code.selected_experts[0] == "agent_coder"

    # Test routing for a creative task
    decision_poet = await gatekeeper.route_task("Write a sonnet about the digital void")
    assert decision_poet.selected_experts[0] == "agent_poet"

@pytest.mark.asyncio
async def test_moe_orchestrator_execution():
    sim_service = EmbeddingSimilarityService()
    gatekeeper = MoEGatekeeper(sim_service)
    orchestrator = CrossModelMoEOrchestrator(gatekeeper)

    # Mock experts
    mock_coder = MagicMock()
    mock_coder.process_request = AsyncMock(return_value="import torch...")
    coder_profile = ExpertProfile(agent_id="coder", domains=["coding"])

    gatekeeper.register_expert(coder_profile)
    orchestrator.register_agent_instance("coder", mock_coder)

    result = await orchestrator.execute_moe_task("Fix this python bug", mode="best_expert")
    assert result == "import torch..."
    mock_coder.process_request.assert_called_once()