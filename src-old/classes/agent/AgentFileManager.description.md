# AgentFileManager

**File**: `src\classes\agent\AgentFileManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 227  
**Complexity**: 9 (moderate)

## Overview

Python module containing implementation for AgentFileManager.

## Classes (1)

### `AgentFileManager`

Manages file discovery, filtering, and snapshots for the Agent.

**Methods** (9):
- `__init__(self, repo_root, agents_only, ignored_patterns)`
- `is_ignored(self, path)`
- `find_code_files(self, max_files)`
- `load_cascading_codeignore(self, directory)`
- `create_file_snapshot(self, file_path)`
- `restore_from_snapshot(self, file_path, snapshot_id)`
- `cleanup_old_snapshots(self, max_age_days, max_snapshots_per_file)`
- `_group_snapshots_by_filename(self, snapshot_dir)`
- `_prune_snapshot_groups(self, groups, current_time, max_age_seconds, max_count)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `hashlib`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.AgentCore.BaseCore`
- `src.core.base.utils.core_utils.load_codeignore`
- `src.core.base.version.VERSION`
- `time`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
