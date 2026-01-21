"""Unit tests for GossipProtocolOrchestrator."""

import pytest
from unittest.mock import MagicMock
from src.infrastructure.swarm.orchestration.consensus.gossip_protocol_orchestrator import (
    GossipProtocolOrchestrator,
)


@pytest.mark.asyncio
async def test_gossip_update_state() -> None:
    fleet = MagicMock()

    orchestrator: GossipProtocolOrchestrator[MagicMock] = GossipProtocolOrchestrator(
        fleet
    )

    await orchestrator.update_state("test_key", "test_value")

    val = await orchestrator.get_synced_state("test_key")

    assert val == "test_value"
    assert orchestrator.versions["test_key"] == 1

    await orchestrator.stop()


@pytest.mark.asyncio
async def test_gossip_multiple_updates() -> None:
    fleet = MagicMock()
    orchestrator: GossipProtocolOrchestrator[MagicMock] = GossipProtocolOrchestrator(
        fleet
    )

    await orchestrator.update_state("test_key", "v1")
    await orchestrator.update_state("test_key", "v2")

    val = await orchestrator.get_synced_state("test_key")
    assert val == "v2"
    assert orchestrator.versions["test_key"] == 2

    await orchestrator.stop()
