# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
HuggingFace tokenizer implementation.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence

from .models import TokenizerConfig, TokenizerInfo, TokenizerBackend
from .base import BaseTokenizer


class HuggingFaceTokenizer(BaseTokenizer):
    """HuggingFace transformers tokenizer wrapper."""
    
    def __init__(self, config: TokenizerConfig):
        super().__init__(config)
        self._tokenizer = None
        self._load_tokenizer()
    
    def _load_tokenizer(self):
        """Load the HuggingFace tokenizer."""
        try:
            from transformers import AutoTokenizer
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.config.model_name,
                revision=self.config.revision,
                trust_remote_code=self.config.trust_remote_code,
                use_fast=self.config.use_fast,
            )
            if self._tokenizer.pad_token is None:
                if self._tokenizer.eos_token is not None:
                    self._tokenizer.pad_token = self._tokenizer.eos_token
                else:
                    self._tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        except ImportError:
            raise ImportError("transformers package required for HuggingFace tokenizer")
    
    @property
    def vocab_size(self) -> int:
        return self._tokenizer.vocab_size
    
    @property
    def bos_token_id(self) -> Optional[int]:
        return self._tokenizer.bos_token_id
    
    @property
    def eos_token_id(self) -> Optional[int]:
        return self._tokenizer.eos_token_id
    
    @property
    def pad_token_id(self) -> Optional[int]:
        return self._tokenizer.pad_token_id
    
    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
    ) -> List[int]:
        return self._tokenizer.encode(text, add_special_tokens=add_special_tokens)
    
    def decode(
        self,
        token_ids: Sequence[int],
        skip_special_tokens: bool = True,
    ) -> str:
        return self._tokenizer.decode(token_ids, skip_special_tokens=skip_special_tokens)
    
    def batch_encode(
        self,
        texts: List[str],
        add_special_tokens: bool = True,
    ) -> List[List[int]]:
        result = self._tokenizer(
            texts,
            add_special_tokens=add_special_tokens,
            padding=False,
            truncation=False,
        )
        return result["input_ids"]
    
    def apply_chat_template(
        self,
        messages: List[Dict[str, str]],
        add_generation_prompt: bool = True,
    ) -> str:
        """Apply chat template to messages."""
        if hasattr(self._tokenizer, 'apply_chat_template'):
            return self._tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=add_generation_prompt,
            )
        raise ValueError("Tokenizer does not support chat templates")
    
    def get_info(self) -> TokenizerInfo:
        if self._info is None:
            has_chat = hasattr(self._tokenizer, 'chat_template') and self._tokenizer.chat_template is not None
            self._info = TokenizerInfo(
                backend=TokenizerBackend.HUGGINGFACE,
                vocab_size=self.vocab_size,
                bos_token_id=self.bos_token_id,
                eos_token_id=self.eos_token_id,
                pad_token_id=self.pad_token_id,
                max_length=self._tokenizer.model_max_length,
                model_name=self.config.model_name,
                is_fast=self._tokenizer.is_fast if hasattr(self._tokenizer, 'is_fast') else False,
                supports_chat_template=has_chat,
                chat_template=self._tokenizer.chat_template if has_chat else None,
            )
        return self._info
