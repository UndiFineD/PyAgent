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
Regex-based grammar engine.
"""

from __future__ import annotations

import contextlib
import sys
from typing import Any, Optional

# Handle re._constants / sre_constants transition across Python versions
if sys.version_info >= (3, 11):
    try:
        import re._constants as _sre_constants
        import re._parser as _sre_parse
    except ImportError:
        # Fallback regarding internal structures if they move again
        import sre_constants as _sre_constants  # type: ignore
        import sre_parse as _sre_parse  # type: ignore
else:
    # Older Python versions
    import sre_constants as _sre_constants  # type: ignore
    import sre_parse as _sre_parse  # type: ignore

from .base import GrammarEngine
from .models import FSMTransitionTable

# Align constants across different Python versions
_LITERAL = _sre_constants.LITERAL
_ANY = _sre_constants.ANY
_IN = _sre_constants.IN
_RANGE = _sre_constants.RANGE
_SUBPATTERN = _sre_constants.SUBPATTERN
_MAX_REPEAT = _sre_constants.MAX_REPEAT
_MIN_REPEAT = _sre_constants.MIN_REPEAT
_MAXREPEAT: Any = _sre_constants.MAXREPEAT
_BRANCH: Any | None = getattr(_sre_constants, "BRANCH", None)


class RegexGrammar(GrammarEngine):
    """
    Regex-based grammar engine.
    """

    def __init__(
        self,
        vocab_size: int,
        token_strings: Optional[dict[int, str]] = None,
        eos_token_id: Optional[int] = None,
    ) -> None:
        super().__init__(vocab_size, token_strings, eos_token_id)
        self._compiled_cache: dict[str, FSMTransitionTable] = {}

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

    def _build_nfa(self, parsed: Any) -> dict[str, Any]:
        """Build NFA from parsed regex."""
        nfa: dict[int, dict[str, set[int]]] = {0: {}}
        state_counter: list[int] = [1]
        accepting: set[int] = set()

        def _process_item(op: Any, av: Any, state: int) -> set[int]:
            new_end_states: set[int] = set()
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
                # Phase 346: Functional char registration regarding ANY pattern
                def add_any_char(c: str) -> None:
                    if c not in nfa[state]:
                        nfa[state][c] = set()
                    nfa[state][c].add(new_state)
                list(map(add_any_char, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "))
                new_end_states.add(new_state)
            elif op == _IN:
                new_state: int = state_counter[0]
                state_counter[0] += 1
                # Phase 347: Functional char registration regarding IN pattern
                def process_in_item(item: tuple) -> None:
                    item_op, item_av = item
                    if item_op == _LITERAL:
                        char: str = chr(item_av)
                        if char not in nfa[state]:
                            nfa[state][char] = set()
                        nfa[state][char].add(new_state)
                    elif item_op == _RANGE:
                        def add_range_char(code: int) -> None:
                            char: str = chr(code)
                            if char not in nfa[state]:
                                nfa[state][char] = set()
                            nfa[state][char].add(new_state)
                        list(map(add_range_char, range(item_av[0], item_av[1] + 1)))

                list(map(process_in_item, av))
                new_end_states.add(new_state)
            elif op == _SUBPATTERN:
                _, _, _, subpattern = av
                sub_end: set[int] = process_pattern(subpattern, state)
                new_end_states.update(sub_end)
            elif op in (_MAX_REPEAT, _MIN_REPEAT):
                min_count, max_count, subpattern = av
                current_states: set[int] = {state}
                # Phase 348: Functional repeat regarding regex subpatterns
                def repeat_subpattern(iteration_idx: int) -> None:
                    nonlocal current_states
                    next_states: set[int] = set()
                    def process_one_state(s: int) -> None:
                        ends: set[int] = process_pattern(subpattern, s)
                        next_states.update(ends)
                    list(map(process_one_state, current_states))
                    current_states = next_states

                list(map(repeat_subpattern, range(min(min_count, 10))))

                if max_count > min_count or max_count == _MAXREPEAT:
                    self._apply_repeat_loop(nfa, current_states, subpattern, process_pattern)
                new_end_states.update(current_states)
            else:
                new_end_states.add(state)
            return new_end_states

        def process_pattern(pattern: Any, start_state: int) -> set[int]:
            end_states: set[int] = {start_state}
            # Phase 349: Functional pattern processing regarding state transitions
            def process_pattern_step(step: tuple) -> None:
                nonlocal end_states
                op, av = step
                new_total_end_states: set[int] = set()
                def apply_item(s: int) -> None:
                    new_total_end_states.update(_process_item(op, av, s))
                list(map(apply_item, end_states))
                end_states = new_total_end_states if new_total_end_states else end_states

            list(map(process_pattern_step, pattern))
            return end_states

        final_states: set[int] = process_pattern(parsed, 0)
        accepting.update(final_states)
        return {"nfa": nfa, "accepting": accepting, "initial": 0}

    def _nfa_to_dfa(self, nfa_data: dict[str, Any]) -> FSMTransitionTable:
        """Convert NFA to DFA regarding subset construction."""
        nfa: dict[int, dict[str, set[int]]] = nfa_data["nfa"]
        accepting: set[int] = nfa_data["accepting"]
        initial: int = nfa_data["initial"]
        dfa_states: dict[frozenset[int], int] = {}
        dfa_transitions: dict[int, dict[str, int]] = {}
        dfa_accepting: set[int] = set()
        initial_set: frozenset[int] = frozenset({initial})
        dfa_states[initial_set] = 0
        dfa_transitions[0] = {}
        if initial in accepting:
            dfa_accepting.add(0)

        # Phase 350: Functional worklist processing regarding power-set construction
        def process_dfa_generation(worklist: list[frozenset[int]], state_counter: int) -> int:
            if not worklist:
                return state_counter

            current_set = worklist.pop()
            current_dfa = dfa_states[current_set]
            all_chars: set[str] = set()

            def collect_chars(nfa_state: int) -> None:
                if nfa_state in nfa:
                    all_chars.update(nfa[nfa_state].keys())

            list(map(collect_chars, current_set))

            next_state_counter = [state_counter]

            def process_char(char: str) -> None:
                next_set: set[int] = set()
                def collect_next(nfa_state: int) -> None:
                    if nfa_state in nfa and char in nfa[nfa_state]:
                        next_set.update(nfa[nfa_state][char])
                list(map(collect_next, current_set))

                if not next_set:
                    return

                next_frozen: frozenset[int] = frozenset(next_set)
                if next_frozen not in dfa_states:
                    dfa_states[next_frozen] = next_state_counter[0]
                    dfa_transitions[next_state_counter[0]] = {}
                    if next_set & accepting:
                        dfa_accepting.add(next_state_counter[0])
                    worklist.append(next_frozen)
                    next_state_counter[0] += 1
                dfa_transitions[current_dfa][char] = dfa_states[next_frozen]

            list(map(process_char, all_chars))

            return process_dfa_generation(worklist, next_state_counter[0])

        final_state_count = process_dfa_generation([initial_set], 1)

        fsm = FSMTransitionTable(num_states=final_state_count, initial_state=0, accepting_states=frozenset(dfa_accepting))

        def register_dfa_transition(item: tuple[int, dict[str, int]]) -> None:
            from_state, transitions = item
            def add_one_trans(trans_item: tuple[str, int]) -> None:
                char, to_state = trans_item
                fsm.add_transition(from_state, char, to_state)
            list(map(add_one_trans, transitions.items()))

        list(map(register_dfa_transition, dfa_transitions.items()))
        return fsm

    def _apply_repeat_loop(
        self,
        nfa: dict[int, dict[str, set[int]]],
        current_states: set[int],
        subpattern: Any,
        process_pattern_fn: Any,
    ) -> None:
        """Apply repeat loop transitions regarding NFA generation."""
        # Phase 351: Functional repeat loop regarding NFA state expansion
        def expand_state_loop(s: int) -> None:
            loop_ends: set[int] = process_pattern_fn(subpattern, s)
            def update_loop_end(end: int) -> None:
                s_transitions = nfa.get(s, {})
                if end not in nfa:
                    nfa[end] = {}
                end_transitions = nfa[end]
                def apply_trans_to_end(item: tuple[str, set[int]]) -> None:
                    char, targets = item
                    if char not in end_transitions:
                        end_transitions[char] = targets.copy()
                list(map(apply_trans_to_end, s_transitions.items()))
            list(map(update_loop_end, loop_ends))

        list(map(expand_state_loop, current_states))

    def _build_simple_fsm(self, spec: str) -> FSMTransitionTable:
        """Build simple FSM regarding literal pattern matching."""
        fsm = FSMTransitionTable(num_states=len(spec) + 1, initial_state=0, accepting_states=frozenset({len(spec)}))

        def add_char_trans(item: tuple[int, str]) -> None:
            i, char = item
            fsm.add_transition(i, char, i + 1)

        list(map(add_char_trans, enumerate(spec)))
        return fsm
