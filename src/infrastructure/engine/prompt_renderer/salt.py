# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Cache salt generation for prompt rendering.
"""

from __future__ import annotations

import hashlib
from typing import Any, Dict, Optional

from .models import PromptConfig, TruncationStrategy


class CacheSaltGenerator:
    """Generate cache salt for prefix caching disambiguation."""

    @classmethod
    def generate(
        cls,
        config: PromptConfig,
        additional_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Generate cache salt based on configuration."""
        components = []
        if config.chat_template:
            components.append(f"template:{hashlib.md5(config.chat_template.encode()).hexdigest()[:8]}")
        if config.add_generation_prompt:
            components.append("gen_prompt")
        if config.add_special_tokens:
            components.append("special_tokens")
        if config.truncation != TruncationStrategy.NONE:
            components.append(f"trunc:{config.truncation.value}")
        if additional_data:
            for key, value in sorted(additional_data.items()):
                components.append(f"{key}:{value}")
        if config.cache_salt:
            components.append(config.cache_salt)

        if not components:
            return ""

        salt_string = "|".join(components)
        return hashlib.sha256(salt_string.encode()).hexdigest()[:16]
