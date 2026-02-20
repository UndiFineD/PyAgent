#!/usr/bin/env python3
"""Minimal smoke tests for A2A communication components used by the suite."""
try:
    from src.core.base.logic.a2a_communication import MessageRouter, A2ACommunicationMixin, AgentCard
except Exception:  # pragma: no cover - import shim
    raise


def test_a2a_imports_smoke() -> None:
    assert MessageRouter is not None
    assert A2ACommunicationMixin is not None
    assert AgentCard is not None
