# AgentUpdateManager

**File**: `src\core\base\common\utils\AgentUpdateManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 229  
**Complexity**: 7 (moderate)

## Overview

Specialized manager for handling agent improvement iterations.

## Classes (1)

### `AgentUpdateManager`

Handles the update logic for code files, including errors, improvements, and tests.
Implements Version Gatekeeping to prevent unstable mutations.

**Methods** (7):
- `__init__(self, repo_root, models, strategy, command_handler, file_manager, core)`
- `_check_gate(self)`
- `update_errors_improvements(self, code_file)`
- `_get_pending_improvements(self, improvements_file)`
- `_mark_improvements_fixed(self, improvements_file, fixed_items)`
- `_log_changes(self, changes_file, fixed_items)`
- `update_changelog_context_tests(self, code_file)`

## Dependencies

**Imports** (14):
- `logging`
- `pathlib.Path`
- `subprocess`
- `sys`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `utils.fix_markdown_content`
- `version.EVOLUTION_PHASE`
- `version.is_gate_open`

---
*Auto-generated documentation*
