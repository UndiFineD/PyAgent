# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Tokenizer protocols.
"""

from __future__ import annotations

from typing import List, Optional, Protocol, Sequence, runtime_checkable


@runtime_checkable
class TokenizerProtocol(Protocol):
    """Protocol for tokenizer implementations."""
    
    @property
    def vocab_size(self) -> int:
        """Size of the vocabulary."""
        ...
    
    @property
    def bos_token_id(self) -> Optional[int]:
        """Beginning of sequence token ID."""
        ...
    
    @property
    def eos_token_id(self) -> Optional[int]:
        """End of sequence token ID."""
        ...
    
    @property
    def pad_token_id(self) -> Optional[int]:
        """Padding token ID."""
        ...
    
    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
    ) -> List[int]:
        """Encode text to token IDs."""
        ...
    
    def decode(
        self,
        token_ids: Sequence[int],
        skip_special_tokens: bool = True,
    ) -> str:
        """Decode token IDs to text."""
        ...
    
    def batch_encode(
        self,
        texts: List[str],
        add_special_tokens: bool = True,
    ) -> List[List[int]]:
        """Batch encode multiple texts."""
        ...
