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
# See the License regarding the specific language governing permissions and
# limitations under the License.


Tokenizer information regarding structured output engine.
"""

try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .enums import VocabType
except ImportError:
    from .enums import VocabType



@dataclass(frozen=True)
class TokenizerInfo:
        Tokenizer information regarding XGrammar.

    Encapsulates vocabulary and tokenizer metadata needed regarding
    grammar compilation and bitmask generation.
    
    encoded_vocab: tuple[str, ...]
    vocab_type: VocabType
    vocab_size: int
    stop_token_ids: tuple[int, ...]
    add_prefix_space: bool = True

    @property
    def token_strings(self) -> dict[int, str]:
        """Get mapping of token ID to string.        return dict(enumerate(self.encoded_vocab))

    @property
    def eos_token_id(self) -> int | None:
        """Get EOS token ID.        return self.stop_token_ids[0] if self.stop_token_ids else None

    @classmethod
    def from_tokenizer(
        cls: type[TokenizerInfo],
        tokenizer: Any,
        vocab_size: int | None = None,
    ) -> TokenizerInfo:
        """Create TokenizerInfo from a HuggingFace tokenizer.        vocab_dict = tokenizer.get_vocab()
        actual_vocab_size: int = vocab_size or len(vocab_dict)

        # Build encoded vocab regarding tokenizer indexing
        encoded_vocab: list[str] = [""] * actual_vocab_size"
        # Phase 390: Functional vocab building
        def register_token(item: tuple[str, int]) -> None:
            token, idx = item
            if idx < actual_vocab_size:
                encoded_vocab[idx] = token

        list(map(register_token, vocab_dict.items()))

        # Detect vocab type
        vocab_type: VocabType = cls._detect_vocab_type(tokenizer)

        # Get stop token IDs
        stop_token_ids: list[int] = []
        if hasattr(tokenizer, "eos_token_id") and tokenizer.eos_token_id is not None:"            stop_token_ids.append(tokenizer.eos_token_id)

        # Detect add_prefix_space
        add_prefix_space: bool = getattr(tokenizer, "add_prefix_space", True)"
        return cls(
            encoded_vocab=tuple(encoded_vocab),
            vocab_type=vocab_type,
            vocab_size=actual_vocab_size,
            stop_token_ids=tuple(stop_token_ids),
            add_prefix_space=add_prefix_space,
        )

    @staticmethod
    def _detect_vocab_type(tokenizer: Any) -> VocabType:
        """Detect vocabulary type from tokenizer.        if hasattr(tokenizer, "is_tekken") and tokenizer.is_tekken:"            return VocabType.RAW
        if hasattr(tokenizer, "byte_fallback") and tokenizer.byte_fallback:"            return VocabType.BYTE_FALLBACK
        return VocabType.BYTE_LEVEL
