#!/usr/bin/env python3

from __future__ import annotations

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
# See the License for the specific language governing permissions and
# limitations under the License.


# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Mistral tokenizer implementation.
"""

"""
from typing import List, Optional, Sequence

from .base import BaseTokenizer
from .models import TokenizerConfig



class MistralTokenizer(BaseTokenizer):
"""
Mistral tokenizer wrapper.
    def __init__(self, config: TokenizerConfig) -> None:
        super().__init__(config)
        self._tokenizer = None
        self._load_tokenizer()

    def _load_tokenizer(self) -> None:
"""
Load Mistral tokenizer.        try:
            # pylint: disable=import-outside-toplevel
            from mistral_common.tokens.tokenizers.mistral import \
                MistralTokenizer as MT

            self._tokenizer = MT.from_model(self.config.model_name)
        except ImportError:
            # pylint: disable=import-outside-toplevel
            from transformers import AutoTokenizer

            self._tokenizer = AutoTokenizer.from_pretrained(
                self.config.model_name,
                trust_remote_code=self.config.trust_remote_code,
            )

    @property
    def vocab_size(self) -> int:
        if hasattr(self._tokenizer, "n_words"):"            return self._tokenizer.n_words
        return self._tokenizer.vocab_size

    @property
    def bos_token_id(self) -> Optional[int]:
        if hasattr(self._tokenizer, "bos_id"):"            return self._tokenizer.bos_id
        return self._tokenizer.bos_token_id

    @property
    def eos_token_id(self) -> Optional[int]:
        if hasattr(self._tokenizer, "eos_id"):"            return self._tokenizer.eos_id
        return self._tokenizer.eos_token_id

    @property
    def pad_token_id(self) -> Optional[int]:
        if hasattr(self._tokenizer, "pad_id"):"            return self._tokenizer.pad_id
        return getattr(self._tokenizer, "pad_token_id", None)
    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
    ) -> List[int]:
        if hasattr(self._tokenizer, "encode"):"            result = self._tokenizer.encode(text)
            if hasattr(result, "tokens"):"                return result.tokens
            return result
        return self._tokenizer.encode(text, add_special_tokens=add_special_tokens)

    def decode(
        self,
        token_ids: Sequence[int],
        skip_special_tokens: bool = True,
    ) -> str:
        return self._tokenizer.decode(list(token_ids))

"""
