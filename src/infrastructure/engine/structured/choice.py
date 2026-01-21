# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Choice-based grammar engine.
"""

from __future__ import annotations

import json
from typing import Dict, List, Optional

from .models import FSMTransitionTable
from .base import GrammarEngine


class ChoiceGrammar(GrammarEngine):
    """
    Grammar engine for fixed choice selection.
    """

    def __init__(
        self,
        vocab_size: int,
        token_strings: Optional[Dict[int, str]] = None,
        eos_token_id: Optional[int] = None,
    ):
        super().__init__(vocab_size, token_strings, eos_token_id)

    def build_fsm(self, spec: str) -> FSMTransitionTable:
        """Build FSM from choice list (JSON array)."""
        choices = json.loads(spec)
        return self._build_trie_fsm(choices)

    def _build_trie_fsm(self, choices: List[str]) -> FSMTransitionTable:
        """Build trie-based FSM for choices."""
        trie: Dict[int, Dict[str, int]] = {0: {}}
        accepting = set()
        state_counter = 1

        for choice in choices:
            current_state = 0
            for char in choice:
                if char not in trie[current_state]:
                    trie[current_state][char] = state_counter
                    trie[state_counter] = {}
                    state_counter += 1
                current_state = trie[current_state][char]
            accepting.add(current_state)

        fsm = FSMTransitionTable(num_states=state_counter, initial_state=0, accepting_states=frozenset(accepting))
        for from_state, transitions in trie.items():
            for char, to_state in transitions.items():
                fsm.add_transition(from_state, char, to_state)
        return fsm
