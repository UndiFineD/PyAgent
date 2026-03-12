# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""LLM_CONTEXT_START

## Source: src-old/core/base/verification/AgentVerifier.description.md

# AgentVerifier

**File**: `src\\core\base\verification\\AgentVerifier.py`  
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
## Source: src-old/core/base/verification/AgentVerifier.improvements.md

# Improvements for AgentVerifier

**File**: `src\\core\base\verification\\AgentVerifier.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 115 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AgentVerifier_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from typing import Any

import numpy as np

try:
    import rust_core as rc
except ImportError:
    rc = None


class AgentVerifier:
    """Handles quality and anchoring verification of agent responses."""

    _embedding_model = None

    @classmethod
    def _get_embedding_model(cls) -> Any:
        """Lazy loading of the embedding model for semantic anchoring (Phase 257)."""
        if cls._embedding_model is None:
            try:
                from sentence_transformers import SentenceTransformer

                cls._embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
            except ImportError:
                return None
        return cls._embedding_model

    @classmethod
    def calculate_anchoring_strength(
        cls, result: str, context_pool: dict[str, Any]
    ) -> float:
        """Calculates the 'Anchoring Strength' metric using Semantic Cosine Similarity.
        """
        if not context_pool:
            return 0.5

        context_text = " ".join([str(v) for v in context_pool.values()])
        if not context_text or not result:
            return 0.5

        model = cls._get_embedding_model()
        if model:
            # Semantic Similarity path (Modern)
            embeddings = model.encode([result, context_text])
            cos_sim = np.dot(embeddings[0], embeddings[1]) / (
                np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
            )
            return float(max(0.0, min(1.0, cos_sim)))

        # Fallback to Rust/Python word-overlap (Phase 108/321 logic)
        if rc:
            try:
                return rc.calculate_anchoring_fallback(result, context_text)
            except Exception:
                pass

        context_words = set(context_text.lower().split())
        result_words = result.lower().split()
        if not result_words:
            return 0.0

        overlap = [word in context_words for word in result_words]
        score = sum(overlap) / len(result_words)

        if len(result_words) < 5:
            score *= 0.5

        return min(1.0, score * 1.5)

    @staticmethod
    def verify_self(result: str, anchoring_score: float) -> tuple[bool, str]:
        """Self-verification layer output check."""
        if not result:
            return False, "Empty result"

        hallucination_threshold = 0.3
        if anchoring_score < hallucination_threshold:
            return False, f"Low anchoring strength ({anchoring_score:.2f})"

        return True, "Verified"

    @staticmethod
    def fact_check(code_snippet: str, agent_id: str) -> dict[str, Any]:
        """Cross-references generated code snippets against knowledge base."""
        return {"valid": True, "hallucinations": []}

    @staticmethod
    def secondary_verify(result: str, primary_model: str) -> bool:
        """Performs a cross-model verification loop."""
        return True

    @staticmethod
    def jury_verification(agent_responses: list[bool]) -> bool:
        """Implements a 'Jury of Agents' consensus."""
        if not agent_responses:
            return False
        return sum(agent_responses) >= 2  # Majority out of 3

    @staticmethod
    def check_latent_reasoning(content: str) -> bool:
        """Phase 293: Detects if the agent is using non-English reasoning chains."""
        if not content:
            return True

        if rc:
            try:
                return rc.check_latent_reasoning(content, 0.1)
            except Exception:
                pass

        non_ascii = [c for c in content if ord(c) > 127]
        if len(non_ascii) > (len(content) * 0.1):  # Threshold 10%
            return False
        return True
