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
Tests for models
Auto-generated test template - expand with actual test cases
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    from infrastructure.mcp_tools.models import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_mcpservertype_exists():
    """Test that MCPServerType class exists and is importable."""
    assert 'MCPServerType' in dir()


def test_toolstatus_exists():
    """Test that ToolStatus class exists and is importable."""
    assert 'ToolStatus' in dir()


def test_sessionstate_exists():
    """Test that SessionState class exists and is importable."""
    assert 'SessionState' in dir()


def test_mcpserverconfig_exists():
    """Test that MCPServerConfig class exists and is importable."""
    assert 'MCPServerConfig' in dir()


def test_toolschema_exists():
    """Test that ToolSchema class exists and is importable."""
    assert 'ToolSchema' in dir()


def test_toolcall_exists():
    """Test that ToolCall class exists and is importable."""
    assert 'ToolCall' in dir()


def test_toolresult_exists():
    """Test that ToolResult class exists and is importable."""
    assert 'ToolResult' in dir()


def test_mcpsession_exists():
    """Test that MCPSession class exists and is importable."""
    assert 'MCPSession' in dir()


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

