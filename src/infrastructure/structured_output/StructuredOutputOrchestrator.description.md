# StructuredOutputOrchestrator

**File**: `src\infrastructure\structured_output\StructuredOutputOrchestrator.py`  
**Type**: Python Module  
**Summary**: 11 classes, 0 functions, 28 imports  
**Lines**: 588  
**Complexity**: 32 (complex)

## Overview

StructuredOutputOrchestrator - Unified structured output orchestration.

Provides a unified interface for structured output backends:
- Backend selection
- Grammar composition
- Request routing
- Performance monitoring

Beyond vLLM innovations:
- Multi-backend fallback
- Auto-backend selection
- Composite grammars
- Streaming constraint checking

## Classes (11)

### `StructuredOutputBackendType`

**Inherits from**: Enum

Types of structured output backends.

### `ConstraintType`

**Inherits from**: Enum

Types of output constraints.

### `GrammarProtocol`

**Inherits from**: Protocol

Protocol for grammar implementations.

**Methods** (4):
- `accept_token(self, token_id)`
- `fill_next_token_bitmask(self, bitmask)`
- `is_terminated(self)`
- `reset(self)`

### `BackendProtocol`

**Inherits from**: Protocol

Protocol for backend implementations.

**Methods** (3):
- `compile_json_schema(self, schema)`
- `allocate_bitmask(self, batch_size)`
- `get_stats(self)`

### `ConstraintSpec`

Specification for output constraint.

Describes the constraint to apply to generation.

**Methods** (1):
- `to_cache_key(self)`

### `OrchestratorConfig`

Configuration for orchestrator.

### `BackendWrapper`

Wrapper for structured output backend.

Provides unified interface and statistics tracking.

**Methods** (3):
- `__init__(self, backend, backend_type)`
- `compile(self, constraint)`
- `get_stats(self)`

### `CompiledGrammarHandle`

Handle to compiled grammar.

Provides state management and bitmask operations.

**Methods** (6):
- `__init__(self, grammar, backend_type, constraint)`
- `accept_token(self, token_id)`
- `fill_next_token_bitmask(self, bitmask)`
- `is_terminated(self)`
- `reset(self)`
- `tokens_accepted(self)`

### `StructuredOutputOrchestrator`

Orchestrator for structured output backends.

Provides unified interface for:
- Backend registration and selection
- Constraint compilation with caching
- Fallback handling
- Performance monitoring

**Methods** (9):
- `__init__(self, tokenizer, config)`
- `register_backend(self, backend_type, backend, set_as_default)`
- `_select_backend(self, constraint)`
- `_try_fallback(self, constraint, tried)`
- `compile(self, constraint)`
- `compile_json_schema(self, schema)`
- `compile_regex(self, pattern)`
- `get_stats(self)`
- `clear_cache(self)`

### `AsyncStructuredOutputOrchestrator`

**Inherits from**: StructuredOutputOrchestrator

Async-enabled orchestrator.

Provides async compilation for non-blocking operation.

### `BatchProcessor`

Batch processor for structured output.

Handles batch-level bitmask operations efficiently.

**Methods** (6):
- `__init__(self, orchestrator, batch_size, vocab_size)`
- `set_constraint(self, batch_idx, constraint)`
- `accept_tokens(self, token_ids)`
- `fill_bitmask(self)`
- `get_terminated_indices(self)`
- `reset(self)`

## Dependencies

**Imports** (28):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `hashlib`
- `json`
- `logging`
- `numpy`
- `rust_core`
- `threading`
- `time`
- `traceback`
- ... and 13 more

---
*Auto-generated documentation*
