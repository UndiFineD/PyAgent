# CoderStyleMixin

**File**: `src\logic\agents\development\mixins\CoderStyleMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 137  
**Complexity**: 5 (moderate)

## Overview

Style checking and auto-fixing logic for CoderCore.

## Classes (1)

### `CoderStyleMixin`

Mixin for style checking and auto-fixing.

**Methods** (5):
- `check_style(self, content, rules)`
- `_check_style_rust(self, content, rules)`
- `_check_multiline_rule(self, content, rule)`
- `_check_line_rule(self, lines, rule)`
- `auto_fix_style(self, content, rules)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `logging`
- `re`
- `src.core.base.types.StyleRule.StyleRule`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Tuple`

---
*Auto-generated documentation*
