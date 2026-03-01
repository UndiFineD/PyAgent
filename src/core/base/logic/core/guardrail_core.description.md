# guardrail_core

**File**: `src\core\base\logic\core\guardrail_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 48  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for guardrail_core.

## Classes (1)

### `GuardrailCore`

Implements output validation and logical checks for agent tasks.
Harvested from agentic-design-patterns.

**Methods** (3):
- `validate_pydantic(output, model)`
- `apply_logical_check(data, check_func)`
- `moderate_content(text, forbidden_keywords)`

## Dependencies

**Imports** (10):
- `json`
- `logging`
- `pydantic.BaseModel`
- `pydantic.ValidationError`
- `re`
- `typing.Any`
- `typing.Callable`
- `typing.Optional`
- `typing.Tuple`
- `typing.Type`

---
*Auto-generated documentation*
