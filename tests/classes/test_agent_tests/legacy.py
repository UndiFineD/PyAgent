import pytest
from pathlib import Path
from typing import Any, List, Dict, Optional
import sys
try:
    from tests.agent_test_utils import *
except ImportError:
    pass

def test_tests_agent_update_file_writes_raw(tmp_path: Path) -> None:
    with agent_dir_on_path():
        mod = load_agent_module("agent_tests.py")
    target = tmp_path / "test_something.py"
    agent = mod.TestsAgent(str(target))
    agent.current_content = "print('hi')\n"
    agent.update_file()
    assert target.read_text(encoding="utf-8") == "print('hi')\n"
