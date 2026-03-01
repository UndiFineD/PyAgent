# SelfArchivingAgent

**File**: `src\classes\specialized\SelfArchivingAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 57  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for SelfArchivingAgent.

## Classes (1)

### `SelfArchivingAgent`

**Inherits from**: BaseAgent

Phase 35: Recursive Self-Archiving.
Identifies abandoned code paths or low-utility memories and compresses them into archives.

**Methods** (4):
- `__init__(self, file_path)`
- `identify_archivable_targets(self, threshold_days)`
- `archive_targets(self, targets)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (7):
- `datetime.datetime`
- `json`
- `logging`
- `os`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `typing.List`

---
*Auto-generated documentation*
