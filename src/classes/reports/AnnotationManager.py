#!/usr/bin/env python3

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from .ReportAnnotation import ReportAnnotation

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

class AnnotationManager:
    """Manager for report annotations and comments.
    Handles adding, retrieving, and managing annotations on reports.
    Attributes:
        annotations: Annotations by report ID.
    Example:
        manager=AnnotationManager()
        manager.add_annotation("report1", "user", "Important note")
        notes=manager.get_annotations("report1")
    """

    def __init__(self) -> None:
        """Initialize annotation manager."""

        self.annotations: Dict[str, List[ReportAnnotation]] = {}
        self._annotation_counter = 0
        logging.debug("AnnotationManager initialized")

    def add_annotation(
        self,
        report_id: str,
        author: str,
        content: str,
        line_number: Optional[int] = None
    ) -> ReportAnnotation:
        """Add an annotation.
        Args:
            report_id: Report to annotate.
            author: Annotation author.
            content: Annotation content.
            line_number: Line number if applicable.
        Returns:
            Created annotation.
        """

        self._annotation_counter += 1
        annotation_id = f"ann_{report_id}_{self._annotation_counter}"
        annotation = ReportAnnotation(
            annotation_id=annotation_id,
            report_id=report_id,
            author=author,
            content=content,
            line_number=line_number
        )
        if report_id not in self.annotations:
            self.annotations[report_id] = []
        self.annotations[report_id].append(annotation)
        return annotation

    def get_annotations(self, report_id: str) -> List[ReportAnnotation]:
        """Get annotations for a report.
        Args:
            report_id: Report ID.
        Returns:
            List of annotations.
        """

        return self.annotations.get(report_id, [])

    def remove_annotation(self, annotation_id: str) -> bool:
        """Remove an annotation.
        Args:
            annotation_id: Annotation to remove.
        Returns:
            True if removed.
        """

        for report_id, anns in list(self.annotations.items()):
            for i, ann in enumerate(anns):
                if ann.annotation_id == annotation_id:
                    self.annotations[report_id].pop(i)
                    return True
        return False
