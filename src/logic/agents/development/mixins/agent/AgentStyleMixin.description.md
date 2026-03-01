# AgentStyleMixin

**File**: `src\logic\agents\development\mixins\agent\AgentStyleMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 70  
**Complexity**: 6 (moderate)

## Overview

Style enforcement logic for CoderAgent.

## Classes (1)

### `AgentStyleMixin`

Mixin for managing and checking code style rules.

**Methods** (6):
- `add_style_rule(self, rule)`
- `remove_style_rule(self, rule_name)`
- `enable_style_rule(self, rule_name)`
- `disable_style_rule(self, rule_name)`
- `check_style(self, content)`
- `auto_fix_style(self, content)`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `src.core.base.types.StyleRule.StyleRule`
- `typing.Any`

---
*Auto-generated documentation*
