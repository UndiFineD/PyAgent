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

# Phase 16: Rust acceleration for template rendering and A/B selection

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import random
import time
from datetime import datetime
from typing import Any
from src.core.base.models import PromptTemplate

__version__ = VERSION

# Phase 16: Rust acceleration imports
try:
    import rust_core
    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False
    logging.debug("rust_core not available, using Python fallback for PromptManagers")


class PromptTemplateManager:
    """Manages a collection of prompt templates."""

    def __init__(self) -> None:
        """Initialize the template manager."""
        self.templates: dict[str, PromptTemplate] = {}

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
        version: str | None = None,
        content: str | None = None,
        description: str = "",
        active: bool = True,
        version_id: str | None = None,
        template_id: str | None = None,
        variant: str | None = None,
        prompt_text: str | None = None,
        weight: float = 1.0,
    ) -> None:
        self.version = version or version_id or ""
        self.content = content or prompt_text or ""

        self.description = description
        self.active = active
        self.created_at = datetime.now()
        self.metrics: dict[str, float] = {}
        self.version_id = self.version
        self.template_id = template_id or ""
        self.variant = variant or ""
        self.prompt_text = self.content
        self.weight = weight


class PromptVersionManager:
    """Manager for prompt versioning and A/B testing."""

    def __init__(self) -> None:
        self.versions: dict[str, PromptVersion] = {}
        self.active_version: str | None = None
        self.metrics: dict[str, dict[str, float]] = {}
        self._old_api_versions: dict[str, list[PromptVersion]] = {}
        self.selection_history: list[dict[str, Any]] = []
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

    def get_active(self) -> PromptVersion | None:
        if self.active_version and self.active_version in self.versions:
            return self.versions[self.active_version]
        return None

    def get_versions(self, template_id: str = "") -> list[PromptVersion]:
        if template_id:
            return self._old_api_versions.get(template_id, [])
        return list(self.versions.values())

    def select_version(self, template_id: str = "") -> PromptVersion | None:
        versions = self.get_versions(template_id)
        if not versions:
            return None
        total_weight = sum(v.weight for v in versions)
        if total_weight <= 0:
            return versions[0]
        
        # Phase 16: Try Rust-accelerated weighted random selection
        selected_idx = None
        if _RUST_AVAILABLE and hasattr(rust_core, "weighted_random_select_rust"):
            try:
                weights = [v.weight for v in versions]
                selected_idx = rust_core.weighted_random_select_rust(weights)
            except Exception:
                selected_idx = None
        
        if selected_idx is not None and 0 <= selected_idx < len(versions):
            version = versions[selected_idx]
        else:
            # Python fallback
            r = random.uniform(0, total_weight)
            cumulative = 0.0
            version = versions[-1]  # Default
            for v in versions:
                cumulative += v.weight
                if r <= cumulative:
                    version = v
                    break
        
        self.selection_history.append(
            {
                "template_id": template_id,
                "version_id": version.version_id,
                "variant": version.variant,
                "timestamp": time.time(),
            }
        )
        return version

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

    def get_best_version(
        self, template_id: str = "", metric: str = "quality"
    ) -> PromptVersion | None:
        versions = (
            self.get_versions(template_id)
            if template_id
            else list(self.versions.values())
        )
        if not versions:
            return None
        best: PromptVersion | None = None
        best_score = -float("inf")
        for version in versions:
            score = version.metrics.get(metric, 0)
            if score > best_score:
                best_score = score
                best = version
        return best

    def generate_report(self, template_id: str = "") -> dict[str, Any]:
        report: dict[str, Any] = {"total_versions": len(self.versions), "versions": {}}
        for version_id, version in self.versions.items():
            report["versions"][version_id] = {
                "content": version.content,
                "active": version.active,
                "metrics": version.metrics,
            }
        return report

    def get_ab_report(self, template_id: str) -> dict[str, Any]:
        versions = self.get_versions(template_id)
        selections = [
            s for s in self.selection_history if s["template_id"] == template_id
        ]
        report: dict[str, Any] = {
            "template_id": template_id,
            "total_selections": len(selections),
            "versions": {},
        }
        for version in versions:
            version_selections = [
                s for s in selections if s["version_id"] == version.version_id
            ]
            report["versions"][version.version_id] = {
                "variant": version.variant,
                "selections": len(version_selections),
                "metrics": self.metrics.get(version.version_id, {}),
            }
        return report
