# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Unified prompt preparation and rendering system.
"""

from .models import (
    EmbeddingInput,
    InputType,
    MultimodalInput,
    PromptConfig,
    RenderMode,
    RenderResult,
    TruncationResult,
    TruncationStrategy,
)
from .base import PromptRenderer
from .renderers import ChatRenderer, CompletionRenderer
from .salt import CacheSaltGenerator
from .truncation import TruncationManager
from .utils import (
    EmbeddingLoader,
    apply_chat_template,
    generate_cache_salt,
    render_prompt,
    truncate_prompt,
)

__all__ = [
    "TruncationStrategy",
    "InputType",
    "RenderMode",
    "PromptConfig",
    "RenderResult",
    "TruncationResult",
    "EmbeddingInput",
    "MultimodalInput",
    "PromptRenderer",
    "CompletionRenderer",
    "ChatRenderer",
    "EmbeddingLoader",
    "TruncationManager",
    "CacheSaltGenerator",
    "render_prompt",
    "apply_chat_template",
    "truncate_prompt",
    "generate_cache_salt",
]
