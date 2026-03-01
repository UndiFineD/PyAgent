# ValidationRuleManager

**File**: `src\core\base\utils\ValidationRuleManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 111  
**Complexity**: 5 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `ValidationRuleManager`

Manage custom validation rules per file type.

Example:
    manager=ValidationRuleManager()
    manager.add_rule(ValidationRule(
        name = "max_line_length",
        file_pattern = "*.py",
        validator=lambda content, path: all(len(l) <= 100 for l in content.split("\n")),
        error_message = "Line too long (>100 chars)",
    ))
    results=manager.validate(file_path, content)

**Methods** (5):
- `__init__(self)`
- `add_rule(self, rule)`
- `remove_rule(self, name)`
- `validate(self, file_path, content)`
- `get_rules_for_file(self, file_path)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `fnmatch`
- `pathlib.Path`
- `src.core.base.models.ValidationRule`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
