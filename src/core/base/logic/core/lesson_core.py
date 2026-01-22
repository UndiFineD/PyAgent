"""
Core logic for Agent Learning and Shared Memory.
(Facade for src.core.base.common.lesson_core)
"""

from src.core.base.common.lesson_core import (
    LessonCore as StandardLessonCore,
    Lesson as Lesson
)


class LessonCore(StandardLessonCore):
    """
    Facade for StandardLessonCore to maintain backward compatibility.
    Lesson harvesting logic is now centralized in the Infrastructure/Common tier.
    """
    pass
