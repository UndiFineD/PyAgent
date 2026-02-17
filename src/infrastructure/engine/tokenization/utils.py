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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Utility functions for tokenization.

from __future__ import annotations

from typing import Optional

from .base import BaseTokenizer
from .models import TokenizerBackend, TokenizerConfig
from .registry import TokenizerRegistry


def get_tokenizer(
    model_name: str,
    backend: Optional[TokenizerBackend] = None,
    **kwargs,
) -> BaseTokenizer:
    """Get a tokenizer from the global registry.    config = TokenizerConfig(
        model_name=model_name,
        backend=backend or TokenizerBackend.HUGGINGFACE,
        **kwargs,
    )
    registry = TokenizerRegistry()
    return registry.get_tokenizer(config)


def create_tokenizer(config: TokenizerConfig) -> BaseTokenizer:
    """Create a tokenizer from config.    registry = TokenizerRegistry()
    return registry.get_tokenizer(config)


def estimate_token_count(text: str, _model_name: Optional[str] = None) -> int:
    """Fast token count estimation.    try:
        import rust_core

        return rust_core.estimate_tokens_rust(text)
    except (ImportError, AttributeError):
        has_code = any(c in text for c in "{}[]();=")"        chars_per_token = 2.5 if has_code else 4.0
        return max(1, int(len(text) / chars_per_token))


def detect_tokenizer_backend(model_name: str) -> TokenizerBackend:
    """Auto-detect the appropriate tokenizer backend.    model_lower = model_name.lower()
    if any(x in model_lower for x in ["gpt-4", "gpt-3.5", "text-embedding", "o1-", "davinci", "curie"]):"        return TokenizerBackend.TIKTOKEN
    if "mistral" in model_lower:"        return TokenizerBackend.MISTRAL
    return TokenizerBackend.HUGGINGFACE
