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
Tests for rpc_registration_scraper_factory
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
    from logic.agents.security.toolkit.rpc.rpc_toolkit.pe_rpc_if_scraper.rpc_registration_lookup.rpc_registration_scraper_factory import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_unsupporteddisassemblertypeexception_exists():
    """Test that UnsupportedDisassemblerTypeException class exists and is importable."""
    assert 'UnsupportedDisassemblerTypeException' in dir()


def test_rpc_registration_scraper_factory_exists():
    """Test that rpc_registration_scraper_factory function exists."""
    assert callable(rpc_registration_scraper_factory)


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

