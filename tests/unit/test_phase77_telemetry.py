#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import pytest
from src.infrastructure.swarm.orchestration.swarm.telemetry import SwarmTelemetryService
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import MoEGatekeeper
from src.infrastructure.engine.kv_cache.context_sharder import ContextShardManager
from src.infrastructure.swarm.orchestration.swarm.topology_manager import TopologyManager
from src.core.base.common.models.communication_models import ExpertProfile

@pytest.mark.asyncio
async def test_telemetry_aggregation():
    """Verifies that the telemetry service correctly aggregates data from all layers."""
    # 1. Setup layers
    gatekeeper = MoEGatekeeper(similarity_service=None)
    shard_manager = ContextShardManager(block_size=512, redundancy_factor=2)
    topology = TopologyManager(gatekeeper=gatekeeper)
    
    telemetry = SwarmTelemetryService(gatekeeper, shard_manager, topology)
    
    # 2. Inject some state
    gatekeeper.register_expert(ExpertProfile(agent_id="test_agent_1", domains=["test"]))
    shard_manager.shard_context("doc_1", 1024, [0, 1])
    shard_manager.mark_rank_dead(99)
    
    # 3. Collect metrics
    metrics = telemetry.get_grid_metrics()
    
    assert metrics["routing"]["total_experts"] == 1
    assert metrics["context"]["total_shards"] == 2
    assert metrics["context"]["dead_ranks"] == 1
    assert metrics["swarm_health"] == "degraded"
    
    # Check bit-depth (default should be float16)
    assert metrics["context"]["shards_by_precision"]["float16"] == 2
    
    # Check Prometheus export
    prom_data = telemetry.export_prometheus()
    assert "swarm_total_shards 2" in prom_data
    
    print("\nPhase 77: Swarm telemetry aggregation verified.")
