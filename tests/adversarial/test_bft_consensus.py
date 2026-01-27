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
Adversarial tests for Byzantine Fault Tolerance (BFT) consensus.
Simulates network partitions, malicious agents, and Sybil attacks.
"""

import hashlib
import pytest
from unittest.mock import MagicMock, patch
from src.logic.agents.security.byzantine_consensus_agent import ByzantineConsensusAgent
from src.logic.agents.security.core.byzantine_core import ByzantineCore

@pytest.fixture
def bft_agent():
    return ByzantineConsensusAgent("test_bft_agent.py")

@pytest.mark.asyncio
async def test_bft_consensus_perfect_agreement(bft_agent):
    """Test standard case where all agents agree."""
    proposals = {
        "AgentA": "def foo(): return 1",
        "AgentB": "def foo(): return 1",
        "AgentC": "def foo(): return 1"
    }
    
    result = await bft_agent.run_committee_vote("Implement foo", proposals)
    assert result["decision"] == "ACCEPTED"
    assert result["reason"] == "Byzantine Quorum Reached"
    assert result["content"] == "def foo(): return 1"

@pytest.mark.asyncio
async def test_bft_consensus_minority_dissent(bft_agent):
    """Test case where 1 agent disagrees (faulty/malicious) but quorum is met."""
    proposals = {
        "AgentA": "valid code",
        "AgentB": "valid code",
        "AgentC": "valid code",
        "AgentBad": "malicious code"
    }
    # 3/4 Agreement = 0.75 > 0.66
    
    result = await bft_agent.run_committee_vote("Task", proposals)
    assert result["decision"] == "ACCEPTED"
    assert result["winning_hash"] == hashlib.sha256(b"valid code").hexdigest()

@pytest.mark.asyncio
async def test_bft_consensus_failure_split_brain(bft_agent):
    """Test case where no majority exists (Split Brain)."""
    proposals = {
        "AgentA": "Option A",
        "AgentB": "Option A",
        "AgentC": "Option B",
        "AgentD": "Option B"
    }
    # 50/50 Split - No consensus
    
    # Mock the fallback AI evaluation to prevent actual LLM calls
    with patch.object(bft_agent, 'think', new_callable=MagicMock) as mock_think:
        mock_think.return_value = "Score: 0.8"
        
        result = await bft_agent.run_committee_vote("Task", proposals)
        
        # Should fallback to AI eval, but since we didn't mock the fallback logic fully returning a clear winner 
        # (defaults to max score), and here scores might be equal or random if not mocked well.
        # But crucially, "Byzantine Quorum Reached" should NOT be the reason.
        
        assert result.get("reason") != "Byzantine Quorum Reached"

@pytest.mark.asyncio
async def test_bft_sybil_attack_simulation(bft_agent):
    """Simulate a Sybil attack where low-reputation agents try to sway the vote."""
    
    # Manually set reputation scores
    bft_agent.reliability_scores = {
        "TrustedA": 1.0,
        "TrustedB": 1.0,
        "Sybil1": 0.1,
        "Sybil2": 0.1,
        "Sybil3": 0.1,
        "Sybil4": 0.1
    }
    
    # Sybils vote for malicious, Trusted vote for valid
    # Trusted Weight = 2.0
    # Sybil Weight = 0.4
    # Total Weight = 2.4
    # Valid Share = 2.0 / 2.4 = 0.83 (Passes Quorum)
    
    proposals = {
        "TrustedA": "valid",
        "TrustedB": "valid",
        "Sybil1": "malicious",
        "Sybil2": "malicious",
        "Sybil3": "malicious",
        "Sybil4": "malicious"
    }
    
    result = await bft_agent.run_committee_vote("Sybil Test", proposals)
    assert result["decision"] == "ACCEPTED"
    assert result["content"] == "valid"

