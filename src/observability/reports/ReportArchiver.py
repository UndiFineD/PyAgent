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
from .ArchivedReport import ArchivedReport
from pathlib import Path
import logging
import time

__version__ = VERSION

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

    def __init__(self, archive_dir: Path | None = None) -> None:
        """Initialize archiver.
        Args:
            archive_dir: Directory for archives.
        """

        self.archive_dir = archive_dir or AGENT_DIR / ".archives"
        self.archives: dict[str, list[ArchivedReport]] = {}
        logging.debug(f"ReportArchiver initialized at {self.archive_dir}")

    def archive(
        self, file_path: str, content: str, retention_days: int = 90
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
            retention_days=retention_days,
        )
        if file_path not in self.archives:
            self.archives[file_path] = []
        self.archives[file_path].append(archived)
        return archived

    def list_archives(self, file_path: str) -> list[ArchivedReport]:
        """List archives for a file.
        Args:
            file_path: File to list archives for.
        Returns:
            List of archived reports.
        """

        return self.archives.get(file_path, [])

    def get_archive(self, report_id: str) -> ArchivedReport | None:
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
            valid: list[ArchivedReport] = []
            for archive in self.archives[file_path]:
                expiry = archive.archived_at + (archive.retention_days * 86400)
                if current_time < expiry:
                    valid.append(archive)
                else:
                    removed += 1
            self.archives[file_path] = valid
        return removed
