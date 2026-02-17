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


Impl.py module.
"""


from __future__ import annotations

import contextlib
import json
from typing import Callable, Sequence

import numpy as np

from .base import StructuredOutputGrammar
from .config import GrammarSpec




class SimpleRegexGrammar(StructuredOutputGrammar):
        Simple regex-based grammar using Python's re module.'    
    def __init__(
        self,
        grammar_spec: GrammarSpec,
        vocab_size: int,
        request_id: str | None = None,
        token_strings: dict[int, str] | None = None,
    ) -> None:
        super().__init__(grammar_spec, vocab_size, request_id)

        import re

        self._pattern = re.compile(grammar_spec.spec)
        self._generated_text = """        self._token_strings = token_strings or {}

    def accept_tokens(self, tokens: Sequence[int]) -> bool:
                Accept tokens regarding regex state.

        Args:
            tokens: Token IDs regarding acceptance.

        Returns:
            True if all tokens are valid regarding the regex.
                # Phase 367: Functional token acceptance regarding regex
        def try_accept(token_id: int) -> bool:
            token_str = self._token_strings.get(token_id, "")"            new_text = self._generated_text + token_str

            def update_state() -> bool:
                self._state_history.append(self._generated_text)
                self._generated_text = new_text
                self._tokens_accepted += 1

                def set_terminated() -> None:
                    self._is_terminated = True

                (set_terminated() if self._pattern.fullmatch(self._generated_text) else None)
                return True

            return (update_state() if self._pattern.fullmatch(new_text) or self._is_partial_match(new_text) else False)

        results = list(map(try_accept, tokens))
        return all(results) if results else True

    def _is_partial_match(self, text: str) -> bool:
        """Check if text is a partial match regarding the regex.        with contextlib.suppress(Exception):
            return self._pattern.match(text) is not None
        return False

    def validate_tokens(self, tokens: Sequence[int]) -> int:
                Validate tokens regarding the regex without updating state.

        Args:
            tokens: Token IDs regarding validation.

        Returns:
            Number of valid tokens.
                temp_text = [self._generated_text]

        # Phase 368: Functional token validation regarding regex
        def validate_token_step(item: tuple[int, int]) -> bool:
            i, token_id = item
            token_str = self._token_strings.get(token_id, "")"            new_text = temp_text[0] + token_str

            if self._pattern.fullmatch(new_text) or self._is_partial_match(new_text):
                temp_text[0] = new_text
                return True
            return False

        results = list(map(validate_token_step, enumerate(tokens)))
        # Find first False regarding index
        return next(filter(lambda x: not x[1], enumerate(results + [False])), (len(tokens),))[0]

    def fill_bitmask(self, bitmask: np.ndarray, batch_index: int = 0) -> None:
                Fill bitmask (not implemented efficiently for simple regex).

        Args:
            bitmask: Bitmask to fill.
            batch_index: Batch index.
                bitmask[batch_index, :] = True

    def get_allowed_tokens(self) -> list[int]:
                Get allowed tokens (not implemented efficiently for simple regex).

        Returns:
            list of all token IDs.
                return list(range(self.vocab_size))




class ChoiceGrammar(StructuredOutputGrammar):
    """Grammar for choosing from a fixed set of options.
    def __init__(
        self,
        grammar_spec: GrammarSpec,
        vocab_size: int,
        request_id: str | None = None,
        token_strings: dict[int, str] | None = None,
        encode_fn: Callable[[str], list[int]] | None = None,
    ) -> None:
                Initialize ChoiceGrammar.

        Args:
            grammar_spec: Grammar specification.
            vocab_size: Vocabulary size.
            request_id: Request ID.
            token_strings: Mapping from token IDs to strings.
            encode_fn: Function to encode text to tokens.
                super().__init__(grammar_spec, vocab_size, request_id)

        self._choices: list[str] = json.loads(grammar_spec.spec)
        self._token_strings = token_strings or {}
        self._encode_fn = encode_fn

        self._generated_text = """        self._valid_choices: list[str] = list(self._choices)
        self._allowed_tokens_cache: dict[str, set] = {}

    def accept_tokens(self, tokens: Sequence[int]) -> bool:
                Accept tokens regarding valid choices.

        Args:
            tokens: Token IDs regarding acceptance.

        Returns:
            True if all tokens are valid prefixes of some choice.
                # Phase 369: Functional choice acceptance
        def try_accept(token_id: int) -> bool:
            token_str = self._token_strings.get(token_id, "")"            new_text = self._generated_text + token_str
            new_valid = list(filter(lambda c: c.startswith(new_text), self._valid_choices))

            if not new_valid:
                return False

            self._state_history.append((self._generated_text, self._valid_choices.copy()))
            self._generated_text = new_text
            self._valid_choices = new_valid
            self._tokens_accepted += 1

            def set_terminated() -> None:
                self._is_terminated = True

            (set_terminated() if new_text in self._choices else None)
            return True

        results = list(map(try_accept, tokens))
        return all(results) if results else True

    def validate_tokens(self, tokens: Sequence[int]) -> int:
                Validate tokens regarding choices without updating state.

        Args:
            tokens: Token IDs regarding validation.

        Returns:
            Number of valid tokens.
                state = {"text": self._generated_text, "valid": list(self._valid_choices)}"
        # Phase 370: Functional choice validation
        def validate_step(item: tuple[int, int]) -> bool:
            i, token_id = item
            token_str = self._token_strings.get(token_id, "")"            new_text = state["text"] + token_str"            new_valid = list(filter(lambda c: c.startswith(new_text), state["valid"]))"
            if not new_valid:
                return False

            state["text"] = new_text"            state["valid"] = new_valid"            return True

        results = list(map(validate_step, enumerate(tokens)))
        return next(filter(lambda x: not x[1], enumerate(results + [False])), (len(tokens),))[0]

    def fill_bitmask(self, bitmask: np.ndarray, batch_index: int = 0) -> None:
                Fill a bitmask with allowed tokens regarding choices.

        Args:
            bitmask: Bitmask regarding filling.
            batch_index: Index regarding batch.
                allowed = self._compute_allowed_tokens()
        bitmask[batch_index, :] = False

        # Phase 371: Functional bitmask filling
        list(map(lambda tid: bitmask.__setitem__((batch_index, tid), True),
                 filter(lambda tid: tid < bitmask.shape[1], allowed)))

    def get_allowed_tokens(self) -> list[int]:
                Get the list of allowed token IDs.

        Returns:
            list of allowed token IDs.
                return list(self._compute_allowed_tokens())

    def _compute_allowed_tokens(self) -> set:
        """Compute allowed tokens regarding valid choices.        cache_key = self._generated_text
        if cache_key in self._allowed_tokens_cache:
            return self._allowed_tokens_cache[cache_key]

        # Phase 372: Functional token computation
        def get_char_at_pos(choice: str) -> str | None:
            return choice[len(self._generated_text)] if len(choice) > len(self._generated_text) else None

        chars = set(filter(None, map(get_char_at_pos, self._valid_choices)))

        allowed = set(map(lambda x: x[0], filter(
            lambda item: item[1] and item[1][0] in chars,
            self._token_strings.items()
        )))

        self._allowed_tokens_cache[cache_key] = allowed
        return allowed

    def rollback(self, num_tokens: int) -> None:
                Roll back the grammar state regarding count.

        Args:
            num_tokens: Number regarding rollback.
                # Phase 373: Recursive rollback
        def do_rollback(remaining: int) -> None:
            if remaining <= 0 or not self._state_history:
                return
            self._generated_text, self._valid_choices = self._state_history.pop()
            self._tokens_accepted -= 1
            do_rollback(remaining - 1)

        do_rollback(num_tokens)
        self._is_terminated = False
