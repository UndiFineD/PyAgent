#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import pytest
import asyncio
import numpy as np
from src.infrastructure.swarm.orchestration.swarm.swarm_training import SwarmTrainingCoordinator

@pytest.mark.asyncio
async def test_swarm_lora_merging():
    """Verifies that adapters from multiple experts can be merged into a global adapter."""
    coordinator = SwarmTrainingCoordinator(node_id="master_rank")

    # Simulate two experts providing their local LoRA adapters
    expert_a_adapter = {
        "domain": "rust_coding",
        "weight": 0.8,
        "tensors": [1.0] * 128
    }
    expert_b_adapter = {
        "domain": "rust_coding",
        "weight": 0.2,
        "tensors": [0.0] * 128
    }

    merged = await coordinator.merge_peer_loras("rust_coding", [expert_a_adapter, expert_b_adapter])

    assert merged["domain"] == "rust_coding"
    # Weighted average: (1.0 * 0.8 + 0.0 * 0.2) / (0.8 + 0.2) = 0.8
    assert pytest.approx(merged["weights"][0]) == 0.8
    assert "consensus_score" in merged

    print("\nPhase 79: P2P Swarm Training & LoRA Merging verified.")
