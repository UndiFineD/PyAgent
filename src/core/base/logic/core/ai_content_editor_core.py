#!/usr/bin/env python3
"""Minimal AI content editor core for tests."""
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
    edits: List[str] = None


@dataclass
class ContentTemplate:
    id: str
    description: str = ""


class AIContentEditorCore:
    def __init__(self) -> None:
        pass

    def edit(self, request: ContentEditRequest) -> ContentEditResult:
        # Nop edit: return text unchanged
        return ContentEditResult(text=request.text, edits=[])


__all__ = ["ContentEditRequest", "ContentEditResult", "ContentTemplate", "AIContentEditorCore"]
