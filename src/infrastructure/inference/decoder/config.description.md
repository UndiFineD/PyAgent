# config

**File**: `src\infrastructure\inference\decoder\config.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 6 imports  
**Lines**: 168  
**Complexity**: 13 (moderate)

## Overview

Python module containing implementation for config.

## Classes (5)

### `SpecMethod`

**Inherits from**: str, Enum

Speculative decoding method.

### `SpeculativeConfig`

Configuration for speculative decoding.

**Methods** (1):
- `should_disable(self, batch_size)`

### `DraftProposal`

A batch of draft tokens proposed by speculator.

**Methods** (2):
- `num_tokens(self)`
- `is_empty(self)`

### `VerificationResult`

Result of verifying draft tokens against target model.

**Methods** (2):
- `acceptance_rate(self)`
- `all_accepted(self)`

### `SpecDecodingMetrics`

Metrics for speculative decoding performance.

**Methods** (8):
- `__post_init__(self)`
- `new(cls, num_spec_tokens)`
- `observe_draft(self, num_draft_tokens, num_accepted_tokens, accepted_positions)`
- `acceptance_rate(self)`
- `avg_accepted_per_draft(self)`
- `position_acceptance_rates(self)`
- `reset(self)`
- `as_dict(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `typing.Any`
- `typing.Sequence`

---
*Auto-generated documentation*
