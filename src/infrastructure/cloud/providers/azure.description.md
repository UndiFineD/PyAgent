# azure

**File**: `src\infrastructure\cloud\providers\azure.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 140  
**Complexity**: 5 (moderate)

## Overview

Azure AI Foundry cloud provider connector.

Provides integration with Azure AI Foundry (formerly Azure ML) for inference requests.

## Classes (1)

### `AzureAIConnector`

**Inherits from**: CloudProviderBase

Connector for Azure AI Foundry models.

Supports models hosted on Azure AI Foundry endpoints, 
including Llama 3, Phi-3, Cohere, etc.

Compatible with OpenAI-style API endpoints provided by Azure.

**Methods** (5):
- `__init__(self, api_key, endpoint, api_version)`
- `name(self)`
- `available_models(self)`
- `_is_entra_token(self)`
- `_calculate_cost(self, model, input_tokens, output_tokens)`

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
- `logging`
- `os`
- `time`
- `typing.Any`
- `typing.AsyncIterator`
- `typing.Dict`
- ... and 2 more

---
*Auto-generated documentation*
