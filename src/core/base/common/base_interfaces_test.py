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
    import pytest
except ImportError:
    import pytest

try:
    from core.base.common.base_interfaces import AgentInterface, OrchestratorInterface, CoreInterface, ContextRecorderInterface, Loadable, Saveable, Component
except ImportError:
    from core.base.common.base_interfaces import AgentInterface, OrchestratorInterface, CoreInterface, ContextRecorderInterface, Loadable, Saveable, Component



def test_agentinterface_basic():
    assert AgentInterface is not None


def test_orchestratorinterface_basic():
    assert OrchestratorInterface is not None


def test_coreinterface_basic():
    assert CoreInterface is not None


def test_contextrecorderinterface_basic():
    assert ContextRecorderInterface is not None


def test_loadable_basic():
    assert Loadable is not None


def test_saveable_basic():
    assert Saveable is not None


def test_component_basic():
    assert Component is not None
