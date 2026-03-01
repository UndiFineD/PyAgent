# gemini

**File**: `src\infrastructure\cloud\providers\gemini.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 209  
**Complexity**: 5 (moderate)

## Overview

Google Gemini cloud provider connector.

Provides integration with Google's Gemini API for inference requests.

## Classes (1)

### `GeminiConnector`

**Inherits from**: CloudProviderBase

Connector for Google Gemini API.

Supports Gemini Pro, Gemini Ultra, and other Gemini model variants.

Example:
    connector = GeminiConnector(api_key="your-api-key")
    
    request = InferenceRequest(
        messages=[{"role": "user", "content": "Hello!"}],
        model="gemini-pro",
    )
    
    response = await connector.complete(request)
    print(response.content)

**Methods** (5):
- `__init__(self, api_key, project_id, location)`
- `name(self)`
- `available_models(self)`
- `estimate_cost(self, request)`
- `_format_messages(self, messages)`

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `base.AuthenticationError`
- `base.CloudProviderBase`
- `base.CloudProviderError`
- `base.InferenceRequest`
- `base.InferenceResponse`
- `base.RateLimitError`
- `httpx`
- `json`
- `os`
- `time`
- `typing.Any`
- `typing.AsyncIterator`
- `typing.Dict`
- `typing.List`
- ... and 2 more

---
*Auto-generated documentation*
