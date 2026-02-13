#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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
Export Format - Enum of supported report export formats

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
Import ExportFormat and use members to select report output format, e.g. ExportFormat.JSON, ExportFormat.HTML; compare with ExportFormat.PDF.value for string filename extensions or to route exporters.

WHAT IT DOES:
Defines a simple Enum (ExportFormat) listing supported report export formats (json, html, pdf, csv) and exposes module __version__ from src.core.base.lifecycle.version for bookkeeping.

WHAT IT SHOULD DO BETTER:
Document intended mapping to MIME types and file extensions, provide utility helpers (from_extension, to_mime, list_supported), include unit tests and integration points with the report-generation pipeline, and validate/normalize input when parsing strings to enum members.

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


class ExportFormat(Enum):
    """Export formats for reports."""

    JSON = "json"
    HTML = "html"
    PDF = "pdf"
    CSV = "csv"
"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ExportFormat(Enum):
    """Export formats for reports."""

    JSON = "json"
    HTML = "html"
    PDF = "pdf"
    CSV = "csv"
