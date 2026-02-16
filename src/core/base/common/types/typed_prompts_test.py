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

import pytest
from core.base.common.types.typed_prompts import TextPrompt, TokensPrompt, EmbedsPrompt, DataPrompt, ExplicitEncoderDecoderPrompt, is_text_prompt, is_tokens_prompt, is_embeds_prompt, is_data_prompt, is_string_prompt, is_explicit_encoder_decoder_prompt, parse_prompt, get_prompt_text, get_prompt_token_ids, has_multi_modal_data, make_text_prompt, make_tokens_prompt, make_embeds_prompt, make_encoder_decoder_prompt, validate_prompt


def test_textprompt_basic():
    assert TextPrompt is not None


def test_tokensprompt_basic():
    assert TokensPrompt is not None


def test_embedsprompt_basic():
    assert EmbedsPrompt is not None


def test_dataprompt_basic():
    assert DataPrompt is not None


def test_explicitencoderdecoderprompt_basic():
    assert ExplicitEncoderDecoderPrompt is not None


def test_is_text_prompt_basic():
    assert callable(is_text_prompt)


def test_is_tokens_prompt_basic():
    assert callable(is_tokens_prompt)


def test_is_embeds_prompt_basic():
    assert callable(is_embeds_prompt)


def test_is_data_prompt_basic():
    assert callable(is_data_prompt)


def test_is_string_prompt_basic():
    assert callable(is_string_prompt)


def test_is_explicit_encoder_decoder_prompt_basic():
    assert callable(is_explicit_encoder_decoder_prompt)


def test_parse_prompt_basic():
    assert callable(parse_prompt)


def test_get_prompt_text_basic():
    assert callable(get_prompt_text)


def test_get_prompt_token_ids_basic():
    assert callable(get_prompt_token_ids)


def test_has_multi_modal_data_basic():
    assert callable(has_multi_modal_data)


def test_make_text_prompt_basic():
    assert callable(make_text_prompt)


def test_make_tokens_prompt_basic():
    assert callable(make_tokens_prompt)


def test_make_embeds_prompt_basic():
    assert callable(make_embeds_prompt)


def test_make_encoder_decoder_prompt_basic():
    assert callable(make_encoder_decoder_prompt)


def test_validate_prompt_basic():
    assert callable(validate_prompt)
