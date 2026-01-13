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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from src.logic.agents.cognitive.context.models.ExportFormat import ExportFormat
from src.logic.agents.cognitive.context.models.ExportedContext import ExportedContext
from datetime import datetime
from typing import List, Optional
import re

__version__ = VERSION

class ContextExporter:
    """Exports context to documentation systems.

    Provides functionality to export context to various formats.

    Example:
        >>> exporter=ContextExporter()
        >>> exported=exporter.export(content, ExportFormat.HTML)
    """

    def __init__(self, default_format: ExportFormat = ExportFormat.MARKDOWN) -> None:
        self.default_format: ExportFormat = default_format

    def set_format(self, format: ExportFormat) -> None:
        """Set the default export format."""
        self.default_format = format

    def get_supported_formats(self) -> List[ExportFormat]:
        """Return all supported export formats."""
        return list(ExportFormat)

    def export(self, content: str, format: Optional[ExportFormat] = None) -> ExportedContext:
        """Export context to specified format.

        Args:
            content: Context content to export.
            format: Target export format. If omitted, uses default_format.

        Returns:
            ExportedContext with exported content.
        """
        fmt = format if format is not None else self.default_format

        exported_content = content
        if fmt == ExportFormat.HTML:
            exported_content = self._to_html(content)
        elif fmt == ExportFormat.RST:
            exported_content = self._to_rst(content)
        return ExportedContext(
            format=fmt,
            content=exported_content,
            created_at=datetime.now().isoformat()
        )

    def _to_html(self, content: str) -> str:
        """Convert markdown to HTML."""
        # Simplified conversion
        html = content
        html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.M)
        html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.M)
        html = re.sub(r"^- (.+)$", r"<li>\1</li>", html, flags=re.M)
        return f"<html><body>{html}</body></html>"

    def _to_rst(self, content: str) -> str:
        """Convert markdown to RST."""
        rst = content
        # Convert headers
        rst = re.sub(r"^# (.+)$", lambda m: m.group(1) + "\n" +
                     "=" * len(m.group(1)), rst, flags=re.M)
        rst = re.sub(r"^## (.+)$", lambda m: m.group(1) + "\n" +
                     "-" * len(m.group(1)), rst, flags=re.M)
        return rst