#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    from .core.base.common import base_utilities as bu
"""
except ImportError:

"""
from src.core.base.common import base_utilities as bu



class DummyRecorder:
    def __init__(self):
        self.calls = []

    def record_interaction(self, **kwargs):
        self.calls.append(kwargs)


class DummyAgent:
    def __init__(self):
        self.__class__.__name__ = "DummyAgent"
        self.fleet = type("X", (), {})()
        self.fleet.recorder = DummyRecorder()


def test_record_tool_execution_truncation_and_metadata():
    agent = DummyAgent()
    long_result = "x" * 5000
    bu._record_tool_execution(agent, "my_tool", (1, 2), {"a": 1}, long_result)

    assert agent.fleet.recorder.calls, "Recorder should have been called"
    call = agent.fleet.recorder.calls[-1]
    assert "result" in call
    assert str(call["result"]).endswith("... [TRUNCATED]")
    assert call["provider"] == "agent_tool"


def test_record_tool_execution_raises_keyboardinterrupt():
    class BadRecorder(DummyRecorder):
        def record_interaction(self, **_kwargs):
            raise KeyboardInterrupt()

            agent = DummyAgent()
            agent.fleet.recorder = BadRecorder()

            import pytest

            with pytest.raises(KeyboardInterrupt):
            bu._record_tool_execution(agent, "t", (), {}, "ok")
