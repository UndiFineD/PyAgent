# MetacognitiveCore

**File**: `src\classes\cognitive\MetacognitiveCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 72  
**Complexity**: 5 (moderate)

## Overview

MetacognitiveCore logic for PyAgent.
Pure logic for evaluating reasoning certainty and consistency.
No I/O or side effects.

## Classes (1)

### `MetacognitiveCore`

Pure logic core for metacognitive evaluation and intention prediction.

**Methods** (5):
- `calibrate_confidence_weight(self, reported_conf, actual_correct, current_weight)`
- `predict_next_intent(self, history)`
- `get_prewarm_targets(self, predicted_intent)`
- `calculate_confidence(reasoning_chain)`
- `aggregate_summary(uncertainty_log)`

## Dependencies

**Imports** (3):
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
