# SelfHealingAgent

**File**: `src\classes\coder\SelfHealingAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 78  
**Complexity**: 4 (simple)

## Overview

Agent specializing in self-healing through telemetry analysis and error correction.

## Classes (1)

### `SelfHealingAgent`

**Inherits from**: BaseAgent

Monitors telemetry for agent failures and proposes fixes.

**Methods** (4):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `scan_for_failures(self)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (11):
- `json`
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `src.classes.base_agent.utilities.create_main_function`
- `src.classes.stats.ObservabilityEngine.ObservabilityEngine`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
