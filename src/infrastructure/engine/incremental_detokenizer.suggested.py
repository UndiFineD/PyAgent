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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
IncrementalDetokenizer - Fast streaming token-to-text conversion.

Inspired by vLLM's v1/engine/detokenizer.py - provides fast and slow paths
for incremental detokenization with stop string detection.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

logger: logging.Logger = logging.getLogger(__name__)

# Constants
INITIAL_INCREMENTAL_DETOKENIZATION_OFFSET: int = 5
INVALID_PREFIX_ERR_MSG: str = "Invalid prefix encountered"


@dataclass
class StopMatch:
    """Result of stop string matching."""

    stop_string: str
    truncate_to: int  # -1 means no truncation


def check_stop_strings(
    output_text: str,
    new_char_count: int,
    stop: list[str],
    include_in_output: bool,
) -> tuple[str, int] | None:
    """
    Check if any stop strings appear in the output text.

    Args:
        output_text: The current output text
        new_char_count: Number of new characters added
        stop: List of stop strings to check
        include_in_output: Whether to include stop string in output

    Returns:
        Tuple of (matched stop string, truncation index) or None
    """
    if not stop or not output_text:
        return None

    # Check from where new characters start
    check_start = max(0, len(output_text) - new_char_count - max(len(s) for s in stop))
    check_text = output_text[check_start:]

    for stop_str in stop:
        pos = check_text.find(stop_str)
        if pos >= 0:
            # Found a stop string
            absolute_pos = check_start + pos
            if include_in_output:
                truncate_to = absolute_pos + len(stop_str)
            else:
                truncate_to = absolute_pos
            return (stop_str, truncate_to)

    return None


def check_stop_strings_rust(
    output_text: str,
    new_char_count: int,
    stop: list[str],
    include_in_output: bool,
) -> tuple[str, int] | None:
    """
    Rust-accelerated stop string checking.
    Falls back to Python implementation.
    """
    try:
        from rust_core import check_stop_strings_rust as _rust_impl

        return _rust_impl(output_text, new_char_count, stop, include_in_output)
    except ImportError:
        return check_stop_strings(output_text, new_char_count, stop, include_in_output)


class IncrementalDetokenizer(ABC):
    """
    Base class for incremental detokenization.

    Converts token IDs to text incrementally, handling special tokens
    and stop strings efficiently.
    """

    def __init__(self) -> None:
        self.token_ids: list[int] = []
        self.output_text: str = ""
        self._last_output_text_offset: int = 0

    @property
    def output_token_ids(self) -> list[int]:
        """Get output token IDs (excluding prompt)."""
        return self.token_ids

    def update(self, new_token_ids: list[int], _stop_terminated: bool) -> str | None:
        """
        Update with new token IDs.

        Args:
            new_token_ids: New token IDs to process
            _stop_terminated: Whether stop condition was hit

        Returns:
            Matched stop string if found, None otherwise
        """
        self.token_ids.extend(new_token_ids)

    def get_next_output_text(self, _finished: bool, _delta: bool) -> str:
        """
        Get output text.

        Args:
            _finished: Whether generation is finished
            _delta: If True, return only new text since last call

        Returns:
            Output text (full or delta)
        """
        return ""

    @classmethod
    def from_new_request(
        cls,
        tokenizer: Any,
        request: Any,
    ) -> "IncrementalDetokenizer":
        """Create detokenizer from a request."""
        if tokenizer is None:
            return NoOpDetokenizer()

        # Try fast path first
        try:
            from transformers import PreTrainedTokenizerFast

            if isinstance(tokenizer, PreTrainedTokenizerFast):
                return FastIncrementalDetokenizer(tokenizer, request)
        except ImportError:
            pass

        # Fall back to slow path
        return SlowIncrementalDetokenizer(tokenizer, request)


class NoOpDetokenizer(IncrementalDetokenizer):
    """No-op detokenizer when tokenizer is not available."""

    def update(self, new_token_ids: list[int], _stop_terminated: bool) -> str | None:
        self.token_ids.extend(new_token_ids)
        return None

    def get_next_output_text(self, _finished: bool, _delta: bool) -> str:
        return ""


