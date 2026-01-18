# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Regex-based grammar engine.
"""

from __future__ import annotations

import sys
import warnings
from typing import Dict, FrozenSet, List, Optional, Set

from .models import FSMTransitionTable
from .base import GrammarEngine

# Handle sre_parse deprecation in Python 3.11+
if sys.version_info >= (3, 11):
    try:
        import re._parser as _sre_parse
    except ImportError:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            import sre_parse as _sre_parse
else:
    import sre_parse as _sre_parse


class RegexGrammar(GrammarEngine):
    """
    Regex-based grammar engine.
    """
    
    def __init__(
        self,
        vocab_size: int,
        token_strings: Optional[Dict[int, str]] = None,
        eos_token_id: Optional[int] = None,
    ):
        super().__init__(vocab_size, token_strings, eos_token_id)
        self._compiled_cache: Dict[str, FSMTransitionTable] = {}
    
    def build_fsm(self, spec: str) -> FSMTransitionTable:
        """Build DFA from regex pattern."""
        if spec in self._compiled_cache:
            return self._compiled_cache[spec]
        
        try:
            parsed = _sre_parse.parse(spec)
            nfa = self._build_nfa(parsed)
            dfa = self._nfa_to_dfa(nfa)
            self._compiled_cache[spec] = dfa
            return dfa
        except Exception:
            return self._build_simple_fsm(spec)
    
    def _build_nfa(self, parsed) -> Dict:
        """Build NFA from parsed regex."""
        nfa: Dict[int, Dict[str, Set[int]]] = {0: {}}
        state_counter = [1]
        accepting = set()
        
        def process_pattern(pattern, start_state: int) -> Set[int]:
            end_states = {start_state}
            for op, av in pattern:
                new_end_states = set()
                for state in end_states:
                    if state not in nfa:
                        nfa[state] = {}
                    
                    if op == _sre_parse.LITERAL:
                        char = chr(av)
                        new_state = state_counter[0]
                        state_counter[0] += 1
                        if char not in nfa[state]:
                            nfa[state][char] = set()
                        nfa[state][char].add(new_state)
                        new_end_states.add(new_state)
                    # (Other ops: ANY, IN, SUBPATTERN, REPEAT... matching the original logic)
                    elif op == _sre_parse.ANY:
                        new_state = state_counter[0]
                        state_counter[0] += 1
                        for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ":
                            if c not in nfa[state]:
                                nfa[state][c] = set()
                            nfa[state][c].add(new_state)
                        new_end_states.add(new_state)
                    elif op == _sre_parse.IN:
                        new_state = state_counter[0]
                        state_counter[0] += 1
                        for item_op, item_av in av:
                            if item_op == _sre_parse.LITERAL:
                                char = chr(item_av)
                                if char not in nfa[state]:
                                    nfa[state][char] = set()
                                nfa[state][char].add(new_state)
                            elif item_op == _sre_parse.RANGE:
                                for code in range(item_av[0], item_av[1] + 1):
                                    char = chr(code)
                                    if char not in nfa[state]:
                                        nfa[state][char] = set()
                                    nfa[state][char].add(new_state)
                        new_end_states.add(new_state)
                    elif op == _sre_parse.SUBPATTERN:
                        _, _, _, subpattern = av
                        sub_end = process_pattern(subpattern, state)
                        new_end_states.update(sub_end)
                    elif op == _sre_parse.MAX_REPEAT or op == _sre_parse.MIN_REPEAT:
                        min_count, max_count, subpattern = av
                        current_states = {state}
                        for _ in range(min(min_count, 10)):
                            next_states = set()
                            for s in current_states:
                                ends = process_pattern(subpattern, s)
                                next_states.update(ends)
                            current_states = next_states
                        if max_count > min_count or max_count == _sre_parse.MAXREPEAT:
                            for s in current_states:
                                loop_ends = process_pattern(subpattern, s)
                                for end in loop_ends:
                                    for char, targets in nfa.get(s, {}).items():
                                        if char not in nfa.get(end, {}):
                                            if end not in nfa: nfa[end] = {}
                                            nfa[end][char] = targets.copy()
                        new_end_states.update(current_states)
                    else:
                        new_end_states.add(state)
                end_states = new_end_states if new_end_states else end_states
            return end_states
        
        final_states = process_pattern(parsed, 0)
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
        if initial in accepting: dfa_accepting.add(0)
        worklist = [initial_set]
        state_counter = 1
        while worklist:
            current_set = worklist.pop()
            current_dfa = dfa_states[current_set]
            all_chars = set()
            for nfa_state in current_set:
                if nfa_state in nfa: all_chars.update(nfa[nfa_state].keys())
            for char in all_chars:
                next_set = set()
                for nfa_state in current_set:
                    if nfa_state in nfa and char in nfa[nfa_state]:
                        next_set.update(nfa[nfa_state][char])
                if not next_set: continue
                next_frozen = frozenset(next_set)
                if next_frozen not in dfa_states:
                    dfa_states[next_frozen] = state_counter
                    dfa_transitions[state_counter] = {}
                    if next_set & accepting: dfa_accepting.add(state_counter)
                    worklist.append(next_frozen)
                    state_counter += 1
                dfa_transitions[current_dfa][char] = dfa_states[next_frozen]
        fsm = FSMTransitionTable(num_states=state_counter, initial_state=0, accepting_states=frozenset(dfa_accepting))
        for from_state, transitions in dfa_transitions.items():
            for char, to_state in transitions.items():
                fsm.add_transition(from_state, char, to_state)
        return fsm

    def _build_simple_fsm(self, spec: str) -> FSMTransitionTable:
        """Build simple FSM for literal pattern matching."""
        fsm = FSMTransitionTable(num_states=len(spec) + 1, initial_state=0, accepting_states=frozenset({len(spec)}))
        for i, char in enumerate(spec):
            fsm.add_transition(i, char, i + 1)
        return fsm
