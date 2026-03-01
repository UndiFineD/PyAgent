# recursive_thinker

**File**: `src\logic\agents\reasoning\recursive_thinker.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 6 imports  
**Lines**: 113  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for recursive_thinker.

## Classes (4)

### `LLMInterface`

**Inherits from**: Protocol

Class LLMInterface implementation.

### `RoundResult`

Class RoundResult implementation.

### `RecursiveThinker`

Implements a recursive thinking pattern (CoRT) to improve agent responses by 
generating alternatives and self-evaluating.
Ported logic from 0xSojalSec-Chain-of-Recursive-Thoughts.

**Methods** (1):
- `__init__(self, llm)`

### `MockThinkerLLM`

Class MockThinkerLLM implementation.

## Dependencies

**Imports** (6):
- `asyncio`
- `dataclasses.dataclass`
- `typing.Any`
- `typing.List`
- `typing.Optional`
- `typing.Protocol`

---
*Auto-generated documentation*
