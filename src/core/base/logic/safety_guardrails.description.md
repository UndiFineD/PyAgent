# safety_guardrails

**File**: `src\core\base\logic\safety_guardrails.py`  
**Type**: Python Module  
**Summary**: 11 classes, 2 functions, 25 imports  
**Lines**: 575  
**Complexity**: 12 (moderate)

## Overview

Guardrails and Safety Patterns for Agent Systems

This module implements comprehensive safety mechanisms for multi-agent systems including:
- Input validation and moderation
- Output validation and filtering
- Structured output schemas
- Error handling and resilience
- Rate limiting and abuse prevention

Based on patterns from agentic_design_patterns repository.

## Classes (11)

### `ValidationResult`

**Inherits from**: BaseModel

Result of a validation operation.

### `SafetyLevel`

**Inherits from**: Enum

Safety enforcement levels.

### `ContentCategory`

**Inherits from**: Enum

Content categories for filtering.

### `SafetyConfig`

Configuration for safety mechanisms.

### `InputValidator`

Validates and moderates input content.

**Methods** (2):
- `__init__(self, config)`
- `_build_patterns(self)`

### `OutputValidator`

Validates and filters output content.

**Methods** (1):
- `__init__(self, config)`

### `RateLimiter`

Rate limiting for agent requests.

**Methods** (1):
- `__init__(self, requests_per_window, window_seconds)`

### `Guardrail`

Comprehensive guardrail system combining multiple safety mechanisms.

**Methods** (2):
- `__init__(self, config)`
- `create_guarded_function(self, func, input_param, output_schema, user_id_param)`

### `ResilienceDecorator`

Decorator for adding resilience patterns to functions.

**Methods** (2):
- `retry_with_exponential_backoff(max_retries, initial_delay, backoff_factor, max_delay)`
- `circuit_breaker(failure_threshold, recovery_timeout, expected_exception)`

### `ResearchSummary`

**Inherits from**: BaseModel

Schema for research summary outputs.

**Methods** (2):
- `validate_title(cls, v)`
- `validate_findings(cls, v)`

### `CodeReviewResult`

**Inherits from**: BaseModel

Schema for code review outputs.

## Functions (2)

### `create_default_guardrail(level)`

Create a guardrail with default configuration.

### `validate_with_schema(schema)`

Decorator to validate function output against a schema.

## Dependencies

**Imports** (25):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `datetime.timedelta`
- `enum.Enum`
- `functools.wraps`
- `json`
- `logging`
- `pydantic.BaseModel`
- `pydantic.Field`
- `pydantic.ValidationError`
- `pydantic.validator`
- ... and 10 more

---
*Auto-generated documentation*
