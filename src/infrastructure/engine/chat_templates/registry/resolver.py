# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Advanced template resolution with caching."""

import re
import threading
from functools import lru_cache
from typing import Dict, Optional
from .config import ModelType
from .base import ChatTemplate
from .registry import ChatTemplateRegistry


class TemplateResolver:
    """Advanced template resolution with caching."""

    def __init__(self, registry: Optional[ChatTemplateRegistry] = None):
        self.registry = registry or ChatTemplateRegistry()
        self._cache: Dict[str, ChatTemplate] = {}
        self._lock = threading.Lock()

    @lru_cache(maxsize=256)
    def resolve(
        self,
        model_name: str,
        model_type: Optional[ModelType] = None,
    ) -> ChatTemplate:
        """Resolve template with caching."""
        # Normalize model name
        normalized = self._normalize_model_name(model_name)

        with self._lock:
            if normalized in self._cache:
                return self._cache[normalized]

            template = self.registry.resolve(normalized)

            # Apply model type hints
            if model_type == ModelType.VISION:
                template = self._wrap_multimodal(template)

            self._cache[normalized] = template
            return template

    def _normalize_model_name(self, name: str) -> str:
        """Normalize model name for matching."""
        # Remove common prefixes/suffixes
        name = name.lower()
        name = re.sub(r"[/\\]", "-", name)
        name = re.sub(r"[-_]", "-", name)
        name = re.sub(r"\.gguf$", "", name)
        name = re.sub(r"\.safetensors$", "", name)
        return name

    def _wrap_multimodal(self, template: ChatTemplate) -> ChatTemplate:
        """Wrap template for multimodal support."""
        # For now, return as-is; can be extended for multimodal
        return template

    def clear_cache(self) -> None:
        """Clear resolution cache."""
        with self._lock:
            self._cache.clear()
        self.resolve.cache_clear()
