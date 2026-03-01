# domain_generator

**File**: `src\logic\agents\security\recon\domain_generator.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 7 imports  
**Lines**: 86  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for domain_generator.

## Classes (4)

### `LLMInterface`

**Inherits from**: Protocol

Class LLMInterface implementation.

### `DomainGenerationResult`

Class DomainGenerationResult implementation.

### `DomainGenerator`

Generates domain variations using LLMs based on pattern recognition/fuzzing.
Ported concepts from 0xSojalSec-cewlai.

**Methods** (1):
- `__init__(self, llm_client)`

### `MockLLM`

Class MockLLM implementation.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (7):
- `asyncio`
- `dataclasses.dataclass`
- `re`
- `typing.Dict`
- `typing.List`
- `typing.Protocol`
- `typing.Set`

---
*Auto-generated documentation*
