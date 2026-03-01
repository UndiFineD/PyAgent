# TemplateManager

**File**: `src\core\base\types\TemplateManager.py`  
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
