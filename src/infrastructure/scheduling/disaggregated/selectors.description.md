# selectors

**File**: `src\infrastructure\scheduling\disaggregated\selectors.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 7 imports  
**Lines**: 91  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for selectors.

## Classes (5)

### `InstanceSelector`

**Inherits from**: ABC

Abstract base for instance selection strategies.

**Methods** (1):
- `select(self, instances, request)`

### `RoundRobinSelector`

**Inherits from**: InstanceSelector

Round-robin instance selection.

**Methods** (2):
- `__init__(self)`
- `select(self, instances, request)`

### `LeastLoadedSelector`

**Inherits from**: InstanceSelector

Select least loaded instance.

**Methods** (1):
- `select(self, instances, request)`

### `RandomSelector`

**Inherits from**: InstanceSelector

Random instance selection.

**Methods** (1):
- `select(self, instances, request)`

### `HashSelector`

**Inherits from**: InstanceSelector

Hash-based consistent instance selection.

**Methods** (1):
- `select(self, instances, request)`

## Dependencies

**Imports** (7):
- `abc.ABC`
- `abc.abstractmethod`
- `config.InstanceInfo`
- `config.ScheduledRequest`
- `random`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
