# HoneypotAgent

**File**: `src\logic\agents\security\HoneypotAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 93  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for HoneypotAgent.

## Classes (1)

### `HoneypotAgent`

**Inherits from**: BaseAgent

Detects and neutralizes prompt injection and adversarial attacks.
Integrated with RedQueenCore for adversarial prompt evolution testing.

**Methods** (4):
- `__init__(self, file_path)`
- `verify_input_safety(self, prompt_input)`
- `generate_test_attacks(self, base_task)`
- `get_trap_statistics(self)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `src.logic.agents.security.core.RedQueenCore.AttackVector`
- `src.logic.agents.security.core.RedQueenCore.RedQueenCore`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
