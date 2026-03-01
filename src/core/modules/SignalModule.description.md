# SignalModule

**File**: `src\core\modules\SignalModule.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 68  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for SignalModule.

## Classes (1)

### `SignalModule`

**Inherits from**: BaseModule

Consolidated core module for signal processing.
Migrated from SignalCore.

**Methods** (5):
- `initialize(self)`
- `execute(self, action)`
- `create_event(self, signal_name, data, sender)`
- `prune_history(self, history, limit)`
- `shutdown(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `datetime.datetime`
- `src.core.base.modules.BaseModule`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