class BaseIncrementalDetokenizer(IncrementalDetokenizer, ABC):
    """
    Base class with common functionality for incremental detokenizers.
    """

    def __init__(self, request: Any) -> None:
        super().__init__()

        # Extract sampling params
        sampling_params: dict[str, Any] = getattr(request, "sampling_params", None) or {}
        if hasattr(sampling_params, "__dict__"):
            sampling_params = sampling_params.__dict__
        elif not isinstance(sampling_params, dict):
            sampling_params = {}

        self.request_id = getattr(request, "request_id", "unknown")
        self.stop: list[str] = sampling_params.get("stop", []) or []
        self.include_stop_str_in_output: bool = sampling_params.get("include_stop_str_in_output", False)
        self.skip_special_tokens: bool = sampling_params.get("skip_special_tokens", True)
        self.min_tokens: int = sampling_params.get("min_tokens", 0)

        # Stop buffer - keep last N chars to check for stop strings spanning tokens
        self.stop_buffer_length: int = max((len(s) for s in self.stop), default=0)

    def update(self, new_token_ids: list[int], stop_terminated: bool) -> str | None:
        """Update with new tokens and check for stop strings."""
        if not new_token_ids:
            return None

        processed_tokens = self._prepare_tokens_for_detokenization(new_token_ids, stop_terminated)
        stop_check_offset = self._detokenize_tokens(processed_tokens)

        if stop_terminated and not self.include_stop_str_in_output:
            # Add back the skipped token to token_ids but not to output
            self.token_ids.append(new_token_ids[-1])

        return self._check_for_stop_strings(stop_check_offset)

    def _prepare_tokens_for_detokenization(self, new_token_ids: list[int], stop_terminated: bool) -> list[int]:
        """Prepare tokens for detokenization, handling stop termination."""
        if stop_terminated and not self.include_stop_str_in_output:
            # Skip last token from detokenization
            return new_token_ids[:-1]
        return new_token_ids

    def _detokenize_tokens(self, token_ids: list[int]) -> int:
        """Detokenize the given tokens and return stop check offset."""
        stop_check_offset = len(self.output_text)
        for token_id in token_ids:
            self.token_ids.append(token_id)
            self.output_text += self.decode_next(token_id)

            # Skip stop check for min_tokens
            if self.min_tokens and len(self.output_token_ids) <= self.min_tokens:
                stop_check_offset = len(self.output_text)
        return stop_check_offset

    def _check_for_stop_strings(self, stop_check_offset: int) -> str | None:
        """Check for stop strings and truncate output if needed."""
        if not self.stop or len(self.output_token_ids) <= self.min_tokens:
            return None

        result = check_stop_strings_rust(
            output_text=self.output_text,
            new_char_count=len(self.output_text) - stop_check_offset,
            stop=self.stop,
            include_in_output=self.include_stop_str_in_output,
        )
        if result is not None:
            stop_string, truncate_to = result
            if truncate_to != -1:
                self.output_text = self.output_text[:truncate_to]
            return stop_string
        return None

    @abstractmethod
    def decode_next(self, next_token_id: int) -> str:
        """Decode a single token to text."""
        raise NotImplementedError

    def get_next_output_text(self, finished: bool, delta: bool) -> str:
        """Get output text with optional buffering."""
        buffer_length = 0 if finished else self.stop_buffer_length

        if not delta:
            if buffer_length:
                return self.output_text[:-buffer_length]
            return self.output_text

        # Delta mode
        length = len(self.output_text) - buffer_length
        last_offset = self._last_output_text_offset

        if last_offset < length:
            self._last_output_text_offset = length
            return self.output_text[last_offset:length]

        return ""


