# Class Breakdown: Config

**File**: `src\infrastructure\orchestration\core\distributed\Config.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `EngineState`

**Line**: 14  
**Inherits**: Enum  
**Methods**: 0

State of a distributed engine instance.

[TIP] **Suggested split**: Move to `enginestate.py`

---

### 2. `WorkerState`

**Line**: 25  
**Inherits**: Enum  
**Methods**: 0

State of a worker process.

[TIP] **Suggested split**: Move to `workerstate.py`

---

### 3. `LoadBalancingStrategy`

**Line**: 36  
**Inherits**: Enum  
**Methods**: 0

Load balancing strategies for data parallel.

[TIP] **Suggested split**: Move to `loadbalancingstrategy.py`

---

### 4. `ParallelConfig`

**Line**: 46  
**Methods**: 2

Configuration for parallelism.

Inspired by vLLM's ParallelConfig.

Attributes:
    data_parallel_size: Number of data parallel replicas.
    tensor_parallel_size: Number of tensor parallel ranks.
   ...

[TIP] **Suggested split**: Move to `parallelconfig.py`

---

### 5. `EngineIdentity`

**Line**: 84  
**Methods**: 1

Identity of a distributed engine instance.

Inspired by vLLM's coordinator identity management.

Attributes:
    dp_rank: Data parallel rank.
    dp_size: Data parallel world size.
    address: Networ...

[TIP] **Suggested split**: Move to `engineidentity.py`

---

### 6. `WorkerIdentity`

**Line**: 106  
**Methods**: 0

Identity of a worker process.

[TIP] **Suggested split**: Move to `workeridentity.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
