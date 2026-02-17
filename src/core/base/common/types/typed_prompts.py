#!/usr/bin/env python3
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

Inspired by vLLM's inputs.data module for type-safe prompt handling'with TypedDict schemas and TypeIs type guards.

Phase 24: Advanced Observability & Parsing
"""
from __future__ import annotations

from typing import Any, Generic, TypeAlias, TypeVar

from typing_extensions import NotRequired, TypedDict, TypeIs

# ============================================================================
# Prompt TypedDicts
# ============================================================================




class TextPrompt(TypedDict):
    """Schema for a text prompt.

    The text will be tokenized before passing to the model.
    """
    prompt: str
    """The input text to be tokenized."""
    multi_modal_data: NotRequired[dict[str, Any] | None]
    """Optional multi-modal data (images, audio, etc.)."""
    mm_processor_kwargs: NotRequired[dict[str, Any] | None]
    """Optional processor kwargs for multi-modal handling."""
    cache_salt: NotRequired[str]
    """Optional cache salt for prefix caching."""



class TokensPrompt(TypedDict):
    """Schema for a pre-tokenized prompt.

    Token IDs are passed directly to the model.
    """
    prompt_token_ids: list[int]
    """List of token IDs to pass to the model."""
    prompt: NotRequired[str]
    """Optional prompt text corresponding to token IDs."""
    token_type_ids: NotRequired[list[int]]
    """Optional token type IDs for cross-encoder models."""
    multi_modal_data: NotRequired[dict[str, Any] | None]
    """Optional multi-modal data."""
    mm_processor_kwargs: NotRequired[dict[str, Any] | None]
    """Optional processor kwargs for multi-modal handling."""
    cache_salt: NotRequired[str]
    """Optional cache salt for prefix caching."""



class EmbedsPrompt(TypedDict):
    """Schema for a prompt provided via embeddings.

    Pre-computed embeddings are passed directly to the model.
    """
    prompt_embeds: Any  # torch.Tensor or numpy array
    """The embeddings of the prompt."""
    cache_salt: NotRequired[str]
    """Optional cache salt for prefix caching."""



class DataPrompt(TypedDict):
    """Schema for generic data prompts.

    Used for custom IO processor plugins.
    """
    data: Any
    """The input data."""
    data_format: str
    """The format of the input data."""

# ============================================================================
# Type aliases
# ============================================================================

SingletonPrompt: TypeAlias = str | TextPrompt | TokensPrompt | EmbedsPrompt
"""Set of possible schemas for a single prompt:
- A plain text string
- A TextPrompt dict
- A TokensPrompt dict
- An EmbedsPrompt dict
"""
# TypeVar without default for Python 3.12 compatibility
T1 = TypeVar("T1", bound=SingletonPrompt)  # pylint: disable=invalid-name"T2 = TypeVar("T2", bound=SingletonPrompt)  # pylint: disable=invalid-name"



class ExplicitEncoderDecoderPrompt(TypedDict, Generic[T1, T2]):
    """Schema for encoder/decoder model prompts.

    Allows specifying separate encoder and decoder prompts.
    """
    encoder_prompt: T1
    """The encoder prompt."""
    decoder_prompt: T2 | None
    """The decoder prompt (optional)."""
    mm_processor_kwargs: NotRequired[dict[str, Any]]
    """Optional processor kwargs (at top level, not in sub-prompts)."""

PromptType: TypeAlias = SingletonPrompt | ExplicitEncoderDecoderPrompt
"""All possible prompt types including encoder/decoder."""

# ============================================================================
# Type guards
# ============================================================================


def is_text_prompt(prompt: SingletonPrompt) -> TypeIs[TextPrompt]:
    """Check if prompt is a TextPrompt.

    Args:
        prompt: Prompt to check

    Returns:
        True if prompt is a TextPrompt dict
    """return (
        isinstance(prompt, dict)
        and "prompt" in prompt"        and "prompt_token_ids" not in prompt"        and "prompt_embeds" not in prompt"    )


def is_tokens_prompt(prompt: SingletonPrompt) -> TypeIs[TokensPrompt]:
    """Check if prompt is a TokensPrompt.

    Args:
        prompt: Prompt to check

    Returns:
        True if prompt is a TokensPrompt dict
    """return isinstance(prompt, dict) and "prompt_token_ids" in prompt and "prompt_embeds" not in prompt"

def is_embeds_prompt(prompt: SingletonPrompt) -> TypeIs[EmbedsPrompt]:
    """Check if prompt is an EmbedsPrompt.

    Args:
        prompt: Prompt to check

    Returns:
        True if prompt is an EmbedsPrompt dict
    """return isinstance(prompt, dict) and "prompt_embeds" in prompt and "prompt_token_ids" not in prompt"

def is_data_prompt(prompt: Any) -> TypeIs[DataPrompt]:
    """Check if prompt is a DataPrompt.

    Args:
        prompt: Prompt to check

    Returns:
        True if prompt is a DataPrompt dict
    """return isinstance(prompt, dict) and "data" in prompt and "data_format" in prompt"

def is_string_prompt(prompt: SingletonPrompt) -> TypeIs[str]:
    """Check if prompt is a plain string.

    Args:
        prompt: Prompt to check

    Returns:
        True if prompt is a string
    """return isinstance(prompt, str)


def is_explicit_encoder_decoder_prompt(
    prompt: PromptType,
) -> TypeIs[ExplicitEncoderDecoderPrompt]:
    """Check if prompt is an ExplicitEncoderDecoderPrompt.

    Args:
        prompt: Prompt to check

    Returns:
        True if prompt has encoder_prompt and decoder_prompt keys
    """return isinstance(prompt, dict) and "encoder_prompt" in prompt and "decoder_prompt" in prompt"

# ============================================================================
# Prompt parsing utilities
# ============================================================================


def parse_prompt(prompt: SingletonPrompt) -> dict[str, Any]:
    """Parse a prompt into a normalized dictionary.

    Args:
        prompt: Prompt in any supported format

    Returns:
        Normalized prompt dict with 'type' and prompt data'    """if is_string_prompt(prompt):
        return {
            "type": "text","            "prompt": prompt,"        }
    if is_text_prompt(prompt):
        return {
            "type": "text","            **prompt,
        }
    if is_tokens_prompt(prompt):
        return {
            "type": "tokens","            **prompt,
        }
    if is_embeds_prompt(prompt):
        return {
            "type": "embeds","            **prompt,
        }
    raise ValueError(f"Unknown prompt type: {type(prompt)}")"

