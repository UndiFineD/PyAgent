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
Wrappers for grammar integration with inference engine.
"""

from typing import List, Optional

try:
    import numpy as np  # noqa: F401

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from .compiled_grammar import CompiledGrammar
from .grammar_matcher import GrammarMatcher


class XGrammarGrammar:
    """
    XGrammar grammar wrapper.

    Provides the interface expected by the structured output system
    while wrapping the internal grammar matcher.
    """

    def __init__(
        self,
        matcher: GrammarMatcher,
        vocab_size: int,
        ctx: Optional[CompiledGrammar] = None,
    ) -> None:
        self.matcher = matcher
        self.vocab_size = vocab_size
        self.ctx = ctx
        self._jump_forward_string: Optional[str] = None

    def accept_token(self, token_id: int) -> bool:
        """Accept a token."""
        return self.matcher.accept_token(token_id)

    def rollback(self, num_tokens: int) -> None:
        """Rollback tokens."""
        self.matcher.rollback(num_tokens)

    def reset(self) -> None:
        """Reset grammar state."""
        self.matcher.reset()

    def is_terminated(self) -> bool:
        """Check if grammar is terminated."""
        return self.matcher.grammar.is_terminated()

    def fill_next_token_bitmask(self, bitmask: "np.ndarray") -> None:
        """Fill bitmask for next token."""
        self.matcher.fill_next_token_bitmask(bitmask)

    def jump_forward_string(self) -> Optional[str]:
        """Get jump-forward string if available."""
        return self._jump_forward_string


class CompositeGrammar:
    """
    Composite grammar for combining multiple constraints.

    Beyond vLLM: Allows chaining multiple grammars for complex constraints.
    """

    def __init__(self, grammars: List[XGrammarGrammar]) -> None:
        self.grammars = grammars
        self.vocab_size = grammars[0].vocab_size if grammars else 0

    def accept_token(self, token_id: int) -> bool:
        """Accept token in all grammars."""
        return all(g.accept_token(token_id) for g in self.grammars)

    def rollback(self, num_tokens: int) -> None:
        """Rollback all grammars."""
        for g in self.grammars:
            g.rollback(num_tokens)

    def reset(self) -> None:
        """Reset all grammars."""
        for g in self.grammars:
            g.reset()

    def is_terminated(self) -> bool:
        """Check if all grammars are terminated."""
        return all(g.is_terminated() for g in self.grammars)

    def fill_next_token_bitmask(self, bitmask: "np.ndarray") -> None:
        """Fill bitmask with intersection of all grammar constraints."""
        if not HAS_NUMPY or not self.grammars:
            return

        # Start with all ones
        bitmask.fill(1)

        # Apply each grammar's constraints (intersection)
        temp_mask = np.ones_like(bitmask)
        for grammar in self.grammars:
            temp_mask.fill(1)
            grammar.fill_next_token_bitmask(temp_mask)
            bitmask &= temp_mask
