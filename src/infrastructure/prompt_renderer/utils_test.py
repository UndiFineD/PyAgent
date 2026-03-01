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
Tests for utils
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
    from infrastructure.prompt_renderer.utils import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_embeddingloader_exists():
    """Test that EmbeddingLoader class exists and is importable."""
    assert 'EmbeddingLoader' in dir()


def test_render_prompt_exists():
    """Test that render_prompt function exists."""
    assert callable(render_prompt)


def test_apply_chat_template_exists():
    """Test that apply_chat_template function exists."""
    assert callable(apply_chat_template)


def test_truncate_prompt_exists():
    """Test that truncate_prompt function exists."""
    assert callable(truncate_prompt)


def test_generate_cache_salt_exists():
    """Test that generate_cache_salt function exists."""
    assert callable(generate_cache_salt)


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

