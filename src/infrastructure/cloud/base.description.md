# base

**File**: `src\infrastructure\cloud\base.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 10 imports  
**Lines**: 218  
**Complexity**: 9 (moderate)

## Overview

Base classes for cloud provider integration.

Defines the abstract interface that all cloud providers must implement,
along with standardized request/response dataclasses.

## Classes (6)

### `InferenceRequest`

Standardized inference request across all cloud providers.

### `InferenceResponse`

Standardized inference response from cloud providers.

### `CloudProviderBase`

**Inherits from**: ABC

Abstract base class for cloud AI provider integrations.

All cloud connectors (Gemini, Bedrock, Groq, etc.) must inherit from this
class and implement the required abstract methods.

Example:
    class MyProvider(CloudProviderBase):
        async def complete(self, request: InferenceRequest) -> InferenceResponse:
            # Implementation here
            ...

**Methods** (6):
- `__init__(self, api_key)`
- `name(self)`
- `is_healthy(self)`
- `available_models(self)`
- `estimate_cost(self, request)`
- `supports_model(self, model)`

### `CloudProviderError`

**Inherits from**: Exception

Base exception for cloud provider errors.

**Methods** (1):
- `__init__(self, message, provider, retriable)`

### `RateLimitError`

**Inherits from**: CloudProviderError

Raised when rate limits are exceeded.

**Methods** (1):
- `__init__(self, message, provider, retry_after)`

### `AuthenticationError`

**Inherits from**: CloudProviderError

Raised when authentication fails.

**Methods** (1):
- `__init__(self, message, provider)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `dataclasses.dataclass`
- `dataclasses.field`
- `typing.Any`
- `typing.AsyncIterator`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
