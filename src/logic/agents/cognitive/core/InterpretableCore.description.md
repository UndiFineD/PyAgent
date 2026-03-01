# InterpretableCore

**File**: `src\logic\agents\cognitive\core\InterpretableCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 96  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for InterpretableCore.

## Classes (1)

### `InterpretableCore`

InterpretableCore implements a logic-bridge for Sparse Autoencoders (SAE).
It simulates the decomposition of LLM activations into human-interpretable features.

Phase 14 Rust Optimizations:
- top_k_indices_rust: Fast top-K selection for activation sparsification
- decompose_activations_rust: Vectorized activation decomposition

**Methods** (4):
- `__init__(self, feature_count)`
- `decompose_activations(self, mock_activations)`
- `simulate_neural_trace(self, agent_name, decision)`
- `_get_label_for_index(self, index)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `logging`
- `rust_core`
- `typing.Any`

---
*Auto-generated documentation*
