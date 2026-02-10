#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Phase 330: Holographic Memory Verification

import pytest
import asyncio
from src.infrastructure.swarm.orchestration.state.holographic_state_orchestrator import HolographicStateOrchestrator

@pytest.mark.asyncio
async def test_holographic_sharding_and_reconstruction():
    """Verifies that the Holographic Orchestrator can shard multi-perspective state and reconstruct it."""
    # Setup - No fleet required for local logic check
    orchestrator = HolographicStateOrchestrator()

    hologram_id = "test_hologram_v4.1.0"
    hologram_wrapper = {
        "timestamp": 123456789,
        "perspectives": {
            "security": {"score": 0.95, "status": "hardened"},
            "performance": {"latency": "5ms", "throughput": "10k/s"},
            "ux": {"responsive": True, "accessibility": 1.0}
        }
    }

    # 1. Shard the hologram
    result = await orchestrator.shard_hologram(hologram_id, hologram_wrapper)
    assert result["status"] == "holographic_sharded"
    assert result["perspectives_count"] == 3
    assert result["hologram_id"] == hologram_id

    # 2. Reconstruct Security perspective
    security_view = await orchestrator.reconstruct_perspective(hologram_id, "security")
    assert security_view is not None
    assert security_view["status"] == "hardened"
    assert security_view["score"] == 0.95

    # 3. Reconstruct UX perspective
    ux_view = await orchestrator.reconstruct_perspective(hologram_id, "ux")
    assert ux_view is not None
    assert ux_view["responsive"] is True

    # 4. Verify local shard lookup
    shards = await orchestrator.find_local_hologram_shards(hologram_id)
    assert len(shards) > 0
    # Every angle should have at least 2 shards (default redundancy in shard_hologram)
    # Total perspectives = 3, redundancy = 2 -> at least 6 shards expected
    assert len(shards) >= 6

@pytest.mark.asyncio
async def test_holographic_projection_handling():
    """Verifies that the orchestrator can handle metadata projections."""
    orchestrator = HolographicStateOrchestrator()

    msg = {
        "type": "hologram_projection",
        "hologram_id": "remote_hologram_123",
        "angles": ["security", "maintainability"],
        "sender_id": "node-remote-01"
    }

    # Should not raise any error
    await orchestrator.handle_projection(msg)
    print("ALL_HOLOGRAPHIC_TESTS_PASSED")

if __name__ == "__main__":
    asyncio.run(test_holographic_sharding_and_reconstruction())
