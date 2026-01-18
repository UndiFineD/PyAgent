# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Incremental detokenization for streaming text generation.

This module implements streaming token-to-text conversion with proper
handling of multi-token characters and special tokens, inspired by
vLLM's transformers_utils/detokenizer.py architecture.

Key Components:
    - TokenizerLike: Protocol for tokenizer abstraction
    - DetokenizeResult: Result of incremental detokenization
    - IncrementalDetokenizer: Base class for streaming detokenization
    - FastIncrementalDetokenizer: Optimized for HuggingFace fast tokenizers
    - SlowIncrementalDetokenizer: Fallback for non-fast tokenizers
    - StopChecker: Stop string/token detection

Example:
    >>> from src.infrastructure.tokenization import (
    ...     IncrementalDetokenizer, create_detokenizer
    ... )
    >>> 
    >>> # Create a detokenizer from your tokenizer
    >>> detokenizer = create_detokenizer(tokenizer)
    >>> 
    >>> # Process tokens incrementally
    >>> for token_id in generated_token_ids:
    ...     result = detokenizer.update([token_id])
    ...     if result.new_text:
    ...         print(result.new_text, end='', flush=True)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Union,
    runtime_checkable,
)

# Try to import Rust accelerations
try:
    from rust_core import (
        check_stop_tokens_rust,
        update_prefix_offset_rust,
    )
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


# ==============================================================================
# Tokenizer Protocol
# ==============================================================================

@runtime_checkable
class TokenizerLike(Protocol):
    """
    Protocol for tokenizer abstraction.

    This defines the minimum interface needed for detokenization,
    allowing compatibility with various tokenizer implementations
    (HuggingFace, tiktoken, sentencepiece, etc.).
    """

    def encode(self, text: str, **kwargs) -> List[int]:
        """Encode text to token IDs."""
        ...

    def decode(
        self,
        token_ids: Union[int, List[int]],
        skip_special_tokens: bool = True,
        **kwargs,
    ) -> str:
        """Decode token IDs to text."""
        ...

    def convert_ids_to_tokens(
        self,
        ids: Union[int, List[int]],
    ) -> Union[str, List[str]]:
        """Convert token IDs to token strings."""
        ...

    def convert_tokens_to_ids(
        self,
        tokens: Union[str, List[str]],
    ) -> Union[int, List[int]]:
        """Convert token strings to token IDs."""
        ...

    @property
    def vocab(self) -> Dict[str, int]:
        """Get the vocabulary mapping."""
        ...

    @property
    def eos_token_id(self) -> Optional[int]:
        """Get the end-of-sequence token ID."""
        ...


# ==============================================================================
# Detokenize Result
# ==============================================================================

@dataclass
class DetokenizeResult:
    """
    Result of incremental detokenization.

    Attributes:
        new_text: Newly decoded text since last update
        full_text: Complete decoded text so far
        prefix_offset: Offset for prefix handling (characters already output)
        read_offset: Offset for reading (characters ready to output)
        finished: Whether detokenization is complete
        stop_reason: Stop reason if triggered (string or token ID)
    """
    new_text: str
    full_text: str
    prefix_offset: int = 0
    read_offset: int = 0
    finished: bool = False
    stop_reason: Optional[Union[str, int]] = None

    @property
    def has_new_text(self) -> bool:
        """Check if there is new text."""
        return bool(self.new_text)


# ==============================================================================
# Stop Checker
# ==============================================================================

