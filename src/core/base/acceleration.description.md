# acceleration

**File**: `src\core\base\acceleration.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 1 imports  
**Lines**: 39  
**Complexity**: 2 (simple)

## Overview

Bridge for Rust Acceleration.
Interfaces with rust_core via PyO3 or CFFI.

## Classes (1)

### `NeuralPruningEngine`

Core engine for pruning neural connections in the swarm.

**Methods** (2):
- `calculate_synaptic_weight_python(self, inputs, weights)`
- `calculate_synaptic_weight(self, inputs, weights)`

## Dependencies

**Imports** (1):
- `__future__.annotations`

---
*Auto-generated documentation*
