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

"""Compiled grammar structures."""

import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional

try:
    import numpy as np  # noqa: F401

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import rust_core  # noqa: F401

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

from .enums import GrammarType
from .models import FSMTransitionTable


@dataclass
class CompiledGrammar:
    """
    Compiled grammar context.

    Holds the compiled grammar state and provides methods for
    token acceptance checking and bitmask generation.
    """

    grammar_type: GrammarType
    grammar_spec: str
    vocab_size: int
    max_rollback_tokens: int = 0
    token_strings: Dict[int, str] = field(default_factory=dict)
    fsm: Optional[FSMTransitionTable] = None
    eos_token_id: Optional[int] = None

    # Internal state
    _current_state: int = field(default=0)
    _accepted_tokens: List[int] = field(default_factory=list)
    _state_history: List[int] = field(default_factory=list)
    _cache_key: str = field(default="")

    def __post_init__(self) -> None:
        self._cache_key = self._compute_cache_key()
        self._state_history = [self._current_state]

    def _compute_cache_key(self) -> str:
        """Compute cache key for grammar."""
        content = f"{self.grammar_type.name}:{self.grammar_spec}"
        return hashlib.md5(content.encode()).hexdigest()[:16]

    def accept_token(self, token_id: int) -> bool:
        """Accept a token and update state."""
        if token_id == self.eos_token_id:
            if self.fsm and self.fsm.is_accepting(self._current_state):
                self._accepted_tokens.append(token_id)
                self._state_history.append(self._current_state)
                return True
            return False

        tstr = self.token_strings.get(token_id, "")
        if not tstr:
            return False

        if not self.fsm:
            self._accepted_tokens.append(token_id)
            return True

        # Try to transition through all characters in the token
        temp_state = self._current_state
        for char in tstr:
            next_state = self.fsm.get_next_state(temp_state, char)
            if next_state == -1:
                return False
            temp_state = next_state

        self._current_state = temp_state
        self._accepted_tokens.append(token_id)
        self._state_history.append(self._current_state)
        return True

    def rollback(self, num_tokens: int) -> None:
        """Rollback the last N tokens."""
        if 0 < num_tokens <= len(self._accepted_tokens):
            self._accepted_tokens = self._accepted_tokens[:-num_tokens]
            self._state_history = self._state_history[: len(self._accepted_tokens) + 1]
            self._current_state = self._state_history[-1]

    def reset(self) -> None:
        """Reset grammar state."""
        self._accepted_tokens.clear()
        self._current_state = 0
        self._state_history = [0]

    def is_terminated(self) -> bool:
        """Check if grammar is in terminal state."""
        if not self.fsm:
            return False
        return self.fsm.is_accepting(self._current_state)

    def fill_bitmask(self, bitmask: "np.ndarray") -> None:
        """Fill bitmask with allowed tokens."""
        if not HAS_NUMPY:
            return

        if not self.fsm:
            bitmask.fill(1)
            return

        # Start with all zeros
        bitmask.fill(0)

        # Get allowed characters in current state
        allowed_chars = self.fsm.get_allowed_chars(self._current_state)

        # Optimize: If no allowed chars, only check if accepting
        if not allowed_chars:
            if self.fsm.is_accepting(self._current_state) and self.eos_token_id is not None:
                bitmask[self.eos_token_id] = 1
            return

        # Simple approach: iterate over all tokens and check if they're allowed
        # High performance approach: use the Rust helper if we have a list of allowed IDs
        allowed_ids = []
        for tid, tstr in self.token_strings.items():
            if not tstr:
                continue

            # Check if this token is allowed starting from current state
            temp_state = self._current_state
            is_valid = True
            for char in tstr:
                next_state = self.fsm.get_next_state(temp_state, char)
                if next_state == -1:
                    is_valid = False
                    break
                temp_state = next_state

            if is_valid:
                allowed_ids.append(tid)

        if self.fsm.is_accepting(self._current_state) and self.eos_token_id is not None:
            allowed_ids.append(self.eos_token_id)

        if HAS_RUST:
            rust_mask = rust_core.xgrammar_bitmask_fill_rust(allowed_ids, self.vocab_size)
            # Update bitmask array
            bitmask[:] = np.array(rust_mask, dtype=bitmask.dtype)
        else:
            for tid in allowed_ids:
                if 0 <= tid < self.vocab_size:
                    bitmask[tid] = 1
