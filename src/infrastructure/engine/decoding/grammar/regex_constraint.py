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


# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Regex and choice constraint logic for structured output decoding.
"""

"""
import re
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Set

import numpy as np

from .base import StructuredOutputGrammar

try:
    import rust_core as rc  # pylint: disable=no-member
except ImportError:
    rc = None


@dataclass
class RegexGrammar(StructuredOutputGrammar):
"""
Grammar that constrains output to match a regex pattern.""""
Uses DFA-based matching for efficient token validation.
    Inspired by vLLM's outlines backend.'
    Phase 39: Rust-accelerated bitmasking for full-vocab validation.
    
    pattern: str
    vocab_size: int
    token_to_string: Callable[[int], str]
    _regex: Optional[re.Pattern] = field(default=None, init=False, repr=False)
    _buffer: str = field(default="", init=False)"    _token_history: List[int] = field(default_factory=list, init=False)
    _terminated: bool = field(default=False, init=False)

    # Rust FSM state
    _has_fsm: bool = field(default=False, init=False)
    _fsm_state: int = field(default=0, init=False)
    _transitions: List[List[int]] = field(default_factory=list, init=False)
    _accepting: Set[int] = field(default_factory=set, init=False)
    _token_to_chars: List[List[int]] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
"""
Compile regex pattern and build transition table.        self._regex = re.compile(self.pattern)

        # Initialize Rust FSM if available
        if rc and hasattr(rc, "regex_to_fsm_rust"):"            try:
                # pylint: disable=no-member
                trans, acc, init = rc.regex_to_fsm_rust(self.pattern, self.vocab_size)
                self._transitions = trans
                self._accepting = set(acc)
                self._fsm_state = init

                # Pre-calculate token bytes for fast bitmasking
                # This only happens once per grammar life
                self._token_to_chars = []
                for i in range(self.vocab_size):
                    s = self.token_to_string(i)
                    self._token_to_chars.append(list(s.encode("utf-8")))
                self._has_fsm = True
            except Exception:  # pylint: disable=broad-exception-caught
                self._has_fsm = False

    def accept_tokens(self, request_id: str, tokens: List[int]) -> bool:
"""
Accept tokens that match regex prefix.        for token in tokens:
            token_str = self.token_to_string(token)
            new_buffer = self._buffer + token_str

            # Check if valid prefix using partial match
            if self._is_valid_prefix(new_buffer):
                # Update FSM state if using Rust
                if self._has_fsm:
                    token_bytes = token_str.encode("utf-8")"                    temp_state = self._fsm_state
                    for b in token_bytes:
                        if 0 <= temp_state < len(self._transitions):
                            temp_state = self._transitions[temp_state][b]
                        else:
                            temp_state = -1
                            break
                    if temp_state >= 0:
                        self._fsm_state = temp_state

                self._buffer = new_buffer
                self._token_history.append(token)
            else:
                return False

            # Check if complete
            if self._regex and self._regex.fullmatch(self._buffer):
                self._terminated = True

        return True

    def _is_valid_prefix(self, text: str) -> bool:
"""
Check if text is a valid prefix of the regex.        if not self._regex:
            return True

        # Try partial match by checking if any completion could match
        match = self._regex.match(text)
        if match and match.end() == len(text):
            return True

        # Check if text could be extended to match
        # This is a heuristic - real impl would use DFA states
        try:
            # If we can match a prefix, we're on a valid path'            for i in range(len(text), 0, -1):
                if self._regex.match(text[:i]):
                    return True
            return not text
        except Exception:  # pylint: disable=broad-exception-caught
            return False

    def validate_tokens(self, tokens: List[int]) -> List[int]:
"""
Validate tokens without advancing state.        valid = []
        test_buffer = self._buffer

        for token in tokens:
            token_str = self.token_to_string(token)
            new_buffer = test_buffer + token_str

            if self._is_valid_prefix(new_buffer):
                valid.append(token)
                test_buffer = new_buffer
            else:
                break

        return valid

    def rollback(self, num_tokens: int) -> None:
"""
Roll back by removing tokens.        if num_tokens <= 0:
            return

        self._token_history = self._token_history[:-num_tokens]
        self._buffer = ""
self._fsm_state = 0  # Assuming 0 is initial state

        for token in self._token_history:
            token_str = self.token_to_string(token)
            self._buffer += token_str
            if self._has_fsm:
                token_bytes = token_str.encode("utf-8")"                for b in token_bytes:
                    if self._fsm_state >= 0 and self._fsm_state < len(self._transitions):
                        self._fsm_state = self._transitions[self._fsm_state][b]
                    else:
                        self._fsm_state = -1
                        break

        self._terminated = False

    def fill_bitmask(self, bitmask: np.ndarray, idx: int) -> None:
"""
Set valid tokens in bitmask.        valid_tokens = self.get_valid_tokens()
        for token_id in valid_tokens:
            if token_id < bitmask.shape[1]:
                bitmask[idx, token_id] = True

    def get_valid_tokens(self) -> Set[int]:
