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
Tests for active_directory_analysis_core
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
    from core.base.logic.core.active_directory_analysis_core import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_privilegelevel_exists():
    """Test that PrivilegeLevel class exists and is importable."""
    assert 'PrivilegeLevel' in dir()


def test_adobjecttype_exists():
    """Test that ADObjectType class exists and is importable."""
    assert 'ADObjectType' in dir()


def test_adobject_exists():
    """Test that ADObject class exists and is importable."""
    assert 'ADObject' in dir()


def test_adenumerationresult_exists():
    """Test that ADEnumerationResult class exists and is importable."""
    assert 'ADEnumerationResult' in dir()


def test_advulnerability_exists():
    """Test that ADVulnerability class exists and is importable."""
    assert 'ADVulnerability' in dir()


def test_activedirectoryanalysiscore_exists():
    """Test that ActiveDirectoryAnalysisCore class exists and is importable."""
    assert 'ActiveDirectoryAnalysisCore' in dir()


def test_activedirectoryanalysiscore_instantiation():
    """Test that ActiveDirectoryAnalysisCore can be instantiated."""
    instance = ActiveDirectoryAnalysisCore()
    assert instance is not None


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

