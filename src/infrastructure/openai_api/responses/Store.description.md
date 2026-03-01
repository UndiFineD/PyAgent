# Store

**File**: `src\infrastructure\openai_api\responses\Store.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 7 imports  
**Lines**: 55  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for Store.

## Classes (2)

### `ResponseStore`

**Inherits from**: ABC

Abstract response store.

### `InMemoryResponseStore`

**Inherits from**: ResponseStore

In-memory response store.

**Methods** (1):
- `__init__(self, max_size)`

## Dependencies

**Imports** (7):
- `Models.Response`
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
