#!/usr/bin/env python3

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from .ArchivedReport import ArchivedReport

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
AGENT_DIR = Path(__file__).resolve().parent.parent.parent  # src/

class ReportArchiver:
    """Manager for report archiving with retention policies.
    Handles archiving, retrieval, and cleanup of historical reports.
    Attributes:
        archive_dir: Directory for archived reports.
        archives: In - memory archive index.
    Example:
        archiver=ReportArchiver(Path("./archives"))
        archiver.archive("file.py", report_content)
        old_reports=archiver.list_archives("file.py")
    """

    def __init__(self, archive_dir: Optional[Path] = None) -> None:
        """Initialize archiver.
        Args:
            archive_dir: Directory for archives.
        """

        self.archive_dir = archive_dir or AGENT_DIR / ".archives"
        self.archives: Dict[str, List[ArchivedReport]] = {}
        logging.debug(f"ReportArchiver initialized at {self.archive_dir}")

    def archive(
        self,
        file_path: str,
        content: str,
        retention_days: int = 90
    ) -> ArchivedReport:
        """Archive a report.
        Args:
            file_path: Source file path.
            content: Report content.
            retention_days: Days to retain.
        Returns:
            Created archive entry.
        """

        report_id = f"{file_path}_{int(time.time())}"
        archived = ArchivedReport(
            report_id=report_id,
            file_path=file_path,
            content=content,
            retention_days=retention_days
        )
        if file_path not in self.archives:
            self.archives[file_path] = []
        self.archives[file_path].append(archived)
        return archived

    def list_archives(self, file_path: str) -> List[ArchivedReport]:
        """List archives for a file.
        Args:
            file_path: File to list archives for.
        Returns:
            List of archived reports.
        """

        return self.archives.get(file_path, [])

    def get_archive(self, report_id: str) -> Optional[ArchivedReport]:
        """Get a specific archive.
        Args:
            report_id: Archive ID.
        Returns:
            Archived report if found.
        """

        for archives in self.archives.values():
            for archive in archives:
                if archive.report_id == report_id:
                    return archive
        return None

    def cleanup_expired(self) -> int:
        """Remove expired archives.
        Returns:
            Number of archives removed.
        """

        removed = 0
        current_time = time.time()
        for file_path in list(self.archives.keys()):
            valid: List[ArchivedReport] = []
            for archive in self.archives[file_path]:
                expiry = archive.archived_at + (archive.retention_days * 86400)
                if current_time < expiry:
                    valid.append(archive)
                else:
                    removed += 1
            self.archives[file_path] = valid
        return removed
