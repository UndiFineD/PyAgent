#!/usr/bin/env python3

import pytest
from src.logic.agents.security.ByzantineConsensusAgent import ByzantineConsensusAgent

def test_red_queen_adversarial_flow() -> None:
    """
    Validates that the swarm can detect and reject low-quality (adversarial) proposals.
    Phase 128: Digital Red Queen / Adversarial Evolution test.
    """
    # Initialize Judge
    judge = ByzantineConsensusAgent("data/logs/red_queen_test.md")
    
    task = "Implement a secure data hashing function."
    
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
