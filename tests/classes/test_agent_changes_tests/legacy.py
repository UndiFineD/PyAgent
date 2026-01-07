import pytest
from pathlib import Path
from typing import Any, List, Dict, Optional
import sys
try:
    from tests.agent_test_utils import *
except ImportError:
    pass

def test_changes_agent_default_content_for_missing_file(tmp_path: Path) -> None:
    with agent_dir_on_path():
        mod = load_agent_module("agent_changes.py")
    target = tmp_path / "missing.changes.md"
    agent = mod.ChangesAgent(str(target))
    assert "No changes recorded" in agent.read_previous_content()
