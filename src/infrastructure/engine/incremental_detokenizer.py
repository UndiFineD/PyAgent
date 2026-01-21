"""
IncrementalDetokenizer - Fast streaming token-to-text conversion.

Inspired by vLLM's v1/engine/detokenizer.py - provides fast and slow paths
for incremental detokenization with stop string detection.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import logging

logger = logging.getLogger(__name__)

# Constants
INITIAL_INCREMENTAL_DETOKENIZATION_OFFSET = 5
INVALID_PREFIX_ERR_MSG = "Invalid prefix encountered"


@dataclass
class StopMatch:
    """Result of stop string matching."""
    stop_string: str
    truncate_to: int  # -1 means no truncation


def check_stop_strings(
    output_text: str,
    new_char_count: int,
    stop: List[str],
    include_in_output: bool,
) -> Optional[Tuple[str, int]]:
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
    stop: List[str],
    include_in_output: bool,
) -> Optional[Tuple[str, int]]:
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

    def __init__(self):
        self.token_ids: List[int] = []
        self.output_text: str = ""
        self._last_output_text_offset: int = 0

    @property
    def output_token_ids(self) -> List[int]:
        """Get output token IDs (excluding prompt)."""
        return self.token_ids

    def update(self, new_token_ids: List[int], stop_terminated: bool) -> Optional[str]:
        """
        Update with new token IDs.

        Args:
            new_token_ids: New token IDs to process
            stop_terminated: Whether stop condition was hit

        Returns:
            Matched stop string if found, None otherwise
        """
        self.token_ids.extend(new_token_ids)
        return None

    def get_next_output_text(self, finished: bool, delta: bool) -> str:
        """
        Get output text.

        Args:
            finished: Whether generation is finished
            delta: If True, return only new text since last call

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

    def update(self, new_token_ids: List[int], stop_terminated: bool) -> Optional[str]:
        self.token_ids.extend(new_token_ids)
        return None

    def get_next_output_text(self, finished: bool, delta: bool) -> str:
        return ""


