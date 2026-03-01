# efficient_change_detector

**File**: `src\core\base\logic\efficient_change_detector.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 15 imports  
**Lines**: 249  
**Complexity**: 11 (moderate)

## Overview

Efficient Change Detection Core - USN-inspired change tracking for file systems
Based on ADSpider's replication metadata approach for efficient monitoring

## Classes (3)

### `ChangeRecord`

Record of a file system change

### `FileMetadata`

Metadata for efficient change detection

### `EfficientChangeDetector`

USN-inspired change detection for file systems
Uses metadata-based tracking instead of full content scanning

**Methods** (11):
- `__init__(self, root_path, enable_hashing)`
- `_should_exclude(self, path)`
- `_calculate_file_hash(self, path)`
- `_get_file_metadata(self, path)`
- `_scan_directory(self, path)`
- `initialize_baseline(self)`
- `detect_changes(self)`
- `get_change_statistics(self)`
- `filter_changes_by_type(self, changes, change_type)`
- `filter_changes_by_path(self, changes, path_pattern)`
- ... and 1 more methods

## Dependencies

**Imports** (15):
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `hashlib`
- `logging`
- `os`
- `pathlib.Path`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`

---
*Auto-generated documentation*
