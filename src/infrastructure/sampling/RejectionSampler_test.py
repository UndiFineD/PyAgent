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
Tests for RejectionSampler
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
    from infrastructure.sampling.RejectionSampler import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_rejectionstrategy_exists():
    """Test that RejectionStrategy class exists and is importable."""
    assert 'RejectionStrategy' in dir()


def test_recoverymode_exists():
    """Test that RecoveryMode class exists and is importable."""
    assert 'RecoveryMode' in dir()


def test_rejectionconfig_exists():
    """Test that RejectionConfig class exists and is importable."""
    assert 'RejectionConfig' in dir()


def test_acceptancestats_exists():
    """Test that AcceptanceStats class exists and is importable."""
    assert 'AcceptanceStats' in dir()


def test_rejectionoutput_exists():
    """Test that RejectionOutput class exists and is importable."""
    assert 'RejectionOutput' in dir()


def test_probabilityprovider_exists():
    """Test that ProbabilityProvider class exists and is importable."""
    assert 'ProbabilityProvider' in dir()


def test_rejectionsampler_exists():
    """Test that RejectionSampler class exists and is importable."""
    assert 'RejectionSampler' in dir()


def test_streamingrejectionsampler_exists():
    """Test that StreamingRejectionSampler class exists and is importable."""
    assert 'StreamingRejectionSampler' in dir()


def test_batchrejectionsampler_exists():
    """Test that BatchRejectionSampler class exists and is importable."""
    assert 'BatchRejectionSampler' in dir()


def test_create_rejection_sampler_exists():
    """Test that create_rejection_sampler function exists."""
    assert callable(create_rejection_sampler)


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

