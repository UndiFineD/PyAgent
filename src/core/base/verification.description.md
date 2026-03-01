# verification

**File**: `src\core\base\verification.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 11 imports  
**Lines**: 159  
**Complexity**: 8 (moderate)

## Overview

Verification logic for agent outputs.
Implements Stanford Reseach 'Anchoring Strength' and Keio University 'Self-Verification' paths.

## Classes (2)

### `ConfigValidator`

Phase 278: Validates configuration files and detects orphaned references.

**Methods** (1):
- `validate_shard_mapping(mapping_path)`

### `AgentVerifier`

Handles quality and anchoring verification of agent responses.

**Methods** (7):
- `_get_embedding_model(cls)`
- `calculate_anchoring_strength(cls, result, context_pool)`
- `verify_self(result, anchoring_score)`
- `fact_check(code_snippet, agent_id)`
- `secondary_verify(result, primary_model)`
- `jury_verification(agent_responses)`
- `check_latent_reasoning(content)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `json`
- `logging`
- `numpy`
- `pathlib.Path`
- `sentence_transformers.SentenceTransformer`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
