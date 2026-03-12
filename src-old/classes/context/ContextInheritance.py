#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/context/ContextInheritance.description.md

# ContextInheritance

**File**: `src\classes\context\ContextInheritance.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 113  
**Complexity**: 7 (moderate)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `ContextInheritance`

Manages context inheritance from parent files.

Provides functionality for child contexts to inherit
from parent contexts.

Example:
    >>> inheritance=ContextInheritance()
    >>> inherited=inheritance.inherit_from("parent.description.md", "child.description.md")

**Methods** (7):
- `__init__(self)`
- `set_mode(self, mode)`
- `set_parent(self, parent_path)`
- `apply(self, child_content, parent_content)`
- `get_hierarchy(self)`
- `inherit_from(self, parent_path, child_path, mode)`
- `resolve_inheritance(self, parent_content, child_content, mode)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `re`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.context.models.InheritanceMode.InheritanceMode`
- `src.logic.agents.cognitive.context.models.InheritedContext.InheritedContext`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/context/ContextInheritance.improvements.md

# Improvements for ContextInheritance

**File**: `src\classes\context\ContextInheritance.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 113 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ContextInheritance_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

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


"""Auto-extracted class from agent_context.py"""

from src.core.base.version import VERSION
from src.logic.agents.cognitive.context.models.InheritanceMode import InheritanceMode
from src.logic.agents.cognitive.context.models.InheritedContext import InheritedContext
from typing import Dict, List, Optional
import re

__version__ = VERSION


class ContextInheritance:
    """Manages context inheritance from parent files.

        Provides functionality for child contexts to inherit
    from parent contexts.

        Example:
            >>> inheritance=ContextInheritance()
            >>> inherited=inheritance.inherit_from("parent.description.md", "child.description.md")
    """

    def __init__(self) -> None:
        """Initialize context inheritance manager."""
        self.inheritance_map: dict[str, InheritedContext] = {}
        self.mode: InheritanceMode = InheritanceMode.MERGE
        self.parent_path: str | None = None

    def set_mode(self, mode: InheritanceMode) -> None:
        """Set inheritance mode."""
        self.mode = mode

    def set_parent(self, parent_path: str) -> None:
        """Set parent context."""
        self.parent_path = parent_path

    def apply(self, child_content: str, parent_content: str) -> str:
        """Apply the currently configured inheritance mode."""
        return self.resolve_inheritance(parent_content, child_content, self.mode)

    def get_hierarchy(self) -> list[str]:
        """Get inheritance hierarchy."""
        return [self.parent_path] if self.parent_path else []

    def inherit_from(
        self,
        parent_path: str,
        child_path: str,
        mode: InheritanceMode = InheritanceMode.MERGE,
    ) -> InheritedContext:
        """Set up inheritance relationship.

        Args:
            parent_path: Path to parent context.
            child_path: Path to child context.
            mode: Inheritance mode.

        Returns:
            InheritedContext configuration.
        """
        inherited = InheritedContext(parent_path=parent_path, mode=mode)
        self.inheritance_map[child_path] = inherited
        return inherited

    def resolve_inheritance(
        self, parent_content: str, child_content: str, mode: InheritanceMode
    ) -> str:
        """Resolve inheritance to produce final content.

        Args:
            parent_content: Parent context content.
            child_content: Child context content.
            mode: Inheritance mode.

        Returns:
            Resolved content.
        """
        if mode == InheritanceMode.OVERRIDE:
            return child_content
        elif mode == InheritanceMode.APPEND:
            return parent_content + "\n\n" + child_content
        else:
            # MERGE
            # Simple merge: keep child sections, add missing from parent
            child_sections = set(re.findall(r"##\s+(\w+)", child_content))
            parent_sections = re.findall(
                r"(##\s+\w+.*?)(?=##|\Z)", parent_content, re.DOTALL
            )

            result = child_content
            for section in parent_sections:
                section_name = re.search(r"##\s+(\w+)", section)
                if section_name and section_name.group(1) not in child_sections:
                    result += "\n" + section.strip()
            return result
