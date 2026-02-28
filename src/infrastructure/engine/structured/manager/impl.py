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
Impl.py module.
"""

from __future__ import annotations

import contextlib
import json
from typing import Callable, Dict, List, Optional, Sequence

import numpy as np

from .base import StructuredOutputGrammar
from .config import GrammarSpec


class SimpleRegexGrammar(StructuredOutputGrammar):
    """
    Simple regex-based grammar using Python's re module.
    """

    def __init__(
        self,
        grammar_spec: GrammarSpec,
        vocab_size: int,
        request_id: Optional[str] = None,
        token_strings: Optional[Dict[int, str]] = None,
    ) -> None:
        super().__init__(grammar_spec, vocab_size, request_id)

        import re

        self._pattern = re.compile(grammar_spec.spec)
        self._generated_text = ""
        self._token_strings = token_strings or {}

    def accept_tokens(self, tokens: Sequence[int]) -> bool:
        """
        Accept tokens and update regex state.

        Args:
            tokens: Token IDs to accept.

        Returns:
            True if all tokens are valid for the regex.
        """
        for token_id in tokens:
            token_str = self._token_strings.get(token_id, "")
            new_text = self._generated_text + token_str

            if self._pattern.fullmatch(new_text) or self._is_partial_match(new_text):
                self._state_history.append(self._generated_text)
                self._generated_text = new_text
                self._tokens_accepted += 1

                if self._pattern.fullmatch(self._generated_text):
                    self._is_terminated = True
            else:
                return False

        return True

    def _is_partial_match(self, text: str) -> bool:
        """Check if text is a partial match for the regex."""
        with contextlib.suppress(Exception):
            return self._pattern.match(text) is not None
        return False

    def validate_tokens(self, tokens: Sequence[int]) -> int:
        """
        Validate tokens against the regex without updating state.

        Args:
            tokens: Token IDs to validate.

        Returns:
            Number of valid tokens.
        """
        temp_text = self._generated_text

        for i, token_id in enumerate(tokens):
            token_str = self._token_strings.get(token_id, "")
            new_text = temp_text + token_str

            if not (self._pattern.fullmatch(new_text) or self._is_partial_match(new_text)):
                return i

            temp_text = new_text

        return len(tokens)

    def fill_bitmask(self, bitmask: np.ndarray, batch_index: int = 0) -> None:
        """
        Fill bitmask (not implemented efficiently for simple regex).

        Args:
            bitmask: Bitmask to fill.
            batch_index: Batch index.
        """
        bitmask[batch_index, :] = True

    def get_allowed_tokens(self) -> List[int]:
        """
        Get allowed tokens (not implemented efficiently for simple regex).

        Returns:
            List of all token IDs.
        """
        return list(range(self.vocab_size))


class ChoiceGrammar(StructuredOutputGrammar):
    """Grammar for choosing from a fixed set of options."""

    def __init__(
        self,
        grammar_spec: GrammarSpec,
        vocab_size: int,
        request_id: Optional[str] = None,
        token_strings: Optional[Dict[int, str]] = None,
        encode_fn: Optional[Callable[[str], List[int]]] = None,
    ) -> None:
        """
        Initialize ChoiceGrammar.

        Args:
            grammar_spec: Grammar specification.
            vocab_size: Vocabulary size.
            request_id: Request ID.
            token_strings: Mapping from token IDs to strings.
            encode_fn: Function to encode text to tokens.
        """
        super().__init__(grammar_spec, vocab_size, request_id)

        self._choices: List[str] = json.loads(grammar_spec.spec)
        self._token_strings = token_strings or {}
        self._encode_fn = encode_fn

        self._generated_text = ""
        self._valid_choices: List[str] = list(self._choices)
        self._allowed_tokens_cache: Dict[str, set] = {}

    def accept_tokens(self, tokens: Sequence[int]) -> bool:
        """
        Accept tokens and update valid choices.

        Args:
            tokens: Token IDs to accept.

        Returns:
            True if all tokens are valid prefixes of some choice.
        """
        for token_id in tokens:
            token_str = self._token_strings.get(token_id, "")
            new_text = self._generated_text + token_str

            new_valid = [c for c in self._valid_choices if c.startswith(new_text)]

            if not new_valid:
                return False

            self._state_history.append((self._generated_text, self._valid_choices.copy()))
            self._generated_text = new_text
            self._valid_choices = new_valid
            self._tokens_accepted += 1

            if new_text in self._choices:
                self._is_terminated = True

        return True

    def validate_tokens(self, tokens: Sequence[int]) -> int:
        """
        Validate tokens against choices without updating state.

        Args:
            tokens: Token IDs to validate.

        Returns:
            Number of valid tokens.
        """
        temp_text = self._generated_text
        temp_valid = list(self._valid_choices)

        for i, token_id in enumerate(tokens):
            token_str = self._token_strings.get(token_id, "")
            new_text = temp_text + token_str

            new_valid = [c for c in temp_valid if c.startswith(new_text)]
            if not new_valid:
                return i

            temp_text = new_text
            temp_valid = new_valid

        return len(tokens)

    def fill_bitmask(self, bitmask: np.ndarray, batch_index: int = 0) -> None:
        """
        Fill a bitmask with allowed tokens for identifying choices.

        Args:
            bitmask: Bitmask to fill.
            batch_index: Index in the batch.
        """
        allowed = self._compute_allowed_tokens()
        bitmask[batch_index, :] = False
        for token_id in allowed:
            if token_id < bitmask.shape[1]:
                bitmask[batch_index, token_id] = True

    def get_allowed_tokens(self) -> List[int]:
        """
        Get the list of allowed token IDs.

        Returns:
            List of allowed token IDs.
        """
        return list(self._compute_allowed_tokens())

    def _compute_allowed_tokens(self) -> set:
        """Compute allowed tokens based on valid choices."""
        cache_key = self._generated_text
        if cache_key in self._allowed_tokens_cache:
            return self._allowed_tokens_cache[cache_key]

        allowed = set()
        for choice in self._valid_choices:
            if len(choice) > len(self._generated_text):
                next_char = choice[len(self._generated_text)]
                for token_id, token_str in self._token_strings.items():
                    if token_str and token_str[0] == next_char:
                        allowed.add(token_id)

        self._allowed_tokens_cache[cache_key] = allowed
        return allowed

    def rollback(self, num_tokens: int) -> None:
        """
        Roll back the grammar state.

        Args:
            num_tokens: Number of tokens to roll back.
        """
        for _ in range(min(num_tokens, len(self._state_history))):
            if self._state_history:
                self._generated_text, self._valid_choices = self._state_history.pop()
                self._tokens_accepted -= 1
        self._is_terminated = False