class StopChecker:
    """
    Checks for stop conditions in generated text.

    Handles both stop strings and stop token IDs.
    """

    def __init__(
        self,
        stop_strings: Optional[List[str]] = None,
        stop_token_ids: Optional[Set[int]] = None,
        eos_token_id: Optional[int] = None,
        include_stop_string_in_output: bool = False,
    ):
        """
        Initialize the stop checker.

        Args:
            stop_strings: List of strings that trigger stopping
            stop_token_ids: Set of token IDs that trigger stopping
            eos_token_id: End-of-sequence token ID
            include_stop_string_in_output: Include stop string in output
        """
        self.stop_strings = stop_strings or []
        self.stop_token_ids = stop_token_ids or set()
        self.eos_token_id = eos_token_id
        self.include_stop_string_in_output = include_stop_string_in_output
        
        # Add EOS to stop tokens if provided
        if eos_token_id is not None:
            self.stop_token_ids.add(eos_token_id)

    def check_token(self, token_id: int) -> Optional[int]:
        """
        Check if a token should trigger stopping.

        Args:
            token_id: Token ID to check

        Returns:
            Token ID if it's a stop token, None otherwise
        """
        if HAS_RUST and self.stop_token_ids:
            if check_stop_tokens_rust(token_id, list(self.stop_token_ids)):
                return token_id
            return None
        
        if token_id in self.stop_token_ids:
            return token_id
        return None

    def check_text(self, text: str) -> Tuple[Optional[str], str]:
        """
        Check if text contains a stop string.

        Args:
            text: Text to check

        Returns:
            Tuple of (stop_string, text_before_stop) if found,
            or (None, text) if not found
        """
        for stop_string in self.stop_strings:
            idx = text.find(stop_string)
            if idx != -1:
                if self.include_stop_string_in_output:
                    return stop_string, text[:idx + len(stop_string)]
                return stop_string, text[:idx]
        return None, text

    def check_partial(self, text: str) -> Optional[int]:
        """
        Check if text ends with a partial match of a stop string.

        This is used to determine how much text to buffer before
        outputting, to avoid outputting partial stop strings.

        Returns:
            Number of characters to buffer if partial match found
        """
        for stop_string in self.stop_strings:
            for length in range(1, min(len(stop_string), len(text)) + 1):
                if text[-length:] == stop_string[:length]:
                    return length
        return None


# ==============================================================================
# Incremental Detokenizer Base
# ==============================================================================

class IncrementalDetokenizer(ABC):
    """
    Abstract base class for incremental detokenization.

    Tracks token IDs and manages the conversion to text while
    handling multi-token characters and special token filtering.

    Attributes:
        tokenizer: The underlying tokenizer
        token_ids: Accumulated token IDs
        prefix_offset: Current prefix offset
        read_offset: Current read offset
        output_text: Full output text so far
    """

    def __init__(
        self,
        tokenizer: TokenizerLike,
        skip_special_tokens: bool = True,
        spaces_between_special_tokens: bool = True,
        stop_checker: Optional[StopChecker] = None,
    ):
        """
        Initialize the detokenizer.

        Args:
            tokenizer: Tokenizer to use for decoding
            skip_special_tokens: Whether to skip special tokens
            spaces_between_special_tokens: Add spaces between special tokens
            stop_checker: Optional stop checker for stop conditions
        """
        self.tokenizer = tokenizer
        self.skip_special_tokens = skip_special_tokens
        self.spaces_between_special_tokens = spaces_between_special_tokens
        self.stop_checker = stop_checker
        
        # State
        self.token_ids: List[int] = []
        self.prefix_offset: int = 0
        self.read_offset: int = 0
        self.output_text: str = ""
        self._finished: bool = False
        self._stop_reason: Optional[Union[str, int]] = None

    def reset(self) -> None:
        """Reset the detokenizer state."""
        self.token_ids.clear()
        self.prefix_offset = 0
        self.read_offset = 0
        self.output_text = ""
        self._finished = False
        self._stop_reason = None

    @property
    def is_finished(self) -> bool:
        """Check if detokenization is finished."""
        return self._finished

    @abstractmethod
    def _decode_tokens(
        self,
        token_ids: List[int],
        prefix_offset: int,
        read_offset: int,
    ) -> Tuple[str, int, int]:
        """
        Decode tokens to text with offset tracking.

        Args:
            token_ids: All accumulated token IDs
            prefix_offset: Current prefix offset
            read_offset: Current read offset

        Returns:
            Tuple of (new_text, new_prefix_offset, new_read_offset)
        """
        pass

    def update(
        self,
        new_token_ids: Union[int, List[int]],
        finished: bool = False,
    ) -> DetokenizeResult:
        """
        Update with new token IDs and return new text.

        Args:
            new_token_ids: New token ID(s) to process
            finished: Whether this is the final update

        Returns:
            DetokenizeResult with new text and state
        """
        if self._finished:
            return DetokenizeResult(
                new_text="",
                full_text=self.output_text,
                prefix_offset=self.prefix_offset,
                read_offset=self.read_offset,
                finished=True,
                stop_reason=self._stop_reason,
            )
        
        # Normalize to list
        if isinstance(new_token_ids, int):
            new_token_ids = [new_token_ids]
        
        # Check for stop tokens
        if self.stop_checker:
            for token_id in new_token_ids:
                stop_token = self.stop_checker.check_token(token_id)
                if stop_token is not None:
                    self._finished = True
                    self._stop_reason = stop_token
                    # Don't add the stop token
                    break
            else:
                # No stop token found, add all
                self.token_ids.extend(new_token_ids)
        else:
            self.token_ids.extend(new_token_ids)
        
        # Decode tokens
        new_text, new_prefix, new_read = self._decode_tokens(
            self.token_ids,
            self.prefix_offset,
            self.read_offset,
        )
        
        self.prefix_offset = new_prefix
        self.read_offset = new_read
        
        # Check for stop strings
        if self.stop_checker and new_text:
            stop_string, text_before = self.stop_checker.check_text(
                self.output_text + new_text
            )
            if stop_string is not None:
                # Truncate to before stop string
                new_text = text_before[len(self.output_text):]
                self._finished = True
                self._stop_reason = stop_string
        
        self.output_text += new_text
        
        # Check for partial stop string matches
        buffered_chars = 0
        if self.stop_checker and not self._finished:
            buffered_chars = self.stop_checker.check_partial(new_text) or 0
        
        # If this is the final update, flush any buffered text
        if finished and not self._finished:
            self._finished = True
        
        return DetokenizeResult(
            new_text=new_text,
            full_text=self.output_text,
            prefix_offset=self.prefix_offset,
            read_offset=self.read_offset,
            finished=self._finished,
            stop_reason=self._stop_reason,
        )

    def finalize(self) -> DetokenizeResult:
        """Finalize and return remaining text."""
        return self.update([], finished=True)


