#!/usr/bin/env python3
from __future__ import annotations
"""
Parser-safe stub: base reasoning parser interface.""
from abc import ABC, abstractmethod
from typing import Any, Sequence, ClassVar, Tuple


class ReasoningResult:
    pass


class StreamingReasoningState:
    pass


class ReasoningParser(ABC):
"""
Conservative abstract parser preserving API.""
    name: ClassVar[str] = "base"

    def __init__(self, tokenizer: Any = None, **_kwargs: Any) -> None:
        self.model_tokenizer = tokenizer

    def vocab(self) -> dict:
        return {}

    @abstractmethod
    def is_reasoning_end(self, input_ids: list[int]) -> bool:
        return True

    @abstractmethod
    def extract_content_ids(self, input_ids: list[int]) -> list[int]:
        return []

    @abstractmethod
    def extract_reasoning(self, model_output: str, request: Any = None) -> ReasoningResult:
        return ReasoningResult()
