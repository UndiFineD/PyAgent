"""Unit tests for GossipProtocolOrchestrator."""
import pytest
from unittest.mock import MagicMock
from src.infrastructure.orchestration.GossipProtocolOrchestrator import GossipProtocolOrchestrator

def test_gossip_update_state() -> None:
    fleet = MagicMock()
    orchestrator: GossipProtocolOrchestrator[MagicMock] = GossipProtocolOrchestrator(fleet)
    
    orchestrator.update_state("test_key", "test_value")
    
    assert orchestrator.get_synced_state("test_key") == "test_value"
    assert orchestrator.versions["test_key"] == 1
    
    orchestrator.shutdown()

def test_gossip_multiple_updates() -> None:
    fleet = MagicMock()
    orchestrator: GossipProtocolOrchestrator[MagicMock] = GossipProtocolOrchestrator(fleet)
    
    orchestrator.update_state("test_key", "v1")
    orchestrator.update_state("test_key", "v2")
    
    assert orchestrator.get_synced_state("test_key") == "v2"
    assert orchestrator.versions["test_key"] == 2
    
    orchestrator.shutdown()
