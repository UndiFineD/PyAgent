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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import random
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from src.core.base.models import PromptTemplate

__version__ = VERSION

class PromptTemplateManager:
    """Manages a collection of prompt templates."""

    def __init__(self) -> None:
        """Initialize the template manager."""
        self.templates: Dict[str, PromptTemplate] = {}

    def register(self, template: PromptTemplate) -> None:
        """Register a prompt template."""
        self.templates[template.name] = template

    def render(self, template_name: str, **kwargs: Any) -> str:
        """Render a template by name."""
        template = self.templates[template_name]
        return template.render(**kwargs)

class PromptVersion:
    """Versioned prompt for A/B testing."""

    def __init__(
        self,
        version: Optional[str] = None,
        content: Optional[str] = None,
        description: str = "",
        active: bool = True,
        version_id: Optional[str] = None,
        template_id: Optional[str] = None,
        variant: Optional[str] = None,
        prompt_text: Optional[str] = None,
        weight: float = 1.0
    ) -> None:
        self.version = version or version_id or ""
        self.content = content or prompt_text or ""
        self.description = description
        self.active = active
        self.created_at = datetime.now()
        self.metrics: Dict[str, float] = {}
        self.version_id = self.version
        self.template_id = template_id or ""
        self.variant = variant or ""
        self.prompt_text = self.content
        self.weight = weight

class PromptVersionManager:
    """Manager for prompt versioning and A/B testing."""

    def __init__(self) -> None:
        self.versions: Dict[str, PromptVersion] = {}
        self.active_version: Optional[str] = None
        self.metrics: Dict[str, Dict[str, float]] = {}
        self._old_api_versions: Dict[str, List[PromptVersion]] = {}
        self.selection_history: List[Dict[str, Any]] = []
        logging.debug("PromptVersionManager initialized")

    def register_version(self, version: PromptVersion) -> None:
        template_id = version.template_id
        if template_id not in self._old_api_versions:
            self._old_api_versions[template_id] = []
        self._old_api_versions[template_id].append(version)
        self.versions[version.version_id] = version
        if self.active_version is None:
            self.active_version = version.version_id

    def add_version(self, version: PromptVersion) -> None:
        self.versions[version.version] = version
        if self.active_version is None:
            self.active_version = version.version

    def set_active(self, version: str) -> None:
        if version in self.versions:
            self.active_version = version
            self.versions[version].active = True

    def get_active(self) -> Optional[PromptVersion]:
        if self.active_version and self.active_version in self.versions:
            return self.versions[self.active_version]
        return None

    def get_versions(self, template_id: str = "") -> List[PromptVersion]:
        if template_id:
            return self._old_api_versions.get(template_id, [])
        return list(self.versions.values())

    def select_version(self, template_id: str = "") -> Optional[PromptVersion]:
        versions = self.get_versions(template_id)
        if not versions:
            return None
        total_weight = sum(v.weight for v in versions)
        if total_weight <= 0:
            return versions[0]
        r = random.uniform(0, total_weight)
        cumulative = 0.0
        for version in versions:
            cumulative += version.weight
            if r <= cumulative:
                self.selection_history.append({
                    "template_id": template_id,
                    "version_id": version.version_id,
                    "variant": version.variant,
                    "timestamp": time.time()
                })
                return version
        return versions[-1]

    def record_metric(self, version_id: str, metric_name: str, value: float) -> None:
        if version_id not in self.metrics:
            self.metrics[version_id] = {}
        if metric_name in self.metrics[version_id]:
            current = self.metrics[version_id][metric_name]
            self.metrics[version_id][metric_name] = (current + value) / 2
        else:
            self.metrics[version_id][metric_name] = value
        if version_id in self.versions:
            self.versions[version_id].metrics[metric_name] = value

    def get_best_version(self, template_id: str = "", metric: str = "quality") -> Optional[PromptVersion]:
        versions = self.get_versions(template_id) if template_id else list(self.versions.values())
        if not versions:
            return None
        best: Optional[PromptVersion] = None
        best_score = -float('inf')
        for version in versions:
            score = version.metrics.get(metric, 0)
            if score > best_score:
                best_score = score
                best = version
        return best

    def generate_report(self, template_id: str = "") -> Dict[str, Any]:
        report: Dict[str, Any] = {"total_versions": len(self.versions), "versions": {}}
        for version_id, version in self.versions.items():
            report["versions"][version_id] = {
                "content": version.content,
                "active": version.active,
                "metrics": version.metrics
            }
        return report

    def get_ab_report(self, template_id: str) -> Dict[str, Any]:
        versions = self.get_versions(template_id)
        selections = [s for s in self.selection_history if s["template_id"] == template_id]
        report: Dict[str, Any] = {"template_id": template_id, "total_selections": len(selections), "versions": {}}
        for version in versions:
            version_selections = [s for s in selections if s["version_id"] == version.version_id]
            report["versions"][version.version_id] = {
                "variant": version.variant,
                "selections": len(version_selections),
                "metrics": self.metrics.get(version.version_id, {})
            }
        return report
