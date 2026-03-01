# multimodal_ai_service

**File**: `src\core\base\logic\multimodal_ai_service.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 10 imports  
**Lines**: 315  
**Complexity**: 11 (moderate)

## Overview

Multimodal AI Service Gateway
============================

Inspired by audio-transcriber's Cloudflare AI Gateway pattern.
Provides unified interface for various AI services (speech, text, vision).

## Classes (5)

### `AIServiceConfig`

Configuration for AI service providers.

**Methods** (1):
- `__post_init__(self)`

### `AIServiceProvider`

**Inherits from**: ABC

Abstract base class for AI service providers.

**Methods** (2):
- `__init__(self, config)`
- `get_model_for_service(self, service_type)`

### `OpenAIProvider`

**Inherits from**: AIServiceProvider

OpenAI API provider.

### `CloudflareProvider`

**Inherits from**: AIServiceProvider

Cloudflare AI Gateway provider.

**Methods** (4):
- `__init__(self, config)`
- `_build_gateway_url(self, model)`
- `_get_content_type(self, data)`
- `_prepare_request_body(self, service_type, data)`

### `MultimodalAIService`

Unified multimodal AI service gateway.

Provides a single interface for various AI services across different providers.

**Methods** (4):
- `__init__(self)`
- `register_provider(self, name, provider)`
- `get_available_services(self, provider)`
- `get_stats(self)`

## Dependencies

**Imports** (10):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `logging`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
