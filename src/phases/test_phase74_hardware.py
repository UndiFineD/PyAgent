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

import pytest
import numpy as np
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import MoEGatekeeper
from src.core.base.common.models.communication_models import ExpertProfile


class MockSimilarity:
    async def get_embedding(self, text: str):
        # Return a neutral vector
        vec = np.ones(384).astype(np.float32)
        return vec / np.linalg.norm(vec)


@pytest.mark.asyncio
async def test_heterogeneous_routing_boost():
    """Verifies that experts on faster hardware get a slight routing preference."""
    similarity = MockSimilarity()
    gatekeeper = MoEGatekeeper(similarity_service=similarity)

    # 1. Standard Hardware Expert
    gatekeeper.register_expert(ExpertProfile(
        agent_id="std_node",
        domains=["general"],
        performance_score=1.0,
        acceleration_type="standard",
        specialization_vector=np.ones(384).tolist()
    ))

    # 2. H100 Accelerated Expert (same score/vector)
    gatekeeper.register_expert(ExpertProfile(
        agent_id="fast_node",
        domains=["general"],
        performance_score=1.0,
        acceleration_type="h100_tensor",
        specialization_vector=np.ones(384).tolist()
    ))

    decision = await gatekeeper.route_task("General query", top_k=2)

    # The fast_node should be first despite identical performance/similarity
    assert decision.selected_experts[0] == "fast_node"
    assert decision.selected_experts[1] == "std_node"

    print("\nPhase 74: Heterogeneous hardware preference verified.")
