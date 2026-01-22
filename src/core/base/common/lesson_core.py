# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Unified Lesson and Learning core."""

import hashlib
import json
import logging
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Set, Dict, Any, Optional
from .base_core import BaseCore

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

class LessonCore(BaseCore):
    """
    Standard implementation for managing shared learnings across the fleet.
    Inherits from BaseCore for standardized persistence.
    """

    def __init__(self, persistence_path: Optional[str] = None, repo_root: Optional[str] = None):
        super().__init__(name="Lesson", repo_root=repo_root)
        self.known_failures: Set[str] = set()
        self.lessons: List[Lesson] = []
        self.persistence_path = Path(persistence_path) if persistence_path else self.get_state_path()
        self.load_lessons()

    def generate_failure_hash(self, error_msg: str) -> str:
        """Generates a stable hash for an error message."""
        if HAS_RUST:
            try: return rc.generate_failure_hash(error_msg)
            except Exception: pass
        normalized = "".join([c for c in error_msg.lower() if not c.isdigit()])
        return hashlib.sha256(normalized.encode()).hexdigest()

    def is_known_failure(self, error_msg: str) -> bool:
        """Checks if the failure mode has been encountered before."""
        return self.generate_failure_hash(error_msg) in self.known_failures

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
        data = {
            "known_failures": list(self.known_failures),
            "lessons": [asdict(l) for l in self.lessons]
        }
        self._storage.save_json(self.persistence_path, data)

    def load_lessons(self) -> None:
        """Loads lessons from disk."""
        data = self._storage.load_json(self.persistence_path)
        if data:
            self.known_failures = set(data.get("known_failures", []))
            self.lessons = [Lesson(**l) for l in data.get("lessons", [])]
