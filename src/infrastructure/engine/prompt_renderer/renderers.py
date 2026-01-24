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
Core renderers for prompt rendering.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from .base import PromptRenderer
from .models import InputType, PromptConfig, RenderResult

logger = logging.getLogger(__name__)


class CompletionRenderer(PromptRenderer):
    """Renderer for completion-style prompts."""

    def render(self, config: PromptConfig) -> RenderResult:
        """Render completion prompt."""
        # Direct token input
        if config.token_ids is not None:
            tokens = config.token_ids
            tokens, trunc_result = self._apply_truncation(tokens, config)

            return RenderResult(
                token_ids=tokens,
                input_type=InputType.TOKENS,
                num_tokens=len(tokens),
                was_truncated=trunc_result is not None,
                truncation_info=trunc_result,
                cache_salt=self._generate_cache_salt(config),
            )

        # Embedding input
        if config.embeddings is not None:
            return RenderResult(
                embeddings=config.embeddings,
                input_type=InputType.EMBEDDING,
                num_tokens=len(config.embeddings),
                cache_salt=self._generate_cache_salt(config),
            )

        # Text input
        text = config.prompt or ""

        if config.strip_whitespace:
            text = text.strip()

        if config.normalize_unicode:
            import unicodedata

            text = unicodedata.normalize("NFC", text)

        tokens = self._tokenize(text, config.add_special_tokens)
        tokens, trunc_result = self._apply_truncation(tokens, config)

        # Regenerate text if truncated
        if trunc_result and trunc_result.removed_tokens > 0:
            text = self._detokenize(tokens)

        return RenderResult(
            text=text,
            token_ids=tokens,
            input_type=InputType.TEXT,
            num_tokens=len(tokens),
            was_truncated=trunc_result is not None,
            truncation_info=trunc_result,
            cache_salt=self._generate_cache_salt(config),
        )


class ChatRenderer(PromptRenderer):
    """Renderer for chat-style prompts."""

    # Default chat template (ChatML-like)
    DEFAULT_TEMPLATE = """{% for message in messages %}{% if message['role'] == 'system' %}<|im_start|>system
{{ message['content'] }}<|im_end|>
{% elif message['role'] == 'user' %}<|im_start|>user
{{ message['content'] }}<|im_end|>
{% elif message['role'] == 'assistant' %}<|im_start|>assistant
{{ message['content'] }}<|im_end|>
{% endif %}{% endfor %}{% if add_generation_prompt %}<|im_start|>assistant
{% endif %}"""

    def render(self, config: PromptConfig) -> RenderResult:
        """Render chat prompt."""
        if config.messages is None:
            # Fallback to completion rendering
            return CompletionRenderer(self.tokenizer, self.max_model_tokens).render(config)

        # Apply chat template
        text = self._apply_template(
            config.messages,
            config.chat_template or self.DEFAULT_TEMPLATE,
            config.add_generation_prompt,
        )

        if config.strip_whitespace:
            text = text.strip()

        # Tokenize
        tokens = self._tokenize(text, config.add_special_tokens)
        tokens, trunc_result = self._apply_truncation(tokens, config)

        # Handle multimodal
        image_positions = None
        if config.images:
            image_positions = self._find_image_positions(text, config.images)

        return RenderResult(
            text=text,
            token_ids=tokens,
            input_type=InputType.TEXT if not image_positions else InputType.MULTIMODAL,
            num_tokens=len(tokens),
            was_truncated=trunc_result is not None,
            truncation_info=trunc_result,
            image_positions=image_positions,
            cache_salt=self._generate_cache_salt(config),
        )

    def _apply_template(
        self,
        messages: List[Dict[str, Any]],
        template: str,
        add_generation_prompt: bool = True,
    ) -> str:
        """Apply Jinja2 chat template."""
        # Try Rust acceleration first
        from .utils import _try_rust_render_template

        rust_rendered = _try_rust_render_template(template, messages, add_generation_prompt)
        if rust_rendered:
            return rust_rendered

        try:
            from jinja2 import BaseLoader, Environment

            env = Environment(loader=BaseLoader())
            tmpl = env.from_string(template)
            return tmpl.render(
                messages=messages,
                add_generation_prompt=add_generation_prompt,
            )
        except ImportError:
            # Fallback without Jinja2
            return self._simple_template(messages, add_generation_prompt)

    def _simple_template(
        self,
        messages: List[Dict[str, Any]],
        add_generation_prompt: bool,
    ) -> str:
        """Simple template without Jinja2."""
        parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            parts.append(f"<|im_start|>{role}\n{content}<|im_end|>")

        if add_generation_prompt:
            parts.append("<|im_start|>assistant\n")

        return "\n".join(parts)

    def _find_image_positions(
        self,
        text: str,
        images: List[Dict[str, Any]],
    ) -> Optional[List[int]]:
        """Find image placeholder positions in text."""
        patterns = ["<image>", "[IMAGE]", "<|image|>", "{{IMAGE}}"]

        # Try Rust acceleration
        from .utils import _try_rust_find_placeholders

        rust_positions = _try_rust_find_placeholders(text, patterns)
        if rust_positions:
            return rust_positions

        positions = []
        for pattern in patterns:
            start = 0
            while True:
                pos = text.find(pattern, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + len(pattern)

        return positions if positions else None
