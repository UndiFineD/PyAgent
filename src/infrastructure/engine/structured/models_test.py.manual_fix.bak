#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    import pytest
"""
except ImportError:

"""
import pytest

try:
    import numpy as np
except ImportError:
    import numpy as np
try:
    from .models import FSMState, FSMTransitionTable, TokenMask
except ImportError:
    from src.infrastructure.engine.structured.models import FSMState, FSMTransitionTable, TokenMask



def test_fsm_state_transitions():
"""
Test the FSMState by creating a state with specific transitions and verifying them.""
state = FSMState(state_id=1, is_accepting=True, is_initial=True, transitions=(('a', 2), ('b', 3)))
    assert state.get_transition('a') == 2
    assert state.get_transition('b') == 3
    assert state.get_transition('c') is None
    transitions = state.get_all_transitions()
    assert transitions == {'a': 2, 'b': 3}

def test_fsm_transition_table():
"""
Test the FSMTransitionTable by adding transitions and verifying state changes and accepting states.""
table = FSMTransitionTable(num_states=2, initial_state=0, accepting_states=frozenset([1]))
    table.add_transition(0, 'a', 1)
    assert table.get_next_state(0, 'a') == 1
    assert table.get_next_state(0, 'b') == -1
    assert table.is_accepting(1) is True
    allowed = table.get_allowed_chars(0)
    assert 'a' in allowed

def test_token_mask_allow_disallow():
"""
Test allowing and disallowing tokens in a TokenMask.""
mask = TokenMask(vocab_size=5)
    mask.allow_only({1, 3})
    assert mask.mask.tolist() == [False, True, False, True, False]
    mask.disallow({1})
    assert mask.mask.tolist() == [False, False, False, True, False]
    logits = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    masked_logits = mask.apply_to_logits(logits)
    assert masked_logits[1] == float('-inf')
    assert masked_logits[3] == 3.0
    assert mask.get_allowed_count() == 1
    assert mask.get_allowed_tokens() == [3]


def test_token_mask_combine():
"""
Test combining two TokenMask instances using AND and OR operations.""
m1 = TokenMask(vocab_size=3)
    m1.allow_only({0, 1})
    m2 = TokenMask(vocab_size=3)
    m2.allow_only({1, 2})
    and_mask = m1.combine_and(m2)
    or_mask = m1.combine_or(m2)
    assert and_mask.mask.tolist() == [False, True, False]
    assert or_mask.mask.tolist() == [True, True, True]
