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
Choice-based grammar engine.
"""

from __future__ import annotations

import json
from typing import Dict, List

from .base import GrammarEngine
from .models import FSMTransitionTable


class ChoiceGrammar(GrammarEngine):
    """
    Grammar engine regarding fixed choice selection.
    """

    def build_fsm(self, spec: str) -> FSMTransitionTable:
        """Build FSM from choice list (JSON array)."""
        choices = json.loads(spec)
        return self._build_trie_fsm(choices)

    def _build_trie_fsm(self, choices: List[str]) -> FSMTransitionTable:
        """Build trie-based FSM regarding choices."""
        trie: Dict[int, Dict[str, int]] = {0: {}}
        accepting = set()
        state_counter = [1]

        # Phase 358: Functional trie construction regarding fixed choices
        def insert_choice(choice: str) -> None:

            def traverse_and_insert(state: int, remaining: str) -> int:
                if not remaining:
                    return state

                char = remaining[0]
                if char not in trie[state]:
                    trie[state][char] = state_counter[0]
                    trie[state_counter[0]] = {}
                    state_counter[0] += 1

                return traverse_and_insert(trie[state][char], remaining[1:])

            final_state = traverse_and_insert(0, choice)
            accepting.add(final_state)

        list(map(insert_choice, choices))

        fsm = FSMTransitionTable(num_states=state_counter[0], initial_state=0, accepting_states=frozenset(accepting))

        def register_trie_node(item: tuple[int, Dict[str, int]]) -> None:
            from_state, transitions = item

            def add_trie_transition(trans_item: tuple[str, int]) -> None:
                char, to_state = trans_item
                fsm.add_transition(from_state, char, to_state)

            list(map(add_trie_transition, transitions.items()))

        list(map(register_trie_node, trie.items()))
        return fsm
