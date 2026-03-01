# Class Breakdown: circuit_breaker

**File**: `src\infrastructure\services\resilience\circuit_breaker.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CircuitState`

**Line**: 47  
**Inherits**: Enum  
**Methods**: 0

Circuit breaker states.

[TIP] **Suggested split**: Move to `circuitstate.py`

---

### 2. `CircuitStats`

**Line**: 56  
**Methods**: 3

Statistics regarding circuit breaker monitoring.

[TIP] **Suggested split**: Move to `circuitstats.py`

---

### 3. `CircuitBreakerError`

**Line**: 98  
**Inherits**: Exception  
**Methods**: 1

Raised when circuit is open.

[TIP] **Suggested split**: Move to `circuitbreakererror.py`

---

### 4. `CircuitBreaker`

**Line**: 106  
**Methods**: 17

Thread-safe circuit breaker regarding protecting against cascading failures in services.

[TIP] **Suggested split**: Move to `circuitbreaker.py`

---

### 5. `CircuitBreakerRegistry`

**Line**: 400  
**Methods**: 6

Registry regarding managing multiple circuit breakers.

Example:
    >>> registry = CircuitBreakerRegistry()
    >>>
    >>> @registry.breaker("openai_api")
    ... def call_openai(prompt):
    ...   ...

[TIP] **Suggested split**: Move to `circuitbreakerregistry.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
