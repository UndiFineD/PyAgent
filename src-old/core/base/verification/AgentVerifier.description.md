# AgentVerifier

**File**: `src\core\base\verification\AgentVerifier.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 115  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for AgentVerifier.

## Classes (1)

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

**Imports** (4):
- `numpy`
- `rust_core`
- `sentence_transformers.SentenceTransformer`
- `typing.Any`

---
*Auto-generated documentation*
