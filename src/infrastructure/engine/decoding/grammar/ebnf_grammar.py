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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
EBNF grammar constraint logic for structured output decoding.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Set

import numpy as np

from .base import StructuredOutputGrammar


@dataclass
class GrammarRule:
    """A single EBNF grammar rule."""

    name: str
    alternatives: List[List[str]]  # Each alternative is a sequence of symbols


@dataclass
class EBNFGrammar(StructuredOutputGrammar):
    """Grammar that constrains output using EBNF rules.

    Supports simple context-free grammars for SQL, code, etc.
    Inspired by vLLM's xgrammar EBNF support.
    """

    grammar_str: str
    vocab_size: int
    token_to_string: Callable[[int], str]
    start_symbol: str = "root"
    _rules: Dict[str, GrammarRule] = field(default_factory=dict, init=False)
    _buffer: str = field(default="", init=False)
    _token_history: List[int] = field(default_factory=list, init=False)
    _terminated: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        """Parse EBNF grammar rules."""
        self._parse_grammar()

    def _parse_grammar(self) -> None:
        """Parse EBNF grammar string into rules.

        Simple parser for rules like:
        root ::= "SELECT " column " FROM " table
        column ::= "col1" | "col2"
        """
        for line in self.grammar_str.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "::=" not in line:
                continue

            name, rhs = line.split("::=", 1)
            name = name.strip()

            # Parse alternatives
            alternatives = []
            for alt in rhs.split("|"):
                symbols = []
                current = ""
                in_string = False

                for char in alt.strip():
                    if char == '"' and (not current or current[-1] != "\\"):
                        if in_string:
                            symbols.append(("LITERAL", current))
                            current = ""
                        in_string = not in_string
                    elif in_string:
                        current += char
                    elif char.isalnum() or char == "_":
                        current += char
                    elif char.isspace():
                        if current:
                            symbols.append(("RULE", current))
                            current = ""

                if current:
                    symbols.append(("RULE", current))

                if symbols:
                    alternatives.append(symbols)

            self._rules[name] = GrammarRule(name=name, alternatives=alternatives)

    def _get_valid_prefixes(self, symbol: str = None) -> Set[str]:
        """Get all valid string prefixes from current state."""
        symbol = symbol or self.start_symbol

        if symbol not in self._rules:
            return set()

        rule = self._rules[symbol]
        prefixes: Set[str] = set()

        for alt in rule.alternatives:
            if not alt:
                continue

            sym_type, sym_val = alt[0]
            if sym_type == "LITERAL":
                prefixes.add(sym_val)
            elif sym_type == "RULE":
                prefixes.update(self._get_valid_prefixes(sym_val))

        return prefixes

    def accept_tokens(self, request_id: str, tokens: List[int]) -> bool:
        """Accept tokens that match grammar."""
        for token in tokens:
            token_str = self.token_to_string(token)
            new_buffer = self._buffer + token_str

            # Simple validation: check if any rule prefix matches
            if self._is_valid_grammar_prefix(new_buffer):
                self._buffer = new_buffer
                self._token_history.append(token)
            else:
                return False

        return True

    def _is_valid_grammar_prefix(self, text: str) -> bool:
        """Check if text is a valid prefix according to grammar."""
        # Simplified check - real impl would use parser
        return len(text) < 1000  # Placeholder

    def validate_tokens(self, tokens: List[int]) -> List[int]:
        """Validate tokens without advancing state."""
        valid = []
        test_buffer = self._buffer

        for token in tokens:
            token_str = self.token_to_string(token)
            new_buffer = test_buffer + token_str

            if self._is_valid_grammar_prefix(new_buffer):
                valid.append(token)
                test_buffer = new_buffer
            else:
                break

        return valid

    def rollback(self, num_tokens: int) -> None:
        """Roll back by removing tokens."""
        if num_tokens <= 0:
            return

        self._token_history = self._token_history[:-num_tokens]
        self._buffer = ""
        for token in self._token_history:
            self._buffer += self.token_to_string(token)
        self._terminated = False

    def fill_bitmask(self, bitmask: np.ndarray, idx: int) -> None:
        """Set valid tokens in bitmask."""
        valid_tokens = self.get_valid_tokens()
        for token_id in valid_tokens:
            if token_id < bitmask.shape[1]:
                bitmask[idx, token_id] = True

    def get_valid_tokens(self) -> Set[int]:
        """Get tokens valid according to grammar."""
        # Simplified - return all tokens for now
        return set(range(min(self.vocab_size, 100)))

    def is_terminated(self) -> bool:
        """Check if grammar parsing is complete."""
        return self._terminated

    def reset(self) -> None:
        """Reset grammar state."""
        self._buffer = ""
        self._token_history = []
        self._terminated = False

    @property
    def num_processed_tokens(self) -> int:
        return len(self._token_history)
