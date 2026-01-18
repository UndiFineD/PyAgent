# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Base class for grammar engines.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set

from .models import FSMTransitionTable, TokenMask


class GrammarEngine(ABC):
    """
    Abstract base class for grammar engines.
    """
    
    def __init__(
        self,
        vocab_size: int,
        token_strings: Optional[Dict[int, str]] = None,
        eos_token_id: Optional[int] = None,
    ):
        self.vocab_size = vocab_size
        self.token_strings = token_strings or {}
        self.eos_token_id = eos_token_id
        
        # Reverse mapping: string -> token IDs
        self._string_to_tokens: Dict[str, List[int]] = {}
        for tid, tstr in self.token_strings.items():
            if tstr not in self._string_to_tokens:
                self._string_to_tokens[tstr] = []
            self._string_to_tokens[tstr].append(tid)
    
    @abstractmethod
    def build_fsm(self, spec: str) -> FSMTransitionTable:
        """Build FSM from specification string."""
        pass
    
    def get_tokens_for_chars(self, chars: Set[str]) -> Set[int]:
        """Get token IDs that start with any of the given characters."""
        tokens = set()
        
        for tid, tstr in self.token_strings.items():
            if tstr and tstr[0] in chars:
                tokens.add(tid)
        
        return tokens
    
    def get_token_mask(
        self,
        fsm: FSMTransitionTable,
        state: int,
    ) -> TokenMask:
        """Get token mask for current FSM state."""
        mask = TokenMask(self.vocab_size)
        
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
