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
Unified prompt preparation and rendering system.
"""

from .base import PromptRenderer  # noqa: F401
from .models import (EmbeddingInput, InputType, MultimodalInput, PromptConfig,  # noqa: F401
                     RenderMode, RenderResult, TruncationResult,
                     TruncationStrategy)
from .renderers import ChatRenderer, CompletionRenderer  # noqa: F401
from .salt import CacheSaltGenerator  # noqa: F401
from .truncation import TruncationManager  # noqa: F401
from .utils import (EmbeddingLoader, apply_chat_template, generate_cache_salt,  # noqa: F401
                    render_prompt, truncate_prompt)

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
