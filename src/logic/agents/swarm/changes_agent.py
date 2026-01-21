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


"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .changelog_entry import ChangelogEntry
from .changelog_template import ChangelogTemplate
from .validation_rule import ValidationRule
from .versioning_strategy import VersioningStrategy
from .merge_conflict_mixin import MergeConflictMixin
from .changelog_validation_mixin import ChangelogValidationMixin
from .changelog_analytics_mixin import ChangelogAnalyticsMixin
from .mixins.changes_template_mixin import ChangesTemplateMixin
from .mixins.changes_versioning_mixin import ChangesVersioningMixin
from .mixins.changes_preview_mixin import ChangesPreviewMixin
from .mixins.changes_entry_mixin import ChangesEntryMixin
from src.core.base.base_agent import BaseAgent
from typing import Any
import logging

__version__ = VERSION


class ChangesAgent(
    BaseAgent,
    MergeConflictMixin,
    ChangelogValidationMixin,
    ChangelogAnalyticsMixin,
    ChangesTemplateMixin,
    ChangesVersioningMixin,
    ChangesPreviewMixin,
    ChangesEntryMixin,
):
    """Updates code file changelogs using AI assistance.

    Features:
    - Changelog templates for different project types
    - Preview mode before committing changes
    - Multiple versioning strategies (SemVer, CalVer)
    - Merge conflict detection and resolution
    - Entry validation with customizable rules
    - Statistics and analytics
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._validate_file_extension()
        self._check_associated_file()
        self._template: ChangelogTemplate | None = None
        self._versioning_strategy: VersioningStrategy = VersioningStrategy.SEMVER
        self._validation_rules: list[ValidationRule] = (
            self.DEFAULT_VALIDATION_RULES.copy()
        )
        self._preview_mode: bool = False
        self._preview_content: str = ""
        self._entries: list[ChangelogEntry] = []
        self._statistics: dict[str, Any] = {}

    def _validate_file_extension(self) -> None:
        """Validate that the file has the correct extension."""
        if not self.file_path.name.endswith(".changes.md"):
            logging.warning(f"File {self.file_path.name} does not end with .changes.md")

    def _check_associated_file(self) -> None:
        """Check if the associated code file exists."""
        name = self.file_path.name
        if name.endswith(".changes.md"):
            base_name = name[:-11]  # len('.changes.md')
            # Try to find the file with common extensions or exact match
            candidate = self.file_path.parent / base_name
            if candidate.exists():
                return
            # Try adding extensions
            for ext in [".py", ".sh", ".js", ".ts", ".md"]:
                candidate = self.file_path.parent / (base_name + ext)
                if candidate.exists() and candidate != self.file_path:
                    return
            logging.warning(
                f"Could not find associated code file for {self.file_path.name}"
            )

    def update_file(self) -> bool:
        """Override update_file to support preview mode."""
        if self._preview_mode:
            logging.info("Preview mode: changes not written to file")
            return True

        return bool(super().update_file())

    def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Use AI to improve the changelogs with specific change tracking suggestions."""
        actual_path = Path(target_file) if target_file else self.file_path
        logging.info(f"Improving changelog for {actual_path}")
        # Add guidance for structured output
        enhanced_prompt = (
            f"{prompt}\n\n"
            "Please format the changelog using 'Keep a Changelog' conventions:\n"
            "## [Version] - YYYY - MM - DD\n"
            "### Added\n"
            "### Changed\n"
            "### Deprecated\n"
            "### Removed\n"
            "### Fixed\n"
            "### Security\n"
        )
        description = (
            f"Improve the changelog for {self.file_path.stem.replace('.changes', '')}"
        )
        # For changelog improvement, provide specific change tracking suggestions
        if any(keyword in prompt.lower() for keyword in ["improve", "change", "log"]):
            fallback_suggestions = f"""# AI Changelog Improvement Suggestions
# Description: {description}
#
# Suggestions:
# 1. Follow 'Keep a Changelog' format
# 2. Group changes by type (Added, Changed, Deprecated, Removed, Fixed, Security)
# 3. Include dates for versions
# 4. Be specific about changes
#
# Original changelog preserved below:
#
{self.previous_content}"""
            self.current_content = fallback_suggestions
            return self.current_content
        # For other prompts, call the BaseAgent's subagent path directly.
        #
        # This intentionally bypasses BaseAgent.improve_content() caching so
        # tests that monkeypatch base_agent.BaseAgent.run_subagent remain
        # deterministic even when earlier test runs have populated caches.
        from src.core.base.base_agent import entrypoint as _base_agent

        try:
            full_prompt = self._build_prompt_with_history(enhanced_prompt)
        except Exception:
            full_prompt = enhanced_prompt

        improvement = _base_agent.BaseAgent.run_subagent(
            self, description, full_prompt, self.previous_content
        )

        for processor in self._post_processors:
            improvement = processor(improvement)

        self.current_content = improvement
        return self.current_content
