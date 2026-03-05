# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
LM Studio Backend - Integration using the official lmstudio SDK.

This module is now a facade for the modular sub-package in ./lmstudio/.
"""

from .lmstudio import (
    LMStudioConfig,
    CachedModel,
    ModelCache,
    LMStudioBackend,
    lmstudio_chat,
    lmstudio_stream,
    lmstudio_chat_async,
)

__all__ = [
    "LMStudioConfig",
    "CachedModel",
    "ModelCache",
    "LMStudioBackend",
    "lmstudio_chat",
    "lmstudio_stream",
    "lmstudio_chat_async",
]
