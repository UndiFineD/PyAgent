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
from src.core.base.Version import VERSION
from .CodeIssue import CodeIssue
from .ExportFormat import ExportFormat
from pathlib import Path
import json
import logging
import re

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
        html_content = re.sub(
            r"# (.+)$", r"<h1>\1</h1>", html_content, flags=re.MULTILINE
        )
        html_content = re.sub(
            r"## (.+)$", r"<h2>\1</h2>", html_content, flags=re.MULTILINE
        )
        html_content = re.sub(
            r"^- (.+)$", r"<li>\1</li>", html_content, flags=re.MULTILINE
        )
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

    def export(
        self, content: str, format: ExportFormat, output_path: Path | None = None
    ) -> str:
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
