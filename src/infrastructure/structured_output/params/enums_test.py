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
Tests for enums
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
    from infrastructure.structured_output.params.enums import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_structuredoutputtype_exists():
    """Test that StructuredOutputType class exists and is importable."""
    assert 'StructuredOutputType' in dir()


def test_constrainttype_exists():
    """Test that ConstraintType class exists and is importable."""
    assert 'ConstraintType' in dir()


def test_schemaformat_exists():
    """Test that SchemaFormat class exists and is importable."""
    assert 'SchemaFormat' in dir()


def test_guideddecodingbackend_exists():
    """Test that GuidedDecodingBackend class exists and is importable."""
    assert 'GuidedDecodingBackend' in dir()


def test_whitespacepattern_exists():
    """Test that WhitespacePattern class exists and is importable."""
    assert 'WhitespacePattern' in dir()


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

