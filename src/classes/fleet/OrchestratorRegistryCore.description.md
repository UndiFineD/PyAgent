# OrchestratorRegistryCore

**File**: `src\classes\fleet\OrchestratorRegistryCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 112  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for OrchestratorRegistryCore.

## Classes (1)

### `OrchestratorRegistryCore`

Pure logic core for Orchestrator Registry.
Handles dynamic discovery of orchestrator classes.

**Methods** (5):
- `__init__(self, current_sdk_version)`
- `process_discovered_files(self, file_paths)`
- `_to_snake_case(self, name)`
- `parse_manifest(self, raw_manifest)`
- `is_compatible(self, required_version)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `os`
- `re`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
