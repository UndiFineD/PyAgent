# groq

**File**: `src\infrastructure\cloud\providers\groq.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 229  
**Complexity**: 5 (moderate)

## Overview

Groq cloud provider connector.

Provides integration with Groq's ultra-fast inference API,
optimized for low-latency LLM inference.

## Classes (1)

### `GroqConnector`

**Inherits from**: CloudProviderBase

Connector for Groq API.

Groq provides ultra-fast inference using their LPU (Language Processing Unit)
technology. Optimized for low-latency use cases.

Example:
    connector = GroqConnector(api_key="your-api-key")
    
    request = InferenceRequest(
        messages=[{"role": "user", "content": "Hello!"}],
        model="llama-3.1-70b-versatile",
    )
    
    response = await connector.complete(request)
    print(response.content)

**Methods** (5):
- `__init__(self, api_key, base_url, timeout)`
- `name(self)`
- `available_models(self)`
- `estimate_cost(self, request)`
- `get_rate_limits(self)`

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `base.AuthenticationError`
- `base.CloudProviderBase`
- `base.CloudProviderError`
- `base.InferenceRequest`
- `base.InferenceResponse`
- `base.RateLimitError`
- `os`
- `time`
- `typing.Any`
- `typing.AsyncIterator`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
