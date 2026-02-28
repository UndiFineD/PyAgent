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

        salt_string: str = "|".join(components)
        return hashlib.sha256(salt_string.encode()).hexdigest()[:16]
