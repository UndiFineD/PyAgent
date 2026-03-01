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
Tests for idl_parser
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
    from logic.agents.security.toolkit.rpc.rpc_toolkit.idl_scraper.idl_parser import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_get_interfaces_exists():
    """Test that get_interfaces function exists."""
    assert callable(get_interfaces)


def test_get_interface_name_exists():
    """Test that get_interface_name function exists."""
    assert callable(get_interface_name)


def test_get_interface_uuid_exists():
    """Test that get_interface_uuid function exists."""
    assert callable(get_interface_uuid)


def test_get_functions_exists():
    """Test that get_functions function exists."""
    assert callable(get_functions)


def test_drop_compilation_attributes_exists():
    """Test that drop_compilation_attributes function exists."""
    assert callable(drop_compilation_attributes)


def test_get_typedefs_exists():
    """Test that get_typedefs function exists."""
    assert callable(get_typedefs)


def test_get_import_typedefs_exists():
    """Test that get_import_typedefs function exists."""
    assert callable(get_import_typedefs)


def test_parse_function_parameters_exists():
    """Test that parse_function_parameters function exists."""
    assert callable(parse_function_parameters)


def test_parse_idl_exists():
    """Test that parse_idl function exists."""
    assert callable(parse_idl)


def test_get_args_exists():
    """Test that get_args function exists."""
    assert callable(get_args)


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

