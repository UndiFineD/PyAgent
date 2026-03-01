# config

**File**: `src\infrastructure\structured_output\manager\config.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 6 imports  
**Lines**: 71  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for config.

## Classes (6)

### `GrammarType`

**Inherits from**: Enum

Types of grammar constraints supported.

### `CompilationStatus`

**Inherits from**: Enum

Status of grammar compilation.

### `GrammarSpec`

Specification for a grammar constraint.

**Methods** (1):
- `to_cache_key(self)`

### `CompilationResult`

Result of grammar compilation.

**Methods** (2):
- `is_ready(self)`
- `is_failed(self)`

### `ValidationResult`

Result of token validation.

### `BackendStats`

Statistics for a structured output backend.

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `dataclasses.dataclass`
- `enum.Enum`
- `enum.auto`
- `hashlib`
- `typing.Optional`

---
*Auto-generated documentation*
