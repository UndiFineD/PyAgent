# Class Breakdown: CircuitBreaker

**File**: `src\infrastructure\resilience\CircuitBreaker.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CircuitState`

**Line**: 29  
**Inherits**: Enum  
**Methods**: 0

Circuit breaker states.

[TIP] **Suggested split**: Move to `circuitstate.py`

---

### 2. `CircuitStats`

**Line**: 37  
**Methods**: 3

Statistics for circuit breaker monitoring.

[TIP] **Suggested split**: Move to `circuitstats.py`

---

### 3. `CircuitBreakerError`

**Line**: 78  
**Inherits**: Exception  
**Methods**: 1

Raised when circuit is open.

[TIP] **Suggested split**: Move to `circuitbreakererror.py`

---

### 4. `CircuitBreaker`

**Line**: 85  
**Methods**: 17

Thread-safe circuit breaker for protecting against cascading failures.

Example:
    >>> breaker = CircuitBreaker(
    ...     failure_threshold=5,
    ...     recovery_timeout=30.0,
    ...     half_...

[TIP] **Suggested split**: Move to `circuitbreaker.py`

---

### 5. `CircuitBreakerRegistry`

**Line**: 374  
**Methods**: 6

Registry for managing multiple circuit breakers.

Example:
    >>> registry = CircuitBreakerRegistry()
    >>> 
    >>> @registry.breaker("openai_api")
    ... def call_openai(prompt):
    ...     ret...

[TIP] **Suggested split**: Move to `circuitbreakerregistry.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
