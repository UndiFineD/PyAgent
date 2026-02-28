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
Base Prompt Renderer class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple

from .models import PromptConfig, RenderResult, TruncationResult
from .salt import CacheSaltGenerator
from .truncation import TruncationManager


class PromptRenderer(ABC):
    """
    Abstract base class for prompt renderers.
    """

    def __init__(
        self,
        tokenizer: Optional[Any] = None,
        max_model_tokens: int = 4096,
    ) -> None:
        self.tokenizer = tokenizer
        self.max_model_tokens = max_model_tokens

    @abstractmethod
    def render(self, config: PromptConfig) -> RenderResult:
        """Render prompt from configuration."""
        raise NotImplementedError("Subclasses must implement render")

    def _tokenize(self, text: str, add_special_tokens: bool = True) -> List[int]:
        """Tokenize text."""
        if self.tokenizer is None:
            return list(range(len(text.split())))
        return self.tokenizer.encode(text, add_special_tokens=add_special_tokens)

    def _detokenize(self, tokens: List[int]) -> str:
        """Detokenize tokens."""
        if self.tokenizer is None:
            return f"<{len(tokens)} tokens>"
        return self.tokenizer.decode(tokens)

    def _apply_truncation(
        self,
        tokens: List[int],
        config: PromptConfig,
    ) -> Tuple[List[int], Optional[TruncationResult]]:
        """Apply truncation to tokens."""
        max_tokens = config.max_tokens or self.max_model_tokens
        if len(tokens) <= max_tokens:
            return tokens, None
        return TruncationManager.truncate(tokens, max_tokens, config.truncation, config.reserve_tokens)

    def _generate_cache_salt(self, config: PromptConfig) -> str:
        """Generate cache salt."""
        return CacheSaltGenerator.generate(config)
