# OrchestratorDiffMixin

**File**: `src\logic\agents\swarm\OrchestratorDiffMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 40  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for OrchestratorDiffMixin.

## Classes (1)

### `OrchestratorDiffMixin`

Diff preview methods for OrchestratorAgent.

**Methods** (3):
- `enable_diff_preview(self, output_format)`
- `preview_changes(self, file_path, new_content)`
- `show_pending_diffs(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `src.core.base.models.DiffOutputFormat`
- `src.core.base.models.DiffResult`
- `src.core.base.utils.DiffGenerator.DiffGenerator`

---
*Auto-generated documentation*
