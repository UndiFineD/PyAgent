# interfaces

**File**: `src\core\base\interfaces.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 9 imports  
**Lines**: 70  
**Complexity**: 12 (moderate)

## Overview

Python module containing implementation for interfaces.

## Classes (4)

### `AgentInterface`

**Inherits from**: Protocol

Core interface for all AI-powered agents. 
Defining this as a Protocol facilitates future Rust implementation (PyO3).

**Methods** (6):
- `read_previous_content(self)`
- `improve_content(self, prompt)`
- `update_file(self)`
- `get_diff(self)`
- `calculate_metrics(self, content)`
- `scan_for_secrets(self, content)`

### `OrchestratorInterface`

**Inherits from**: Protocol

Interface for fleet orchestrators.

**Methods** (2):
- `execute_task(self, task)`
- `get_status(self)`

### `CoreInterface`

**Inherits from**: Protocol

Pure logic interface. High-performance, no-IO, candidate for Rust parity.

**Methods** (3):
- `process_data(self, data)`
- `validate(self, content)`
- `get_metadata(self)`

### `ContextRecorderInterface`

**Inherits from**: Protocol

Interface for cognitive recording and context harvesting.

**Methods** (1):
- `record_interaction(self, provider, model, prompt, result, meta)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Protocol`
- `typing.runtime_checkable`

---
*Auto-generated documentation*
