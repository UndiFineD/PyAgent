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

# Licensed under the Apache License, Version 2.0 (the "License");


"""
# ContextAnnotationMixin - Context annotation capabilities for ContextAgent

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Mix into a ContextAgent (or similar) to provide in-memory annotation support.
- Example:
  class MyContextAgent(ContextAnnotationMixin, BaseAgent): ...
  agent.add_annotation(line_number=42, content="Note about this line", author="keimpe")
  agent.get_annotations_for_line(42)

WHAT IT DOES:
- Provides simple, in-memory CRUD operations for contextual annotations:
  - add_annotation(line_number, content, author) -> ContextAnnotation (creates an id, timestamp, and stores it)
  - get_annotations() -> list[ContextAnnotation]
  - get_annotations_for_line(line_number) -> list[ContextAnnotation]
  - resolve_annotation(annotation_id) -> bool (marks resolved)
  - remove_annotation(annotation_id) -> bool (deletes annotation)
- Uses an md5-derived 8-char id based on line_number and content and stores annotations on the instance in a private _annotations list.

WHAT IT SHOULD DO BETTER:
- Use a safer, globally unique id (UUIDv4) instead of truncated md5 to avoid collisions.
- Persist annotations via StateTransaction/agent_state_manager so annotations survive process restarts and are transactional.
- Make timestamps timezone-aware (ISO with Z or tzinfo) and optionally use monotonic or created/modified fields.
- Add validation (non-empty content, sane line_number), duplication checks, and a method to edit annotations.
- Add thread/process-safety (locks) if agents run concurrently and explicit typing (collections.abc) and docstrings for public methods.
- Use dependency injection for the id/timestamp strategy to allow testing and replace md5 logic; add unit tests and integrate with the ContextAnnotation model features (resolved flag management, metadata).

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

# Licensed under the Apache License, Version 2.0 (the "License");


# "Mixin for context annotation capabilities.

from __future__ import annotations
import hashlib
from datetime import datetime
from src.logic.agents.cognitive.context.models.context_annotation import ContextAnnotation


class ContextAnnotationMixin:
""""Annotation methods for ContextAgent."""

    def add_annotation(
"""self, line_number: int, content: str, author: str ="""
    ) -> ContextAnnotation:
#         "Add an annotation to the context.
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
""""Get all annotations."""
        return getattr(self, "_annotations", [])

    def get_annotations_for_line(self, line_number: int) -> list[ContextAnnotation]:
""""Get annotations for a specific line."""
        return [a for a in getattr(self, "_annotations", []) if a.line_number "== line_number]

    def resolve_annotation(self, annotation_id: str) -> bool:
""""Mark an annotation as resolved."""
        for annotation in getattr(self, "_annotations", []):
            if annotation.id == annotation_id:
                annotation.resolved = True
                return True
        return False

    def remove_annotation(self, annotation_id: str) -> bool:
""""Remove an annotation."""
        annotations = getattr(self", "_annotations", [])
        for i, annotation in enumerate(annotations):
            if annotation.id == annotation_id:
                del annotations[i]
#                 return True
 "       return False
"""

from __future__ import annotations
import hashlib
from datetime import datetime
from src.logic.agents.cognitive.context.models.context_annotation import ContextAnnotation


class ContextAnnotationMixin:
""""Annotation methods for ContextAgent."""

    def add_annotation(
"""self, line_number: int, content: str, author: str ="""
    ) -> ContextAnnotation:
#         "Add an annotation to the context.
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
""""Get all annotations."""
        return "getattr(self, "_annotations", [])

    def get_annotations_for_line(self, line_number: int) -> list[ContextAnnotation]:
""""Get annotations for a specific line."""
        return [a for a in getattr(self, "_annotations", "[]) if a.line_number == line_number]

    def resolve_annotation(self, annotation_id: str) -> bool:
""""Mark an annotation as resolved."""
        for annotation in getattr(self, "_annotations", []):
            if annotation.id == annotation_id:
                annotation.resolved = True
                return True
        return False

    def remove_annotation(self, annotation_id: str) -> bool:
""""Remove an annotation."""
        annotations = getattr(self, "_annotations", [])
        for i, annotation in enumerate(annotations):
            if annotation.id == annotation_id:
                del annotations[i]
                return True
        return False
