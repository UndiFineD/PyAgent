# environment_mixin

**File**: `src\core\base\mixins\environment_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 164  
**Complexity**: 1 (simple)

## Overview

Module: environment_mixin
Provides environment management capabilities to agents.

## Classes (1)

### `EnvironmentMixin`

Mixin providing environment management capabilities to agents.
Allows agents to create and manage isolated execution environments.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `contextlib.asynccontextmanager`
- `logging`
- `os`
- `src.core.base.common.models.base_models.EnvironmentConfig`
- `src.core.base.common.models.base_models.EnvironmentInstance`
- `src.core.base.common.models.core_enums.EnvironmentIsolation`
- `src.core.base.environment.get_environment_manager`
- `src.core.base.lifecycle.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
