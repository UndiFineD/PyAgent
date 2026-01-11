#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_improvements.py"""

from .ArchivedImprovement import ArchivedImprovement
from .Improvement import Improvement
from .ImprovementCategory import ImprovementCategory

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, cast
import hashlib
import json
import logging
import re
import subprocess
import time


































from src.core.base.version import VERSION
__version__ = VERSION

class ImprovementArchive:
    """Archives old or completed improvements.

    Maintains history of archived improvements.

    Attributes:
        archive: List of archived improvements.
    """

    def __init__(self) -> None:
        """Initialize the archive."""
        self.archive: List[ArchivedImprovement] = []

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

    def restore(self, improvement_id: str) -> Optional[Improvement]:
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
        category: Optional[ImprovementCategory] = None
    ) -> List[ArchivedImprovement]:
        """Search the archive.

        Args:
            query: Text to search for.
            category: Filter by category.

        Returns:
            Matching archived improvements.
        """
        results: List[ArchivedImprovement] = []
        for archived in self.archive:
            imp = archived.improvement
            if category and imp.category != category:
                continue
            if query and query.lower() not in imp.title.lower():
                continue
            results.append(archived)
        return results

    def get_archive_stats(self) -> Dict[str, Any]:
        """Get archive statistics."""
        by_category: Dict[str, int] = {}
        for archived in self.archive:
            cat = archived.improvement.category.value
            by_category[cat] = by_category.get(cat, 0) + 1

        return {
            "total_archived": len(self.archive),
            "by_category": by_category
        }
