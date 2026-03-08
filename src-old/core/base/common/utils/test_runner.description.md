# test_runner

**File**: `src\core\base\common\utils\test_runner.py`  
**Type**: Python Module  
**Summary**: 0 classes, 2 functions, 7 imports  
**Lines**: 70  
**Complexity**: 2 (simple)

## Overview

Test runner utilities.

Provides a small helper to execute focused pytest runs and return results.
Used by agents to verify changes before committing.

## Functions (2)

### `_build_pytest_command(kexpr, extra_args)`

### `run_focused_tests_for_files(files, timeout)`

Run a focused pytest subset based on changed file names.

Args:
    files: Iterable of changed file paths (relative or absolute).
    timeout: Timeout in seconds for the pytest invocation.

Returns:
    (success: bool, output: str)

Behavior:
    - Extracts base names from files and builds a -k expression joining with 'or'.
    - If no file names can be extracted, runs the entire `tests/unit` suite as a conservative fallback.

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `pathlib.Path`
- `shlex`
- `subprocess`
- `typing.Iterable`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
