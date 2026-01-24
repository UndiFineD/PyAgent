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
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Jinja2 template implementations."""

import logging
from typing import Any, Dict, List, Optional

from .base import ChatTemplate
from .config import (BUILTIN_TEMPLATES, RenderOptions, TemplateConfig,
                     TemplateType)

logger = logging.getLogger(__name__)


class JinjaTemplate(ChatTemplate):
    """Jinja2-based chat template."""

    def __init__(self, config: TemplateConfig):
        super().__init__(config)
        self._template = None
        self._env = None

    def get_template_string(self) -> str:
        """Get template string."""
        if self.config.template_string:
            return self.config.template_string

        if self.config.template_path:
            with open(self.config.template_path) as f:
                return f.read()

        # Use builtin
        if self.config.template_type in BUILTIN_TEMPLATES:
            return BUILTIN_TEMPLATES[self.config.template_type]

        return BUILTIN_TEMPLATES[TemplateType.CHATML]

    def _get_env(self):
        """Get Jinja environment."""
        if self._env is None:
            try:
                from jinja2 import BaseLoader, Environment, StrictUndefined

                self._env = Environment(
                    loader=BaseLoader(),
                    undefined=StrictUndefined,
                    autoescape=False,
                    trim_blocks=True,
                    lstrip_blocks=True,
                )

                # Add custom filters
                self._env.filters["trim"] = str.strip

            except ImportError:
                logger.warning("Jinja2 not available")
                self._env = None

        return self._env

    def _get_template(self):
        """Get compiled Jinja template."""
        if self._template is None:
            env = self._get_env()
            if env:
                template_string = self.get_template_string()
                self._template = env.from_string(template_string)
        return self._template

    def render(
        self,
        messages: List[Dict[str, Any]],
        options: Optional[RenderOptions] = None,
    ) -> str:
        """Render messages using Jinja template."""
        options = options or RenderOptions()

        # Filter messages
        filtered = []
        for msg in messages:
            if not options.include_system and msg.get("role") == "system":
                continue
            filtered.append(msg)

        template = self._get_template()
        if template:
            try:
                result = template.render(
                    messages=filtered,
                    add_generation_prompt=options.add_generation_prompt,
                )

                if options.strip_whitespace:
                    result = result.strip()

                return result

            except Exception as e:
                logger.error(f"Template rendering error: {e}")
                return self._fallback_render(filtered, options)

        return self._fallback_render(filtered, options)

    def _fallback_render(
        self,
        messages: List[Dict[str, Any]],
        options: RenderOptions,
    ) -> str:
        """Fallback rendering without Jinja."""
        parts = []

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                parts.append(f"<|im_start|>system\n{content}<|im_end|>")
            elif role == "user":
                parts.append(f"<|im_start|>user\n{content}<|im_end|>")
            elif role == "assistant":
                parts.append(f"<|im_start|>assistant\n{content}<|im_end|>")
            elif role == "tool":
                parts.append(f"<|im_start|>tool\n{content}<|im_end|>")

        if options.add_generation_prompt:
            parts.append("<|im_start|>assistant\n")

        return "\n".join(parts)
