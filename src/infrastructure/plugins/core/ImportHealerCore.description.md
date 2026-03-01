# ImportHealerCore

**File**: `src\infrastructure\plugins\core\ImportHealerCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 40  
**Complexity**: 2 (simple)

## Overview

Core logic for Broken Import Self-Healing (Phase 186).
Suggests fixes for ModuleNotFound errors and builds import maps.

## Classes (1)

### `ImportHealerCore`

Class ImportHealerCore implementation.

**Methods** (2):
- `suggest_fix(error_message)`
- `build_internal_import_map(directory)`

## Dependencies

**Imports** (4):
- `os`
- `re`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