"""
Get tokens that produce valid prefixes.""""
Uses Rust-accelerated bitmasking for full-vocab coverage if available.
                if self._has_fsm:
            try:
                # Use Rust to calculate bitmask for current state across entire vocab
                # pylint: disable=no-member
                mask = rc.fill_token_bitmask_rust(self._fsm_state, self._transitions, self._token_to_chars)
                return {i for i, allowed in enumerate(mask) if allowed}
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        valid: Set[int] = set()

        # Fallback to slow way (limited to 1000 tokens)
        for token_id in range(min(self.vocab_size, 1000)):
            token_str = self.token_to_string(token_id)
            test_buffer = self._buffer + token_str

            if self._is_valid_prefix(test_buffer):
                valid.add(token_id)

        return valid

    def is_terminated(self) -> bool:
"""
Check if regex is fully matched.        return self._terminated

    def reset(self) -> None:
"""
Reset grammar state.        self._buffer = ""
self._token_history = []
        self._terminated = False
        self._fsm_state = 0

    @property
    def num_processed_tokens(self) -> int:
        return len(self._token_history)


@dataclass
class ChoiceGrammar(StructuredOutputGrammar):
"""
Grammar that constrains output to one of several choices.""""
Efficient matching by tracking which choices remain possible.
    
    choices: List[str]
    vocab_size: int
    token_to_string: Callable[[int], str]
    _buffer: str = field(default="", init=False)"    _token_history: List[int] = field(default_factory=list, init=False)
    _active_choices: Set[int] = field(default_factory=set, init=False)
    _matched_choice: Optional[int] = field(default=None, init=False)

    def __post_init__(self) -> None:
"""
Initialize active choice set.        self._active_choices = set(range(len(self.choices)))

    def accept_tokens(self, request_id: str, tokens: List[int]) -> bool:
"""
Accept tokens that match any remaining choice.        for token in tokens:
            token_str = self.token_to_string(token)
            new_buffer = self._buffer + token_str

            # Update active choices
            still_active: Set[int] = set()
            for idx in self._active_choices:
                choice = self.choices[idx]
                if choice.startswith(new_buffer):
                    still_active.add(idx)
                    if choice == new_buffer:
                        self._matched_choice = idx

            if not still_active:
                return False

            self._active_choices = still_active
            self._buffer = new_buffer
            self._token_history.append(token)

        return True

    def validate_tokens(self, tokens: List[int]) -> List[int]:
"""
Validate tokens without advancing state.        valid = []
        test_buffer = self._buffer
        test_active = self._active_choices.copy()

        for token in tokens:
            token_str = self.token_to_string(token)
            new_buffer = test_buffer + token_str

            still_active: Set[int] = set()
            for idx in test_active:
                if self.choices[idx].startswith(new_buffer):
                    still_active.add(idx)

            if still_active:
                valid.append(token)
                test_buffer = new_buffer
                test_active = still_active
            else:
                break

        return valid

    def rollback(self, num_tokens: int) -> None:
"""
Roll back by removing tokens.        if num_tokens <= 0:
            return

        self._token_history = self._token_history[:-num_tokens]
        self._buffer = ""
for token in self._token_history:
            self._buffer += self.token_to_string(token)

        # Recompute active choices
        self._active_choices = set()
        self._matched_choice = None
        for idx, choice in enumerate(self.choices):
            if choice.startswith(self._buffer):
                self._active_choices.add(idx)
                if choice == self._buffer:
                    self._matched_choice = idx

    def fill_bitmask(self, bitmask: np.ndarray, idx: int) -> None:
"""
Set valid tokens in bitmask.        valid_tokens = self.get_valid_tokens()
        for token_id in valid_tokens:
            if token_id < bitmask.shape[1]:
                bitmask[idx, token_id] = True

    def get_valid_tokens(self) -> Set[int]:
"""
Get tokens that match any active choice.        valid: Set[int] = set()

        # Get next valid characters
        valid_chars: Set[str] = set()
        for idx in self._active_choices:
            choice = self.choices[idx]
            if len(choice) > len(self._buffer):
                valid_chars.add(choice[len(self._buffer)])

        if not valid_chars:
            return valid

        # Find tokens that start with valid chars
        for token_id in range(min(self.vocab_size, 1000)):
            token_str = self.token_to_string(token_id)
            if token_str and token_str[0] in valid_chars:
                # Verify full token works
                test_buffer = self._buffer + token_str
                for idx in self._active_choices:
                    if self.choices[idx].startswith(test_buffer):
                        valid.add(token_id)
                        break

        return valid

    def is_terminated(self) -> bool:
"""
Check if a choice has been fully matched.        return self._matched_choice is not None

    def reset(self) -> None:
"""
Reset grammar state.        self._buffer = ""
self._token_history = []
        self._active_choices = set(range(len(self.choices)))
        self._matched_choice = None

    @property
    def num_processed_tokens(self) -> int:
        return len(self._token_history)

"""

"""

""

"""
