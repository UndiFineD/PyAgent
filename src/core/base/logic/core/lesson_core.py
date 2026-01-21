"""
Core logic for Agent Learning and Shared Memory.
"""

from __future__ import annotations
import hashlib
from dataclasses import dataclass
from pathlib import Path

try:
    import rust_core as rc

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


@dataclass
class Lesson:
    """Captures a learned pattern or error correction for shared memory."""

    error_pattern: str
    cause: str
    solution: str
    impact_score: float = 0.5


class LessonCore:
    """Core logic for managing shared learnings across the fleet."""

    def __init__(self, persistence_path: str = "data/memory/shared_lessons.json") -> None:
        self.known_failures: set[str] = set()
        self.lessons: list[Lesson] = []
        self.persistence_path = Path(persistence_path)
        self.load_lessons()

    def generate_failure_hash(self, error_msg: str) -> str:
        """Generates a stable hash for an error message (ignoring line numbers/paths)."""
        if HAS_RUST:
            try:
                # pylint: disable=no-member
                # Assuming rust_core has this, otherwise fallback
                return rc.generate_failure_hash(error_msg)  # type: ignore[attr-defined]
            except Exception: # pylint: disable=broad-exception-caught
                pass
        # Simple normalization: lower case and strip numbers
        normalized = "".join([c for c in error_msg.lower() if not c.isdigit()])
        return hashlib.sha256(normalized.encode()).hexdigest()

    def is_known_failure(self, error_msg: str) -> bool:
        """Checks if the failure mode has been encountered before."""
        f_hash = self.generate_failure_hash(error_msg)
        return f_hash in self.known_failures

    def record_lesson(self, lesson: Lesson) -> str:
        """Records a new lesson and returns the failure hash."""
        f_hash = self.generate_failure_hash(lesson.error_pattern)
        if f_hash not in self.known_failures:
            self.known_failures.add(f_hash)
            self.lessons.append(lesson)
            self.save_lessons()
        return f_hash

    def save_lessons(self) -> None:
        """Persists lessons to disk."""
        try:
            self.persistence_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "known_failures": list(self.known_failures),
                "lessons": [
                    {
                        "error_pattern": l.error_pattern,
                        "cause": l.cause,
                        "solution": l.solution,
                        "impact_score": l.impact_score
                    } for l in self.lessons
                ]
            }
            with open(self.persistence_path, "w", encoding="utf-8") as f:
                import json
                json.dump(data, f, indent=2)
        except Exception as e: # pylint: disable=broad-exception-caught
            import logging
            logging.error("Failed to save lessons: %s", e)

    def load_lessons(self) -> None:
        """Loads lessons from disk."""
        if not self.persistence_path.exists():
            return
        try:
            with open(self.persistence_path, "r", encoding="utf-8") as f:
                import json
                data = json.load(f)
                self.known_failures = set(data.get("known_failures", []))
                self.lessons = [
                    Lesson(**l) for l in data.get("lessons", [])
                ]
        except Exception as e: # pylint: disable=broad-exception-caught
            import logging
            logging.error("Failed to load lessons: %s", e)

    def get_related_lessons(
        self, error_msg: str, all_lessons: list[Lesson]
    ) -> list[Lesson]:
        """Returns lessons that match the normalized error pattern."""
        target_hash = self.generate_failure_hash(error_msg)
        return [
            lesson
            for lesson in all_lessons
            if self.generate_failure_hash(lesson.error_pattern) == target_hash
        ]
