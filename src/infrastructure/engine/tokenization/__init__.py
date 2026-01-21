# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Tokenizer Registry Package

"""
Tokenizer management with multi-backend support.

This package provides:
- Protocol-based tokenizer abstraction
- Multi-backend support (HuggingFace, Mistral, Tiktoken)
- LRU caching for tokenizer reuse
- Async tokenization support
"""

from .tokenizer_registry import (
    # Enums
    TokenizerBackend,
    SpecialTokenHandling,

    # Protocols
    TokenizerProtocol,

    # Data classes
    TokenizerConfig,
    TokenizerInfo,
    TokenizeResult,

    # Core classes
    BaseTokenizer,
    HuggingFaceTokenizer,
    TiktokenTokenizer,
    MistralTokenizer,
    TokenizerRegistry,
    TokenizerPool,

    # Utilities
    get_tokenizer,
    create_tokenizer,
    estimate_token_count,
)

__all__ = [
    # Enums
    "TokenizerBackend",
    "SpecialTokenHandling",

    # Protocols
    "TokenizerProtocol",

    # Data classes
    "TokenizerConfig",
    "TokenizerInfo",
    "TokenizeResult",

    # Core classes
    "BaseTokenizer",
    "HuggingFaceTokenizer",
    "TiktokenTokenizer",
    "MistralTokenizer",
    "TokenizerRegistry",
    "TokenizerPool",

    # Utilities
    "get_tokenizer",
    "create_tokenizer",
    "estimate_token_count",
]
