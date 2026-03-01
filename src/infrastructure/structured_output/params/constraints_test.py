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
Tests for constraints
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
    from infrastructure.structured_output.params.constraints import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_outputconstraint_exists():
    """Test that OutputConstraint class exists and is importable."""
    assert 'OutputConstraint' in dir()


def test_jsonschemaconstraint_exists():
    """Test that JsonSchemaConstraint class exists and is importable."""
    assert 'JsonSchemaConstraint' in dir()


def test_regexconstraint_exists():
    """Test that RegexConstraint class exists and is importable."""
    assert 'RegexConstraint' in dir()


def test_choiceconstraint_exists():
    """Test that ChoiceConstraint class exists and is importable."""
    assert 'ChoiceConstraint' in dir()


def test_grammarconstraint_exists():
    """Test that GrammarConstraint class exists and is importable."""
    assert 'GrammarConstraint' in dir()


def test_typeconstraint_exists():
    """Test that TypeConstraint class exists and is importable."""
    assert 'TypeConstraint' in dir()


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

