#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/core/base/types/TemplateManager.description.md

# TemplateManager

**File**: `src\\core\base\types\\TemplateManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 101  
**Complexity**: 4 (simple)

## Overview

Auto-extracted class from agent_changes.py

## Classes (1)

### `TemplateManager`

Manages entry templates with placeholders.

Provides template storage and application functionality.

Attributes:
    templates: Dictionary of templates by name.

Example:
    >>> manager=TemplateManager()
    >>> manager.add_template("bug_fix", "Fixed {issue} in {component}")
    >>> text=manager.apply_template("bug_fix", {"issue": "#123", "component": "auth"})

**Methods** (4):
- `__init__(self)`
- `add_template(self, name, template_text, description)`
- `apply_template(self, name, values)`
- `get_template_placeholders(self, name)`

## Dependencies

**Imports** (6):
- `EntryTemplate.EntryTemplate`
- `__future__.annotations`
- `re`
- `src.core.base.version.VERSION`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/core/base/types/TemplateManager.improvements.md

# Improvements for TemplateManager

**File**: `src\\core\base\types\\TemplateManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 101 lines (medium)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `TemplateManager_test.py` with pytest tests

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


"""Auto-extracted class from agent_changes.py"""

import re

from src.core.base.version import VERSION

from .EntryTemplate import EntryTemplate

__version__ = VERSION


class TemplateManager:
    """Manages entry templates with placeholders.

    Provides template storage and application functionality.

    Attributes:
        templates: Dictionary of templates by name.

    Example:
        >>> manager=TemplateManager()
        >>> manager.add_template("bug_fix", "Fixed {issue} in {component}")
        >>> text=manager.apply_template("bug_fix", {"issue": "#123", "component": "auth"})

    """

    def __init__(self) -> None:
        """Initialize the template manager."""
        self.templates: dict[str, EntryTemplate] = {}

    def add_template(
        self, name: str, template_text: str, description: str = ""
    ) -> EntryTemplate:
        """Add a new template.

        Args:
            name: Template name.
            template_text: Template with placeholders.
            description: Template description.

        Returns:
            The created EntryTemplate.

        """
        # Extract placeholders
        placeholders = re.findall(r"\{(\w+)\}", template_text)

        template = EntryTemplate(
            name=name,
            template_text=template_text,
            placeholders=placeholders,
            description=description,
        )
        self.templates[name] = template
        return template

    def apply_template(self, name: str, values: dict[str, str]) -> str:
        """Apply a template with values.

        Args:
            name: Template name.
            values: Dictionary of placeholder values.

        Returns:
            Filled - in template text.

        """
        template = self.templates.get(name)
        if not template:
            return ""

        result = template.template_text
        for placeholder, value in values.items():
            result = result.replace(f"{{{placeholder}}}", value)
        return result

    def get_template_placeholders(self, name: str) -> list[str]:
        """Get placeholders for a template.

        Args:
            name: Template name.

        Returns:
            List of placeholder names.

        """
        template = self.templates.get(name)
        return template.placeholders if template else []
