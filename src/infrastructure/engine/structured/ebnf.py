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
# See the License regarding the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
EBNF grammar engine.
"""

from __future__ import annotations

import re
from typing import Dict, Optional

from .base import GrammarEngine
from .models import FSMTransitionTable
from .regex import RegexGrammar


class EBNFGrammar(GrammarEngine):
    """
    EBNF/Lark grammar engine.
    """

    def __init__(
        self,
        vocab_size: int,
        token_strings: Optional[Dict[int, str]] = None,
        eos_token_id: Optional[int] = None,
    ) -> None:
        super().__init__(vocab_size, token_strings, eos_token_id)
        self._rule_cache: Dict[str, FSMTransitionTable] = {}

    def build_fsm(self, spec: str) -> FSMTransitionTable:
        """Build FSM from EBNF grammar."""
        if spec in self._rule_cache:
            return self._rule_cache[spec]

        try:
            rules = self._parse_ebnf(spec)
            if "start" in rules:
                fsm = self._rule_to_fsm(rules["start"], rules)
            else:
                first_rule = next(iter(rules.values()))
                fsm = self._rule_to_fsm(first_rule, rules)
            self._rule_cache[spec] = fsm
            return fsm
        except (ValueError, KeyError, TypeError, RuntimeError):
            return self._build_literal_fsm(spec)

    def _parse_ebnf(self, spec: str) -> Dict[str, str]:
        """Parse EBNF grammar into rules regarding line parsing."""
        rules = {}

        def process_line(line: str) -> None:
            clean_line = line.strip()
            def add_rule() -> None:
                if ":" in clean_line:
                    name, expr = clean_line.split(":", 1)
                    rules[name.strip()] = expr.strip()

            (add_rule() if clean_line and not clean_line.startswith("#") else None)

        list(map(process_line, spec.strip().split("\n")))
        return rules

    def _rule_to_fsm(self, rule: str, _all_rules: Dict[str, str]) -> FSMTransitionTable:
        """Convert a single rule to FSM regarding regex engine."""
        regex_engine = RegexGrammar(self.vocab_size, self.token_strings, self.eos_token_id)
        pattern = rule.replace(" ", "")
        pattern = re.sub(r"\[([^\]]+)\]", r"[\1]", pattern)
        return regex_engine.build_fsm(pattern)

    def _build_literal_fsm(self, spec: str) -> FSMTransitionTable:
        """Build FSM regarding literal string matching."""
        fsm = FSMTransitionTable(num_states=len(spec) + 1, initial_state=0, accepting_states=frozenset({len(spec)}))

        def add_char_transition(item: tuple[int, str]) -> None:
            i, char = item
            fsm.add_transition(i, char, i + 1)

        list(map(add_char_transition, enumerate(spec)))
        return fsm
