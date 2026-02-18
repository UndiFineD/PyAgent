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
    from .bridge import MCPServerInfo, MCPServerType, MCPCategory, MCPServerConfig, MCPTool, MCPServerRegistry, MCPServerInstance, MCPBridge, MCPToolOrchestrator
except ImportError:
    from .bridge import MCPServerInfo, MCPServerType, MCPCategory, MCPServerConfig, MCPTool, MCPServerRegistry, MCPServerInstance, MCPBridge, MCPToolOrchestrator



def test_mcpserverinfo_basic():
    assert MCPServerInfo is not None


def test_mcpservertype_basic():
    assert MCPServerType is not None


def test_mcpcategory_basic():
    assert MCPCategory is not None


def test_mcpserverconfig_basic():
    assert MCPServerConfig is not None


def test_mcptool_basic():
    assert MCPTool is not None


def test_mcpserverregistry_basic():
    assert MCPServerRegistry is not None


def test_mcpserverinstance_basic():
    assert MCPServerInstance is not None


def test_mcpbridge_basic():
    assert MCPBridge is not None


def test_mcptoolorchestrator_basic():
    assert MCPToolOrchestrator is not None
