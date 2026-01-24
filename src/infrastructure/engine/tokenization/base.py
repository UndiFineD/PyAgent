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
Base class for tokenizers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Sequence

from .models import TokenizerConfig, TokenizeResult, TokenizerInfo


class BaseTokenizer(ABC):
    """Abstract base class for tokenizers."""

    def __init__(self, config: TokenizerConfig):
        self.config = config
        self._info: Optional[TokenizerInfo] = None

    @property
    @abstractmethod
    def vocab_size(self) -> int:
        """Size of the vocabulary."""
        pass

    @property
    @abstractmethod
    def bos_token_id(self) -> Optional[int]:
        """Beginning of sequence token ID."""
        pass

    @property
    @abstractmethod
    def eos_token_id(self) -> Optional[int]:
        """End of sequence token ID."""
        pass

    @property
    @abstractmethod
    def pad_token_id(self) -> Optional[int]:
        """Padding token ID."""
        pass

    @abstractmethod
    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
    ) -> List[int]:
        """Encode text to token IDs."""
        pass

    @abstractmethod
    def decode(
        self,
        token_ids: Sequence[int],
        skip_special_tokens: bool = True,
    ) -> str:
        """Decode token IDs to text."""
        pass

    def batch_encode(
        self,
        texts: List[str],
        add_special_tokens: bool = True,
    ) -> List[List[int]]:
        """Batch encode multiple texts."""
        return [self.encode(text, add_special_tokens) for text in texts]

    def batch_decode(
        self,
        token_ids_list: List[Sequence[int]],
        skip_special_tokens: bool = True,
    ) -> List[str]:
        """Batch decode multiple token sequences."""
        return [self.decode(ids, skip_special_tokens) for ids in token_ids_list]

    def tokenize(
        self,
        text: str,
        add_special_tokens: bool = True,
        return_offsets: bool = False,
    ) -> TokenizeResult:
        """Full tokenization with metadata."""
        input_ids = self.encode(text, add_special_tokens)
        return TokenizeResult(
            input_ids=input_ids,
            attention_mask=[1] * len(input_ids),
            num_tokens=len(input_ids),
        )

    def get_info(self) -> TokenizerInfo:
        """Get tokenizer information."""
        if self._info is None:
            self._info = TokenizerInfo(
                backend=self.config.backend,
                vocab_size=self.vocab_size,
                bos_token_id=self.bos_token_id,
                eos_token_id=self.eos_token_id,
                pad_token_id=self.pad_token_id,
                max_length=self.config.max_length or 8192,
                model_name=self.config.model_name,
            )
        return self._info

    def estimate_tokens(self, text: str) -> int:
        """Fast token count estimation without full tokenization."""
        return max(1, len(text) // 4)
