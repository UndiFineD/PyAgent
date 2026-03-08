"""
LLM_CONTEXT_START

## Source: src-old/tools/test_plugin_sandbox.description.md

# test_plugin_sandbox

**File**: `src\tools\test_plugin_sandbox.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 2 imports  
**Lines**: 23  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for test_plugin_sandbox.

## Dependencies

**Imports** (2):
- `pathlib.Path`
- `src.core.base.managers.PluginManager.PluginManager`

---
*Auto-generated documentation*
## Source: src-old/tools/test_plugin_sandbox.improvements.md

# Improvements for test_plugin_sandbox

**File**: `src\tools\test_plugin_sandbox.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 23 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `test_plugin_sandbox_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from src.core.base.managers.PluginManager import PluginManager
from pathlib import Path

pm = PluginManager()
discovered = pm.discover()
print(f"Discovered: {discovered}")

if "test_sandbox" in pm.loaded_meta:
    meta = pm.loaded_meta["test_sandbox"]
    print(f"Meta for test_sandbox: {meta}")
    plugin = pm.load_plugin("test_sandbox")
    if plugin:
        print("Plugin loaded successfully.")
        # Try to run it on a 'src' file (should be blocked if read:src is missing)
        res = plugin.run(Path("src/core/base/BaseAgent.py"), {})
        print(f"Run result on src: {res}")
        # Try to run it on a 'temp' file (should be allowed)
        res = plugin.run(Path("temp/test.txt"), {})
        print(f"Run result on temp: {res}")
else:
    print("test_sandbox not discovered.")
