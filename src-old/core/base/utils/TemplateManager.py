#!/usr/bin/env python3
r"""
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

r"""Auto-extracted class from agent.py"""
