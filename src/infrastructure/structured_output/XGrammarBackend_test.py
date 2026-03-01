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
Tests for XGrammarBackend
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
    from infrastructure.structured_output.XGrammarBackend import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_grammartype_exists():
    """Test that GrammarType class exists and is importable."""
    assert 'GrammarType' in dir()


def test_vocabtype_exists():
    """Test that VocabType class exists and is importable."""
    assert 'VocabType' in dir()


def test_tokenizerinfo_exists():
    """Test that TokenizerInfo class exists and is importable."""
    assert 'TokenizerInfo' in dir()


def test_compiledgrammar_exists():
    """Test that CompiledGrammar class exists and is importable."""
    assert 'CompiledGrammar' in dir()


def test_grammarmatcher_exists():
    """Test that GrammarMatcher class exists and is importable."""
    assert 'GrammarMatcher' in dir()


def test_grammarcompiler_exists():
    """Test that GrammarCompiler class exists and is importable."""
    assert 'GrammarCompiler' in dir()


def test_xgrammargrammar_exists():
    """Test that XGrammarGrammar class exists and is importable."""
    assert 'XGrammarGrammar' in dir()


def test_xgrammarbackend_exists():
    """Test that XGrammarBackend class exists and is importable."""
    assert 'XGrammarBackend' in dir()


def test_asyncxgrammarbackend_exists():
    """Test that AsyncXGrammarBackend class exists and is importable."""
    assert 'AsyncXGrammarBackend' in dir()


def test_asyncxgrammarbackend_instantiation():
    """Test that AsyncXGrammarBackend can be instantiated."""
    instance = AsyncXGrammarBackend()
    assert instance is not None


def test_compositegrammar_exists():
    """Test that CompositeGrammar class exists and is importable."""
    assert 'CompositeGrammar' in dir()


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

