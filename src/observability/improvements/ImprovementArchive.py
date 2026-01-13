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

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .ArchivedImprovement import ArchivedImprovement
from .Improvement import Improvement
from .ImprovementCategory import ImprovementCategory
from datetime import datetime
from typing import Any, Dict, List, Optional

__version__ = VERSION

class ImprovementArchive:
    """Archives old or completed improvements.

    Maintains history of archived improvements.

    Attributes:
        archive: List of archived improvements.
    """

    def __init__(self) -> None:
        """Initialize the archive."""
        self.archive: list[ArchivedImprovement] = []

    def archive_improvement(
        self,
        improvement: Improvement,
        reason: str,
        archived_by: str = ""
    ) -> ArchivedImprovement:
        """Archive an improvement.

        Args:
            improvement: The improvement to archive.
            reason: Why it's being archived.
            archived_by: Who archived it.

        Returns:
            The archived improvement record.
        """
        archived = ArchivedImprovement(
            improvement=improvement,
            archived_date=datetime.now().isoformat(),
            archived_by=archived_by,
            archive_reason=reason
        )
        self.archive.append(archived)
        return archived

    def restore(self, improvement_id: str) -> Improvement | None:
        """Restore an archived improvement.

        Args:
            improvement_id: ID of the improvement to restore.

        Returns:
            The restored improvement or None.
        """
        for i, archived in enumerate(self.archive):
            if archived.improvement.id == improvement_id:
                imp = archived.improvement
                del self.archive[i]
                return imp
        return None

    def search_archive(
        self,
        query: str = "",
        category: ImprovementCategory | None = None
    ) -> list[ArchivedImprovement]:
        """Search the archive.

        Args:
            query: Text to search for.
            category: Filter by category.

        Returns:
            Matching archived improvements.
        """
        results: list[ArchivedImprovement] = []
        for archived in self.archive:
            imp = archived.improvement
            if category and imp.category != category:
                continue
            if query and query.lower() not in imp.title.lower():
                continue
            results.append(archived)
        return results

    def get_archive_stats(self) -> dict[str, Any]:
        """Get archive statistics."""
        by_category: dict[str, int] = {}
        for archived in self.archive:
            cat = archived.improvement.category.value
            by_category[cat] = by_category.get(cat, 0) + 1

        return {
            "total_archived": len(self.archive),
            "by_category": by_category
        }