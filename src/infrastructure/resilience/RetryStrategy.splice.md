# Class Breakdown: RetryStrategy

**File**: `src\infrastructure\resilience\RetryStrategy.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `JitterType`

**Line**: 26  
**Inherits**: Enum  
**Methods**: 0

Types of jitter for backoff.

[TIP] **Suggested split**: Move to `jittertype.py`

---

### 2. `RetryStats`

**Line**: 35  
**Methods**: 1

Statistics for retry operations.

[TIP] **Suggested split**: Move to `retrystats.py`

---

### 3. `RetryExhaustedError`

**Line**: 57  
**Inherits**: Exception  
**Methods**: 1

Raised when all retries are exhausted.

[TIP] **Suggested split**: Move to `retryexhaustederror.py`

---

### 4. `RetryStrategy`

**Line**: 70  
**Methods**: 6

Configurable retry strategy with exponential backoff and jitter.

Example:
    >>> retry = RetryStrategy(
    ...     max_attempts=5,
    ...     base_delay=1.0,
    ...     max_delay=60.0,
    ...   ...

[TIP] **Suggested split**: Move to `retrystrategy.py`

---

### 5. `RetryBudget`

**Line**: 320  
**Methods**: 6

Token bucket for limiting total retries across operations.

Prevents excessive retries during widespread failures.

Example:
    >>> budget = RetryBudget(max_retries_per_second=10.0)
    >>> 
    >>> ...

[TIP] **Suggested split**: Move to `retrybudget.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
