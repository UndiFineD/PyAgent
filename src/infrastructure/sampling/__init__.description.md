# __init__

**File**: `src\infrastructure\sampling\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 27 imports  
**Lines**: 86  
**Complexity**: 0 (simple)

## Overview

Sampling infrastructure module.

Provides unified sampling strategies for token generation,
inspired by vLLM's v1/sample architecture.

Phase 40 additions:
- AdvancedSamplingParams with vLLM parity
- Bad words blocking
- Token whitelisting
- Mirostat sampling
- Adaptive sampling based on entropy
- Temperature scheduling

## Dependencies

**Imports** (27):
- `AdvancedSamplingParams.AdvancedSamplingParams`
- `AdvancedSamplingParams.BadWordsProcessor`
- `AdvancedSamplingParams.LogitBiasBuilder`
- `AdvancedSamplingParams.MirostatSampler`
- `AdvancedSamplingParams.OutputKind`
- `AdvancedSamplingParams.SamplingEngine`
- `AdvancedSamplingParams.StopCondition`
- `AdvancedSamplingParams.TemperatureSchedule`
- `AdvancedSamplingParams.TokenWhitelistProcessor`
- `AdvancedSamplingParams.create_advanced_sampling_params`
- `AdvancedSamplingParams.create_sampling_params`
- `Base.HAS_RUST`
- `Base.Sampler`
- `BeamSearch.BeamHypothesis`
- `BeamSearch.BeamSearchConfig`
- ... and 12 more

---
*Auto-generated documentation*
