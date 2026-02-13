#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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
Annotation Manager - Manage report annotations

Lightweight in-memory manager for ReportAnnotation objects keyed by report ID.

DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate AnnotationManager and use add_annotation(report_id, author, content, line_number=None) to create annotations.
- Retrieve annotations with get_annotations(report_id).
- Remove by annotation_id using remove_annotation(annotation_id).
Example:
manager = AnnotationManager()
ann = manager.add_annotation("report1", "user", "Important note")
notes = manager.get_annotations("report1")
removed = manager.remove_annotation(ann.annotation_id)

WHAT IT DOES:
- Keeps annotations in an in-memory dict mapping report_id -> list[ReportAnnotation].
- Generates simple unique annotation IDs using an incremental counter and report_id.
- Provides three primary operations: add_annotation, get_annotations, and remove_annotation.
- Minimal logging on initialization; relies on ReportAnnotation for annotation structure.

WHAT IT SHOULD DO BETTER:
- Persist annotations to durable storage (DB or file) so annotations survive process restarts.
- Add thread/process-safety (locks or transactional state manager) for concurrent use.
- Validate inputs and return richer error information (exceptions vs booleans).
- Expose APIs for updating annotations, bulk operations, searching/filtering, and timestamping metadata.
- Improve ID generation to avoid collisions across processes and include creation timestamps.
- Add comprehensive unit tests and stronger logging for operational visibility.

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

from src.core.base.lifecycle.version import VERSION

from .report_annotation import ReportAnnotation

__version__ = VERSION


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

        self.annotations: dict[str, list[ReportAnnotation]] = {}
        self._annotation_counter = 0
        logging.debug("AnnotationManager initialized")

    def add_annotation(
        self, report_id: str, author: str, content: str, line_number: int | None = None
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
            line_number=line_number,
        )
        if report_id not in self.annotations:
            self.annotations[report_id] = []
        self.annotations[report_id].append(annotation)
        return annotation

    def get_annotations(self, report_id: str) -> list[ReportAnnotation]:
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
"""

from __future__ import annotations

import logging

from src.core.base.lifecycle.version import VERSION

from .report_annotation import ReportAnnotation

__version__ = VERSION


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

        self.annotations: dict[str, list[ReportAnnotation]] = {}
        self._annotation_counter = 0
        logging.debug("AnnotationManager initialized")

    def add_annotation(
        self, report_id: str, author: str, content: str, line_number: int | None = None
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
            line_number=line_number,
        )
        if report_id not in self.annotations:
            self.annotations[report_id] = []
        self.annotations[report_id].append(annotation)
        return annotation

    def get_annotations(self, report_id: str) -> list[ReportAnnotation]:
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
