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


# #
# ChangesAgent - Changelog management for code files with AI assistance
# #
[Brief Summary]
# DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate with path to a .changes.md file and use improve_content to generate or refine changelog text; use update_file() to persist unless preview mode is enabled.
- Example:
  agent = ChangesAgent(rC:\repo\\\\module.changes.md")
  await agent.improve_content("Summarize recent changes and suggest version bump")
  agent.update_file()

WHAT IT DOES:
- Detects and validates .changes.md files and attempts to locate the associated code file.
- Provides AI-assisted changelog improvement using structured "Keep a Changelog" formatting and supports preview mode to avoid writing.
- Offers templating, validation rules, versioning strategies (default SemVer), merge-conflict handling, changelog analytics, entry previewing, and entry management via mixins.

WHAT IT SHOULD DO BETTER:
- Use transactional StateTransaction for file writes to ensure atomic updates and safe rollbacks.
- Improve associated-file detection (workspace-aware search, configurable extensions) and surface clearer diagnostics to the user.
- Make versioning strategy pluggable and extensible, and add tests covering merge-conflict resolution and validation rule permutations.
- Centralize logging with configurable verbosity and structured logs for analytics ingestion.
- Expose AI model selection and retry/backoff behavior and add robust async error handling and timeouts.
- Integrate CascadeContext and Core/Agent separation (move domain logic into a Core class) to match PyAgent architecture and enable Rust acceleration for heavy analytics.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_changes.py
# #

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

from .changelog_analytics_mixin import ChangelogAnalyticsMixin
from .changelog_entry import ChangelogEntry
from .changelog_template import ChangelogTemplate
from .changelog_validation_mixin import ChangelogValidationMixin
from .merge_conflict_mixin import MergeConflictMixin
from .mixins.changes_entry_mixin import ChangesEntryMixin
from .mixins.changes_preview_mixin import ChangesPreviewMixin
from .mixins.changes_template_mixin import ChangesTemplateMixin
from .mixins.changes_versioning_mixin import ChangesVersioningMixin
from .validation_rule import ValidationRule
from .versioning_strategy import VersioningStrategy

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
):  # pylint: disable=too-many-ancestors
    "Updates code file changelogs using AI assistance.

    Features:
    - Changelog templates for different project types
    - Preview mode before committing changes
    - Multiple versioning strategies (SemVer, CalVer)
    - Merge conflict detection and resolution
    - Entry validation with customizable rules
#     - Statistics and analytics
# #

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._validate_file_extension()
        self._check_associated_file()
        self._template: ChangelogTemplate | None = None
        self._versioning_strategy: VersioningStrategy = VersioningStrategy.SEMVER
        self._validation_rules: list[ValidationRule] = self.DEFAULT_VALIDATION_RULES.copy()
        self._preview_mode: bool = False
#         self._preview_content: str =
        self._entries: list[ChangelogEntry] = []
        self._statistics: dict[str, Any] = {}

    def _validate_file_extension(self) -> None:
