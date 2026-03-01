# RetryStrategy

**File**: `src\infrastructure\resilience\RetryStrategy.py`  
**Type**: Python Module  
**Summary**: 5 classes, 1 functions, 15 imports  
**Lines**: 420  
**Complexity**: 15 (moderate)

## Overview

RetryStrategy - Exponential backoff with jitter for resilient retries.

Goes beyond vLLM with production-grade retry patterns including:
- Exponential backoff with configurable base and max
- Jitter (full, equal, decorrelated) to prevent thundering herd
- Retry budgets to limit total retry attempts
- Retryable exception filtering

Phase 18: Beyond vLLM - Resilience Patterns

## Classes (5)

### `JitterType`

**Inherits from**: Enum

Types of jitter for backoff.

### `RetryStats`

Statistics for retry operations.

**Methods** (1):
- `to_dict(self)`

### `RetryExhaustedError`

**Inherits from**: Exception

Raised when all retries are exhausted.

**Methods** (1):
- `__init__(self, message, attempts, last_exception)`

### `RetryStrategy`

Configurable retry strategy with exponential backoff and jitter.

Example:
    >>> retry = RetryStrategy(
    ...     max_attempts=5,
    ...     base_delay=1.0,
    ...     max_delay=60.0,
    ...     jitter=JitterType.FULL,
    ...     retryable_exceptions=(ConnectionError, TimeoutError),
    ... )
    >>> 
    >>> @retry
    ... def flaky_operation():
    ...     return external_api_call()
    >>> 
    >>> result = flaky_operation()

**Methods** (6):
- `__init__(self, max_attempts, base_delay, max_delay, exponential_base, jitter, retryable_exceptions, non_retryable_exceptions, on_retry)`
- `stats(self)`
- `_calculate_delay(self, attempt)`
- `_is_retryable(self, exc)`
- `execute(self, func)`
- `__call__(self, func)`

### `RetryBudget`

Token bucket for limiting total retries across operations.

Prevents excessive retries during widespread failures.

Example:
    >>> budget = RetryBudget(max_retries_per_second=10.0)
    >>> 
    >>> if budget.can_retry():
    ...     budget.record_retry()
    ...     do_retry()

**Methods** (6):
- `__init__(self, max_retries_per_second, min_retries_per_second, retry_ratio)`
- `_refill(self)`
- `record_request(self)`
- `can_retry(self)`
- `record_retry(self)`
- `get_stats(self)`

## Functions (1)

### `retry(max_attempts, base_delay, max_delay, jitter, retryable_exceptions)`

Decorator for retrying functions with exponential backoff.

Example:
    >>> @retry(max_attempts=3, base_delay=1.0)
    ... def unstable_operation():
    ...     return risky_call()

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `functools`
- `inspect`
- `random`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.ParamSpec`
- `typing.Sequence`
- `typing.TypeVar`

---
*Auto-generated documentation*
