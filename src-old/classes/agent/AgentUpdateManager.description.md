# AgentUpdateManager

**File**: `src\classes\agent\AgentUpdateManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 229  
**Complexity**: 8 (moderate)

## Overview

Specialized manager for handling agent improvement iterations.

## Classes (1)

### `AgentUpdateManager`

Handles the update logic for code files, including errors, improvements, and tests.
Implements Version Gatekeeping to prevent unstable mutations.

**Methods** (8):
- `__init__(self, repo_root, models, strategy, command_handler, file_manager, core)`
- `_check_gate(self)`
- `update_errors_improvements(self, code_file)`
- `_get_pending_improvements(self, improvements_file)`
- `_mark_improvements_fixed(self, improvements_file, fixed_items)`
- `_log_changes(self, changes_file, fixed_items)`
- `update_changelog_context_tests(self, code_file)`
- `update_code(self, code_file)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `src.core.base.utils.core_utils.fix_markdown_content`
- `src.core.base.version.EVOLUTION_PHASE`
- `src.core.base.version.VERSION`
- `src.core.base.version.is_gate_open`
- `sys`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
