# __init__

**File**: `src\infrastructure\cloud\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 18 imports  
**Lines**: 62  
**Complexity**: 1 (simple)

## Overview

Cloud Infrastructure Module - Multi-cloud integration for PyAgent.

Provides unified interface for cloud AI providers with intelligent routing,
budget management, and health-aware failover.

## Functions (1)

### `__getattr__(name)`

Lazy load cloud components on first access.

## Dependencies

**Imports** (18):
- `__future__.annotations`
- `base.CloudProviderBase`
- `base.InferenceRequest`
- `base.InferenceResponse`
- `budget.BudgetManager`
- `providers.bedrock.AWSBedrockConnector`
- `providers.gemini.GeminiConnector`
- `providers.groq.GroqConnector`
- `routing.IntelligentRouter`
- `typing.TYPE_CHECKING`
- ... and 3 more

---
*Auto-generated documentation*
