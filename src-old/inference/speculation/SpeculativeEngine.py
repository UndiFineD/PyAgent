
r"""LLM_CONTEXT_START

## Source: src-old/inference/speculation/SpeculativeEngine.description.md

# SpeculativeEngine

**File**: `src\inference\speculation\SpeculativeEngine.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 13 imports  
**Lines**: 37  
**Complexity**: 0 (simple)

## Overview

Speculative Decoding Engine - Facade pattern for backward compatibility.

## Dependencies

**Imports** (13):
- `engine.DraftProposal`
- `engine.DrafterBase`
- `engine.EagleProposer`
- `engine.HybridDrafter`
- `engine.NgramProposer`
- `engine.SpecDecodingMetrics`
- `engine.SpecMethod`
- `engine.SpeculativeConfig`
- `engine.SpeculativeEngine`
- `engine.SuffixProposer`
- `engine.TokenVerifier`
- `engine.VerificationResult`
- `engine.create_speculative_decoder`

---
*Auto-generated documentation*
## Source: src-old/inference/speculation/SpeculativeEngine.improvements.md

# Improvements for SpeculativeEngine

**File**: `src\inference\speculation\SpeculativeEngine.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 37 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SpeculativeEngine_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Speculative Decoding Engine - Facade pattern for backward compatibility."""

from .engine import (
    DrafterBase,
    DraftProposal,
    EagleProposer,
    HybridDrafter,
    NgramProposer,
    SpecDecodingMetrics,
    SpecMethod,
    SpeculativeConfig,
    SpeculativeEngine,
    SuffixProposer,
    TokenVerifier,
    VerificationResult,
    create_speculative_decoder,
)

__all__ = [
    "SpecMethod",
    "SpeculativeConfig",
    "DraftProposal",
    "VerificationResult",
    "SpecDecodingMetrics",
    "DrafterBase",
    "NgramProposer",
    "SuffixProposer",
    "EagleProposer",
    "HybridDrafter",
    "TokenVerifier",
    "SpeculativeEngine",
    "create_speculative_decoder",
]

