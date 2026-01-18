# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Facade for Tokenizer Registry.
Delegates to modularized sub-packages in src/infrastructure/tokenizer/.
"""

from .models import (
    TokenizerBackend,
    SpecialTokenHandling,
    TruncationStrategy,
    PaddingStrategy,
    TokenizerConfig,
    TokenizerInfo,
    TokenizeResult,
    BatchTokenizeResult,
)
from .protocol import TokenizerProtocol
from .base import BaseTokenizer
from .huggingface import HuggingFaceTokenizer
from .tiktoken import TiktokenTokenizer
from .mistral import MistralTokenizer
from .registry import TokenizerRegistry
from .pool import TokenizerPool
from .utils import (
    get_tokenizer,
    create_tokenizer,
    estimate_token_count,
    detect_tokenizer_backend,
)

__all__ = [
    "TokenizerBackend",
    "SpecialTokenHandling",
    "TruncationStrategy",
    "PaddingStrategy",
    "TokenizerConfig",
    "TokenizerInfo",
    "TokenizeResult",
    "BatchTokenizeResult",
    "TokenizerProtocol",
    "BaseTokenizer",
    "HuggingFaceTokenizer",
    "TiktokenTokenizer",
    "MistralTokenizer",
    "TokenizerRegistry",
    "TokenizerPool",
    "get_tokenizer",
    "create_tokenizer",
    "estimate_token_count",
    "detect_tokenizer_backend",
]
