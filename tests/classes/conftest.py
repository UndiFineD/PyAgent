"""Pytest fixtures shared across all core module tests."""

import pytest
import sys
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from tests.agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture
def base_agent_module() -> Any:
    """Load and return the base_agent module."""
    with agent_dir_on_path():
        return load_agent_module("base_agent.py")


@pytest.fixture
def base_agent(base_agent_module: Any) -> Any:
    """Create a BaseAgent instance for testing."""
    class ConcreteAgent(base_agent_module.BaseAgent):
        def _process_logic(self, content: str) -> str:
            return content
            
    return ConcreteAgent("test.md")
