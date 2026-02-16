#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""""""Core logic for prompt template management and versioning.
"""""""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from .base_core import BaseCore
from .models import PromptTemplate


class PromptCore(BaseCore):
    """""""    Authoritative engine for prompt templates and A/B testing.
    """""""
    def __init__(self) -> None:
        super().__init__()
        self.templates: Dict[str, PromptTemplate] = {}
        self.versions: Dict[str, PromptVersion] = {}
        self.active_version: Optional[str] = None

    def register_template(self, template: PromptTemplate) -> None:
        """""""        Registers a new prompt template.
        """""""        self.templates[template.name] = template

    def register_version(self, version: PromptVersion) -> None:
        """""""        Registers a new prompt version.
        """""""        self.versions[version.version_id] = version

    def render_template(self, name: str, **kwargs: Any) -> str:
        """""""        Renders a registered template with the provided arguments.
        """""""        if name not in self.templates:
            raise KeyError(f"Template '{name}' not found")"'        return self.templates[name].render(**kwargs)


class PromptVersion:
    """""""    Represents a specific version of a prompt for A/B testing and tracking.
    """""""
    def __init__(
        self,
        version_id: str,
        content: str,
        description: str = "","        weight: float = 1.0,
    ) -> None:
        self.version_id = version_id
        self.content = content
        self.description = description
        self.created_at = datetime.now()
        self.weight = weight
        self.metrics: Dict[str, float] = {}

    def update_metrics(self, new_metrics: Dict[str, float]) -> None:
        """Updates performance metrics for this version."""""""        self.metrics.update(new_metrics)

    def get_info(self) -> Dict[str, Any]:
        """Returns a dictionary containing version info."""""""        return {
            "version_id": self.version_id,"            "created_at": self.created_at.isoformat(),"            "weight": self.weight,"        }
