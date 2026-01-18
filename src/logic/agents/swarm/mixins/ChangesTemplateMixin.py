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
Template management logic for ChangesAgent.
"""

from __future__ import annotations
import logging
from typing import List
from ..ChangelogTemplate import ChangelogTemplate

class ChangesTemplateMixin:
    """Mixin for managing changelog templates."""

    # Default templates for different project types
    DEFAULT_TEMPLATES: dict[str, ChangelogTemplate] = {
        "python": ChangelogTemplate(
            name="Python",
            project_type="python",
            sections=["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"],
            include_contributors=True,
        ),
        "javascript": ChangelogTemplate(
            name="JavaScript",
            project_type="javascript",
            sections=["Features", "Bug Fixes", "Breaking Changes", "Documentation"],
        ),
        "generic": ChangelogTemplate(
            name="Generic",
            project_type="generic",
            sections=["Added", "Changed", "Fixed", "Removed"],
        ),
    }

    def set_template(self, template_name: str) -> None:
        """Set the changelog template by name."""
        if template_name in self.DEFAULT_TEMPLATES:
            self._template = self.DEFAULT_TEMPLATES[template_name]
            logging.info(f"Using template: {self._template.name}")
        else:
            logging.warning(f"Unknown template '{template_name}', using generic")
            self._template = self.DEFAULT_TEMPLATES["generic"]

    def create_custom_template(
        self,
        name: str,
        project_type: str,
        sections: List[str],
        header_format: str = "## [{version}] - {date}",
        include_links: bool = True,
        include_contributors: bool = False,
    ) -> ChangelogTemplate:
        """Create a custom changelog template."""
        template = ChangelogTemplate(
            name=name,
            project_type=project_type,
            sections=sections,
            header_format=header_format,
            include_links=include_links,
            include_contributors=include_contributors,
        )
        self._template = template
        return template

    def get_template_sections(self) -> List[str]:
        """Get the sections for the current template."""
        if hasattr(self, "_template") and self._template:
            return self._template.sections
        return ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]
