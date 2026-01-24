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
Tiktoken tokenizer implementation.
"""

from __future__ import annotations

from typing import List, Optional, Sequence

from .base import BaseTokenizer
from .models import TokenizerConfig


class TiktokenTokenizer(BaseTokenizer):
    """OpenAI tiktoken tokenizer wrapper."""

    MODEL_ENCODINGS = {
        "gpt-4": "cl100k_base",
        "gpt-4o": "o200k_base",
        "gpt-4-turbo": "cl100k_base",
        "gpt-3.5-turbo": "cl100k_base",
        "text-embedding-ada-002": "cl100k_base",
        "text-embedding-3-small": "cl100k_base",
        "text-embedding-3-large": "cl100k_base",
    }

    def __init__(self, config: TokenizerConfig):
        super().__init__(config)
        self._encoding = None
        self._load_tokenizer()

    def _load_tokenizer(self):
        """Load tiktoken encoding."""
        try:
            import tiktoken

            model_name = self.config.model_name.lower()
            if model_name in ["cl100k_base", "p50k_base", "r50k_base", "o200k_base"]:
                self._encoding = tiktoken.get_encoding(model_name)
            else:
                encoding_name = self.MODEL_ENCODINGS.get(model_name)
                if encoding_name:
                    self._encoding = tiktoken.get_encoding(encoding_name)
                else:
                    try:
                        self._encoding = tiktoken.encoding_for_model(model_name)
                    except KeyError:
                        self._encoding = tiktoken.get_encoding("cl100k_base")
        except ImportError:
            raise ImportError("tiktoken package required for Tiktoken tokenizer")

    @property
    def vocab_size(self) -> int:
        return self._encoding.n_vocab

    @property
    def bos_token_id(self) -> Optional[int]:
        return None

    @property
    def eos_token_id(self) -> Optional[int]:
        try:
            return self._encoding.encode("<|endoftext|>", allowed_special={"<|endoftext|>"})[0]
        except Exception:
            return None

    @property
    def pad_token_id(self) -> Optional[int]:
        return None

    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
    ) -> List[int]:
        return self._encoding.encode(text)

    def decode(
        self,
        token_ids: Sequence[int],
        skip_special_tokens: bool = True,
    ) -> str:
        return self._encoding.decode(list(token_ids))

    def encode_batch(
        self,
        texts: List[str],
        add_special_tokens: bool = True,
    ) -> List[List[int]]:
        return self._encoding.encode_batch(texts)

    def estimate_tokens(self, text: str) -> int:
        return len(self._encoding.encode(text))
