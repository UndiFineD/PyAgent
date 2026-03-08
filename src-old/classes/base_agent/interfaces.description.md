# interfaces

**File**: `src\classes\base_agent\interfaces.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 8 imports  
**Lines**: 37  
**Complexity**: 11 (moderate)

## Overview

Python module containing implementation for interfaces.

## Classes (3)

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

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `pathlib.Path`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Protocol`
- `typing.runtime_checkable`

---
*Auto-generated documentation*
