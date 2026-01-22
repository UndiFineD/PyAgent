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

"""
Core logic for prompt template management and versioning.
"""

from __future__ import annotations
import logging
import random
from datetime import datetime
from typing import Any, Dict, List, Optional
from .base_core import BaseCore
from .models import PromptTemplate

class PromptCore(BaseCore):
    """
    Authoritative engine for prompt templates and A/B testing.
    """
    def __init__(self) -> None:
        super().__init__()
        self.templates: Dict[str, PromptTemplate] = {}
        self.versions: Dict[str, PromptVersion] = {}
        self.active_version: Optional[str] = None

    def register_template(self, template: PromptTemplate) -> None:
        self.templates[template.name] = template

    def render_template(self, name: str, **kwargs: Any) -> str:
        if name not in self.templates:
            raise KeyError(f"Template '{name}' not found")
        return self.templates[name].render(**kwargs)

class PromptVersion:
    def __init__(
        self,
        version_id: str,
        content: str,
        description: str = "",
        weight: float = 1.0,
    ) -> None:
        self.version_id = version_id
        self.content = content
        self.description = description
        self.created_at = datetime.now()
        self.weight = weight
        self.metrics: Dict[str, float] = {}
