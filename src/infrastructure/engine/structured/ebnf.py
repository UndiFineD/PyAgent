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
    ):
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
        except Exception:
            return self._build_literal_fsm(spec)

    def _parse_ebnf(self, spec: str) -> Dict[str, str]:
        """Parse EBNF grammar into rules."""
        rules = {}
        for line in spec.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                name, expr = line.split(":", 1)
                rules[name.strip()] = expr.strip()
        return rules

    def _rule_to_fsm(self, rule: str, all_rules: Dict[str, str]) -> FSMTransitionTable:
        """Convert a single rule to FSM."""
        regex_engine = RegexGrammar(self.vocab_size, self.token_strings, self.eos_token_id)
        pattern = rule.replace(" ", "")
        pattern = re.sub(r"\[([^\]]+)\]", r"[\1]", pattern)
        return regex_engine.build_fsm(pattern)

    def _build_literal_fsm(self, spec: str) -> FSMTransitionTable:
        """Build FSM for literal string matching."""
        fsm = FSMTransitionTable(num_states=len(spec) + 1, initial_state=0, accepting_states=frozenset({len(spec)}))
        for i, char in enumerate(spec):
            fsm.add_transition(i, char, i + 1)
        return fsm