class FastIncrementalDetokenizer(BaseIncrementalDetokenizer):
    """
    Fast incremental detokenizer using tokenizers library's DecodeStream.

    Requires tokenizers >= 0.21.1 for DecodeStream support.
    """

    def __init__(self, tokenizer: Any, request: Any) -> None:
        super().__init__(request)

        self.tokenizer_wrapper = tokenizer

        # Get inner tokenizer
        self.tokenizer = getattr(tokenizer, "_tokenizer", tokenizer)

        # Initialize decode stream (mock for now since DecodeStream may not be available)
        self._decode_buffer: list[int] = []
        self._last_decoded: str = ""

        # Handle spaces between special tokens
        sampling_params = getattr(request, "sampling_params", None) or {}
        if hasattr(sampling_params, "__dict__"):
            sampling_params = sampling_params.__dict__
        elif not isinstance(sampling_params, dict):
            sampling_params = {}

        self.spaces_between_special_tokens = self.skip_special_tokens or sampling_params.get(
            "spaces_between_special_tokens", True
        )

        # Track added tokens for special handling
        self.added_token_ids: dict[int, str] = {}
        self.last_special: bool = False

        if hasattr(tokenizer, "get_added_tokens_decoder"):
            try:
                for tid, tok in tokenizer.get_added_tokens_decoder().items():
                    content = getattr(tok, "content", str(tok))
                    self.added_token_ids[tid] = content
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        # Prime with prompt tokens
        prompt_token_ids = getattr(request, "prompt_token_ids", None) or []
        if prompt_token_ids:
            # Take suffix for priming
            prompt_suffix = prompt_token_ids[-min(24, len(prompt_token_ids)) :]
            for tid in prompt_suffix:
                self._protected_step(tid)

    def _protected_step(self, next_token_id: int) -> str | None:
        """Decode one token with error protection."""
        try:
            self._decode_buffer.append(next_token_id)
            decoded: str = self._execute_decode()

            # Get new text
            if len(decoded) > len(self._last_decoded):
                new_text: str = decoded[len(self._last_decoded) :]
                self._last_decoded = decoded
                return new_text

            return ""

        except (OverflowError, TypeError) as e:
            logger.warning("Invalid token id %s: %s", next_token_id, e)
            return None
        except Exception as e:
            return self._handle_decode_exception(e, next_token_id)

    def _execute_decode(self) -> str:
        """Call the appropriate decode method on the tokenizer."""
        if hasattr(self.tokenizer, "decode"):
            return self.tokenizer.decode(
                self._decode_buffer,
                skip_special_tokens=self.skip_special_tokens,
            )
        if hasattr(self.tokenizer_wrapper, "decode"):
            return self.tokenizer_wrapper.decode(
                self._decode_buffer,
                skip_special_tokens=self.skip_special_tokens,
            )
        return ""

    def _handle_decode_exception(self, e: Exception, next_token_id: int) -> str | None:
        """Handle exceptions during the decode process."""
        if str(e).startswith(INVALID_PREFIX_ERR_MSG):
            logger.warning("Invalid prefix in request %s, resetting", self.request_id)
            # Reset decode state
            self._decode_buffer = [next_token_id]
            self._last_decoded = ""
            return None
        raise e

    def decode_next(self, next_token_id: int) -> str:
        """Decode the next token."""
        token = self._protected_step(next_token_id)

        if not self.spaces_between_special_tokens:
            special_token = self.added_token_ids.get(next_token_id)
            is_special = special_token is not None

            if is_special and self.last_special:
                # Return raw token without prefix spaces
                token = special_token

            self.last_special = is_special

        return token or ""


