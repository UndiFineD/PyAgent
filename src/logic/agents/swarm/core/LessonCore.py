
from __future__ import annotations
import hashlib
from typing import List, Set
from dataclasses import dataclass

@dataclass
class Lesson:
    error_pattern: str
    cause: str
    solution: str
    impact_score: float = 0.5

class LessonCore:
    """Pure logic for cross-fleet lesson aggregation.
    Uses bloom-filter-like hashing to track known failure modes.
    """
    
    def __init__(self) -> None:
        self.known_failures: Set[str] = set()

    def generate_failure_hash(self, error_msg: str) -> str:
        """Generates a stable hash for an error message (ignoring line numbers/paths)."""
        # Simple normalization: lower case and strip numbers
        normalized = "".join([c for c in error_msg.lower() if not c.isdigit()])
        return hashlib.md5(normalized.encode()).hexdigest()

    def is_known_failure(self, error_msg: str) -> bool:
        """Checks if the failure mode has been encountered before."""
        f_hash = self.generate_failure_hash(error_msg)
        return f_hash in self.known_failures

    def record_lesson(self, lesson: Lesson) -> str:
        """Records a new lesson and returns the failure hash."""
        f_hash = self.generate_failure_hash(lesson.error_pattern)
        self.known_failures.add(f_hash)
        return f_hash

    def get_related_lessons(self, error_msg: str, all_lessons: List[Lesson]) -> List[Lesson]:
        """Returns lessons that match the normalized error pattern."""
        target_hash = self.generate_failure_hash(error_msg)
        return [l for l in all_lessons if self.generate_failure_hash(l.error_pattern) == target_hash]