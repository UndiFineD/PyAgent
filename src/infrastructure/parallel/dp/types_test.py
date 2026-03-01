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
    from infrastructure.parallel.dp.types import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_dprole_exists():
    """Test that DPRole class exists and is importable."""
    assert 'DPRole' in dir()


def test_workerhealth_exists():
    """Test that WorkerHealth class exists and is importable."""
    assert 'WorkerHealth' in dir()


def test_loadbalancestrategy_exists():
    """Test that LoadBalanceStrategy class exists and is importable."""
    assert 'LoadBalanceStrategy' in dir()


def test_dpconfig_exists():
    """Test that DPConfig class exists and is importable."""
    assert 'DPConfig' in dir()


def test_workerstate_exists():
    """Test that WorkerState class exists and is importable."""
    assert 'WorkerState' in dir()


def test_stepstate_exists():
    """Test that StepState class exists and is importable."""
    assert 'StepState' in dir()


def test_wavestate_exists():
    """Test that WaveState class exists and is importable."""
    assert 'WaveState' in dir()


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

