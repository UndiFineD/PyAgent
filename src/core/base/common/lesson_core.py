<<<<<<< HEAD
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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
"""Unified Lesson and Learning core."""

import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional, Set

from .base_core import BaseCore

try:
    import rust_core as rc

=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Unified Lesson and Learning core."""

import hashlib
import json
import logging
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Set, Dict, Any, Optional
from src.core.base.common.base_core import BaseCore

try:
    import rust_core as rc
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    HAS_RUST = True
except ImportError:
    HAS_RUST = False

<<<<<<< HEAD

@dataclass
class Lesson:
    """Captures a learned pattern or error correction for shared memory."""

=======
@dataclass
class Lesson:
    """Captures a learned pattern or error correction for shared memory."""
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    error_pattern: str
    cause: str
    solution: str
    impact_score: float = 0.5

<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class LessonCore(BaseCore):
    """
    Standard implementation for managing shared learnings across the fleet.
    Inherits from BaseCore for standardized persistence.
    """

<<<<<<< HEAD
    def __init__(self, persistence_path: Optional[str] = None, repo_root: Optional[str] = None) -> None:
        super().__init__(name="Lesson", repo_root=repo_root)
        self.known_failures: Set[str] = set()
        self.lessons: List[Lesson] = []
        if persistence_path:
            self.persistence_path = Path(persistence_path)
        else:
            self.persistence_path = self.get_state_path()
=======
    def __init__(self, persistence_path: Optional[str] = None, repo_root: Optional[str] = None):
        super().__init__(name="Lesson", repo_root=repo_root)
        self.known_failures: Set[str] = set()
        self.lessons: List[Lesson] = []
        self.persistence_path = Path(persistence_path) if persistence_path else self.get_state_path()
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self.load_lessons()

    def generate_failure_hash(self, error_msg: str) -> str:
        """Generates a stable hash for an error message."""
        if HAS_RUST:
<<<<<<< HEAD
            try:
                # pylint: disable=no-member
                return rc.generate_failure_hash(error_msg)  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass
=======
            try: return rc.generate_failure_hash(error_msg)
            except Exception: pass
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
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
<<<<<<< HEAD
        data = {"known_failures": list(self.known_failures), "lessons": [asdict(lesson) for lesson in self.lessons]}
=======
        data = {
            "known_failures": list(self.known_failures),
            "lessons": [asdict(l) for l in self.lessons]
        }
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self._storage.save_json(self.persistence_path, data)

    def load_lessons(self) -> None:
        """Loads lessons from disk."""
        data = self._storage.load_json(self.persistence_path)
        if data:
            self.known_failures = set(data.get("known_failures", []))
<<<<<<< HEAD
            self.lessons = [Lesson(**lesson) for lesson in data.get("lessons", [])]
=======
            self.lessons = [Lesson(**l) for l in data.get("lessons", [])]
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
