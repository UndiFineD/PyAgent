# BashCore

**File**: `src\logic\agents\development\core\BashCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 65  
**Complexity**: 2 (simple)

## Overview

Core logic for Bash script analysis (Phase 175).
Integrates shellcheck for linting generated scripts.

## Classes (1)

### `BashCore`

Class BashCore implementation.

**Methods** (2):
- `lint_script(script_path, recorder)`
- `wrap_with_safety_flags(content)`

## Dependencies

**Imports** (4):
- `json`
- `os`
- `src.core.base.interfaces.ContextRecorderInterface`
- `subprocess`

---
*Auto-generated documentation*