class SlowIncrementalDetokenizer(BaseIncrementalDetokenizer):
    """
    Slow incremental detokenizer using Python-based approach.

    Compatible with all tokenizers but slower than FastIncrementalDetokenizer.
    """

    def __init__(self, tokenizer: Any, request: Any) -> None:
        super().__init__(request)

        self.tokenizer = tokenizer

        # Get prompt info
        prompt_token_ids = getattr(request, "prompt_token_ids", None) or []
        self.prompt_len = len(prompt_token_ids)

        # Initialize tokens list with prompt
        if prompt_token_ids:
            try:
                self.tokens = tokenizer.convert_ids_to_tokens(
                    prompt_token_ids[-INITIAL_INCREMENTAL_DETOKENIZATION_OFFSET - 2 :],
                    skip_special_tokens=self.skip_special_tokens,
                )
            except Exception:  # pylint: disable=broad-exception-caught
                self.tokens = [""] * min(INITIAL_INCREMENTAL_DETOKENIZATION_OFFSET + 2, len(prompt_token_ids))
        else:
            self.tokens = []

        self.read_offset = len(self.tokens)
        self.prefix_offset = max(self.read_offset - INITIAL_INCREMENTAL_DETOKENIZATION_OFFSET, 0)

        # Copy prompt IDs to token_ids
        self.token_ids = list(prompt_token_ids)

        # Sampling params for spaces handling
        sampling_params = getattr(request, "sampling_params", None) or {}
        if hasattr(sampling_params, "__dict__"):
            sampling_params = sampling_params.__dict__
        elif not isinstance(sampling_params, dict):
            sampling_params = {}

        self.spaces_between_special_tokens = sampling_params.get("spaces_between_special_tokens", True)

    @property
    def output_token_ids(self) -> list[int]:
        """Get output token IDs (excluding prompt)."""
        return self.token_ids[self.prompt_len :] if self.prompt_len else self.token_ids

    def decode_next(self, next_token_id: int) -> str:
        """Decode next token using incremental approach."""
        # 1. Get new tokens from ID
        new_tokens: list[str] = self._get_tokens_for_id(next_token_id)
        self.tokens.extend(new_tokens)
        output_tokens = self.tokens

        # 2. Convert tokens to string and handle prefix
        # Get prefix and new text
        try:
            prefix_text: str = self.tokenizer.convert_tokens_to_string(
                output_tokens[self.prefix_offset : self.read_offset]
            )
            new_text: str = self.tokenizer.convert_tokens_to_string(output_tokens[self.prefix_offset :])
        except Exception:  # pylint: disable=broad-exception-caught
            return ""

        # 3. Validation and offset update
        if self._is_incomplete_text(new_text, prefix_text):
            return ""

        self.prefix_offset = self.read_offset
        self.read_offset = len(output_tokens)

        return new_text[len(prefix_text) :]

    def _get_tokens_for_id(self, token_id: int) -> list[str]:
        """Convert a single token ID to a list of token strings."""
        try:
            new_tokens: list[str] = self.tokenizer.convert_ids_to_tokens(
                [token_id],
                skip_special_tokens=self.skip_special_tokens,
            )
            if isinstance(new_tokens, str):
                new_tokens = [new_tokens]
        except Exception:  # pylint: disable=broad-exception-caught
            new_tokens = [""]

        # Ensure no None values in results
        return [t if t is not None else "" for t in new_tokens]

    def _is_incomplete_text(self, new_text: str, prefix_text: str) -> bool:
        """Check if newly decoded text is incomplete (e.g. partial UTF-8)."""
        return len(new_text) <= len(prefix_text) or new_text.endswith("")


def validate_utf8(text: str) -> bool:
    """Validate that text is valid UTF-8."""
    try:
        text.encode("utf-8").decode("utf-8")
        return True
    except UnicodeError:
        return False


def validate_utf8_rust(text: str) -> bool:
    """Rust-accelerated UTF-8 validation."""
    try:
        from rust_core import validate_utf8_rust as _rust_impl

        return _rust_impl(text)
    except (ImportError, AttributeError):
        return validate_utf8(text)


__all__ = [
    "StopMatch",
    "check_stop_strings",
    "check_stop_strings_rust",
    "IncrementalDetokenizer",
    "NoOpDetokenizer",
    "BaseIncrementalDetokenizer",
    "FastIncrementalDetokenizer",
    "SlowIncrementalDetokenizer",
    "validate_utf8",
    "validate_utf8_rust",
    "INITIAL_INCREMENTAL_DETOKENIZATION_OFFSET",
]
