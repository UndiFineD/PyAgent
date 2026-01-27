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
Test Red Queen Adversarial Agent.
"""

# pylint: disable=wrong-import-order
import pytest
<<<<<<< HEAD
from src.logic.agents.security.ByzantineConsensusAgent import ByzantineConsensusAgent
=======
from src.logic.agents.security.byzantine_consensus_agent import ByzantineConsensusAgent
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)

def test_red_queen_adversarial_flow() -> None:
    """
    Validates that the swarm can detect and reject low-quality (adversarial) proposals.
    Phase 128: Digital Red Queen / Adversarial Evolution test.
    """
    # Initialize Judge
    judge = ByzantineConsensusAgent("data/logs/red_queen_test.md")
    
    task = "Implement a secure data hashing function."
<<<<<<< HEAD
    
=======

    # Mock the AI evaluation to avoid external calls and timeouts
    async def mock_think(prompt: str) -> str:
        if "agent_alpha" in prompt:
            return "0.95"
        if "agent_beta" in prompt:
            return "0.6"
        if "agent_gamma" in prompt:
            return "0.2"
        return "0.1"

    # Inject mock
    judge.think = mock_think

>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)
    # 1. Simulate multiple agent responses (one good, two weak)
    proposals = {
        "agent_alpha": "import hashlib\ndef hash_data(data):\n    return hashlib.sha256(data.encode()).hexdigest()",
        "agent_beta": "def hash_data(data):\n    # TODO: Security audit needed\n    return str(hash(data))",
        "agent_gamma": "FIXME: Just return data for now\ndef hash_data(data): return data"
    }
    
    # 2. Run Byzantine Consensus
    result = judge.run_committee_vote(task, proposals)
    
    # 3. Assertions
    assert result["decision"] == "ACCEPTED"
    assert result["winner"] == "agent_alpha"
    assert result["confidence"] > 0.6
    assert "agent_beta" in result["consensus_stats"]["voters"]
    assert "TODO" not in result["content"]

if __name__ == "__main__":
    pytest.main([__file__])
