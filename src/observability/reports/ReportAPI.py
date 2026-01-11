#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from generate_agent_reports.py"""

from .ReportType import ReportType

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, cast
import ast
import hashlib
import json
import logging
import re
import sys
import time

# Define AGENT_DIR for default parameter

































from src.core.base.version import VERSION
__version__ = VERSION

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

    def list_reports(self, file_pattern: str = "*.md") -> List[str]:
        """List available reports.
        Args:
            file_pattern: Glob pattern.
        Returns:
            List of report paths.
        """

        return [str(p) for p in self.reports_dir.glob(file_pattern)]

    def get_report(self, file_stem: str, report_type: ReportType) -> Optional[str]:
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
        self,
        file_stem: str,
        report_type: ReportType,
        content: str
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
