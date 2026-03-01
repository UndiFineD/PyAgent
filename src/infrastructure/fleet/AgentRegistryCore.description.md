# AgentRegistryCore

**File**: `src\infrastructure\fleet\AgentRegistryCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 244  
**Complexity**: 11 (moderate)

## Overview

AgentRegistryCore logic for version compatibility and manifest validation.
Pure logic component to be potentially rustified.

Phase 15 Rust Optimizations:
- topological_sort_rust: O(V+E) topological ordering for agent load order
- to_snake_case_rust: Fast CamelCase to snake_case conversion
- detect_cycles_rust: DFS-based cycle detection in dependency graphs

## Classes (1)

### `AgentRegistryCore`

Pure logic core for Agent Registry.

**Methods** (11):
- `__init__(self, current_sdk_version)`
- `process_discovered_files(self, file_paths)`
- `_register_agent_variants(self, discovered, agent_name, module_path)`
- `_get_short_name(self, name)`
- `parse_manifest(self, raw_manifest)`
- `is_compatible(self, required_version)`
- `detect_circular_dependencies(self, dep_graph)`
- `_to_snake_case(self, name)`
- `validate_agent_structure(self, agent_instance, required_methods)`
- `calculate_load_order(self, dep_graph)`
- ... and 1 more methods

## Dependencies

**Imports** (10):
- `VersionGate.VersionGate`
- `__future__.annotations`
- `logging`
- `os`
- `re`
- `rust_core.detect_cycles_rust`
- `rust_core.to_snake_case_rust`
- `rust_core.topological_sort_rust`
- `src.core.base.Version.VERSION`
- `typing.Any`

---
*Auto-generated documentation*
