"""LLM_CONTEXT_START

## Source: src-old/logic/agents/system/core/MultiModalCore.description.md

# MultiModalCore

**File**: `src\\logic\agents\\system\\core\\MultiModalCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 54  
**Complexity**: 3 (simple)

## Overview

Core logic for Multi-Modal Context (Phase 178).
Handles interactions with vision models for bug analysis.

## Classes (1)

### `MultiModalCore`

Class MultiModalCore implementation.

**Methods** (3):
- `encode_image(image_path)`
- `construct_vision_payload(model, prompt, base64_image)`
- `parse_bug_report(vision_response)`

## Dependencies

**Imports** (3):
- `base64`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/system/core/MultiModalCore.improvements.md

# Improvements for MultiModalCore

**File**: `src\\logic\agents\\system\\core\\MultiModalCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 54 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: MultiModalCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MultiModalCore_test.py` with pytest tests

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

"""
Core logic for Multi-Modal Context (Phase 178).
Handles interactions with vision models for bug analysis.
"""

import base64
from typing import Any


class MultiModalCore:
    @staticmethod
    def encode_image(image_path: str) -> str:
        """Encodes an image file to base64.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    @staticmethod
    def construct_vision_payload(
        model: str, prompt: str, base64_image: str
    ) -> dict[str, Any]:
        """Constructs a payload for a vision model (OpenAI-style).
        """
        return {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            "max_tokens": 500,
        }

    @staticmethod
    def parse_bug_report(vision_response: str) -> dict[str, Any]:
        """Simplifies vision response into a structured bug report.
        """
        # Heuristic parsing - in reality, we'd use JSON mode if supported
        is_bug = "bug" in vision_response.lower() or "error" in vision_response.lower()
        return {
            "potential_bug": is_bug,
            "description": vision_response,
            "confidence": 0.85 if is_bug else 0.5,
        }
