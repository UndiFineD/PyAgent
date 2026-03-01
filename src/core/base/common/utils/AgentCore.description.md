# AgentCore

**File**: `src\core\base\common\utils\AgentCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 103  
**Complexity**: 5 (moderate)

## Overview

AgentCore: Pure logic component for the Agent system.
Handles data transformation, parsing, and decision-making without IO side-effects.
Ready for conversion to a Rust library with strong typing.

## Classes (1)

### `AgentCore`

Logic-only core for managing improvement tasks and state.

**Methods** (5):
- `__init__(self, settings)`
- `parse_improvements_content(self, content)`
- `update_fixed_items(self, content, fixed_items)`
- `generate_changelog_entries(self, fixed_items)`
- `score_improvement_items(self, items)`

## Dependencies

**Imports** (5):
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
