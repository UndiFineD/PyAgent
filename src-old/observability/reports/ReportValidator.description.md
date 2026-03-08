# ReportValidator

**File**: `src\observability\reports\ReportValidator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 81  
**Complexity**: 3 (simple)

## Overview

Auto-extracted class from generate_agent_reports.py

## Classes (1)

### `ReportValidator`

Validator for report data integrity.
Validates report structure, content, and checksums.
Example:
    validator=ReportValidator()
    result=validator.validate(content)
    if not result.valid:
        print(result.errors)

**Methods** (3):
- `__init__(self)`
- `validate(self, content)`
- `verify_checksum(self, content, expected)`

## Dependencies

**Imports** (7):
- `ValidationResult.ValidationResult`
- `__future__.annotations`
- `hashlib`
- `logging`
- `re`
- `src.core.base.version.VERSION`
- `typing.List`

---
*Auto-generated documentation*
