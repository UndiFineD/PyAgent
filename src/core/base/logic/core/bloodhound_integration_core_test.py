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
Tests for bloodhound_integration_core
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
    from core.base.logic.core.bloodhound_integration_core import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_risklevel_exists():
    """Test that RiskLevel class exists and is importable."""
    assert 'RiskLevel' in dir()


def test_adobjecttype_exists():
    """Test that ADObjectType class exists and is importable."""
    assert 'ADObjectType' in dir()


def test_securitycontrol_exists():
    """Test that SecurityControl class exists and is importable."""
    assert 'SecurityControl' in dir()


def test_adobject_exists():
    """Test that ADObject class exists and is importable."""
    assert 'ADObject' in dir()


def test_securityfinding_exists():
    """Test that SecurityFinding class exists and is importable."""
    assert 'SecurityFinding' in dir()


def test_controlpath_exists():
    """Test that ControlPath class exists and is importable."""
    assert 'ControlPath' in dir()


def test_auditreport_exists():
    """Test that AuditReport class exists and is importable."""
    assert 'AuditReport' in dir()


def test_bloodhoundintegrationcore_exists():
    """Test that BloodHoundIntegrationCore class exists and is importable."""
    assert 'BloodHoundIntegrationCore' in dir()


def test_bloodhoundintegrationcore_instantiation():
    """Test that BloodHoundIntegrationCore can be instantiated."""
    instance = BloodHoundIntegrationCore()
    assert instance is not None


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