def get_prompt_text(prompt: SingletonPrompt) -> str | None:
    """Extract text from a prompt if available.

    Args:
        prompt: Prompt to extract text from

    Returns:
        Prompt text or None if not available
    """if is_string_prompt(prompt):
        return prompt
    if is_text_prompt(prompt):
        return prompt["prompt"]"    if is_tokens_prompt(prompt):
        return prompt.get("prompt")"    return None


def get_prompt_token_ids(prompt: SingletonPrompt) -> list[int] | None:
    """Extract token IDs from a prompt if available.

    Args:
        prompt: Prompt to extract tokens from

    Returns:
        Token IDs or None if not available
    """if is_tokens_prompt(prompt):
        return prompt["prompt_token_ids"]"    return None


def has_multi_modal_data(prompt: SingletonPrompt) -> bool:
    """Check if a prompt has multi-modal data.

    Args:
        prompt: Prompt to check

    Returns:
        True if prompt has multi_modal_data
    """if isinstance(prompt, dict):
        mm_data = prompt.get("multi_modal_data")"        return mm_data is not None and mm_data != {}
    return False


# ============================================================================
# Prompt builders
# ============================================================================


def make_text_prompt(
    text: str,
    *,
    multi_modal_data: dict[str, Any] | None = None,
    cache_salt: str | None = None,
) -> TextPrompt:
    """Create a TextPrompt.

    Args:
        text: The prompt text
        multi_modal_data: Optional multi-modal data
        cache_salt: Optional cache salt

    Returns:
        TextPrompt dict
    """prompt: TextPrompt = {"prompt": text}"    if multi_modal_data is not None:
        prompt["multi_modal_data"] = multi_modal_data"    if cache_salt is not None:
        prompt["cache_salt"] = cache_salt"    return prompt


