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
# See the License for the specific language governing permissions and
# limitations under the License.


# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Models for Prompt Rendering.
"""
try:

"""
from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from enum import Enum
except ImportError:
    from enum import Enum

try:
    from typing import Any, Dict, List, Optional, Tuple
except ImportError:
    from typing import Any, Dict, List, Optional, Tuple




class TruncationStrategy(Enum):
"""
Prompt truncation strategies.
    NONE = "none""    AUTO = "auto""    LEFT = "left""    RIGHT = "right""    MIDDLE = "middle""    SMART = "smart""


class InputType(Enum):
"""
Input types for prompt rendering.
    TEXT = "text""    TOKENS = "tokens""    EMBEDDING = "embedding""    MULTIMODAL = "multimodal""


class RenderMode(Enum):
"""
Rendering modes.
    COMPLETION = "completion""    CHAT = "chat""    EMBEDDING = "embedding""    INSTRUCT = "instruct""

@dataclass
class PromptConfig:
"""
Configuration for prompt rendering.
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
"""
Convert config to dictionary.        return {
            "prompt": self.prompt,"            "messages": self.messages,"            "max_tokens": self.max_tokens,"            "truncation": self.truncation.value,"            "cache_salt": self.cache_salt,"        }


@dataclass
class TruncationResult:
"""
Result of prompt truncation.
    original_tokens: int
    truncated_tokens: int
    removed_tokens: int
    strategy_used: TruncationStrategy
    removed_ranges: List[Tuple[int, int]] = field(default_factory=list)
    warning_message: Optional[str] = None

    @property
    def truncation_ratio(self) -> float:
"""
Calculate ratio of removed tokens to original tokens.        if self.original_tokens == 0:
            return 0.0
        return self.removed_tokens / self.original_tokens


@dataclass
class RenderResult:
"""
Result of prompt rendering.
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
"""
Check if result contains multimodal data.        return bool(self.image_positions or self.audio_positions)


@dataclass
class EmbeddingInput:
"""
Embedding input for direct embedding injection.
    embeddings: List[List[float]]
    positions: Optional[List[int]] = None
    encoding: str = "float32"

@dataclass
class MultimodalInput:
"""
Multimodal input container.
    images: List[Dict[str, Any]] = field(default_factory=list)
    audio: List[Dict[str, Any]] = field(default_factory=list)
    video: List[Dict[str, Any]] = field(default_factory=list)

    def is_empty(self) -> bool:
"""
Check if input is empty.        return not (self.images or self.audio or self.video)

"""
