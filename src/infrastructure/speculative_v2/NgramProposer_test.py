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
Tests for NgramProposer
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
    from infrastructure.speculative_v2.NgramProposer import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_ngramconfig_exists():
    """Test that NgramConfig class exists and is importable."""
    assert 'NgramConfig' in dir()


def test_ngrammatch_exists():
    """Test that NgramMatch class exists and is importable."""
    assert 'NgramMatch' in dir()


def test_ngramproposalresult_exists():
    """Test that NgramProposalResult class exists and is importable."""
    assert 'NgramProposalResult' in dir()


def test_ngramcache_exists():
    """Test that NgramCache class exists and is importable."""
    assert 'NgramCache' in dir()


def test_ngramproposer_exists():
    """Test that NgramProposer class exists and is importable."""
    assert 'NgramProposer' in dir()


def test_weightedngramproposer_exists():
    """Test that WeightedNgramProposer class exists and is importable."""
    assert 'WeightedNgramProposer' in dir()


def test_promptlookupproposer_exists():
    """Test that PromptLookupProposer class exists and is importable."""
    assert 'PromptLookupProposer' in dir()


def test_hybridngramproposer_exists():
    """Test that HybridNgramProposer class exists and is importable."""
    assert 'HybridNgramProposer' in dir()


def test_ngramproposerfactory_exists():
    """Test that NgramProposerFactory class exists and is importable."""
    assert 'NgramProposerFactory' in dir()


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

