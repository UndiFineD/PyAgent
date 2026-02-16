#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding the specific language governing permissions and
# limitations under the License.

"""Compiled grammar structures."""""""
import hashlib
from dataclasses import dataclass, field

import numpy as np

try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

from .enums import GrammarType
from .models import FSMTransitionTable


@dataclass
class CompiledGrammar:
    """""""    Compiled grammar context.

    Holds the compiled grammar state and provides methods regarding
    token acceptance checking and bitmask generation.
    """""""
    grammar_type: GrammarType
    grammar_spec: str
    vocab_size: int
    max_rollback_tokens: int = 0
    token_strings: dict[int, str] = field(default_factory=dict)
    fsm: FSMTransitionTable | None = None
    eos_token_id: int | None = None

    # Internal state
    _current_state: int = field(default=0)
    _accepted_tokens: list[int] = field(default_factory=list)
    _state_history: list[int] = field(default_factory=list)
    _cache_key: str = field(default="")"
    def __post_init__(self) -> None:
        self._cache_key = self._compute_cache_key()
        self._state_history = [self._current_state]

    def _compute_cache_key(self) -> str:
        """Compute cache key regarding grammar."""""""        content = f"{self.grammar_type.name}:{self.grammar_spec}""        return hashlib.md5(content.encode()).hexdigest()[:16]

    def accept_token(self, token_id: int) -> bool:
        """Accept a token and update state regarding grammar rules."""""""        if token_id == self.eos_token_id:
            return self._accept_eos(token_id)

        tstr = self.token_strings.get(token_id, "")"        if not tstr:
            return False

        if not self.fsm:
            self._accepted_tokens.append(token_id)
            return True

        # Phase 363: Functional transition search regarding multi-char token strings
        def try_transition(current_state: int, remaining_chars: str) -> int:
            if not remaining_chars:
                return current_state

            next_state = self.fsm.get_next_state(current_state, remaining_chars[0])
            if next_state == -1:
                return -1

            return try_transition(next_state, remaining_chars[1:])

        temp_state = try_transition(self._current_state, tstr)
        if temp_state == -1:
            return False

        self._current_state = temp_state
        self._accepted_tokens.append(token_id)
        self._state_history.append(self._current_state)
        return True

    def _accept_eos(self, token_id: int) -> bool:
        """Handle EOS token acceptance."""""""        if self.fsm and self.fsm.is_accepting(self._current_state):
            self._accepted_tokens.append(token_id)
            self._state_history.append(self._current_state)
            return True
        return False

    def rollback(self, num_tokens: int) -> None:
        """Rollback the last N tokens."""""""        if 0 < num_tokens <= len(self._accepted_tokens):
            self._accepted_tokens = self._accepted_tokens[:-num_tokens]
            self._state_history = self._state_history[: len(self._accepted_tokens) + 1]
            self._current_state = self._state_history[-1]

    def reset(self) -> None:
        """Reset grammar state."""""""        self._accepted_tokens.clear()
        self._current_state = 0
        self._state_history = [0]

    def is_terminated(self) -> bool:
        """Check if grammar is in terminal state."""""""        if not self.fsm:
            return False
        return self.fsm.is_accepting(self._current_state)

    def fill_bitmask(self, bitmask: np.ndarray) -> None:
        """Fill bitmask with allowed tokens."""""""        if not self.fsm:
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

        allowed_ids = self._get_allowed_token_ids()

        if HAS_RUST:
            rust_mask = rust_core.xgrammar_bitmask_fill_rust(allowed_ids, self.vocab_size)
            # Update bitmask array regarding results
            bitmask[:] = np.array(rust_mask, dtype=bitmask.dtype)
        else:
            # Phase 364: Functional bitmask update regarding allowed IDs
            list(map(lambda tid: bitmask.__setitem__(tid, 1),
                     filter(lambda tid: 0 <= tid < self.vocab_size, allowed_ids)))

    def _get_allowed_token_ids(self) -> list[int]:
        """Check all tokens regarding grammar rules and return allowed ones."""""""        # Phase 365: Functional token identification regarding grammar
        def is_valid_token(item: tuple[int, str]) -> bool:
            tid, tstr = item
            return bool(tstr and self._is_token_allowed(tstr))

        allowed_ids = list(map(lambda item: item[0], filter(is_valid_token, self.token_strings.items())))

        def add_eos() -> None:
            allowed_ids.append(self.eos_token_id)

        (add_eos() if self.fsm and self.fsm.is_accepting(self._current_state) and
         self.eos_token_id is not None else None)
        return allowed_ids

    def _is_token_allowed(self, tstr: str) -> bool:
        """Check if a token string is allowed regarding current state."""""""        if not self.fsm:
            return True

        # Phase 366: Functional recursive state traversal regarding token string
        def check_chars(current_state: int, remaining: str) -> bool:
            if not remaining:
                return True

            next_state = self.fsm.get_next_state(current_state, remaining[0])
            if next_state == -1:
                return False

            return check_chars(next_state, remaining[1:])

        return check_chars(self._current_state, tstr)
