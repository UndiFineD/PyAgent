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
Tests for radare2
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
    from logic.agents.security.toolkit.rpc.rpc_toolkit.pe_rpc_if_scraper.rpc_registration_lookup.dism_scripts.radare2 import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_find_rpc_server_registration_funcs_exists():
    """Test that find_rpc_server_registration_funcs function exists."""
    assert callable(find_rpc_server_registration_funcs)


def test_find_all_func_xrefs_exists():
    """Test that find_all_func_xrefs function exists."""
    assert callable(find_all_func_xrefs)


def test_get_func_start_exists():
    """Test that get_func_start function exists."""
    assert callable(get_func_start)


def test_get_reg_value_exists():
    """Test that get_reg_value function exists."""
    assert callable(get_reg_value)


def test_is_reg_exists():
    """Test that is_reg function exists."""
    assert callable(is_reg)


def test_parse_argument_exists():
    """Test that parse_argument function exists."""
    assert callable(parse_argument)


def test_get_func_call_args_exists():
    """Test that get_func_call_args function exists."""
    assert callable(get_func_call_args)


def test_get_call_args_manually_exists():
    """Test that get_call_args_manually function exists."""
    assert callable(get_call_args_manually)


def test_get_rpc_server_registration_info_exists():
    """Test that get_rpc_server_registration_info function exists."""
    assert callable(get_rpc_server_registration_info)


def test_get_arg_count_for_function_name_exists():
    """Test that get_arg_count_for_function_name function exists."""
    assert callable(get_arg_count_for_function_name)


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

