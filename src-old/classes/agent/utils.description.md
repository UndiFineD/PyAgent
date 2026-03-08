# utils

**File**: `src\classes\agent\utils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 4 functions, 11 imports  
**Lines**: 168  
**Complexity**: 4 (simple)

## Overview

Utility functions used by the Agent classes.

## Functions (4)

### `load_codeignore(root)`

Load and parse ignore patterns from .codeignore file.

Reads the .codeignore file from the repository root and extracts all
ignore patterns (lines that are not empty or comments).

Caches patterns to avoid re-parsing on subsequent calls. Cache is invalidated
if the file is modified (checked by file mtime).

Args:
    root: Path to the repository root directory.

Returns:
    Set of ignore patterns (strings) from the .codeignore file.
    Returns empty set if file doesn't exist.

Raises:
    None. Logs warnings if file cannot be read but doesn't raise.

Example:
    patterns=load_codeignore(Path('/repo'))
    # patterns might be: {'*.log', '__pycache__/', 'venv/**'}

Note:
    - Lines starting with '#' are treated as comments and ignored
    - Empty lines are skipped
    - File encoding is assumed to be UTF-8
    - Patterns are cached with mtime checking for efficiency

### `setup_logging(verbosity)`

Configure logging based on verbosity level.

Defaults to WARNING to capture only errors and failures as requested.

### `_multiprocessing_worker(agent_instance, file_path)`

Worker function for multiprocessing file processing.

This function must be at module level to be pickleable for multiprocessing.

### `_load_fix_markdown_content()`

Load the markdown fixer module dynamically.

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `collections.abc.Callable`
- `importlib.util`
- `logging`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `sys`
- `typing.Any`
- `typing.Optional`
- `typing.Set`
- `typing.cast`

---
*Auto-generated documentation*
