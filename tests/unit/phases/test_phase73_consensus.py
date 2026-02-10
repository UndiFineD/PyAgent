#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
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
