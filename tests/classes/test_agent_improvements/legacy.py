import pytest
from pathlib import Path
from typing import Any, List, Dict, Optional
import sys
try:
    from tests.agent_test_utils import *
except ImportError:
    pass

def test_improvements_agent_delegates_to_base(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, base_agent_module: Any
) -> None:
    with agent_dir_on_path():
        mod = load_agent_module("agent_improvements.py")

    def fake_run_subagent(
            self: Any,
            description: str,
            prompt: str,
            original_content: str = "") -> str:
        return "IMPROVED"

    monkeypatch.setattr(
        base_agent_module.BaseAgent,
        "run_subagent",
        fake_run_subagent,
        raising=True)
    target = tmp_path / "x.improvements.md"
    target.write_text("BEFORE", encoding="utf-8")
    agent = mod.ImprovementsAgent(str(target))
    agent.read_previous_content()
    assert agent.improve_content("prompt") == "IMPROVED"
