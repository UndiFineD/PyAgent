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


"""
Matcher for grammar-based token validation.

"""
from dataclasses import dataclass, field
from typing import Any, List

try:
    import numpy as np  # noqa: F401
except ImportError:
    pass

from .compiled_grammar import CompiledGrammar


@dataclass
class GrammarMatcher:
        Grammar matcher with rollback support.

    Wraps CompiledGrammar with additional state management
    for speculative decoding scenarios.
    
    grammar: CompiledGrammar
    max_rollback_tokens: int = 0

    # State tracking
    _token_history: List[int] = field(default_factory=list)
    _state_history: List[Any] = field(default_factory=list)

    def accept_token(self, token_id: int) -> bool:
"""
Accept token with history tracking.        # Save state before accepting
        if self.max_rollback_tokens > 0:
            self._token_history.append(token_id)
            # Trim history if needed
            if len(self._token_history) > self.max_rollback_tokens:
                self._token_history.pop(0)

        return self.grammar.accept_token(token_id)

    def rollback(self, num_tokens: int) -> None:
"""
Rollback with history.        num_tokens = min(num_tokens, len(self._token_history))
        if num_tokens > 0:
            self._token_history = self._token_history[:-num_tokens]
            self.grammar.rollback(num_tokens)

    def reset(self) -> None:
"""
Reset matcher state.        self._token_history.clear()
        self._state_history.clear()
        self.grammar.reset()

    def fill_next_token_bitmask(self, bitmask: "np.ndarray") -> None:"        """
Fill bitmask for next token.        self.grammar.fill_bitmask(bitmask)

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""
