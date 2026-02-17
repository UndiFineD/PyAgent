#!/usr/bin/env python3
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

# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Tokenizer Registry Package

Tokenizer management with multi-backend support.

This package provides:
- Protocol-based tokenizer abstraction
- Multi-backend support (HuggingFace, Mistral, Tiktoken)
- LRU caching for tokenizer reuse
- Async tokenization support

from .tokenizer_registry import (  # Enums; Protocols; Data classes; Core classes; Utilities  # noqa: F401
    BaseTokenizer, HuggingFaceTokenizer, MistralTokenizer,
    SpecialTokenHandling, TiktokenTokenizer, TokenizerBackend, TokenizerConfig,
    TokenizeResult, TokenizerInfo, TokenizerPool, TokenizerProtocol,
    TokenizerRegistry, create_tokenizer, estimate_token_count, get_tokenizer)

__all__ = [
    # Enums
    "TokenizerBackend","    "SpecialTokenHandling","    # Protocols
    "TokenizerProtocol","    # Data classes
    "TokenizerConfig","    "TokenizerInfo","    "TokenizeResult","    # Core classes
    "BaseTokenizer","    "HuggingFaceTokenizer","    "TiktokenTokenizer","    "MistralTokenizer","    "TokenizerRegistry","    "TokenizerPool","    # Utilities
    "get_tokenizer","    "create_tokenizer","    "estimate_token_count","]
