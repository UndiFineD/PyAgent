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
from core.base.logic.core.ai_agent_orchestration_core import MessagePart, UIMessage, ConversationThread, ToolDefinition, AgentConfig, StreamingContext, MemoryProvider, ToolProvider, StreamingProvider, CodeExecutionProvider, AIAgentOrchestrationCore


def test_messagepart_basic():
    assert MessagePart is not None


def test_uimessage_basic():
    assert UIMessage is not None


def test_conversationthread_basic():
    assert ConversationThread is not None


def test_tooldefinition_basic():
    assert ToolDefinition is not None


def test_agentconfig_basic():
    assert AgentConfig is not None


def test_streamingcontext_basic():
    assert StreamingContext is not None


def test_memoryprovider_basic():
    assert MemoryProvider is not None


def test_toolprovider_basic():
    assert ToolProvider is not None


def test_streamingprovider_basic():
    assert StreamingProvider is not None


def test_codeexecutionprovider_basic():
    assert CodeExecutionProvider is not None


def test_aiagentorchestrationcore_basic():
    assert AIAgentOrchestrationCore is not None
