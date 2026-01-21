"""Legacy unit tests for Context agent logic."""

import pytest
from pathlib import Path
from typing import Any

try:
    from tests.utils.agent_test_utils import *
except ImportError:
    pass


def test_context_agent_delegates_to_base(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, base_agent_module: Any
) -> None:
    import asyncio

    with agent_dir_on_path():
        mod = load_agent_module("src/logic/agents/cognitive/context_agent.py")

    async def fake_run_subagent(
        self: Any, description: str, prompt: str, original_content: str = ""
    ) -> str:
        return "IMPROVED"

    monkeypatch.setattr(
        base_agent_module.BaseAgent, "run_subagent", fake_run_subagent, raising=True
    )
    target = tmp_path / "x.description.md"
    target.write_text("BEFORE", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.read_previous_content()
    assert asyncio.run(agent.improve_content("prompt")) == "IMPROVED"
