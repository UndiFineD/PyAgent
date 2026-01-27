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

"""
Tokenizer information for structured output engine.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from .enums import VocabType


@dataclass(frozen=True)
class TokenizerInfo:
    """
    Tokenizer information for XGrammar.

    Encapsulates vocabulary and tokenizer metadata needed for
    grammar compilation and bitmask generation.
    """

    encoded_vocab: Tuple[str, ...]
    vocab_type: VocabType
    vocab_size: int
    stop_token_ids: Tuple[int, ...]
    add_prefix_space: bool = True

    @property
    def token_strings(self) -> Dict[int, str]:
        """Get mapping of token ID to string."""
        return dict(enumerate(self.encoded_vocab))

    @property
    def eos_token_id(self) -> Optional[int]:
        """Get EOS token ID."""
        return self.stop_token_ids[0] if self.stop_token_ids else None

    @classmethod
    def from_tokenizer(
        cls,
        tokenizer: Any,
        vocab_size: Optional[int] = None,
    ) -> "TokenizerInfo":
        """Create TokenizerInfo from a HuggingFace tokenizer."""
        vocab_dict = tokenizer.get_vocab()
<<<<<<< HEAD
        actual_vocab_size: int = vocab_size or len(vocab_dict)

        # Build encoded vocab maintaining tokenizer's indexing
        encoded_vocab: list[str] = [""] * actual_vocab_size
=======
        actual_vocab_size = vocab_size or len(vocab_dict)

        # Build encoded vocab maintaining tokenizer's indexing
        encoded_vocab = [""] * actual_vocab_size
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)
        for token, idx in vocab_dict.items():
            if idx < actual_vocab_size:
                encoded_vocab[idx] = token

        # Detect vocab type
<<<<<<< HEAD
        vocab_type: VocabType = cls._detect_vocab_type(tokenizer)
=======
        vocab_type = cls._detect_vocab_type(tokenizer)
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)

        # Get stop token IDs
        stop_token_ids = []
        if hasattr(tokenizer, "eos_token_id") and tokenizer.eos_token_id is not None:
            stop_token_ids.append(tokenizer.eos_token_id)

        # Detect add_prefix_space
<<<<<<< HEAD
        add_prefix_space: Any | bool = getattr(tokenizer, "add_prefix_space", True)
=======
        add_prefix_space = getattr(tokenizer, "add_prefix_space", True)
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)

        return cls(
            encoded_vocab=tuple(encoded_vocab),
            vocab_type=vocab_type,
            vocab_size=actual_vocab_size,
            stop_token_ids=tuple(stop_token_ids),
            add_prefix_space=add_prefix_space,
        )

    @staticmethod
    def _detect_vocab_type(tokenizer: Any) -> VocabType:
        """Detect vocabulary type from tokenizer."""
        if hasattr(tokenizer, "is_tekken") and tokenizer.is_tekken:
            return VocabType.RAW
        if hasattr(tokenizer, "byte_fallback") and tokenizer.byte_fallback:
            return VocabType.BYTE_FALLBACK
        return VocabType.BYTE_LEVEL
