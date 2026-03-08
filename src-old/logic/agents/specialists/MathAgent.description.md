# MathAgent

**File**: `src\logic\agents\specialists\MathAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 15 imports  
**Lines**: 178  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for MathAgent.

## Classes (1)

### `MathAgent`

**Inherits from**: BaseAgent

Agent specializing in symbolic math, numerical computation, and logical proofs.
Utilizes Rust-accelerated evaluation where available.

**Methods** (3):
- `__init__(self, file_path)`
- `_sanitize_expression(self, expr)`
- `_record_calculation(self, expression, result, engine)`

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `logging`
- `math`
- `numpy`
- `re`
- `rust_core`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.BaseUtilities.as_tool`
- `src.core.base.Version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
