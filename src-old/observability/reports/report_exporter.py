#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/observability/reports/report_exporter.description.md

# Description: src/observability/reports/report_exporter.py

Module overview:
- `ReportExporter` converts report content into various export formats (HTML, CSV, JSON) and can write to disk.
- Provides `to_html`, `to_csv`, and `export` methods for simple conversions.

Behavioral notes:
- Uses lightweight regex-based Markdown-to-HTML conversion; suitable for basic reports but not full CommonMark fidelity.
- `to_csv` expects a list of `CodeIssue` objects.

Public classes/functions:
- `ReportExporter` with methods `to_html`, `to_csv`, `export`.
## Source: src-old/observability/reports/report_exporter.improvements.md

# Improvements: src/observability/reports/report_exporter.py

Potential improvements:
- Replace ad-hoc markdown-to-HTML conversion with a robust library like `markdown` or `marko` to support full syntax.
- Add unit tests for `to_html` and `to_csv` with varied inputs and edge cases (special characters, quotes, newlines).
- Allow configurable CSV delimiter and quoting behavior.
- Provide async or streaming export methods for large reports to avoid loading everything into memory.
- Validate `CodeIssue` shapes and add graceful handling for missing fields.
- Add options for PDF/PPT export via third-party libraries (pandoc, weasyprint) if needed.

LLM_CONTEXT_END
"""
from __future__ import annotations


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


r"""Auto-extracted class from generate_agent_reports.py"""
