# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Models for Prompt Rendering.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union


class TruncationStrategy(Enum):
    """Prompt truncation strategies."""
    NONE = "none"
    AUTO = "auto"
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"
    SMART = "smart"


class InputType(Enum):
    """Input types for prompt rendering."""
    TEXT = "text"
    TOKENS = "tokens"
    EMBEDDING = "embedding"
    MULTIMODAL = "multimodal"


class RenderMode(Enum):
    """Rendering modes."""
    COMPLETION = "completion"
    CHAT = "chat"
    EMBEDDING = "embedding"
    INSTRUCT = "instruct"


@dataclass
class PromptConfig:
    """Configuration for prompt rendering."""
    prompt: Optional[str] = None
    messages: Optional[List[Dict[str, Any]]] = None
    token_ids: Optional[List[int]] = None
    embeddings: Optional[List[List[float]]] = None
    chat_template: Optional[str] = None
    add_generation_prompt: bool = True
    add_special_tokens: bool = True
    max_tokens: Optional[int] = None
    truncation: TruncationStrategy = TruncationStrategy.AUTO
    reserve_tokens: int = 0
    images: Optional[List[Dict[str, Any]]] = None
    audio: Optional[List[Dict[str, Any]]] = None
    cache_salt: Optional[str] = None
    enable_prefix_cache: bool = True
    strip_whitespace: bool = True
    normalize_unicode: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "prompt": self.prompt,
            "messages": self.messages,
            "max_tokens": self.max_tokens,
            "truncation": self.truncation.value,
            "cache_salt": self.cache_salt,
        }


@dataclass
class TruncationResult:
    """Result of prompt truncation."""
    original_tokens: int
    truncated_tokens: int
    removed_tokens: int
    strategy_used: TruncationStrategy
    removed_ranges: List[Tuple[int, int]] = field(default_factory=list)
    warning_message: Optional[str] = None

    @property
    def truncation_ratio(self) -> float:
        if self.original_tokens == 0:
            return 0.0
        return self.removed_tokens / self.original_tokens


@dataclass
class RenderResult:
    """Result of prompt rendering."""
    text: Optional[str] = None
    token_ids: Optional[List[int]] = None
    embeddings: Optional[List[List[float]]] = None
    input_type: InputType = InputType.TEXT
    num_tokens: int = 0
    was_truncated: bool = False
    truncation_info: Optional[TruncationResult] = None
    image_positions: Optional[List[int]] = None
    audio_positions: Optional[List[int]] = None
    cache_salt: Optional[str] = None
    cache_prefix_hash: Optional[str] = None

    @property
    def is_multimodal(self) -> bool:
        return bool(self.image_positions or self.audio_positions)


@dataclass
class EmbeddingInput:
    """Embedding input for direct embedding injection."""
    embeddings: List[List[float]]
    positions: Optional[List[int]] = None
    encoding: str = "float32"


@dataclass
class MultimodalInput:
    """Multimodal input container."""
    images: List[Dict[str, Any]] = field(default_factory=list)
    audio: List[Dict[str, Any]] = field(default_factory=list)
    video: List[Dict[str, Any]] = field(default_factory=list)

    def is_empty(self) -> bool:
        return not (self.images or self.audio or self.video)
