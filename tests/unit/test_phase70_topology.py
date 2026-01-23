#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import pytest
import asyncio
import numpy as np
from src.infrastructure.swarm.orchestration.swarm.topology_manager import TopologyManager
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import MoEGatekeeper
from src.core.base.common.models.communication_models import ExpertProfile

class MockSimilarity:
    async def get_embedding(self, text: str):
        return np.random.randn(384).astype(np.float32)

@pytest.mark.asyncio
async def test_expert_cloning():
    """Verifies that high-demand experts are cloned automatically."""
    similarity = MockSimilarity()
    gatekeeper = MoEGatekeeper(similarity_service=similarity)

    # 5 is threshold for testing
    topology = TopologyManager(gatekeeper=gatekeeper, clone_threshold=5)
    gatekeeper.topology_manager = topology

    gatekeeper.register_expert(ExpertProfile(
        agent_id="busy_expert",
        domains=["math"],
        performance_score=1.0
    ))

    # Trigger routing 10 times
    for _ in range(6):
        await gatekeeper.route_task("Calculate pi", top_k=1)
        # Give small sleep for async task
        await asyncio.sleep(0.01)

    stats = topology.get_topology_stats()
    assert stats["total_replicas"] >= 1
    assert "busy_expert_replica_1" in gatekeeper.experts
    assert gatekeeper.experts["busy_expert_replica_1"].is_replica is True
    assert gatekeeper.experts["busy_expert_replica_1"].parent_id == "busy_expert"

    print(f"\nPhase 70: Expert cloning verified. Stats: {stats}")

@pytest.mark.asyncio
async def test_replica_routing():
    """Verifies that replicas are included in routing decisions."""
    similarity = MockSimilarity()
    gatekeeper = MoEGatekeeper(similarity_service=similarity)
    topology = TopologyManager(gatekeeper=gatekeeper, clone_threshold=100)

    # Manually clone
    gatekeeper.register_expert(ExpertProfile(
        agent_id="master_agent",
        domains=["logic"],
        performance_score=1.0
    ))
    await topology.clone_expert("master_agent")

    assert "master_agent_replica_1" in gatekeeper.experts

    # Route task
    decision = await gatekeeper.route_task("Solve this riddle", top_k=2)
    # Both master and replica should have high scores and might both be selected
    # (given they have the same specialization vector)
    assert len(decision.selected_experts) == 2
    assert "master_agent" in decision.selected_experts
    assert "master_agent_replica_1" in decision.selected_experts
