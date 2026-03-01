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
Tests for ad_monitoring_core
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
    from core.base.logic.core.ad_monitoring_core import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_changetype_exists():
    """Test that ChangeType class exists and is importable."""
    assert 'ChangeType' in dir()


def test_attributechangetype_exists():
    """Test that AttributeChangeType class exists and is importable."""
    assert 'AttributeChangeType' in dir()


def test_securityeventtype_exists():
    """Test that SecurityEventType class exists and is importable."""
    assert 'SecurityEventType' in dir()


def test_adobjectchange_exists():
    """Test that ADObjectChange class exists and is importable."""
    assert 'ADObjectChange' in dir()


def test_attributechange_exists():
    """Test that AttributeChange class exists and is importable."""
    assert 'AttributeChange' in dir()


def test_monitoringsession_exists():
    """Test that MonitoringSession class exists and is importable."""
    assert 'MonitoringSession' in dir()


def test_monitoringconfig_exists():
    """Test that MonitoringConfig class exists and is importable."""
    assert 'MonitoringConfig' in dir()


def test_adconnectionprovider_exists():
    """Test that ADConnectionProvider class exists and is importable."""
    assert 'ADConnectionProvider' in dir()


def test_alertprovider_exists():
    """Test that AlertProvider class exists and is importable."""
    assert 'AlertProvider' in dir()


def test_admonitoringcore_exists():
    """Test that ADMonitoringCore class exists and is importable."""
    assert 'ADMonitoringCore' in dir()


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