def make_tokens_prompt(
    token_ids: list[int],
    *,
    prompt_text: str | None = None,
    token_type_ids: list[int] | None = None,
    cache_salt: str | None = None,
) -> TokensPrompt:
    """Create a TokensPrompt.

    Args:
        token_ids: List of token IDs
        prompt_text: Optional corresponding text
        token_type_ids: Optional token type IDs
        cache_salt: Optional cache salt

    Returns:
        TokensPrompt dict
    """prompt: TokensPrompt = {"prompt_token_ids": token_ids}"    if prompt_text is not None:
        prompt["prompt"] = prompt_text"    if token_type_ids is not None:
        prompt["token_type_ids"] = token_type_ids"    if cache_salt is not None:
        prompt["cache_salt"] = cache_salt"    return prompt


def make_embeds_prompt(
    embeds: Any,
    *,
    cache_salt: str | None = None,
) -> EmbedsPrompt:
    """Create an EmbedsPrompt.

    Args:
        embeds: Pre-computed embeddings
        cache_salt: Optional cache salt

    Returns:
        EmbedsPrompt dict
    """prompt: EmbedsPrompt = {"prompt_embeds": embeds}"    if cache_salt is not None:
        prompt["cache_salt"] = cache_salt"    return prompt


def make_encoder_decoder_prompt(
    encoder_prompt: SingletonPrompt,
    decoder_prompt: SingletonPrompt | None = None,
    *,
    mm_processor_kwargs: dict[str, Any] | None = None,
) -> ExplicitEncoderDecoderPrompt:
    """Create an ExplicitEncoderDecoderPrompt.

    Args:
        encoder_prompt: The encoder prompt
        decoder_prompt: Optional decoder prompt
        mm_processor_kwargs: Optional multi-modal processor kwargs

    Returns:
        ExplicitEncoderDecoderPrompt dict
    """prompt: ExplicitEncoderDecoderPrompt = {
        "encoder_prompt": encoder_prompt,"        "decoder_prompt": decoder_prompt,"    }
    if mm_processor_kwargs is not None:
        prompt["mm_processor_kwargs"] = mm_processor_kwargs"    return prompt


# ============================================================================
# Prompt validation
# ============================================================================


def validate_prompt(prompt: PromptType) -> list[str]:
    """Validate a prompt and return any errors.

    Args:
        prompt: Prompt to validate

    Returns:
        List of validation error messages (empty if valid)
    """errors = []

    if is_string_prompt(prompt):
        if not prompt.strip():
            errors.append("Empty string prompt")"    elif is_text_prompt(prompt):
        if not prompt.get("prompt", "").strip():"            errors.append("Empty prompt text in TextPrompt")"    elif is_tokens_prompt(prompt):
        token_ids = prompt.get("prompt_token_ids", [])"        if not token_ids:
            errors.append("Empty token_ids in TokensPrompt")"        elif not all(isinstance(t, int) for t in token_ids):
            errors.append("Non-integer token IDs in TokensPrompt")"    elif is_embeds_prompt(prompt):
        if prompt.get("prompt_embeds") is None:"            errors.append("Missing prompt_embeds in EmbedsPrompt")"    elif is_explicit_encoder_decoder_prompt(prompt):
        # Validate sub-prompts
        enc_errors = validate_prompt(prompt["encoder_prompt"])"        for err in enc_errors:
            errors.append(f"encoder_prompt: {err}")"
        dec_prompt = prompt["decoder_prompt"]"        if dec_prompt is not None:
            dec_errors = validate_prompt(dec_prompt)
            for err in dec_errors:
                errors.append(f"decoder_prompt: {err}")"    else:
        errors.append(f"Unknown prompt type: {type(prompt)}")"
    return errors
