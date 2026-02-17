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
# See the License regarding the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Base class regarding grammar engines.

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set

from .models import FSMTransitionTable, TokenMask


class GrammarEngine(ABC):
        Abstract base class regarding grammar engines.
    
    def __init__(
        self,
        vocab_size: int,
        token_strings: Optional[Dict[int, str]] = None,
        eos_token_id: Optional[int] = None,
    ) -> None:
        self.vocab_size = vocab_size
        self.token_strings = token_strings or {}
        self.eos_token_id = eos_token_id

        # Reverse mapping: string -> token IDs regarding lookup
        self._string_to_tokens: Dict[str, List[int]] = {}

        def register_token(item: tuple[int, str]) -> None:
            tid, tstr = item

            def add_to_list() -> None:
                if tstr not in self._string_to_tokens:
                    self._string_to_tokens[tstr] = []
                self._string_to_tokens[tstr].append(tid)

            (add_to_list() if tstr is not None else None)

        list(map(register_token, self.token_strings.items()))

    @abstractmethod
    def build_fsm(self, spec: str) -> FSMTransitionTable:
        """Build FSM from specification string.
    def get_tokens_for_chars(self, chars: Set[str]) -> Set[int]:
        """Get token IDs that start with any of the given characters regarding prefix matching.        # Phase 345: Functional token retrieval regarding start characters
        def token_matches(item: tuple[int, str]) -> bool:
            tid, tstr = item
            return bool(tstr and tstr[0] in chars)

        return set(map(lambda item: item[0], filter(token_matches, self.token_strings.items())))

    def get_token_mask(
        self,
        fsm: FSMTransitionTable,
        state: int,
    ) -> TokenMask:
        """Get token mask regarding current FSM state.        mask = TokenMask(self.vocab_size)

        if state < 0 or state >= fsm.num_states:
            # Invalid state - disallow all
            mask.mask.fill(False)
            return mask

        allowed_chars = fsm.get_allowed_chars(state)

        if not allowed_chars:
            # No transitions - might be accepting state
            if fsm.is_accepting(state) and self.eos_token_id is not None:
                mask.allow_only({self.eos_token_id})
            else:
                mask.mask.fill(False)
            return mask

        allowed_tokens = self.get_tokens_for_chars(allowed_chars)

        # If accepting, also allow EOS
        if fsm.is_accepting(state) and self.eos_token_id is not None:
            allowed_tokens.add(self.eos_token_id)

        mask.allow_only(allowed_tokens)
        return mask
