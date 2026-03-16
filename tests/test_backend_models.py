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
"""Tests for WebSocket message schema models."""

import pytest

from backend.models import (
    ActionRequestMessage,
    InitMessage,
    RunTaskMessage,
    SignalMessage,
    TaskDeltaMessage,
)


def test_init_message_valid():
    msg = InitMessage(type="init", session_id="abc-123")
    assert msg.session_id == "abc-123"


def test_run_task_message_valid():
    msg = RunTaskMessage(type="runTask", task_id="t1", task="generateText", payload={"prompt": "hello"})
    assert msg.task == "generateText"


def test_task_delta_message_valid():
    msg = TaskDeltaMessage(task_id="t1", delta="hello ")
    assert msg.type == "taskDelta"


def test_action_request_message_valid():
    msg = ActionRequestMessage(action="openWindow", params={"appId": "editor"})
    assert msg.action == "openWindow"


def test_signal_message_valid():
    msg = SignalMessage(type="signal", session_id="s1", peer_id="p1", signal_type="offer", payload={"sdp": "..."})
    assert msg.signal_type == "offer"
