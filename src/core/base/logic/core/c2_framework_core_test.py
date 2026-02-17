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

import pytest
from core.base.logic.core.c2_framework_core import CommunicationProtocol, AgentStatus, TaskStatus, ListenerType, C2Profile, C2Agent, C2Listener, C2Task, C2Extender, C2Session, C2Tunnel, C2Framework, C2FrameworkCore


def test_communicationprotocol_basic():
    assert CommunicationProtocol is not None


def test_agentstatus_basic():
    assert AgentStatus is not None


def test_taskstatus_basic():
    assert TaskStatus is not None


def test_listenertype_basic():
    assert ListenerType is not None


def test_c2profile_basic():
    assert C2Profile is not None


def test_c2agent_basic():
    assert C2Agent is not None


def test_c2listener_basic():
    assert C2Listener is not None


def test_c2task_basic():
    assert C2Task is not None


def test_c2extender_basic():
    assert C2Extender is not None


def test_c2session_basic():
    assert C2Session is not None


def test_c2tunnel_basic():
    assert C2Tunnel is not None


def test_c2framework_basic():
    assert C2Framework is not None


def test_c2frameworkcore_basic():
    assert C2FrameworkCore is not None
