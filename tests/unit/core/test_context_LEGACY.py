#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
