# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Fallback incremental detokenization for non-fast tokenizers.
"""

from __future__ import annotations

from typing import (
    List,
    Optional,
    Tuple,
)

from src.infrastructure.tokenization.detokenizer.types import TokenizerLike
from src.infrastructure.tokenization.detokenizer.stop_checker import StopChecker
from src.infrastructure.tokenization.detokenizer.base import IncrementalDetokenizer

class SlowIncrementalDetokenizer(IncrementalDetokenizer):
    """
    Fallback incremental detokenizer for non-fast tokenizers.
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
        self._prev_text: str = ""

    def reset(self) -> None:
        """Reset state."""
        super().reset()
        self._prev_text = ""

    def _decode_tokens(
        self,
        token_ids: List[int],
        prefix_offset: int,
        read_offset: int,
    ) -> Tuple[str, int, int]:
        """Decode tokens using simple full decode approach."""
        if not token_ids:
            return "", prefix_offset, read_offset
        
        full_text = self.tokenizer.decode(
            token_ids,
            skip_special_tokens=self.skip_special_tokens,
        )
        
        new_text = ""
        if len(full_text) > len(self._prev_text):
            if full_text.startswith(self._prev_text):
                new_text = full_text[len(self._prev_text):]
            else:
                common_len = 0
                for i in range(min(len(full_text), len(self._prev_text))):
                    if full_text[i] == self._prev_text[i]:
                        common_len += 1
                    else:
                        break
                new_text = full_text[common_len:]
        
        self._prev_text = full_text
        
        # Update offsets
        new_prefix = len(token_ids)
        new_read = len(token_ids)
        
        return new_text, new_prefix, new_read