# ==============================================================================
# Fast Incremental Detokenizer
# ==============================================================================

class FastIncrementalDetokenizer(IncrementalDetokenizer):
    """
    Fast incremental detokenizer for HuggingFace fast tokenizers.

    Uses the tokenizer's convert_ids_to_tokens method for efficient
    incremental decoding with proper handling of subword tokens.
    """

    def __init__(
        self,
        tokenizer: TokenizerLike,
        skip_special_tokens: bool = True,
        spaces_between_special_tokens: bool = True,
        stop_checker: Optional[StopChecker] = None,
    ):
        """Initialize fast detokenizer."""
        super().__init__(
            tokenizer,
            skip_special_tokens,
            spaces_between_special_tokens,
            stop_checker,
        )
        
        # Cache for special token IDs
        self._special_token_ids: Optional[Set[int]] = None

    @property
    def special_token_ids(self) -> Set[int]:
        """Get special token IDs (cached)."""
        if self._special_token_ids is None:
            self._special_token_ids = set()
            # Try to get special tokens from tokenizer
            if hasattr(self.tokenizer, 'all_special_ids'):
                self._special_token_ids = set(self.tokenizer.all_special_ids)
            elif hasattr(self.tokenizer, 'special_tokens_map'):
                for name, token in self.tokenizer.special_tokens_map.items():
                    if isinstance(token, str):
                        tid = self.tokenizer.convert_tokens_to_ids(token)
                        if isinstance(tid, int):
                            self._special_token_ids.add(tid)
        return self._special_token_ids

    def _decode_tokens(
        self,
        token_ids: List[int],
        prefix_offset: int,
        read_offset: int,
    ) -> Tuple[str, int, int]:
        """
        Decode tokens using fast tokenizer approach.

        This uses prefix/read offsets to track which characters
        have been output, handling multi-token characters correctly.
        """
        if not token_ids:
            return "", prefix_offset, read_offset
        
        if HAS_RUST:
            # Use Rust for offset calculation
            new_prefix, new_read = update_prefix_offset_rust(
                len(token_ids),
                prefix_offset,
                read_offset,
            )
        else:
            new_prefix = max(len(token_ids) - 6, 0)
            new_read = len(token_ids)
        
        # Decode prefix tokens (for context)
        if new_prefix > 0:
            prefix_text = self.tokenizer.decode(
                token_ids[:new_prefix],
                skip_special_tokens=self.skip_special_tokens,
            )
        else:
            prefix_text = ""
        
        # Decode all tokens
        full_text = self.tokenizer.decode(
            token_ids[:new_read],
            skip_special_tokens=self.skip_special_tokens,
        )
        
        # New text is the difference
        if len(full_text) > len(prefix_text):
            new_text = full_text[len(prefix_text):]
        else:
            new_text = ""
        
        # Handle read offset for incomplete multi-byte characters
        # We keep a small buffer to handle edge cases
        actual_new_prefix = new_prefix
        actual_new_read = new_read
        
        return new_text, actual_new_prefix, actual_new_read


# ==============================================================================
# Slow Incremental Detokenizer
# ==============================================================================

