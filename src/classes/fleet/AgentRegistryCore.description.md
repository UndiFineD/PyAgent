# AgentRegistryCore

**File**: `src\classes\fleet\AgentRegistryCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 79  
**Complexity**: 5 (moderate)

## Overview

AgentRegistryCore logic for version compatibility and manifest validation.
Pure logic component to be potentially rustified.

## Classes (1)

### `AgentRegistryCore`

Pure logic core for Agent Registry.

**Methods** (5):
- `__init__(self, current_sdk_version)`
- `process_discovered_files(self, file_paths)`
- `parse_manifest(self, raw_manifest)`
- `is_compatible(self, required_version)`
- `validate_agent_structure(self, agent_instance, required_methods)`

## Dependencies

**Imports** (7):
- `VersionGate.VersionGate`
- `os`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
