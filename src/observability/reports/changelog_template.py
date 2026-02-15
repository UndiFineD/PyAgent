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
changelog_template.py - Changelog entry template dataclass

DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Import ChangelogTemplate and instantiate with project name and type:
  from src.tools.changelog_template import ChangelogTemplate
  tmpl = ChangelogTemplate(name="pyagent", project_type="library")
- Customize sections, header_format, include_links and include_contributors as needed and render your changelog generator around this template.
- Typical use: collect changelog items per section, format version/date into header_format, and emit Markdown using sections order.

WHAT IT DOES:
- Provides a simple dataclass that defines the shape and defaults for changelog generation: project name, project_type, ordered sections (Added, Changed, Deprecated, Removed, Fixed, Security), header format template, and booleans controlling links and contributor inclusion.
- Centralizes changelog formatting defaults so other code can compose or render changelog entries consistently across the project.

WHAT IT SHOULD DO BETTER:
- Add validation (e.g., non-empty name/project_type and valid header_format placeholders), and type-safe section names.
- Provide helper methods to render a full changelog entry to Markdown (inject version, date, links, and contributors), and utilities for semantic-version sorting and link resolution.
- Support localization for date formatting, configurable section ordering, and optional per-section metadata (e.g., item authors, PR links).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ChangelogTemplate:
    """Template for changelog entries."""

    name: str
    project_type: str
    sections: list[str] = field(
        default_factory=lambda: [
            "Added",
            "Changed",
            "Deprecated",
            "Removed",
            "Fixed",
            "Security",
        ]
    )
    header_format: str = "## [{version}] - {date}"
    include_links: bool = True
    include_contributors: bool = False
