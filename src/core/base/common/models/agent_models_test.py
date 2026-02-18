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
    from core.base.common.models.agent_models import AgentConfig, ComposedAgent, AgentHealthCheck, AgentPluginConfig, ExecutionProfile, AgentPipeline, AgentParallel, AgentRouter
except ImportError:
    from core.base.common.models.agent_models import AgentConfig, ComposedAgent, AgentHealthCheck, AgentPluginConfig, ExecutionProfile, AgentPipeline, AgentParallel, AgentRouter



def test_agentconfig_basic():
    assert AgentConfig is not None


def test_composedagent_basic():
    assert ComposedAgent is not None


def test_agenthealthcheck_basic():
    assert AgentHealthCheck is not None


def test_agentpluginconfig_basic():
    assert AgentPluginConfig is not None


def test_executionprofile_basic():
    assert ExecutionProfile is not None


def test_agentpipeline_basic():
    assert AgentPipeline is not None


def test_agentparallel_basic():
    assert AgentParallel is not None


def test_agentrouter_basic():
    assert AgentRouter is not None
