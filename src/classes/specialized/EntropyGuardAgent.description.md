# EntropyGuardAgent

**File**: `src\classes\specialized\EntropyGuardAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 43  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for EntropyGuardAgent.

## Classes (1)

### `EntropyGuardAgent`

**Inherits from**: BaseAgent

Phase 60: Quantum-Resistant Cryptographic Layer.
Manages simulated post-quantum cryptographic (PQC) keys and entropy pools.

**Methods** (4):
- `__init__(self, path)`
- `generate_pqc_keypair(self, fleet_id)`
- `simulate_quantum_safe_encrypt(self, data, target_fleet_id)`
- `rotate_entropy_pool(self)`

## Dependencies

**Imports** (8):
- `hashlib`
- `logging`
- `os`
- `src.classes.base_agent.BaseAgent`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
