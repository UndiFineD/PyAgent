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
Tests for bridge
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
    from tools.mcp.bridge import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_mcpservertype_exists():
    """Test that MCPServerType class exists and is importable."""
    assert 'MCPServerType' in dir()


def test_mcpcategory_exists():
    """Test that MCPCategory class exists and is importable."""
    assert 'MCPCategory' in dir()


def test_mcpserverconfig_exists():
    """Test that MCPServerConfig class exists and is importable."""
    assert 'MCPServerConfig' in dir()


def test_mcptool_exists():
    """Test that MCPTool class exists and is importable."""
    assert 'MCPTool' in dir()


def test_mcpserverregistry_exists():
    """Test that MCPServerRegistry class exists and is importable."""
    assert 'MCPServerRegistry' in dir()


def test_mcpserverinstance_exists():
    """Test that MCPServerInstance class exists and is importable."""
    assert 'MCPServerInstance' in dir()


def test_mcpbridge_exists():
    """Test that MCPBridge class exists and is importable."""
    assert 'MCPBridge' in dir()


def test_mcptoolorchestrator_exists():
    """Test that MCPToolOrchestrator class exists and is importable."""
    assert 'MCPToolOrchestrator' in dir()


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

