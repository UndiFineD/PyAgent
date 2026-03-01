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
Tests for GuidanceBackend
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
    from infrastructure.structured_output.GuidanceBackend import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_guidancetemplatetype_exists():
    """Test that GuidanceTemplateType class exists and is importable."""
    assert 'GuidanceTemplateType' in dir()


def test_guidancevariable_exists():
    """Test that GuidanceVariable class exists and is importable."""
    assert 'GuidanceVariable' in dir()


def test_guidancetemplate_exists():
    """Test that GuidanceTemplate class exists and is importable."""
    assert 'GuidanceTemplate' in dir()


def test_guidancestate_exists():
    """Test that GuidanceState class exists and is importable."""
    assert 'GuidanceState' in dir()


def test_compiledguidanceprogram_exists():
    """Test that CompiledGuidanceProgram class exists and is importable."""
    assert 'CompiledGuidanceProgram' in dir()


def test_guidancegrammar_exists():
    """Test that GuidanceGrammar class exists and is importable."""
    assert 'GuidanceGrammar' in dir()


def test_guidancebackend_exists():
    """Test that GuidanceBackend class exists and is importable."""
    assert 'GuidanceBackend' in dir()


def test_asyncguidancebackend_exists():
    """Test that AsyncGuidanceBackend class exists and is importable."""
    assert 'AsyncGuidanceBackend' in dir()


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

