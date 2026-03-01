# __init__

**File**: `src\infrastructure\backend\vllm_advanced\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 16 imports  
**Lines**: 71  
**Complexity**: 0 (simple)

## Overview

Advanced vLLM Integration Module.

Phase 31: Extends PyAgent's vLLM integration with:
- AsyncLLMEngine for high-throughput async inference
- Streaming responses for real-time token output
- LoRA adapter management for efficient fine-tuned models
- Guided decoding for structured output (JSON, regex)

## Dependencies

**Imports** (16):
- `AsyncVllmEngine.AsyncEngineConfig`
- `AsyncVllmEngine.AsyncRequestHandle`
- `AsyncVllmEngine.AsyncVllmEngine`
- `GuidedDecoder.ChoiceConstraint`
- `GuidedDecoder.GuidedConfig`
- `GuidedDecoder.GuidedDecoder`
- `GuidedDecoder.JsonSchema`
- `GuidedDecoder.RegexPattern`
- `LoraManager.LoraAdapter`
- `LoraManager.LoraConfig`
- `LoraManager.LoraManager`
- `LoraManager.LoraRegistry`
- `StreamingEngine.StreamCallback`
- `StreamingEngine.StreamingConfig`
- `StreamingEngine.StreamingVllmEngine`
- ... and 1 more

---
*Auto-generated documentation*
