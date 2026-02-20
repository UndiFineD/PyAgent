#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""TypedPrompts - Type-safe prompt schemas with type guards.

This module provides simple runtime checks and helpers for handling
different prompt formats used across the codebase. The implementations
are intentionally small and test-focused.
"""

from typing import Any, Generic, TypeAlias, TypeVar
try:
    from typing_extensions import NotRequired, TypedDict
except Exception:  # pragma: no cover - very old Pythons
    from typing import TypedDict  # type: ignore


# Prompt TypedDicts
class TextPrompt(TypedDict, total=False):
    prompt: str
    multi_modal_data: NotRequired[dict[str, Any] | None]
    mm_processor_kwargs: NotRequired[dict[str, Any] | None]
    cache_salt: NotRequired[str]


class TokensPrompt(TypedDict, total=False):
    prompt_token_ids: list[int]
    prompt: NotRequired[str]
    token_type_ids: NotRequired[list[int]]
    multi_modal_data: NotRequired[dict[str, Any] | None]
    mm_processor_kwargs: NotRequired[dict[str, Any] | None]
    cache_salt: NotRequired[str]


class EmbedsPrompt(TypedDict, total=False):
    prompt_embeds: Any
    cache_salt: NotRequired[str]


class DataPrompt(TypedDict, total=False):
    data: Any
    data_format: str


# Type aliases
SingletonPrompt: TypeAlias = str | TextPrompt | TokensPrompt | EmbedsPrompt
T1 = TypeVar("T1", bound=SingletonPrompt)
T2 = TypeVar("T2", bound=SingletonPrompt)


class ExplicitEncoderDecoderPrompt(TypedDict, Generic[T1, T2], total=False):
    encoder_prompt: T1
    decoder_prompt: T2 | None
    mm_processor_kwargs: NotRequired[dict[str, Any]]


PromptType: TypeAlias = SingletonPrompt | ExplicitEncoderDecoderPrompt


# Type guards (runtime checks)
def is_text_prompt(prompt: SingletonPrompt) -> bool:
    return isinstance(prompt, dict) and "prompt" in prompt and "prompt_token_ids" not in prompt and "prompt_embeds" not in prompt


def is_tokens_prompt(prompt: SingletonPrompt) -> bool:
    return isinstance(prompt, dict) and "prompt_token_ids" in prompt and "prompt_embeds" not in prompt


def is_embeds_prompt(prompt: SingletonPrompt) -> bool:
    return isinstance(prompt, dict) and "prompt_embeds" in prompt and "prompt_token_ids" not in prompt


def is_data_prompt(prompt: Any) -> bool:
    return isinstance(prompt, dict) and "data" in prompt and "data_format" in prompt


def is_string_prompt(prompt: SingletonPrompt) -> bool:
    return isinstance(prompt, str)


def is_explicit_encoder_decoder_prompt(prompt: PromptType) -> bool:
    return isinstance(prompt, dict) and "encoder_prompt" in prompt and "decoder_prompt" in prompt


# Prompt parsing utilities
def parse_prompt(prompt: SingletonPrompt) -> dict[str, Any]:
    if is_string_prompt(prompt):
        return {"type": "text", "prompt": prompt}
    if is_text_prompt(prompt):
        return {"type": "text", **prompt}
    if is_tokens_prompt(prompt):
        return {"type": "tokens", **prompt}
    if is_embeds_prompt(prompt):
        return {"type": "embeds", **prompt}
    if is_data_prompt(prompt):
        return {"type": "data", **prompt}
    raise ValueError(f"Unknown prompt type: {type(prompt)}")


def get_prompt_text(prompt: SingletonPrompt) -> str | None:
    if is_string_prompt(prompt):
        return prompt
    if is_text_prompt(prompt):
        return prompt.get("prompt")
    if is_tokens_prompt(prompt):
        return prompt.get("prompt")
    return None


def get_prompt_token_ids(prompt: SingletonPrompt) -> list[int] | None:
    if is_tokens_prompt(prompt):
        return prompt.get("prompt_token_ids")
    return None


def has_multi_modal_data(prompt: SingletonPrompt) -> bool:
    if isinstance(prompt, dict):
        return "multi_modal_data" in prompt and bool(prompt.get("multi_modal_data"))
    return False


# Simple factory helpers used by tests
def make_text_prompt(text: str, **kwargs: Any) -> TextPrompt:
    p: TextPrompt = {"prompt": text}
    p.update(kwargs)
    return p


def make_tokens_prompt(token_ids: list[int], **kwargs: Any) -> TokensPrompt:
    p: TokensPrompt = {"prompt_token_ids": token_ids}
    p.update(kwargs)
    return p


def make_embeds_prompt(embeds: Any, **kwargs: Any) -> EmbedsPrompt:
    p: EmbedsPrompt = {"prompt_embeds": embeds}
    p.update(kwargs)
    return p


def make_encoder_decoder_prompt(encoder: SingletonPrompt, decoder: SingletonPrompt | None = None, **kwargs: Any) -> ExplicitEncoderDecoderPrompt:
    p: ExplicitEncoderDecoderPrompt = {"encoder_prompt": encoder, "decoder_prompt": decoder}
    p.update(kwargs)
    return p


def validate_prompt(prompt: PromptType) -> bool:
    try:
        if is_explicit_encoder_decoder_prompt(prompt):
            # both encoder and decoder should be valid singleton prompts
            return True
        parse_prompt(prompt)  # will raise for unknown types
        return True
    except Exception:
        return False

