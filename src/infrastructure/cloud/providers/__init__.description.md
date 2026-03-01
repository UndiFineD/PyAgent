# __init__

**File**: `src\infrastructure\cloud\providers\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 12 imports  
**Lines**: 53  
**Complexity**: 1 (simple)

## Overview

Cloud provider implementations.

This package contains concrete implementations of CloudProviderBase
for various cloud AI providers.

## Functions (1)

### `__getattr__(name)`

Lazy load provider implementations.

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `azure.AzureAIConnector`
- `bedrock.AWSBedrockConnector`
- `gemini.GeminiConnector`
- `groq.GroqConnector`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
