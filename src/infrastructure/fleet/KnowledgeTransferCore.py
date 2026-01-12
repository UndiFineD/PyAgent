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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.



from typing import List, Dict, Any, Set

class KnowledgeTransferCore:
    """
    Pure logic for Knowledge Transfer.
    Handles merging of lesson datasets.
    """

    def merge_lessons(self, current_lessons: List[Any], imported_lessons: List[Any]) -> List[Any]:
        """Merges imported lessons into the current set, avoiding duplicates."""
        # Normalize to dicts only
        valid_current = [l for l in current_lessons if isinstance(l, dict)]
        valid_imported = [l for l in imported_lessons if isinstance(l, dict)]
        
        # Create a signature set for existing lessons
        # Signature = (failure_context, correction) usually unique enough
        seen_signatures: Set[str] = set()
        
        for l in valid_current:
            sig = f"{l.get('failure_context')}|{l.get('correction')}"
            seen_signatures.add(sig)
            
        merged = list(valid_current) # Start with current
        
        for lesson in valid_imported:
            sig = f"{lesson.get('failure_context')}|{lesson.get('correction')}"
            if sig not in seen_signatures:
                merged.append(lesson)
                seen_signatures.add(sig)
                
        return merged
