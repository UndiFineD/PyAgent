import pytest
import sys
from pathlib import Path
from tests.agent_test_utils import load_agent_module

@pytest.fixture
def report_module():
    """Fixture that returns the loaded generate_agent_reports module."""
    # The module is generate_agent_reports.py in src/
    src_dir = Path(__file__).parent.parent.parent.parent / "src"
    module_path = src_dir / "generate_agent_reports.py"
    return load_agent_module(module_path)
