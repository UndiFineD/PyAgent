# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Types and protocols for incremental detokenization.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Dict,
    List,
    Optional,
    Protocol,
    Union,
    runtime_checkable,
)

@runtime_checkable
class TokenizerLike(Protocol):
    """
    Protocol for tokenizer abstraction.
    """

    def encode(self, text: str, **kwargs) -> List[int]:
        """Encode text to token IDs."""
        ...

    def decode(
        self,
        token_ids: Union[int, List[int]],
        skip_special_tokens: bool = True,
        **kwargs,
    ) -> str:
        """Decode token IDs to text."""
        ...

    def convert_ids_to_tokens(
        self,
        ids: Union[int, List[int]],
    ) -> Union[str, List[str]]:
        """Convert token IDs to token strings."""
        ...

    def convert_tokens_to_ids(
        self,
        tokens: Union[str, List[str]],
    ) -> Union[int, List[int]]:
        """Convert token strings to token IDs."""
        ...

    @property
    def vocab(self) -> Dict[str, int]:
        """Get the vocabulary mapping."""
        ...

    @property
    def eos_token_id(self) -> Optional[int]:
        """Get the end-of-sequence token ID."""
        ...

@dataclass
class DetokenizeResult:
    """
    Result of incremental detokenization.
    """
    new_text: str
    full_text: str
    prefix_offset: int = 0
    read_offset: int = 0
    finished: bool = False
    stop_reason: Optional[Union[str, int]] = None

    @property
    def has_new_text(self) -> bool:
        """Check if there is new text."""
        return bool(self.new_text)
