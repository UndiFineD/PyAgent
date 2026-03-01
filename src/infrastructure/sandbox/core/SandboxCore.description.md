# SandboxCore

**File**: `src\infrastructure\sandbox\core\SandboxCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 4 imports  
**Lines**: 48  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for SandboxCore.

## Classes (2)

### `SandboxConfig`

Immutable configuration for agent sandboxing.

### `SandboxCore`

Pure logic for containerized agent runtimes and resource isolation.
Handles enforcement logic, quota calculations, and security constraints.

**Methods** (3):
- `validate_code_execution(self, code, config)`
- `calculate_resource_usage(self, start_cpu, end_cpu, duration)`
- `get_security_profile(self, risk_level)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `typing`

---
*Auto-generated documentation*
