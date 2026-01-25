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
"""
Test Coder Legacy module.
"""

import pytest
from pathlib import Path
from typing import Any
import sys
import asyncio
from unittest.mock import MagicMock
from contextlib import contextmanager


@contextmanager
def agent_dir_on_path():
    base_path = Path(__file__).resolve().parent.parent.parent.parent / "src"
    parent_path = base_path.parent
    if str(parent_path) not in sys.path:
        sys.path.insert(0, str(parent_path))
    try:
        yield
    finally:
        if str(parent_path) in sys.path:
            sys.path.remove(str(parent_path))


def load_agent_module(relative_path: str):
    import importlib.util

    file_path = (
        Path(__file__).resolve().parent.parent.parent.parent / "src" / relative_path
    )
    spec = importlib.util.spec_from_file_location("dynamic_agent", file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_coder_agent_keyword_prompt_generates_suggestions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, agent_module: Any
) -> None:
    # Always mock rust_core for this test
    mock_rust = MagicMock()
    mock_rust.CoderCore = MagicMock(return_value=MagicMock())
    mock_rust.generate_neural_response = MagicMock(
        return_value="x=1 # AI GENERATED CONTENT"
    )
    monkeypatch.setitem(sys.modules, "rust_core", mock_rust)
    async def fake_improve_content(self, prompt: str, **kwargs: Any) -> str:
        return "x=1 # AI GENERATED CONTENT"

    import src.core.base.lifecycle.base_agent

    print(f"DEBUG: src.core.base.BaseAgent type: {type(src.core.base.BaseAgent)}")
    if isinstance(src.core.base.BaseAgent, type):
        # If it is the class itself (weird import issue)
        monkeypatch.setattr(
            src.core.base.BaseAgent, "improve_content", fake_improve_content
        )
    else:
        monkeypatch.setattr(
            src.core.base.BaseAgent.BaseAgent, "improve_content", fake_improve_content
        )

    with agent_dir_on_path():
        mod = load_agent_module("logic/agents/development/code_generator_agent.py")

    target = tmp_path / "x.py"
    target.write_text("# initial", encoding="utf-8")

    agent = mod.CoderAgent(str(target))
    agent.previous_content = "ORIGINAL"

    out = asyncio.run(agent.improve_content("Improve this code"))

    assert "AI GENERATED CONTENT" in out