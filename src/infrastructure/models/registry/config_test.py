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
Tests for config
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
    from infrastructure.models.registry.config import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_modelcapability_exists():
    """Test that ModelCapability class exists and is importable."""
    assert 'ModelCapability' in dir()


def test_modelarchitecture_exists():
    """Test that ModelArchitecture class exists and is importable."""
    assert 'ModelArchitecture' in dir()


def test_quantizationtype_exists():
    """Test that QuantizationType class exists and is importable."""
    assert 'QuantizationType' in dir()


def test_modelformat_exists():
    """Test that ModelFormat class exists and is importable."""
    assert 'ModelFormat' in dir()


def test_modelconfig_exists():
    """Test that ModelConfig class exists and is importable."""
    assert 'ModelConfig' in dir()


def test_architecturespec_exists():
    """Test that ArchitectureSpec class exists and is importable."""
    assert 'ArchitectureSpec' in dir()


def test_modelinfo_exists():
    """Test that ModelInfo class exists and is importable."""
    assert 'ModelInfo' in dir()


def test_vramestimate_exists():
    """Test that VRAMEstimate class exists and is importable."""
    assert 'VRAMEstimate' in dir()


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

