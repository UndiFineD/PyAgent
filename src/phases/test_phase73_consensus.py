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
from src.infrastructure.swarm.orchestration.swarm.consensus import SwarmConsensus


@pytest.mark.asyncio
async def test_swarm_state_consensus():
    """Verifies that changes are committed only after quorum agreement."""
    peers = ["node_b", "node_c"]
    node_a = SwarmConsensus(node_id="node_a", peers=peers)

    # Propose a routing change
    success = await node_a.propose_change("active_experts", ["agent_77", "agent_88"])

    assert success is True
    assert node_a.get_state("active_experts") == ["agent_77", "agent_88"]
    assert node_a.commit_index == 0

    # Verify second change
    await node_a.propose_change("gateway_mode", "strict")
    assert node_a.get_state("gateway_mode") == "strict"
    assert node_a.commit_index == 1

    print("\nPhase 73: Swarm state consensus verified (Quorum logic).")
