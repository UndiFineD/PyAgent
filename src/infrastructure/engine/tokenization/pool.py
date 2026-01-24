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
Tokenizer pool for parallel processing.
"""

from __future__ import annotations

import threading
import time
from typing import List, Optional

from .base import BaseTokenizer
from .models import TokenizerConfig
from .registry import TokenizerRegistry


class TokenizerPool:
    """Thread-safe pool of tokenizers."""

    def __init__(self, config: TokenizerConfig, pool_size: int = 4):
        self.config = config
        self.pool_size = pool_size
        self._pool: List[BaseTokenizer] = []
        self._available: List[bool] = []
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._init_pool()

    def _init_pool(self):
        registry = TokenizerRegistry()
        for _ in range(self.pool_size):
            tokenizer = registry.get_tokenizer(self.config)
            self._pool.append(tokenizer)
            self._available.append(True)

    def acquire(self, timeout: Optional[float] = None) -> Optional[BaseTokenizer]:
        with self._condition:
            start = time.monotonic()
            while True:
                for i, available in enumerate(self._available):
                    if available:
                        self._available[i] = False
                        return self._pool[i]
                if timeout is not None:
                    remaining = timeout - (time.monotonic() - start)
                    if remaining <= 0:
                        return None
                    self._condition.wait(remaining)
                else:
                    self._condition.wait()

    def release(self, tokenizer: BaseTokenizer):
        with self._condition:
            for i, t in enumerate(self._pool):
                if t is tokenizer:
                    self._available[i] = True
                    self._condition.notify()
                    return

    def __enter__(self) -> BaseTokenizer:
        tokenizer = self.acquire()
        if tokenizer is None:
            raise RuntimeError("Failed to acquire tokenizer from pool")
        self._current = tokenizer
        return tokenizer

    def __exit__(self, *args):
        self.release(self._current)
