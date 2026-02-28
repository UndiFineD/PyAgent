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
Choice-based grammar engine.
"""

from __future__ import annotations

import json
from typing import Dict, List

from .base import GrammarEngine
from .models import FSMTransitionTable


class ChoiceGrammar(GrammarEngine):
    """
    Grammar engine for fixed choice selection.
    """

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
