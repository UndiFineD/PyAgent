# base_agent

**File**: `src\core\base\base_agent.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 2 imports  
**Lines**: 25  
**Complexity**: 0 (simple)

## Overview

Compatibility shim for older imports expecting `src.core.base.base_agent`.

This module re-exports the modern BaseAgent implementation located under
`src.core.base.lifecycle.base_agent` to maintain backward compatibility with
external code and tests.

## Dependencies

**Imports** (2):
- `__future__.annotations`
- `src.core.base.lifecycle.base_agent.BaseAgent`

---
*Auto-generated documentation*
