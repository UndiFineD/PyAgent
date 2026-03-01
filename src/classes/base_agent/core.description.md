# core

**File**: `src\classes\base_agent\core.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 14 imports  
**Lines**: 160  
**Complexity**: 14 (moderate)

## Overview

Foundation for high-performance 'Core' components.
These classes are designed to be eventually implemented in Rust (using PyO3 or FFI).
They should remain as 'pure' as possible - no complex dependencies on AI or IO.

## Classes (3)

### `CodeQualityReport`

Class CodeQualityReport implementation.

### `BaseCore`

Pure logic core for all agents.

**Methods** (12):
- `__init__(self, workspace_root)`
- `detect_workspace_root(file_path)`
- `is_path_ignored(self, path, repo_root, ignored_patterns)`
- `calculate_diff(self, old_content, new_content, filename)`
- `fix_markdown(self, content)`
- `validate_content_safety(self, content)`
- `score_response_quality(self, response)`
- `filter_code_files(self, files, repo_root, ignored_patterns, supported_extensions)`
- `generate_cache_key(self, prompt, content, model)`
- `estimate_tokens(self, text)`
- ... and 2 more methods

### `LogicCore`

Base class for performance-critical logic.

**Methods** (2):
- `process_text(self, text)`
- `analyze_structure(self, text)`

## Dependencies

**Imports** (14):
- `dataclasses.dataclass`
- `dataclasses.field`
- `difflib`
- `fnmatch`
- `hashlib`
- `logging`
- `os`
- `pathlib.Path`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
