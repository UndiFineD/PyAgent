# EvolutionCore

**File**: `src\classes\fleet\EvolutionCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 62  
**Complexity**: 3 (simple)

## Overview

EvolutionCore logic for agent fleet adaptation.
Contains pure logic for template generation and hyperparameter optimization.

## Classes (1)

### `EvolutionCore`

Pure logic core for evolutionary agent development.
Designed for future Rust implementation (Core/Shell pattern).
No I/O or global state.

**Methods** (3):
- `__init__(self, default_temp)`
- `generate_agent_template(self, name, capabilities, base_type)`
- `compute_mutations(self, fleet_stats)`

## Dependencies

**Imports** (4):
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