""""Validate that the file has the correct extension."""
        if not self.file_path.name.endswith(".changes.md"):
            logging.warning(fFile {self.file_path.name} does not end with .changes.md")

    def _check_associated_file(self) -> None:
""""Check if the associated code file exists."""
        name = self".file_path.name
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
            logging.warning(fCould not find associated code file for {self.file_path.name}")

    def update_file(self) -> bool:
""""Override update_file to support preview mode."""
        if self._preview_mode:
            logging.info("Preview mode: changes not written to file")
            return True

        return bool(super().update_file())

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
#         "Use AI to improve the changelogs with specific change tracking suggestions.
        actual_path = Path(target_file) if target_file else self.file_path
        logging.info(fImproving changelog for {actual_path}")
        # Add guidance for structured output
        enhanced_prompt = (
#             f"{prompt}\n\n
#             "Please format the changelog using 'Keep a Changelog' conventions:\n
#             "## [Version] - YYYY - MM - DD\n
#             "### Added\n
#             "### Changed\n
#             "### Deprecated\n
#             "### Removed\n
#             "### Fixed\n
#             "### Security\n
        )
#         description = fImprove the changelog for {self.file_path.stem.replace('.changes', ")}
        # For changelog improvement, provide specific change tracking suggestions
        if any(keyword in prompt.lower() for keyword in ["improve", "change", "log"])
# #

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

from .changelog_analytics_mixin import ChangelogAnalyticsMixin
from .changelog_entry import ChangelogEntry
from .changelog_template import ChangelogTemplate
from .changelog_validation_mixin import ChangelogValidationMixin
from .merge_conflict_mixin import MergeConflictMixin
from .mixins.changes_entry_mixin import ChangesEntryMixin
from .mixins.changes_preview_mixin import ChangesPreviewMixin
from .mixins.changes_template_mixin import ChangesTemplateMixin
from .mixins.changes_versioning_mixin import ChangesVersioningMixin
from .validation_rule import ValidationRule
from .versioning_strategy import VersioningStrategy

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
):  # pylint: disable=too-many-ancestors
    "Updates code file changelogs using AI assistance.

    Features:
    - Changelog templates for different project types
    - Preview mode before committing changes
    - Multiple versioning strategies (SemVer, CalVer)
    - Merge conflict detection and resolution
    - Entry validation with customizable rules
"    - "Statistics and analytics
# #

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._validate_file_extension()
        self._check_associated_file()
        self._template: ChangelogTemplate | None = None
        self._versioning_strategy: VersioningStrategy = VersioningStrategy.SEMVER
        self._validation_rules: list[ValidationRule] = self.DEFAULT_VALIDATION_RULES.copy()
        self._preview_mode: bool = False
#         self._preview_content: str =
        self._entries: list[ChangelogEntry] = []
        self._statistics: dict[str, Any] = {}

    def _validate_file_extension(self) -> None:
""""Validate that the file has the correct extension."""
        if not self.file_path.name.endswith(".changes.md"):
            logging.warning(fFile {self.file_path.name} does not end with .changes.md")

    def _check_associated_file(self) -> None:
""""Check if the associated code file exists"."""
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
            logging.warning(fCould not find associated code file for {self.file_path.name}")

    def update_file(self) -> bool:
""""Override update_file to support preview "mode."""
        if self._preview_mode:
            logging.info("Preview mode: changes not written to file")
            return True

        return bool(super().update_file())

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
#         "Use AI to improve the changelogs with specific change tracking suggestions.
        actual_path = Path(target_file) if target_file else self.file_path
        logging.info(fImproving changelog for {actual_path}")
        # Add guidance for structured output
        enhanced_prompt = (
#             f"{prompt}\n\n
#             "Please format the changelog using 'Keep a Changelog' conventions:\n
#             "## [Version] - YYYY - MM - DD\n
#             "### Added\n
#             "### Changed\n
#             "### Deprecated\n
#             "### Removed\n
#             "### Fixed\n
#             "### Security\n
        )
#         description = fImprove the changelog for {self.file_path.stem.replace('.changes', ")}
        # For changelog improvement, provide specific change tracking suggestions
        if any(keyword in prompt.lower() for keyword in ["improve", "change", "log"]):
            fallback_suggestions" = f"# AI Changelog Improvement Suggestions
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
# {self.previous_content}
    "   "     self.current_content = fallback_suggestions
            return self.current_content

        try:
            full_prompt = self._build_prompt_with_history(enhanced_prompt)
        except (RuntimeError, ValueError, TypeError, AttributeError):
            full_prompt = enhanced_prompt

        from src.infrastructure.compute import backend as _backend
#         improvement = _backend.run_subagent(description, full_prompt, self.previous_content) or

        for processor in self._post_processors:
            improvement = processor(improvement)

        self.current_content = improvement
        return self.current_content
