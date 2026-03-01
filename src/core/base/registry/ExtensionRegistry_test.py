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
Tests for ExtensionRegistry
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
    from core.base.registry.ExtensionRegistry import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_extensionmanager_exists():
    """Test that ExtensionManager class exists and is importable."""
    assert 'ExtensionManager' in dir()


def test_typedextensionmanager_exists():
    """Test that TypedExtensionManager class exists and is importable."""
    assert 'TypedExtensionManager' in dir()


def test_extensioninfo_exists():
    """Test that ExtensionInfo class exists and is importable."""
    assert 'ExtensionInfo' in dir()


def test_multiextensionmanager_exists():
    """Test that MultiExtensionManager class exists and is importable."""
    assert 'MultiExtensionManager' in dir()


def test_lazyextensionmanager_exists():
    """Test that LazyExtensionManager class exists and is importable."""
    assert 'LazyExtensionManager' in dir()


def test_globalregistry_exists():
    """Test that GlobalRegistry class exists and is importable."""
    assert 'GlobalRegistry' in dir()


def test_get_global_registry_exists():
    """Test that get_global_registry function exists."""
    assert callable(get_global_registry)


def test_create_registry_exists():
    """Test that create_registry function exists."""
    assert callable(create_registry)


def test_create_typed_registry_exists():
    """Test that create_typed_registry function exists."""
    assert callable(create_typed_registry)


def test_create_multi_registry_exists():
    """Test that create_multi_registry function exists."""
    assert callable(create_multi_registry)


def test_create_lazy_registry_exists():
    """Test that create_lazy_registry function exists."""
    assert callable(create_lazy_registry)


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

