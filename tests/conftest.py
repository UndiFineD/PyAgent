"""Pytest configuration for PyAgent tests."""
import pytest
import tempfile
from pathlib import Path
from src.infrastructure.fleet.AgentRegistry import AgentRegistry

@pytest.fixture
def agent_sandbox():
    """Provides a clean, temporary src/ and data/ environment for agent tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        src_dir = temp_path / "src"
        data_dir = temp_path / "data"
        src_dir.mkdir()
        data_dir.mkdir()
        
        # Initialize basic structure
        (src_dir / "__init__.py").touch()
        
        yield temp_path

@pytest.fixture
def agent_registry():
    """Provides a central AgentRegistry for test use."""
    workspace_root = Path(__file__).parent.parent
    return AgentRegistry.get_agent_map(workspace_root)
