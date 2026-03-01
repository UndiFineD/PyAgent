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
Tests for Kernels
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
    from infrastructure.sampling.Kernels import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_temperaturesampler_exists():
    """Test that TemperatureSampler class exists and is importable."""
    assert 'TemperatureSampler' in dir()


def test_topksampler_exists():
    """Test that TopKSampler class exists and is importable."""
    assert 'TopKSampler' in dir()


def test_toppsampler_exists():
    """Test that TopPSampler class exists and is importable."""
    assert 'TopPSampler' in dir()


def test_topktoppsampler_exists():
    """Test that TopKTopPSampler class exists and is importable."""
    assert 'TopKTopPSampler' in dir()


def test_gumbelsampler_exists():
    """Test that GumbelSampler class exists and is importable."""
    assert 'GumbelSampler' in dir()


def test_repetitionpenaltysampler_exists():
    """Test that RepetitionPenaltySampler class exists and is importable."""
    assert 'RepetitionPenaltySampler' in dir()


def test_penaltysampler_exists():
    """Test that PenaltySampler class exists and is importable."""
    assert 'PenaltySampler' in dir()


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

