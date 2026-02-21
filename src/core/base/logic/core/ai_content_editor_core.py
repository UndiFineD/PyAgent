#!/usr/bin/env python3
"""Minimal stub for ai_content_editor_core used during repairs."""

from __future__ import annotations


class AIContentEditorCore:
    """Repair-time stub of AIContentEditorCore."""

    def __init__(self, *args, **kwargs) -> None:
        pass


__all__ = ["AIContentEditorCore"]

#!/usr/bin/env python3
"""
Parser-safe stub: AI content editor core (conservative).

Minimal stub to keep public symbols available for imports and tests.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ContentEditRequest:
    text: str
    template_id: Optional[str] = None


@dataclass
class ContentEditResult:
    text: str
    edits: List[str]


class AIContentEditorCore:
    def edit(self, request: ContentEditRequest) -> ContentEditResult:
        return ContentEditResult(text=request.text, edits=[])


__all__ = ["ContentEditRequest", "ContentEditResult", "AIContentEditorCore"]
