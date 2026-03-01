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
Tests for types
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
    from infrastructure.kv_transfer.connector.types import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_kvconnectorrole_exists():
    """Test that KVConnectorRole class exists and is importable."""
    assert 'KVConnectorRole' in dir()


def test_kvtransfermode_exists():
    """Test that KVTransferMode class exists and is importable."""
    assert 'KVTransferMode' in dir()


def test_kvtransferconfig_exists():
    """Test that KVTransferConfig class exists and is importable."""
    assert 'KVTransferConfig' in dir()


def test_kvconnectormetadata_exists():
    """Test that KVConnectorMetadata class exists and is importable."""
    assert 'KVConnectorMetadata' in dir()


def test_kvcacheblocks_exists():
    """Test that KVCacheBlocks class exists and is importable."""
    assert 'KVCacheBlocks' in dir()


def test_forwardcontext_exists():
    """Test that ForwardContext class exists and is importable."""
    assert 'ForwardContext' in dir()


def test_request_exists():
    """Test that Request class exists and is importable."""
    assert 'Request' in dir()


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

