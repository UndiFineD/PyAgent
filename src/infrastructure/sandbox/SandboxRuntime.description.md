# SandboxRuntime

**File**: `src\infrastructure\sandbox\SandboxRuntime.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 30  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for SandboxRuntime.

## Classes (1)

### `SandboxRuntime`

Shell/Manager for containerized agent runtimes.
Wraps the pure SandboxCore with I/O and runtime orchestration.

**Methods** (2):
- `__init__(self)`
- `run_isolated(self, agent_id, code, risk_level)`

## Dependencies

**Imports** (4):
- `logging`
- `src.infrastructure.sandbox.core.SandboxCore.SandboxCore`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
