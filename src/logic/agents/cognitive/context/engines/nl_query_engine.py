#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from .NLQueryResult import NLQueryResult

from src.classes.base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import re
import zlib

class NLQueryEngine:
    """Searches context with natural language queries.

    Provides natural language interface for searching context.

    Example:
        >>> engine=NLQueryEngine()
        >>> result=engine.query("How does authentication work?", contexts)
    """

    def __init__(self) -> None:
        """Initialize NL query engine."""
        self.contexts: Dict[str, str] = {}

    def add_context(self, name: str, content: str) -> None:
        """Add context to the engine."""
        self.contexts[name] = content

    def extract_keywords(self, query: str) -> List[str]:
        """Extract keywords from query."""
        return query.lower().split()

    def query(self, question: str, contexts: Optional[Dict[str, str]] = None) -> NLQueryResult:
        """Query contexts with natural language.

        Args:
            question: Natural language question.
            contexts: Optional dictionary of context file paths to contents.
                      If omitted, uses contexts added via add_context().

        Returns:
            NLQueryResult with answer.
        """
        # Simplified NL query - in production, use LLM
        relevant: List[str] = []
        keywords = question.lower().split()
        active_contexts = contexts if contexts is not None else self.contexts
        for path, content in active_contexts.items():
            content_lower = content.lower()
            if any(kw in content_lower for kw in keywords):
                relevant.append(path)
        return NLQueryResult(
            query=question,
            answer=f"Found {len(relevant)} relevant context files",
            relevant_contexts=relevant,
            confidence=0.7 if relevant else 0.2
        )
