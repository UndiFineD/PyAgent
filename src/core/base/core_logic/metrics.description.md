# metrics

**File**: `src\core\base\core_logic\metrics.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 72  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for metrics.

## Classes (1)

### `MetricsCore`

Class MetricsCore implementation.

**Methods** (6):
- `calculate_anchoring_strength(self, result, context_pool)`
- `verify_self(self, result, anchoring_score)`
- `assess_response_quality(self, response, metadata)`
- `_assess_quality_python(self, response, metadata)`
- `calculate_priority_score(self, priority, urgency)`
- `calculate_token_estimate(self, text, chars_per_token)`

## Dependencies

**Imports** (10):
- `logging`
- `rust_core`
- `src.core.base.AgentVerification.AgentVerifier`
- `src.core.base.models.AgentPriority`
- `src.core.base.models.ResponseQuality`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
