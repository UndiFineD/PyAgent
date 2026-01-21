# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Fast incremental detokenization for HuggingFace fast tokenizers.
"""

from __future__ import annotations

from typing import (
    List,
    Optional,
    Set,
    Tuple,
)

from src.infrastructure.engine.tokenization.detokenizer.types import TokenizerLike
from src.infrastructure.engine.tokenization.detokenizer.stop_checker import StopChecker
from src.infrastructure.engine.tokenization.detokenizer.base import IncrementalDetokenizer

# Try to import Rust accelerations
try:
    from rust_core import update_prefix_offset_rust
    HAS_RUST = True
except ImportError:
    HAS_RUST = False

class FastIncrementalDetokenizer(IncrementalDetokenizer):
    """
    Fast incremental detokenizer for HuggingFace fast tokenizers.
    """

    def __init__(
        self,
        tokenizer: TokenizerLike,
        skip_special_tokens: bool = True,
        spaces_between_special_tokens: bool = True,
        stop_checker: Optional[StopChecker] = None,
    ):
        super().__init__(
            tokenizer,
            skip_special_tokens,
            spaces_between_special_tokens,
            stop_checker,
        )
        self._special_token_ids: Optional[Set[int]] = None

    @property
    def special_token_ids(self) -> Set[int]:
        """Get special token IDs (cached)."""
        if self._special_token_ids is None:
            self._special_token_ids = set()
            if hasattr(self.tokenizer, 'all_special_ids'):
                self._special_token_ids = set(self.tokenizer.all_special_ids)
            elif hasattr(self.tokenizer, 'special_tokens_map'):
                for name, token in self.tokenizer.special_tokens_map.items():
                    if isinstance(token, str):
                        tid = self.tokenizer.convert_tokens_to_ids(token)
                        if isinstance(tid, int):
                            self._special_token_ids.add(tid)
        return self._special_token_ids

    def _decode_tokens(
        self,
        token_ids: List[int],
        prefix_offset: int,
        read_offset: int,
    ) -> Tuple[str, int, int]:
        """Decode tokens using fast tokenizer approach."""
        if not token_ids:
            return "", prefix_offset, read_offset
        
        if HAS_RUST:
            new_prefix, new_read = update_prefix_offset_rust(
                len(token_ids),
                prefix_offset,
                read_offset,
            )
        else:
            new_prefix = max(len(token_ids) - 6, 0)
            new_read = len(token_ids)
        
        if new_prefix > 0:
            prefix_text = self.tokenizer.decode(
                token_ids[:new_prefix],
                skip_special_tokens=self.skip_special_tokens,
            )
        else:
            prefix_text = ""
        
        full_text = self.tokenizer.decode(
            token_ids[:new_read],
            skip_special_tokens=self.skip_special_tokens,
        )
        
        if len(full_text) > len(prefix_text):
            new_text = full_text[len(prefix_text):]
        else:
            new_text = ""
        
        return new_text, new_prefix, new_read
