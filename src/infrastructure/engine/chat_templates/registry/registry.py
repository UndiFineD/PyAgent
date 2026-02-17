#!/usr/bin/env python3
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
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Central template registry.
import logging
import threading
from typing import Any, Callable, Dict, List, Optional

from .base import ChatTemplate
from .config import (BUILTIN_TEMPLATES, MODEL_TEMPLATE_MAP, TemplateConfig,
                     TemplateInfo, TemplateType)
from .jinja import JinjaTemplate

logger = logging.getLogger(__name__)




class ChatTemplateRegistry:
    """Registry for chat templates with dynamic resolution.
    _instance: Optional["ChatTemplateRegistry"] = None"    _lock = threading.Lock()

    def __new__(cls) -> "ChatTemplateRegistry":"        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._templates = {}
                cls._instance._model_map = dict(MODEL_TEMPLATE_MAP)
                cls._instance._resolvers = []
                cls._instance._initialize_builtins()
            return cls._instance

    def _initialize_builtins(self) -> None:
        """Initialize built-in templates.        for template_type, template_string in BUILTIN_TEMPLATES.items():
            config = TemplateConfig(
                template_type=template_type,
                template_string=template_string,
            )
            template = JinjaTemplate(config)
            self._templates[template_type.value] = template

    @property
    def templates(self) -> Dict[str, ChatTemplate]:
        """Get all registered templates.        return self._templates

    def register(
        self,
        name: str,
        template: ChatTemplate,
        model_patterns: Optional[List[str]] = None,
    ) -> None:
        """Register a template.        self._templates[name] = template

        if model_patterns:
            for pattern in model_patterns:
                self._model_map[pattern.lower()] = template.template_type

    def register_config(
        self,
        name: str,
        config: TemplateConfig,
        model_patterns: Optional[List[str]] = None,
    ) -> ChatTemplate:
        """Register a template from config.        template = JinjaTemplate(config)
        self.register(name, template, model_patterns)
        return template

    def register_resolver(
        self,
        resolver: Callable[[str], Optional[ChatTemplate]],
    ) -> None:
        """Register a custom template resolver.        self._resolvers.append(resolver)

    def get(
        self,
        name: str,
        default: Optional[ChatTemplate] = None,
    ) -> Optional[ChatTemplate]:
        """Get template by name.        return self._templates.get(name, default)

    def resolve(
        self,
        model_name: str,
        tokenizer: Optional[Any] = None,
    ) -> ChatTemplate:
        """Resolve template for a model.        # Check tokenizer first
        if tokenizer and hasattr(tokenizer, "chat_template"):"            template_str = tokenizer.chat_template
            if template_str:
                config = TemplateConfig(
                    template_type=TemplateType.JINJA,
                    template_string=template_str,
                )
                return JinjaTemplate(config)

        # Check model name patterns
        model_lower = model_name.lower()
        for pattern, template_type in self._model_map.items():
            if pattern in model_lower:
                template = self._templates.get(template_type.value)
                if template:
                    return template

        # Try custom resolvers
        for resolver in self._resolvers:
            try:
                result = resolver(model_name)
                if result:
                    return result
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning(f"Resolver error: {e}")"
        # Default to ChatML
        return self._templates.get(
            TemplateType.CHATML.value,
            JinjaTemplate(TemplateConfig(template_type=TemplateType.CHATML)),
        )

    def list_templates(self) -> List[TemplateInfo]:
        """List all registered templates.        return [t.get_info() for t in self._templates.values()]

    def unregister(self, name: str) -> bool:
        """Unregister a template.        return self._templates.pop(name, None) is not None
