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
Test Phase62 Fusion module.
"""
# Tests for Phase 62: Weighted Expert Fusion

import pytest
from unittest.mock import MagicMock, AsyncMock
from src.infrastructure.swarm.orchestration.swarm.expert_fusion import WeightedExpertFusion
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import MoEGatekeeper
from src.infrastructure.swarm.orchestration.swarm.cross_model_moe_orchestrator import CrossModelMoEOrchestrator
from src.infrastructure.engine.models.similarity import EmbeddingSimilarityService
from src.core.base.common.models.communication_models import ExpertProfile


@pytest.mark.asyncio
async def test_weighted_plurality_fusion():
    fusion = WeightedExpertFusion()

    outputs = ["Answer A", "Answer B", "Answer A"]
    weights = [0.4, 0.5, 0.3]  # Answer A total = 0.7, Answer B total = 0.5
    expert_ids = ["e1", "e2", "e3"]

    result = await fusion.fuse_outputs(outputs, weights, expert_ids, mode="weighted_plurality")
    assert result.merged_content == "Answer A"
    assert result.consensus_score > 0.5


@pytest.mark.asyncio
async def test_moe_orchestrator_mixture_mode():
    sim_service = EmbeddingSimilarityService()
    gatekeeper = MoEGatekeeper(sim_service)
    orchestrator = CrossModelMoEOrchestrator(gatekeeper)

    # Setup two experts
    expert1_profile = ExpertProfile(agent_id="e1", domains=["test"], performance_score=1.0)
    expert2_profile = ExpertProfile(agent_id="e2", domains=["test"], performance_score=0.8)

    gatekeeper.register_expert(expert1_profile)
    gatekeeper.register_expert(expert2_profile)

    # Mock behavior
    mock_e1 = MagicMock()
    mock_e1.process_request = AsyncMock(return_value="Result X")
    mock_e2 = MagicMock()
    mock_e2.process_request = AsyncMock(return_value="Result X")

    orchestrator.register_agent_instance("e1", mock_e1)
    orchestrator.register_agent_instance("e2", mock_e2)

    # Mixture execution
    result = await orchestrator.execute_moe_task("Sample prompt", mode="mixture")
    assert result == "Result X"
    assert mock_e1.process_request.called
    assert mock_e2.process_request.called
