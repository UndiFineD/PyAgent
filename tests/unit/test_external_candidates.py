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

from src.external_candidates.holo import VideoProcessor
from src.external_candidates.banner import banner
from src.external_candidates.llava_prompt import get_question_text, get_choice_text
from src.external_candidates.system_prompt_formatter import SystemPromptFormatter
from src.external_candidates.videoagent_utils import execute_agent_chain


def test_holo_import():
    v = VideoProcessor()
    try:
        v()
    except NotImplementedError:
        pass


def test_banner_print(capsys):
    banner()
    captured = capsys.readouterr()
    assert "Created by" in captured.out


def test_llava_helpers():
    problem = {"question": "Q?", "choices": ["a", "b"], "answer": 0}
    assert get_question_text(problem) == "Q?"
    assert "(A)" in get_choice_text(problem, ["A", "B"])  # formatting check


def test_system_prompt_formatter():
    fmt = SystemPromptFormatter()
    out = fmt.format(task="do X", instructions="step1")
    assert "Task" in out and "Instructions" in out


def test_execute_agent_chain_stub():
    class DummyAgent:
        def execute(self, **kwargs):
            return {"out": "ok"}

    agent_graph = [{
        "node": "a",
        "inputs": [{"name": "in1"}],
        "outputs": [{"name": "out", "links": []}],
        "class": DummyAgent
    }]
    agent_chain = ["a"]
    user_input_graph = [{"node": "u", "description": "d", "links": [{"a": "in1"}], "value": "v"}]
    ctx = execute_agent_chain(agent_graph, agent_chain, user_input_graph, interactive=False)
    assert isinstance(ctx, dict)
