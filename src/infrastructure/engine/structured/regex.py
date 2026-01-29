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
Regex-based grammar engine.
"""

from __future__ import annotations

import contextlib
from sre_constants import _NamedIntConstant
import sys
import warnings
from typing import Dict, Optional, Set

from re._constants import _NamedIntConstant

from .base import GrammarEngine
from .models import FSMTransitionTable

# Handle sre_parse deprecation in Python 3.11+
if sys.version_info >= (3, 11):
    try:
        # pylint: disable=deprecated-module,ungrouped-imports
        import re._constants as _sre_constants
        import re._parser as _sre_parse
    except ImportError:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            # pylint: disable=deprecated-module,ungrouped-imports
            import sre_constants as _sre_constants  # type: ignore
            import sre_parse as _sre_parse  # type: ignore
else:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # pylint: disable=deprecated-module,ungrouped-imports
        import sre_constants as _sre_constants  # type: ignore
        import sre_parse as _sre_parse  # type: ignore

# Align constants across different Python versions
_LITERAL = _sre_constants.LITERAL
_ANY = _sre_constants.ANY
_IN = _sre_constants.IN
_RANGE = _sre_constants.RANGE
_SUBPATTERN = _sre_constants.SUBPATTERN
_MAX_REPEAT = _sre_constants.MAX_REPEAT
_MIN_REPEAT = _sre_constants.MIN_REPEAT
_MAXREPEAT: _NamedIntConstant | _NamedIntConstant = _sre_constants.MAXREPEAT
_BRANCH: contextlib.Any | None = getattr(_sre_constants, "BRANCH", None)


class RegexGrammar(GrammarEngine):
    """
    Regex-based grammar engine.
    """

    def __init__(
        self,
        vocab_size: int,
        token_strings: Optional[Dict[int, str]] = None,
        eos_token_id: Optional[int] = None,
    ) -> None:
        super().__init__(vocab_size, token_strings, eos_token_id)
        self._compiled_cache: Dict[str, FSMTransitionTable] = {}

    def build_fsm(self, spec: str) -> FSMTransitionTable:
        """Build DFA from regex pattern."""
        if spec in self._compiled_cache:
            return self._compiled_cache[spec]

        with contextlib.suppress(Exception):
            parsed = _sre_parse.parse(spec)
            nfa = self._build_nfa(parsed)
            dfa: FSMTransitionTable = self._nfa_to_dfa(nfa)
            self._compiled_cache[spec] = dfa
            return dfa

        return self._build_simple_fsm(spec)

    def _build_nfa(self, parsed) -> Dict:
        """Build NFA from parsed regex."""
        nfa: Dict[int, Dict[str, Set[int]]] = {0: {}}
        state_counter: list[int] = [1]
        accepting = set()

        def _process_item(op, av, state: int) -> Set[int]:
            new_end_states = set()
            if state not in nfa:
                nfa[state] = {}

            if op == _LITERAL:
                char: str = chr(av)
                new_state: int = state_counter[0]
                state_counter[0] += 1
                if char not in nfa[state]:
                    nfa[state][char] = set()
                nfa[state][char].add(new_state)
                new_end_states.add(new_state)
            elif op == _ANY:
                new_state: int = state_counter[0]
                state_counter[0] += 1
                for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ":
                    if c not in nfa[state]:
                        nfa[state][c] = set()
                    nfa[state][c].add(new_state)
                new_end_states.add(new_state)
            elif op == _IN:
                new_state: int = state_counter[0]
                state_counter[0] += 1
                for item_op, item_av in av:
                    if item_op == _LITERAL:
                        char: str = chr(item_av)
                        if char not in nfa[state]:
                            nfa[state][char] = set()
                        nfa[state][char].add(new_state)
                    elif item_op == _RANGE:
                        for code in range(item_av[0], item_av[1] + 1):
                            char: str = chr(code)
                            if char not in nfa[state]:
                                nfa[state][char] = set()
                            nfa[state][char].add(new_state)
                new_end_states.add(new_state)
            elif op == _SUBPATTERN:
                _, _, _, subpattern = av
                sub_end: Set[int] = process_pattern(subpattern, state)
                new_end_states.update(sub_end)
            elif op in (_MAX_REPEAT, _MIN_REPEAT):
                min_count, max_count, subpattern = av
                current_states: Set[int] = {state}
                for _ in range(min(min_count, 10)):
                    next_states = set()
                    for s in current_states:
                        ends: Set[int] = process_pattern(subpattern, s)
                        next_states.update(ends)
                    current_states = next_states
                if max_count > min_count or max_count == _MAXREPEAT:
                    self._apply_repeat_loop(nfa, current_states, subpattern, process_pattern)
                new_end_states.update(current_states)
            else:
                new_end_states.add(state)
            return new_end_states

        def process_pattern(pattern, start_state: int) -> Set[int]:
            end_states: Set[int] = {start_state}
            for op, av in pattern:
                new_total_end_states = set()
                for state in end_states:
                    new_total_end_states.update(_process_item(op, av, state))
                end_states = new_total_end_states if new_total_end_states else end_states
            return end_states

        final_states: Set[int] = process_pattern(parsed, 0)
        accepting.update(final_states)
        return {"nfa": nfa, "accepting": accepting, "initial": 0}

    def _nfa_to_dfa(self, nfa_data: Dict) -> FSMTransitionTable:
        """Convert NFA to DFA."""
        nfa = nfa_data["nfa"]
        accepting = nfa_data["accepting"]
        initial = nfa_data["initial"]
        dfa_states = {}
        dfa_transitions: Dict[int, Dict[str, int]] = {}
        dfa_accepting = set()
        initial_set = frozenset({initial})
        dfa_states[initial_set] = 0
        dfa_transitions[0] = {}
        if initial in accepting:
            dfa_accepting.add(0)
        worklist = [initial_set]
        state_counter = 1
        while worklist:
            current_set = worklist.pop()
            current_dfa = dfa_states[current_set]
            all_chars = set()
            for nfa_state in current_set:
                if nfa_state in nfa:
                    all_chars.update(nfa[nfa_state].keys())
            for char in all_chars:
                next_set = set()
                for nfa_state in current_set:
                    if nfa_state in nfa and char in nfa[nfa_state]:
                        next_set.update(nfa[nfa_state][char])
                if not next_set:
                    continue
                next_frozen = frozenset(next_set)
                if next_frozen not in dfa_states:
                    dfa_states[next_frozen] = state_counter
                    dfa_transitions[state_counter] = {}
                    if next_set & accepting:
                        dfa_accepting.add(state_counter)
                    worklist.append(next_frozen)
                    state_counter += 1
                dfa_transitions[current_dfa][char] = dfa_states[next_frozen]
        fsm = FSMTransitionTable(num_states=state_counter, initial_state=0, accepting_states=frozenset(dfa_accepting))
        for from_state, transitions in dfa_transitions.items():
            for char, to_state in transitions.items():
                fsm.add_transition(from_state, char, to_state)
        return fsm

    def _apply_repeat_loop(self, nfa, current_states, subpattern, process_pattern_fn) -> None:
        """Apply repeat loop transitions to NFA."""
        for s in current_states:
            loop_ends = process_pattern_fn(subpattern, s)
            for end in loop_ends:
                s_transitions = nfa.get(s, {})
                if end not in nfa:
                    nfa[end] = {}
                end_transitions = nfa[end]
                for char, targets in s_transitions.items():
                    if char not in end_transitions:
                        end_transitions[char] = targets.copy()

    def _build_simple_fsm(self, spec: str) -> FSMTransitionTable:
        """Build simple FSM for literal pattern matching."""
        fsm = FSMTransitionTable(num_states=len(spec) + 1, initial_state=0, accepting_states=frozenset({len(spec)}))
        for i, char in enumerate(spec):
            fsm.add_transition(i, char, i + 1)
        return fsm
