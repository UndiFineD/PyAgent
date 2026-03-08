#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/swarm/mixins/ChangesPreviewMixin.description.md

# ChangesPreviewMixin

**File**: `src\logic\agents\swarm\mixins\ChangesPreviewMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 59  
**Complexity**: 4 (simple)

## Overview

Preview management logic for ChangesAgent.

## Classes (1)

### `ChangesPreviewMixin`

Mixin for managing preview mode and changes.

**Methods** (4):
- `enable_preview_mode(self)`
- `disable_preview_mode(self)`
- `get_preview(self)`
- `preview_changes(self, content)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `logging`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/swarm/mixins/ChangesPreviewMixin.improvements.md

# Improvements for ChangesPreviewMixin

**File**: `src\logic\agents\swarm\mixins\ChangesPreviewMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 59 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ChangesPreviewMixin_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

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

"""
Preview management logic for ChangesAgent.
"""

import logging
from typing import Any, Dict


class ChangesPreviewMixin:
    """Mixin for managing preview mode and changes."""

    def enable_preview_mode(self) -> None:
        """Enable preview mode - changes won't be written to file."""
        self._preview_mode = True
        logging.info("Preview mode enabled")

    def disable_preview_mode(self) -> None:
        """Disable preview mode."""
        self._preview_mode = False
        logging.info("Preview mode disabled")

    def get_preview(self) -> str:
        """Get the preview of changes without applying them."""
        return (
            self._preview_content
            if getattr(self, "_preview_content", "")
            else getattr(self, "current_content", "")
        )

    def preview_changes(self, content: str) -> Dict[str, Any]:
        """Preview changes and return a summary."""
        self._preview_content = content

        # Calculate diff statistics
        original_lines = getattr(self, "previous_content", "").split("\n")
        new_lines = content.split("\n")

        added = len([line for line in new_lines if line and line not in original_lines])
        removed = len(
            [line for line in original_lines if line and line not in new_lines]
        )

        return {
            "original_lines": len(original_lines),
            "new_lines": len(new_lines),
            "lines_added": added,
            "lines_removed": removed,
            "preview": content[:500] + "..." if len(content) > 500 else content,
        }
