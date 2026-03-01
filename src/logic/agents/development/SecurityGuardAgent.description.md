# SecurityGuardAgent

**File**: `src\logic\agents\development\SecurityGuardAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 136  
**Complexity**: 9 (moderate)

## Overview

Agent specializing in security validation and safety checks.

## Classes (1)

### `SecurityGuardAgent`

**Inherits from**: BaseAgent

Protects the workspace by validating diffs and commands.

**Methods** (9):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `scan_for_secrets(self, content)`
- `audit_command(self, command)`
- `validate_shell_script(self, script_content)`
- `scan_for_injection(self, content)`
- `generate_safety_report(self, task, code_changes, commands)`
- `detect_jailbreak(self, prompt)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `src.logic.agents.development.SecurityCore.SecurityCore`
- `typing.List`
- `typing.Tuple`

---
*Auto-generated documentation*
