#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

"""Minimal Lesson model to satisfy imports during tests.

This provides small, well-typed placeholders used by mixins and
other components during test collection.
"""

@dataclass
class Lesson:
    id: str
    title: str = ""
    content: str = ""


class LessonCore:
    """Lightweight facade for lesson operations used in tests."""

    def create_lesson(self, title: str, content: str) -> Lesson:
        return Lesson(id="generated", title=title, content=content)

    def get_lesson(self, lesson_id: str) -> Any:
        return None


__all__ = ["Lesson", "LessonCore"]
