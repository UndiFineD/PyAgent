# RuffComplexityParser

**File**: `src\infrastructure\dev\scripts\analysis\RuffComplexityParser.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 5 imports  
**Lines**: 72  
**Complexity**: 1 (simple)

## Overview

Parses Ruff JSON output to extract and rank cyclomatic complexity violations.
Ported from temp/check_complexity.py for re-use.

## Functions (1)

### `parse_ruff_complexity(json_file, threshold)`

Reads ruff_output.json and prints ranked complexity issues.

## Dependencies

**Imports** (5):
- `argparse`
- `json`
- `os`
- `pathlib.Path`
- `re`

---
*Auto-generated documentation*
