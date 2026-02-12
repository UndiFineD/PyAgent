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
Tests for Phase 61: Cross-Model MoE Orchestration.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import numpy as np
import pytest

from src.core.base.common.models.communication_models import ExpertProfile
from src.infrastructure.engine.models.similarity import EmbeddingSimilarityService
from src.infrastructure.swarm.orchestration.swarm.cross_model_moe_orchestrator import \
    CrossModelMoEOrchestrator
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import \
    MoEGatekeeper


@pytest.mark.asyncio
async def test_moe_routing_accuracy():
    """Verify that MoE routing correctly identifies specialized experts."""
    sim_service = EmbeddingSimilarityService()
    gatekeeper = MoEGatekeeper(sim_service)

    # Use orthogonal vectors for deterministic testing
    vec_coder = [0.0] * 384
    vec_coder[0] = 1.0
    vec_poet = [0.0] * 384
    vec_poet[1] = 1.0

    # Register a Coding Expert
    coder_profile = ExpertProfile(
        agent_id="agent_coder",
        domains=["python", "rust", "debugging", "coding"],
        performance_score=1.0,
        specialization_vector=vec_coder
    )
    # Register a Poetry Expert
    poet_profile = ExpertProfile(
        agent_id="agent_poet",
        domains=["poetry", "creative writing", "literature"],
        performance_score=0.9,
        specialization_vector=vec_poet
    )

    gatekeeper.register_expert(coder_profile)
    gatekeeper.register_expert(poet_profile)

    # Mock the similarity service to return vectors that match our experts
    # For coding task, return something close to vec_coder
    with patch.object(sim_service, "get_embedding", side_effect=[
        np.array(vec_coder, dtype=np.float32),  # For coding prompt
        np.array(vec_poet, dtype=np.float32)   # For poetry prompt
    ]):
        # Test routing for a code task
        decision_code = await gatekeeper.route_task("Write a fast rust function for matrix multiplication")
        assert decision_code.selected_experts[0] == "agent_coder"

        # Test routing for a creative task
        decision_poet = await gatekeeper.route_task("Write a sonnet about the digital void")
        assert decision_poet.selected_experts[0] == "agent_poet"


@pytest.mark.asyncio
async def test_moe_orchestrator_execution():
    """Verify that the MoE orchestrator can coordinate expert execution."""
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
