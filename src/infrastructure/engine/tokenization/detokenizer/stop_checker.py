# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Stop condition checker for detokenization.
"""

from __future__ import annotations

from typing import (
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

# Try to import Rust accelerations
try:
    from rust_core import check_stop_tokens_rust
    HAS_RUST = True
except ImportError:
    HAS_RUST = False

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
        self.stop_strings = stop_strings or []
        self.stop_token_ids = stop_token_ids or set()
        self.eos_token_id = eos_token_id
        self.include_stop_string_in_output = include_stop_string_in_output

        # Add EOS to stop tokens if provided
        if eos_token_id is not None:
            self.stop_token_ids.add(eos_token_id)

    def check_token(self, token_id: int) -> Optional[int]:
        """Check if a token should trigger stopping."""
        if HAS_RUST and self.stop_token_ids:
            if check_stop_tokens_rust(token_id, list(self.stop_token_ids)):
                return token_id
            return None

        if token_id in self.stop_token_ids:
            return token_id
        return None

    def check_text(self, text: str) -> Tuple[Optional[str], str]:
        """Check if text contains a stop string."""
        for stop_string in self.stop_strings:
            idx = text.find(stop_string)
            if idx != -1:
                if self.include_stop_string_in_output:
                    return stop_string, text[:idx + len(stop_string)]
                return stop_string, text[:idx]
        return None, text

    def check_partial(self, text: str) -> Optional[int]:
        """Check if text ends with a partial match of a stop string."""
        for stop_string in self.stop_strings:
            for length in range(1, min(len(stop_string), len(text)) + 1):
                if text[-length:] == stop_string[:length]:
                    return length
        return None
