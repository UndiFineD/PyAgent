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

import pytest
import numpy as np
from unittest.mock import AsyncMock, MagicMock
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import MoEGatekeeper
from src.infrastructure.swarm.orchestration.swarm.reward_predictor import ExpertRewardPredictor
from src.core.base.common.models.communication_models import ExpertProfile

@pytest.mark.asyncio
async def test_routing_with_reward_bias():
    # 1. Setup Wisdom (Expert B is a 'top expert')
    mock_wisdom = {
        "top_experts": [("expert_b", 1.0)],
        "expert_synergies": {"expert_b": {"some_other": 0.9}},
        "domain_baselines": {"coding": 0.8}
    }
    predictor = ExpertRewardPredictor(mock_wisdom)

    # 2. Setup Gatekeeper with 2 identical experts
    mock_sim = MagicMock()
    mock_sim.get_embedding = AsyncMock(return_value=np.zeros(384))
    
    gatekeeper = MoEGatekeeper(mock_sim, reward_predictor=predictor)
    
    # Expert A: standard
    p_a = ExpertProfile(agent_id="expert_a", domains=["coding"], performance_score=1.0)
    p_a.specialization_vector = [1.0] * 384
    
    # Expert B: same specs as A, but is in the wisdom 'top experts'
    p_b = ExpertProfile(agent_id="expert_b", domains=["coding"], performance_score=1.0)
    p_b.specialization_vector = [1.0] * 384
    
    gatekeeper.register_expert(p_a)
    gatekeeper.register_expert(p_b)

    # 3. Route task
    decision = await gatekeeper.route_task("write some code", top_k=1)

    # 4. Expert B should win due to the reward boost even if similarities were equal
    # (Similarity calculation uses hash(domains) for random vec if none provided, but we set them equal)
    assert decision.selected_experts[0] == "expert_b"
    print(f"\n[Phase 83] Reward predictor correctly prioritized 'expert_b' based on historical merit.")