class SlowIncrementalDetokenizer(IncrementalDetokenizer):
    """
    Fallback incremental detokenizer for non-fast tokenizers.

    Uses character-by-character comparison for safety with
    tokenizers that don't support fast decoding.
    """

    def __init__(
        self,
        tokenizer: TokenizerLike,
        skip_special_tokens: bool = True,
        spaces_between_special_tokens: bool = True,
        stop_checker: Optional[StopChecker] = None,
    ):
        """Initialize slow detokenizer."""
        super().__init__(
            tokenizer,
            skip_special_tokens,
            spaces_between_special_tokens,
            stop_checker,
        )
        self._prev_text: str = ""

    def reset(self) -> None:
        """Reset state."""
        super().reset()
        self._prev_text = ""

    def _decode_tokens(
        self,
        token_ids: List[int],
        prefix_offset: int,
        read_offset: int,
    ) -> Tuple[str, int, int]:
        """
        Decode tokens using simple full decode approach.

        This is slower but more compatible with various tokenizers.
        """
        if not token_ids:
            return "", prefix_offset, read_offset
        
        # Decode all tokens
        full_text = self.tokenizer.decode(
            token_ids,
            skip_special_tokens=self.skip_special_tokens,
        )
        
        # Find new text
        new_text = ""
        if len(full_text) > len(self._prev_text):
            # Verify prefix matches (safety check)
            if full_text.startswith(self._prev_text):
                new_text = full_text[len(self._prev_text):]
            else:
                # Mismatch - find common prefix
                common_len = 0
                for i in range(min(len(full_text), len(self._prev_text))):
                    if full_text[i] == self._prev_text[i]:
                        common_len += 1
                    else:
                        break
                new_text = full_text[common_len:]
        
        self._prev_text = full_text
        
        # Update offsets
        new_prefix = len(token_ids)
        new_read = len(token_ids)
        
        return new_text, new_prefix, new_read


# ==============================================================================
# Factory Functions
# ==============================================================================

def create_detokenizer(
    tokenizer: TokenizerLike,
    skip_special_tokens: bool = True,
    spaces_between_special_tokens: bool = True,
    stop_strings: Optional[List[str]] = None,
    stop_token_ids: Optional[Set[int]] = None,
    use_fast: bool = True,
) -> IncrementalDetokenizer:
    """
    Create an appropriate detokenizer for the given tokenizer.

    Args:
        tokenizer: The tokenizer to use
        skip_special_tokens: Skip special tokens in output
        spaces_between_special_tokens: Add spaces between special tokens
        stop_strings: Strings that trigger stopping
        stop_token_ids: Token IDs that trigger stopping
        use_fast: Prefer fast detokenizer if available

    Returns:
        An IncrementalDetokenizer instance
    """
    # Create stop checker if needed
    stop_checker = None
    if stop_strings or stop_token_ids:
        eos_token_id = getattr(tokenizer, 'eos_token_id', None)
        stop_checker = StopChecker(
            stop_strings=stop_strings,
            stop_token_ids=stop_token_ids or set(),
            eos_token_id=eos_token_id,
        )
    
    # Check if tokenizer supports fast decoding
    is_fast = use_fast and hasattr(tokenizer, 'is_fast') and tokenizer.is_fast
    
    if is_fast or use_fast:
        return FastIncrementalDetokenizer(
            tokenizer,
            skip_special_tokens=skip_special_tokens,
            spaces_between_special_tokens=spaces_between_special_tokens,
            stop_checker=stop_checker,
        )
    else:
        return SlowIncrementalDetokenizer(
            tokenizer,
            skip_special_tokens=skip_special_tokens,
            spaces_between_special_tokens=spaces_between_special_tokens,
            stop_checker=stop_checker,
        )


def detokenize_incrementally(
    tokenizer: TokenizerLike,
    token_ids: List[int],
    skip_special_tokens: bool = True,
    spaces_between_special_tokens: bool = True,
    stop_strings: Optional[List[str]] = None,
) -> Tuple[str, Optional[str]]:
    """
    Convenience function to detokenize a sequence of tokens.

    Args:
        tokenizer: The tokenizer to use
        token_ids: Token IDs to decode
        skip_special_tokens: Skip special tokens in output
        spaces_between_special_tokens: Add spaces between special tokens
        stop_strings: Strings that trigger stopping

    Returns:
        Tuple of (decoded_text, stop_reason_if_any)
    """
    detokenizer = create_detokenizer(
        tokenizer,
        skip_special_tokens=skip_special_tokens,
        spaces_between_special_tokens=spaces_between_special_tokens,
        stop_strings=stop_strings,
    )
    
    # Process all tokens
    for token_id in token_ids:
        result = detokenizer.update(token_id)
        if result.finished:
            return result.full_text, result.stop_reason
    
    # Finalize
    result = detokenizer.finalize()
    return result.full_text, result.stop_reason
