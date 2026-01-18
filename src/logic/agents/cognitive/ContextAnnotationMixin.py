#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
import hashlib
from datetime import datetime
from src.logic.agents.cognitive.context.models.ContextAnnotation import ContextAnnotation


class ContextAnnotationMixin:
    """Annotation methods for ContextAgent."""

    def add_annotation(
        self, line_number: int, content: str, author: str = ""
    ) -> ContextAnnotation:
        """Add an annotation to the context."""
        annotation = ContextAnnotation(
            id=hashlib.md5(f"{line_number}:{content}".encode()).hexdigest()[:8],
            line_number=line_number,
            content=content,
            author=author,
            timestamp=datetime.now().isoformat(),
        )
        if not hasattr(self, "_annotations"):
            self._annotations: list[ContextAnnotation] = []
        self._annotations.append(annotation)
        return annotation

    def get_annotations(self) -> list[ContextAnnotation]:
        """Get all annotations."""
        return getattr(self, "_annotations", [])

    def get_annotations_for_line(self, line_number: int) -> list[ContextAnnotation]:
        """Get annotations for a specific line."""
        return [a for a in getattr(self, "_annotations", []) if a.line_number == line_number]

    def resolve_annotation(self, annotation_id: str) -> bool:
        """Mark an annotation as resolved."""
        for annotation in getattr(self, "_annotations", []):
            if annotation.id == annotation_id:
                annotation.resolved = True
                return True
        return False

    def remove_annotation(self, annotation_id: str) -> bool:
        """Remove an annotation."""
        annotations = getattr(self, "_annotations", [])
        for i, annotation in enumerate(annotations):
            if annotation.id == annotation_id:
                del annotations[i]
                return True
        return False
