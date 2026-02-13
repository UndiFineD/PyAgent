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
Report Exporter - Exporting reports to multiple formats

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate and use programmatically:
  exporter = ReportExporter()
  html = exporter.to_html(markdown_text, title="My Report")
  csv_text = exporter.to_csv(list_of_CodeIssue_objects)
  exporter.export(report_text, ExportFormat.HTML, Path("report.html"))
- Intended for CLI or programmatic integration where simple HTML/JSON/CSV exports suffice.

WHAT IT DOES:
- Provides a lightweight ReportExporter class that converts simple markdown-like text to minimal HTML, serializes report content to JSON, and renders a list of CodeIssue objects as CSV.
- to_html: Performs basic regex-based conversions for top-level headings, second-level headings, list items and inline code.
- to_csv: Emits a CSV header and rows for CodeIssue.message, category, severity, line_number and function_name; values are minimally quoted.
- export: Chooses HTML/JSON/raw output based on ExportFormat and optionally writes the result to disk using Path.write_text.

WHAT IT SHOULD DO BETTER:
- Use a proper markdown renderer (e.g., python-markdown or mistune) to correctly handle nested lists, code blocks, links, emphasis, and HTML sanitization instead of fragile regex substitutions.
- Properly escape and CSV-quote fields (use csv module) to avoid broken CSV for messages containing newlines, commas or quotes; include encoding and newline handling for cross-platform correctness.
- Expand supported formats (PDF, PPTX) via robust libraries (weasyprint, reportlab, python-pptx) and add streaming/output buffering for large reports.
- Improve error handling and logging (raise informative exceptions on I/O errors), add type validation for inputs, and provide async variants for integration with asyncio-based workflows.
- Add unit tests for edge cases, CI coverage, and configuration for templates, CSS, and HTML sanitization to prevent XSS when embedding untrusted content.

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

import json
import logging
import re
from pathlib import Path

from src.core.base.lifecycle.version import VERSION

from .code_issue import CodeIssue
from .export_format import ExportFormat

__version__ = VERSION


class ReportExporter:
    """Exporter for various report formats.
    Exports reports to different formats including PDF, PPT, CSV.
    Example:
        exporter=ReportExporter()
        html=exporter.to_html(markdown_content)
        csv_data=exporter.to_csv(issues)
    """

    def __init__(self) -> None:
        """Initialize exporter."""

        logging.debug("ReportExporter initialized")

    def to_html(self, content: str, title: str = "Report") -> str:
        """Convert markdown to HTML.
        Args:
            content: Markdown content.
            title: Document title.
        Returns:
            HTML content.
        """

        # Simple markdown to HTML conversion
        html_content = content
        html_content = re.sub(r"# (.+)$", r"<h1>\1</h1>", html_content, flags=re.MULTILINE)
        html_content = re.sub(r"## (.+)$", r"<h2>\1</h2>", html_content, flags=re.MULTILINE)
        html_content = re.sub(r"^- (.+)$", r"<li>\1</li>", html_content, flags=re.MULTILINE)
        html_content = re.sub(r"`([^`]+)`", r"<code>\1</code>", html_content)
        return f"""<!DOCTYPE html>
<html>
<head><title>{title}</title></head>
<body>{html_content}</body>
</html>"""

    def to_csv(self, issues: list[CodeIssue]) -> str:
        """Export issues to CSV.
        Args:
            issues: List of issues.
        Returns:
            CSV content.
        """

        lines = ["message,category,severity,line_number,function_name"]
        for issue in issues:
            lines.append(
                f'"{issue.message}",{issue.category.name},{issue.severity.name},'
                f'{issue.line_number or ""},"{issue.function_name or ""}"'
            )
        return "\n".join(lines)

    def export(self, content: str, format: ExportFormat, output_path: Path | None = None) -> str:
        """Export report to format.
        Args:
            content: Report content.
            format: Target format.
            output_path: Optional output file.
        Returns:
            Exported content.
        """

        if format == ExportFormat.HTML:
            result = self.to_html(content)
        elif format == ExportFormat.JSON:
            result = json.dumps({"content": content})
        else:
            result = content
        if output_path:
            output_path.write_text(result, encoding="utf-8")
        return result
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path

from src.core.base.lifecycle.version import VERSION

from .code_issue import CodeIssue
from .export_format import ExportFormat

__version__ = VERSION


class ReportExporter:
    """Exporter for various report formats.
    Exports reports to different formats including PDF, PPT, CSV.
    Example:
        exporter=ReportExporter()
        html=exporter.to_html(markdown_content)
        csv_data=exporter.to_csv(issues)
    """

    def __init__(self) -> None:
        """Initialize exporter."""

        logging.debug("ReportExporter initialized")

    def to_html(self, content: str, title: str = "Report") -> str:
        """Convert markdown to HTML.
        Args:
            content: Markdown content.
            title: Document title.
        Returns:
            HTML content.
        """

        # Simple markdown to HTML conversion
        html_content = content
        html_content = re.sub(r"# (.+)$", r"<h1>\1</h1>", html_content, flags=re.MULTILINE)
        html_content = re.sub(r"## (.+)$", r"<h2>\1</h2>", html_content, flags=re.MULTILINE)
        html_content = re.sub(r"^- (.+)$", r"<li>\1</li>", html_content, flags=re.MULTILINE)
        html_content = re.sub(r"`([^`]+)`", r"<code>\1</code>", html_content)
        return f"""<!DOCTYPE html>
<html>
<head><title>{title}</title></head>
<body>{html_content}</body>
</html>"""

    def to_csv(self, issues: list[CodeIssue]) -> str:
        """Export issues to CSV.
        Args:
            issues: List of issues.
        Returns:
            CSV content.
        """

        lines = ["message,category,severity,line_number,function_name"]
        for issue in issues:
            lines.append(
                f'"{issue.message}",{issue.category.name},{issue.severity.name},'
                f'{issue.line_number or ""},"{issue.function_name or ""}"'
            )
        return "\n".join(lines)

    def export(self, content: str, format: ExportFormat, output_path: Path | None = None) -> str:
        """Export report to format.
        Args:
            content: Report content.
            format: Target format.
            output_path: Optional output file.
        Returns:
            Exported content.
        """

        if format == ExportFormat.HTML:
            result = self.to_html(content)
        elif format == ExportFormat.JSON:
            result = json.dumps({"content": content})
        else:
            result = content
        if output_path:
            output_path.write_text(result, encoding="utf-8")
        return result
