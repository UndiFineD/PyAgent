# KnowledgeTransferEngine

**File**: `src\classes\fleet\KnowledgeTransferEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 50  
**Complexity**: 4 (simple)

## Overview

Engine for cross-fleet knowledge transfer.
Enables sharing lessons between decoupled fleet instances.

## Classes (1)

### `KnowledgeTransferEngine`

Manages export and import of knowledge/lessons between fleets.
Shell for KnowledgeTransferCore.

**Methods** (4):
- `__init__(self, workspace_root)`
- `export_knowledge(self, fleet_id, knowledge_data)`
- `import_knowledge(self, source_file)`
- `merge_lessons(self, current_lessons, imported_lessons)`

## Dependencies

**Imports** (7):
- `KnowledgeTransferCore.KnowledgeTransferCore`
- `json`
- `logging`
- `pathlib.Path`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
