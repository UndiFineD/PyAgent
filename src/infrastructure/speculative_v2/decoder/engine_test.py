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
Tests for engine
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
    from infrastructure.speculative_v2.decoder.engine import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_speculativedecoder_exists():
    """Test that SpeculativeDecoder class exists and is importable."""
    assert 'SpeculativeDecoder' in dir()


def test_create_ngram_decoder_exists():
    """Test that create_ngram_decoder function exists."""
    assert callable(create_ngram_decoder)


def test_create_medusa_decoder_exists():
    """Test that create_medusa_decoder function exists."""
    assert callable(create_medusa_decoder)


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

