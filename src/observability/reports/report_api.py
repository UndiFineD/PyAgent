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
from src.core.base.version import VERSION
from .report_type import ReportType
from pathlib import Path
import logging

__version__ = VERSION

# Define AGENT_DIR for default parameter

AGENT_DIR = Path(__file__).resolve().parent.parent.parent  # src/


class ReportAPI:
    """API for programmatic report access.
    Provides a RESTful - style interface for report operations.
    Example:
        api=ReportAPI()
        reports=api.list_reports()
        report=api.get_report("file.py", ReportType.ERRORS)
    """

    def __init__(self, reports_dir: Path = AGENT_DIR) -> None:
        """Initialize API.
        Args:
            reports_dir: Directory containing reports.
        """
        self.reports_dir = reports_dir
        logging.debug(f"ReportAPI initialized for {reports_dir}")

    def list_reports(self, file_pattern: str = "*.md") -> list[str]:
        """List available reports.
        Args:
            file_pattern: Glob pattern.
        Returns:
            List of report paths.
        """

        return [str(p) for p in self.reports_dir.glob(file_pattern)]

    def get_report(self, file_stem: str, report_type: ReportType) -> str | None:
        """Get a specific report.
        Args:
            file_stem: File stem.
            report_type: Report type.
        Returns:
            Report content if found.
        """

        suffix_map = {
            ReportType.DESCRIPTION: ".description.md",
            ReportType.ERRORS: ".errors.md",
            ReportType.IMPROVEMENTS: ".improvements.md",
        }
        suffix = suffix_map.get(report_type, ".md")
        path = self.reports_dir / f"{file_stem}{suffix}"
        if path.exists():
            return path.read_text(encoding="utf-8")
        return None

    def create_report(
        self, file_stem: str, report_type: ReportType, content: str
    ) -> bool:
        """Create or update a report.
        Args:
            file_stem: File stem.
            report_type: Report type.
            content: Report content.
        Returns:
            True if successful.
        """

        suffix_map = {
            ReportType.DESCRIPTION: ".description.md",
            ReportType.ERRORS: ".errors.md",
            ReportType.IMPROVEMENTS: ".improvements.md",
        }
        suffix = suffix_map.get(report_type, ".md")
        path = self.reports_dir / f"{file_stem}{suffix}"
        try:
            path.write_text(content, encoding="utf-8")
            return True
        except Exception:
            return False
