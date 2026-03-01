# AgentFileManager

**File**: `src\core\base\common\utils\AgentFileManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 203  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for AgentFileManager.

## Classes (1)

### `AgentFileManager`

Manages file discovery, filtering, and snapshots for the Agent.

**Methods** (7):
- `__init__(self, repo_root, agents_only, ignored_patterns)`
- `is_ignored(self, path)`
- `find_code_files(self, max_files)`
- `load_cascading_codeignore(self, directory)`
- `create_file_snapshot(self, file_path)`
- `restore_from_snapshot(self, file_path, snapshot_id)`
- `cleanup_old_snapshots(self, max_age_days, max_snapshots_per_file)`

## Dependencies

**Imports** (11):
- `fnmatch`
- `hashlib`
- `logging`
- `os`
- `pathlib.Path`
- `time`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `utils.load_codeignore`

---
*Auto-generated documentation*
