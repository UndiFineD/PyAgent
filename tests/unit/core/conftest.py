"""Pytest fixtures for test_base_agent tests."""

import pytest
import sys
from pathlib import Path
from typing import Any

# Add src to path

from tests.utils.agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture(autouse=True)
def disable_sessions(monkeypatch) -> None:
    """Disable sessions for all base_agent tests to ensure mocks work correctly."""
    monkeypatch.setenv("DV_AGENT_USE_SESSION", "false")


@pytest.fixture
def base_agent_module() -> Any:
    """Load and return the base_agent module."""
    with agent_dir_on_path():
        return load_agent_module("core/base/BaseAgent.py")


@pytest.fixture
def base_agent(base_agent_module: Any) -> Any:
    """Create a BaseAgent instance for testing."""
    # BaseAgent might be abstract, so we might need a concrete implementation
    # or just use the class if it's not strictly abstract in a way that prevents instantiation.
    class ConcreteAgent(base_agent_module.BaseAgent):
        def _process_logic(self, content: str) -> str:
            return content
            
    return ConcreteAgent()
