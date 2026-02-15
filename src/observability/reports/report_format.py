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
Report Format - Enumerating supported report output formats"""
"""
[Brief Summary]
# DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Import the enum and use the members to select an output format for report generation:
  from report_format import ReportFormat, __version__
  fmt = ReportFormat.MARKDOWN
- Compare or switch on fmt.value to drive serialization, templating, or renderer selection.
- Use __version__ to tag generated reports with the library version.

WHAT IT DOES:
- Declares a small, explicit Enum (ReportFormat) that centralizes the supported output formats for the reporting subsystem (markdown, json, html).
- Exposes a __version__ value sourced from the project's lifecycle version for consistent version tagging.

WHAT IT SHOULD DO BETTER:
- Provide mappings to MIME types, file extensions, or serializer functions so consumers don't duplicate format-to-handler logic.
- Add unit tests and examples showing how to use the enum with the report generator, and include docstrings explaining intended semantics (e.g., whether HTML includes full pages or fragments).
- Consider adding a fallback/unknown member or a factory that returns a renderer object (strategy pattern) to decouple format selection from serialization logic.

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
"""""""""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ReportFormat(Enum):
    """Output format for report""""""s."""

    MARKDOWN = "markdown"
    JSON = "json"
    HTML = "html"
