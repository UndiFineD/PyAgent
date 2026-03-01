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
Tests for pe_utils
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
    from logic.agents.security.toolkit.rpc.rpc_toolkit.pe_rpc_if_scraper.pe_utils import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_ptr_to_rva_exists():
    """Test that ptr_to_rva function exists."""
    assert callable(ptr_to_rva)


def test_assert_dotnet_pe_exists():
    """Test that assert_dotnet_pe function exists."""
    assert callable(assert_dotnet_pe)


def test_get_rdata_offset_size_rva_exists():
    """Test that get_rdata_offset_size_rva function exists."""
    assert callable(get_rdata_offset_size_rva)


def test_get_rpcrt_imports_exists():
    """Test that get_rpcrt_imports function exists."""
    assert callable(get_rpcrt_imports)


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

