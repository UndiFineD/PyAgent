# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Mistral tokenizer implementation.
"""

from __future__ import annotations

from typing import List, Optional, Sequence

from .models import TokenizerConfig
from .base import BaseTokenizer


class MistralTokenizer(BaseTokenizer):
    """Mistral tokenizer wrapper."""
    
    def __init__(self, config: TokenizerConfig):
        super().__init__(config)
        self._tokenizer = None
        self._load_tokenizer()
    
    def _load_tokenizer(self):
        """Load Mistral tokenizer."""
        try:
            from mistral_common.tokens.tokenizers.mistral import MistralTokenizer as MT
            self._tokenizer = MT.from_model(self.config.model_name)
        except ImportError:
            from transformers import AutoTokenizer
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.config.model_name,
                trust_remote_code=True,
            )
    
    @property
    def vocab_size(self) -> int:
        if hasattr(self._tokenizer, 'n_words'):
            return self._tokenizer.n_words
        return self._tokenizer.vocab_size
    
    @property
    def bos_token_id(self) -> Optional[int]:
        if hasattr(self._tokenizer, 'bos_id'):
            return self._tokenizer.bos_id
        return self._tokenizer.bos_token_id
    
    @property
    def eos_token_id(self) -> Optional[int]:
        if hasattr(self._tokenizer, 'eos_id'):
            return self._tokenizer.eos_id
        return self._tokenizer.eos_token_id
    
    @property
    def pad_token_id(self) -> Optional[int]:
        if hasattr(self._tokenizer, 'pad_id'):
            return self._tokenizer.pad_id
        return getattr(self._tokenizer, 'pad_token_id', None)
    
    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
    ) -> List[int]:
        if hasattr(self._tokenizer, 'encode'):
            result = self._tokenizer.encode(text)
            if hasattr(result, 'tokens'):
                return result.tokens
            return result
        return self._tokenizer.encode(text, add_special_tokens=add_special_tokens)
    
    def decode(
        self,
        token_ids: Sequence[int],
        skip_special_tokens: bool = True,
    ) -> str:
        return self._tokenizer.decode(list(token_ids))
