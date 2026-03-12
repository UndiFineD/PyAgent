#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/core/base/utils/TemplateManager.description.md

# TemplateManager

**File**: `src\core\base\utils\TemplateManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 90  
**Complexity**: 5 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `TemplateManager`

Manage agent templates for common use cases.

Example:
    manager=TemplateManager()
    manager.add_template(AgentTemplate(
        name = "python_cleanup",
        agents = ["coder", "tests"],
        file_patterns = ["*.py"],
    ))

    template=manager.get_template("python_cleanup")
    agent=template_to_agent(template)

**Methods** (5):
- `__init__(self)`
- `_register_defaults(self)`
- `add_template(self, template)`
- `get_template(self, name)`
- `list_templates(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `src.core.base.utils.AgentTemplate.AgentTemplate`
- `src.core.base.version.VERSION`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/utils/TemplateManager.improvements.md

# Improvements for TemplateManager

**File**: `src\core\base\utils\TemplateManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 90 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `TemplateManager_test.py` with pytest tests

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

"""Auto-extracted class from agent.py"""
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

# Imports use the `core` package root rather than `src.core` to stay
# consistent with how tests add `src` to sys.path.
from typing import List, Optional, Dict
from src.core.base.version import VERSION
from src.core.base.utils.AgentTemplate import AgentTemplate

__version__ = VERSION


class TemplateManager:
    """Manage agent templates for common use cases.

    Example:
        manager=TemplateManager()
        manager.add_template(AgentTemplate(
            name = "python_cleanup",
            agents = ["coder", "tests"],
            file_patterns = ["*.py"],
        ))

        template=manager.get_template("python_cleanup")
        agent=template_to_agent(template)
    """

    def __init__(self) -> None:
        """Initialize manager."""
        self._templates: dict[str, AgentTemplate] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register default templates."""
        self._templates["python_full"] = AgentTemplate(
            name="python_full",
            description="Full Python code improvement",
            agents=["coder", "tests", "documentation", "errors"],
            file_patterns=["*.py"],
        )

        self._templates["markdown_docs"] = AgentTemplate(
            name="markdown_docs",
            description="Markdown documentation improvement",
            agents=["documentation"],
            file_patterns=["*.md"],
        )

        self._templates["quick_fix"] = AgentTemplate(
            name="quick_fix",
            description="Quick fixes only",
            agents=["coder"],
            config={"max_files": 10},
            file_patterns=["*.py"],
        )

    def add_template(self, template: AgentTemplate) -> None:
        """Add a template.

        Args:
            template: Template to add.
        """
        self._templates[template.name] = template

    def get_template(self, name: str) -> AgentTemplate | None:
        """Get a template by name.

        Args:
            name: Template name.

        Returns:
            Template or None if not found.
        """
        return self._templates.get(name)

    def list_templates(self) -> list[str]:
        """List available template names."""
        return list(self._templates.keys())
