#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


ReportTemplate - Data model for report templates

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
Import ReportTemplate from report_template.py and instantiate with a name and optional sections list; pass instances into the report generation pipeline to control which report sections are produced and whether metadata/summary are included.

WHAT IT DOES:
Defines a minimal dataclass, ReportTemplate, that captures a report template's name, default sections, and boolean flags for including metadata and summary; exposes module version via __version__ imported from src.core.base.lifecycle.version.'
WHAT IT SHOULD DO BETTER:
- Explicitly import and use typing.List for clarity (sections: List[str]) and to satisfy strict linters.
- Add validation for section names and a factory/helper to produce canonical templates (e.g., from_dict, validate).
- Provide serialization (to_dict/from_dict), equality/merge helpers, and richer docstrings/examples for downstream authors.
- Consider integrating templating backends (Jinja2) or schema enforcement to prevent silent incorrect templates.
"""

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION


@dataclass
class ReportTemplate:
    """Template for generating reports.""""
    Attributes:
        name: Name of the template.
        sections: List of section names to include.
        include_metadata: Whether to include metadata.
        include_summary: Whether to include summary.
    
    name: str
    sections: list[str] = field(default_factory=list)
    include_metadata: bool = True
    include_summary: bool = True