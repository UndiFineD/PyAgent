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


"""
ReportArchiver - Manage report archiving and retention

[Brief Summary]
A lightweight in-memory manager for archiving, retrieving and pruning historical reports with a simple retention policy. DATE: 2026-02-12
AUTHOR: Keimpe de Jong

USAGE:
from pathlib import Path
from report_archiver import ReportArchiver
archiver = ReportArchiver(Path("./archives"))
entry = archiver.archive("src/module.py", "report content", retention_days=30)
archiver.list_archives("src/module.py")
archiver.get_archive(entry.report_id)
removed_count = archiver.cleanup_expired()

WHAT IT DOES:
- Provides an API to create ArchivedReport entries keyed by source file path.
- Keeps an in-memory index (self.archives) mapping file paths to lists of ArchivedReport objects.
- Generates report_id using the file path and epoch timestamp, and supports listing, lookup and retention-based cleanup.

WHAT IT SHOULD DO BETTER:
- Persist archives to disk (or use StateTransaction) so archives survive process restarts instead of only in-memory storage.
- Add thread/process-safety and atomic file operations for concurrent access and long-running agents.
- Use Path types for file_path parameters, richer metadata (author, format), configurable retention policies per namespace, timezone-aware timestamps, and unit tests covering edge cases.
- Improve logging and error handling, and integrate with the project's archival storage or rust_core for high-throughput scenarios.

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

import logging
import time
from pathlib import Path

from src.core.base.lifecycle.version import VERSION

from .archived_report import ArchivedReport

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

    def archive(self, file_path: str, content: str, retention_days: int = 90) -> ArchivedReport:
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
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

from src.core.base.lifecycle.version import VERSION

from .archived_report import ArchivedReport

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

    def archive(self, file_path: str, content: str, retention_days: int = 90) -> ArchivedReport:
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
