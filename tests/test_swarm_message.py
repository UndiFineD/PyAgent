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
"""Tests for swarm message model (prj0000022)."""

import pytest

from swarm.message_model import Message, validate_message


def _valid():
    return {
        "id": "uuid-1",
        "timestamp": "2026-03-09T00:00Z",
        "type": "task_request",
        "priority": "high",
        "source": "agent-1",
        "destination": "scheduler",
        "payload": {"foo": "bar"},
        "checksum": "abc",
    }


def test_validate_message_accepts_valid():
    assert validate_message(_valid()) is True


def test_validate_message_rejects_missing_field():
    from pydantic import ValidationError

    bad = _valid()
    del bad["checksum"]
    with pytest.raises(ValidationError):
        validate_message(bad)


def test_message_model_fields():
    m = Message(**_valid())
    assert m.id == "uuid-1"
    assert m.priority == "high"
    assert m.payload == {"foo": "bar"}
