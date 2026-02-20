#!/usr/bin/env python3
"""Minimal import test for BaseAgentCore to ensure module loads."""
try:
    from src.core.base.lifecycle.base_agent_core import BaseAgentCore
except Exception:  # pragma: no cover - test shim
    # If import fails, let pytest capture the error when collecting
    raise


def test_base_agent_core_imports_and_instantiate() -> None:
    """Simple smoke test: import and instantiate BaseAgentCore."""
    core = BaseAgentCore()
    assert core is not None