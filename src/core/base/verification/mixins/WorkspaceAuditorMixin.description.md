# WorkspaceAuditorMixin

**File**: `src\core\base\verification\mixins\WorkspaceAuditorMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 134  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for WorkspaceAuditorMixin.

## Classes (1)

### `WorkspaceAuditorMixin`

Methods for auditing the workspace for tech debt with Rust acceleration.

**Methods** (2):
- `audit_workspace(self, root_dir)`
- `_check_is_stub(self, tree)`

## Dependencies

**Imports** (9):
- `StubDetectorMixin.StubDetectorMixin`
- `ast`
- `logging`
- `pathlib.Path`
- `re`
- `rust_core`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
