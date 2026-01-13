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
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.version import VERSION
from typing import List, Any, Set

__version__ = VERSION

class KnowledgeTransferCore:
    """
    Pure logic for Knowledge Transfer.
    Handles merging of lesson datasets.
    """

    def merge_lessons(self, current_lessons: list[Any], imported_lessons: list[Any]) -> list[Any]:
        """Merges imported lessons into the current set, avoiding duplicates."""
        # Normalize to dicts only
        valid_current = [lesson for lesson in current_lessons if isinstance(lesson, dict)]
        valid_imported = [lesson for lesson in imported_lessons if isinstance(lesson, dict)]
        
        # Create a signature set for existing lessons
        # Signature = (failure_context, correction) usually unique enough
        seen_signatures: set[str] = set()
        
        for lesson in valid_current:
            sig = f"{lesson.get('failure_context')}|{lesson.get('correction')}"
            seen_signatures.add(sig)
            
        merged = list(valid_current) # Start with current
        
        for lesson in valid_imported:
            sig = f"{lesson.get('failure_context')}|{lesson.get('correction')}"
            if sig not in seen_signatures:
                merged.append(lesson)
                seen_signatures.add(sig)
                
        return merged