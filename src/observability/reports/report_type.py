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
report_type.py - Defines ReportType enum for agent report categories

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Import the module and use ReportType to select or compare report kinds when generating agent reports:
  from src.interface.reports.report_type import ReportType
  if report.type == ReportType.ERRORS: ...
- Use ReportType.value to obtain the canonical string for serialization, filenames, or CLI flags.
- Use enum membership (ReportType('errors')) to parse incoming strings safely.

WHAT IT DOES:
- Provides a single, small Enum (ReportType) that centralizes the canonical report category identifiers used across the reporting codepath.
- Exposes module __version__ from src.core.base.lifecycle.version.VERSION so report code can stamp generated artifacts with the package version.
- Keeps report category strings consistent (description, errors, improvements, summary) to avoid magic strings sprinkled through the codebase.

WHAT IT SHOULD DO BETTER:
- Add module-level documentation and explicit import path comments so callers know the intended import location and stability guarantees.
- Provide utility methods or mappings (e.g., human-readable labels, file name templates, CLI flag parsing helpers) to avoid repetitive string handling elsewhere.
- Include unit tests that assert serialization/deserialization, case-insensitive parsing, and that the enum values remain stable across releases; consider a runtime guard that fails fast if external config expects additional types.
- Document backward-compatibility policy for adding/removing report types and consider extensibility hooks (e.g., allow plugins to register new report types).

FILE CONTENT SUMMARY:
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


"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ReportType(Enum):
    """Type of report to generate."""

    DESCRIPTION = "description"
    ERRORS = "errors"
    IMPROVEMENTS = "improvements"
    SUMMARY = "summary"
"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ReportType(Enum):
    """Type of report to generate."""

    DESCRIPTION = "description"
    ERRORS = "errors"
    IMPROVEMENTS = "improvements"
    SUMMARY = "summary"
