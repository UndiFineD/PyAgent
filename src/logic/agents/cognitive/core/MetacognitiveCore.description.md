# MetacognitiveCore

**File**: `src\logic\agents\cognitive\core\MetacognitiveCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 121  
**Complexity**: 5 (moderate)

## Overview

MetacognitiveCore logic for PyAgent.
Pure logic for evaluating reasoning certainty and consistency.
No I/O or side effects.

## Classes (1)

### `MetacognitiveCore`

Pure logic core for metacognitive evaluation and intention prediction.

Phase 14 Rust Optimizations:
- count_hedge_words_rust: Fast multi-pattern matching for hedge word detection
- predict_intent_rust: Optimized pattern-based intent classification

**Methods** (5):
- `calibrate_confidence_weight(self, reported_conf, actual_correct, current_weight)`
- `predict_next_intent(self, history)`
- `get_prewarm_targets(self, predicted_intent)`
- `calculate_confidence(reasoning_chain)`
- `aggregate_summary(uncertainty_log)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `logging`
- `rust_core`
- `src.core.base.Version.VERSION`
- `typing.Any`

---
*Auto-generated documentation*
