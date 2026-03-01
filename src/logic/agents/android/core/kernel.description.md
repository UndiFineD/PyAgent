# kernel

**File**: `src\logic\agents\android\core\kernel.py`  
**Type**: Python Module  
**Summary**: 0 classes, 5 functions, 8 imports  
**Lines**: 131  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for kernel.

## Functions (5)

### `run_adb_command(command)`

Executes a shell command via ADB.

### `get_screen_state()`

Dumps the current UI XML and returns the sanitized JSON string.

### `execute_action(action)`

Executes the action decided by the LLM.

### `get_llm_decision(goal, screen_context)`

Sends screen context to LLM and asks for the next move.

### `run_agent(goal, max_steps)`

## Dependencies

**Imports** (8):
- `json`
- `openai.OpenAI`
- `os`
- `sanitizer`
- `subprocess`
- `time`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
