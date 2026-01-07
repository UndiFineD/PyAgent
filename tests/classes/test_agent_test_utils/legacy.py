import pytest
from pathlib import Path
from typing import Any, List, Dict, Optional
import sys
try:
    from tests.agent_test_utils import *
except ImportError:
    pass

def test_agent_dir_on_path_modifies_sys_path() -> None:
    """Test that agent_dir_on_path adds AGENT_DIR to sys.path."""
    original_path = list(sys.path)
    with agent_dir_on_path():
        assert str(AGENT_DIR) in sys.path

    # Should be restored
    assert sys.path == original_path
