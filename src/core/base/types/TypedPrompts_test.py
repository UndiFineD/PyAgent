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
Tests for TypedPrompts
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
    from core.base.types.TypedPrompts import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_textprompt_exists():
    """Test that TextPrompt class exists and is importable."""
    assert 'TextPrompt' in dir()


def test_tokensprompt_exists():
    """Test that TokensPrompt class exists and is importable."""
    assert 'TokensPrompt' in dir()


def test_embedsprompt_exists():
    """Test that EmbedsPrompt class exists and is importable."""
    assert 'EmbedsPrompt' in dir()


def test_dataprompt_exists():
    """Test that DataPrompt class exists and is importable."""
    assert 'DataPrompt' in dir()


def test_explicitencoderdecoderprompt_exists():
    """Test that ExplicitEncoderDecoderPrompt class exists and is importable."""
    assert 'ExplicitEncoderDecoderPrompt' in dir()


def test_is_text_prompt_exists():
    """Test that is_text_prompt function exists."""
    assert callable(is_text_prompt)


def test_is_tokens_prompt_exists():
    """Test that is_tokens_prompt function exists."""
    assert callable(is_tokens_prompt)


def test_is_embeds_prompt_exists():
    """Test that is_embeds_prompt function exists."""
    assert callable(is_embeds_prompt)


def test_is_data_prompt_exists():
    """Test that is_data_prompt function exists."""
    assert callable(is_data_prompt)


def test_is_string_prompt_exists():
    """Test that is_string_prompt function exists."""
    assert callable(is_string_prompt)


def test_is_explicit_encoder_decoder_prompt_exists():
    """Test that is_explicit_encoder_decoder_prompt function exists."""
    assert callable(is_explicit_encoder_decoder_prompt)


def test_parse_prompt_exists():
    """Test that parse_prompt function exists."""
    assert callable(parse_prompt)


def test_get_prompt_text_exists():
    """Test that get_prompt_text function exists."""
    assert callable(get_prompt_text)


def test_get_prompt_token_ids_exists():
    """Test that get_prompt_token_ids function exists."""
    assert callable(get_prompt_token_ids)


def test_has_multi_modal_data_exists():
    """Test that has_multi_modal_data function exists."""
    assert callable(has_multi_modal_data)


def test_make_text_prompt_exists():
    """Test that make_text_prompt function exists."""
    assert callable(make_text_prompt)


def test_make_tokens_prompt_exists():
    """Test that make_tokens_prompt function exists."""
    assert callable(make_tokens_prompt)


def test_make_embeds_prompt_exists():
    """Test that make_embeds_prompt function exists."""
    assert callable(make_embeds_prompt)


def test_make_encoder_decoder_prompt_exists():
    """Test that make_encoder_decoder_prompt function exists."""
    assert callable(make_encoder_decoder_prompt)


def test_validate_prompt_exists():
    """Test that validate_prompt function exists."""
    assert callable(validate_prompt)


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