class BaseIncrementalDetokenizer(IncrementalDetokenizer, ABC):
    """
    Base class with common functionality for incremental detokenizers.
    """

    def __init__(self, request: Any):
        super().__init__()

        # Extract sampling params
        sampling_params = getattr(request, 'sampling_params', None) or {}
        if hasattr(sampling_params, '__dict__'):
            sampling_params = sampling_params.__dict__
        elif not isinstance(sampling_params, dict):
            sampling_params = {}

        self.request_id = getattr(request, 'request_id', 'unknown')
        self.stop: List[str] = sampling_params.get('stop', []) or []
        self.include_stop_str_in_output: bool = sampling_params.get('include_stop_str_in_output', False)
        self.skip_special_tokens: bool = sampling_params.get('skip_special_tokens', True)
        self.min_tokens: int = sampling_params.get('min_tokens', 0)

        # Stop buffer - keep last N chars to check for stop strings spanning tokens
        self.stop_buffer_length: int = max((len(s) for s in self.stop), default=0)

    def update(self, new_token_ids: List[int], stop_terminated: bool) -> Optional[str]:
        """Update with new tokens and check for stop strings."""
        if not new_token_ids:
            return None

        skipped_stop_token_id = None
        if stop_terminated and not self.include_stop_str_in_output:
            # Skip last token from detokenization
            skipped_stop_token_id = new_token_ids[-1]
            new_token_ids = new_token_ids[:-1]

        # Detokenize
        stop_check_offset = len(self.output_text)
        for token_id in new_token_ids:
            self.token_ids.append(token_id)
            self.output_text += self.decode_next(token_id)

            # Skip stop check for min_tokens
            if self.min_tokens and len(self.output_token_ids) <= self.min_tokens:
                stop_check_offset = len(self.output_text)

        if skipped_stop_token_id is not None:
            self.token_ids.append(skipped_stop_token_id)

        # Check stop strings
        stop_string = None
        if self.stop and len(self.output_token_ids) > self.min_tokens:
            result = check_stop_strings(
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

    def __init__(self, tokenizer: Any, request: Any):
        super().__init__(request)

        self.tokenizer_wrapper = tokenizer

        # Get inner tokenizer
        self.tokenizer = getattr(tokenizer, '_tokenizer', tokenizer)

        # Initialize decode stream (mock for now since DecodeStream may not be available)
        self._decode_buffer: List[int] = []
        self._last_decoded: str = ""

        # Handle spaces between special tokens
        sampling_params = getattr(request, 'sampling_params', None) or {}
        if hasattr(sampling_params, '__dict__'):
            sampling_params = sampling_params.__dict__
        elif not isinstance(sampling_params, dict):
            sampling_params = {}

        self.spaces_between_special_tokens = (
            self.skip_special_tokens or
            sampling_params.get('spaces_between_special_tokens', True)
        )

        # Track added tokens for special handling
        self.added_token_ids: Dict[int, str] = {}
        self.last_special: bool = False

        if hasattr(tokenizer, 'get_added_tokens_decoder'):
            try:
                for tid, tok in tokenizer.get_added_tokens_decoder().items():
                    content = getattr(tok, 'content', str(tok))
                    self.added_token_ids[tid] = content
            except Exception:
                pass

        # Prime with prompt tokens
        prompt_token_ids = getattr(request, 'prompt_token_ids', None) or []
        if prompt_token_ids:
            # Take suffix for priming
            prompt_suffix = prompt_token_ids[-min(24, len(prompt_token_ids)):]
            for tid in prompt_suffix:
                self._protected_step(tid)

    def _protected_step(self, next_token_id: int) -> Optional[str]:
        """Decode one token with error protection."""
        try:
            self._decode_buffer.append(next_token_id)

            # Decode current buffer
            if hasattr(self.tokenizer, 'decode'):
                decoded = self.tokenizer.decode(
                    self._decode_buffer,
                    skip_special_tokens=self.skip_special_tokens,
                )
            elif hasattr(self.tokenizer_wrapper, 'decode'):
                decoded = self.tokenizer_wrapper.decode(
                    self._decode_buffer,
                    skip_special_tokens=self.skip_special_tokens,
                )
            else:
                decoded = ""

            # Get new text
            if len(decoded) > len(self._last_decoded):
                new_text = decoded[len(self._last_decoded):]
                self._last_decoded = decoded
                return new_text

            return ""

        except (OverflowError, TypeError) as e:
            logger.warning(f"Invalid token id {next_token_id}: {e}")
            return None
        except Exception as e:
            if str(e).startswith(INVALID_PREFIX_ERR_MSG):
                logger.warning(f"Invalid prefix in request {self.request_id}, resetting")
                # Reset decode state
                self._decode_buffer = [next_token_id]
                self._last_decoded = ""
                return None
            raise

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

    def __init__(self, tokenizer: Any, request: Any):
        super().__init__(request)

        self.tokenizer = tokenizer

        # Get prompt info
        prompt_token_ids = getattr(request, 'prompt_token_ids', None) or []
        self.prompt_len = len(prompt_token_ids)

        # Initialize tokens list with prompt
        if prompt_token_ids:
            try:
                self.tokens = tokenizer.convert_ids_to_tokens(
                    prompt_token_ids[-INITIAL_INCREMENTAL_DETOKENIZATION_OFFSET - 2:],
                    skip_special_tokens=self.skip_special_tokens,
                )
            except Exception:
                self.tokens = [""] * min(INITIAL_INCREMENTAL_DETOKENIZATION_OFFSET + 2, len(prompt_token_ids))
        else:
            self.tokens = []

        self.read_offset = len(self.tokens)
        self.prefix_offset = max(self.read_offset - INITIAL_INCREMENTAL_DETOKENIZATION_OFFSET, 0)

        # Copy prompt IDs to token_ids
        self.token_ids = list(prompt_token_ids)

        # Sampling params for spaces handling
        sampling_params = getattr(request, 'sampling_params', None) or {}
        if hasattr(sampling_params, '__dict__'):
            sampling_params = sampling_params.__dict__
        elif not isinstance(sampling_params, dict):
            sampling_params = {}

        self.spaces_between_special_tokens = sampling_params.get('spaces_between_special_tokens', True)

    @property
    def output_token_ids(self) -> List[int]:
        """Get output token IDs (excluding prompt)."""
        return self.token_ids[self.prompt_len:] if self.prompt_len else self.token_ids

    def decode_next(self, next_token_id: int) -> str:
        """Decode next token using incremental approach."""
        # Get new token
        try:
            new_tokens = self.tokenizer.convert_ids_to_tokens(
                [next_token_id],
                skip_special_tokens=self.skip_special_tokens,
            )
            if isinstance(new_tokens, str):
                new_tokens = [new_tokens]
        except Exception:
            new_tokens = [""]

        # Handle None tokens
        new_tokens = [t if t is not None else "" for t in new_tokens]

        # Add to tokens list
        self.tokens.extend(new_tokens)
        output_tokens = self.tokens

        # Get prefix and new text
        try:
            prefix_text = self.tokenizer.convert_tokens_to_string(
                output_tokens[self.prefix_offset:self.read_offset]
            )
            new_text = self.tokenizer.convert_tokens_to_string(
                output_tokens[self.prefix_offset:]
            )
        except Exception:
            return ""

        # Check for incomplete UTF-8
        if len(new_text) <= len(prefix_text) or new_text.endswith("�"):
            return ""

        # Update offsets
        self.prefix_offset = self.read_offset
        self.read_offset = len(output_tokens)

        return new_text[len(prefix_text):]


def validate_utf8(text: str) -> bool:
    """Validate that text is valid UTF-8."""
    try:
        text.encode('utf-8').decode('utf-8')
        return True
    except UnicodeError:
        return False


def validate_utf8_rust(text: str) -> bool:
    """Rust-accelerated UTF-8 validation."""
    try:
        from rust_core import validate_utf8_rust as _rust_impl
        return _rust_impl(text)
    except ImportError:
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
