"""Legacy unit tests for the coder module."""
import pytest
from pathlib import Path
from typing import Any, List, Dict, Optional
import sys
try:
    from tests.utils.agent_test_utils import *
except ImportError:
    pass

def test_coder_agent_keyword_prompt_generates_suggestions(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, base_agent_module: Any) -> str:
    def fake_improve_content(self, prompt: str) -> str:
        return "x=1 # AI GENERATED CONTENT"

    monkeypatch.setattr(base_agent_module.BaseAgent, "improve_content", fake_improve_content)

    with agent_dir_on_path():
        mod = load_agent_module("coder/code_generator.py")
    target = tmp_path / "x.py"
    agent = mod.CoderAgent(str(target))
    agent.previous_content = "ORIGINAL"
    out = agent.improve_content("Improve this code")
    assert out == "x=1 # AI GENERATED CONTENT"
