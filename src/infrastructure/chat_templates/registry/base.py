# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Abstract base classes for chat templates."""

import hashlib
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .config import TemplateType, TemplateConfig, TemplateInfo, RenderOptions


class ChatTemplate(ABC):
    """Abstract base class for chat templates."""

    def __init__(self, config: TemplateConfig):
        self.config = config
        self._cached_hash: Optional[str] = None

    @property
    def template_type(self) -> TemplateType:
        return self.config.template_type

    @property
    def template_hash(self) -> str:
        """Get hash of template for caching."""
        if self._cached_hash is None:
            template_str = self.get_template_string()
            self._cached_hash = hashlib.md5(
                template_str.encode()
            ).hexdigest()[:12]
        return self._cached_hash

    @abstractmethod
    def get_template_string(self) -> str:
        """Get the template string."""
        ...

    @abstractmethod
    def render(
        self,
        messages: List[Dict[str, Any]],
        options: Optional[RenderOptions] = None,
    ) -> str:
        """Render messages using the template."""
        ...

    def get_info(self) -> TemplateInfo:
        """Get template information."""
        return TemplateInfo(
            name=self.config.template_type.value,
            template_type=self.config.template_type,
        )
