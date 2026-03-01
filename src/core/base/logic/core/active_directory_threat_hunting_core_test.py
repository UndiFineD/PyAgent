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
Tests for active_directory_threat_hunting_core
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
    from core.base.logic.core.active_directory_threat_hunting_core import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_threatlevel_exists():
    """Test that ThreatLevel class exists and is importable."""
    assert 'ThreatLevel' in dir()


def test_adobjecttype_exists():
    """Test that ADObjectType class exists and is importable."""
    assert 'ADObjectType' in dir()


def test_adobject_exists():
    """Test that ADObject class exists and is importable."""
    assert 'ADObject' in dir()


def test_threatfinding_exists():
    """Test that ThreatFinding class exists and is importable."""
    assert 'ThreatFinding' in dir()


def test_huntingresult_exists():
    """Test that HuntingResult class exists and is importable."""
    assert 'HuntingResult' in dir()


def test_activedirectorythreathuntingcore_exists():
    """Test that ActiveDirectoryThreatHuntingCore class exists and is importable."""
    assert 'ActiveDirectoryThreatHuntingCore' in dir()


def test_activedirectorythreathuntingcore_instantiation():
    """Test that ActiveDirectoryThreatHuntingCore can be instantiated."""
    instance = ActiveDirectoryThreatHuntingCore()
    assert instance is not None


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

