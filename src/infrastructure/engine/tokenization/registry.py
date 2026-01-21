# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Tokenizer registry.
"""

from __future__ import annotations

import threading
from collections import OrderedDict
from typing import Dict, Optional

from .models import TokenizerConfig, TokenizerBackend
from .base import BaseTokenizer
from .huggingface import HuggingFaceTokenizer
from .tiktoken import TiktokenTokenizer
from .mistral import MistralTokenizer


class TokenizerRegistry:
    """Central registry for tokenizer management."""

    _instance: Optional['TokenizerRegistry'] = None
    _lock = threading.Lock()

    def __new__(cls) -> 'TokenizerRegistry':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, max_cached: int = 16):
        if self._initialized:
            return
        self._cache: OrderedDict[int, BaseTokenizer] = OrderedDict()
        self._max_cached = max_cached
        self._cache_lock = threading.RLock()
        self._stats = {"hits": 0, "misses": 0, "evictions": 0}
        self._initialized = True

    def get_tokenizer(self, config: TokenizerConfig) -> BaseTokenizer:
        """Get or create a tokenizer."""
        key = hash(config)
        with self._cache_lock:
            if key in self._cache:
                self._stats["hits"] += 1
                self._cache.move_to_end(key)
                return self._cache[key]
            self._stats["misses"] += 1

        tokenizer = self._create_tokenizer(config)
        with self._cache_lock:
            while len(self._cache) >= self._max_cached:
                self._cache.popitem(last=False)
                self._stats["evictions"] += 1
            self._cache[key] = tokenizer
        return tokenizer

    def _create_tokenizer(self, config: TokenizerConfig) -> BaseTokenizer:
        """Create tokenizer based on backend."""
        if config.backend == TokenizerBackend.HUGGINGFACE:
            return HuggingFaceTokenizer(config)
        elif config.backend == TokenizerBackend.TIKTOKEN:
            return TiktokenTokenizer(config)
        elif config.backend == TokenizerBackend.MISTRAL:
            return MistralTokenizer(config)
        else:
            return self._auto_create(config)

    def _auto_create(self, config: TokenizerConfig) -> BaseTokenizer:
        """Auto-detect and create appropriate tokenizer."""
        model_name = config.model_name.lower()
        if any(name in model_name for name in ["gpt-4", "gpt-3.5", "text-embedding"]):
            config = TokenizerConfig(model_name=config.model_name, backend=TokenizerBackend.TIKTOKEN)
            return TiktokenTokenizer(config)
        if "mistral" in model_name:
            config = TokenizerConfig(model_name=config.model_name, backend=TokenizerBackend.MISTRAL)
            return MistralTokenizer(config)
        return HuggingFaceTokenizer(config)

    def clear_cache(self):
        with self._cache_lock:
            self._cache.clear()

    def get_stats(self) -> Dict[str, int]:
        with self._cache_lock:
            return {**self._stats, "cached": len(self._cache), "max_cached": self._max_cached}
