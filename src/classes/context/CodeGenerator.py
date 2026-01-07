#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from .GeneratedCode import GeneratedCode

from base_agent import BaseAgent
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

class CodeGenerator:
    """Generates code based on context.

    Uses context information to generate relevant code.

    Example:
        >>> generator=CodeGenerator()
        >>> code=generator.generate("Create a login function", context)
    """

    def __init__(self) -> None:
        self.language: str = "python"
        self.contexts: Dict[str, str] = {}

    def set_language(self, language: str) -> None:
        """Set the default target language for generated code."""
        self.language = language

    def add_context(self, name: str, content: str) -> None:
        """Add a named context document that can be referenced later."""
        self.contexts[name] = content

    def get_supported_languages(self) -> List[str]:
        """Return supported target languages."""
        return [
            "python",
            "javascript",
            "typescript",
            "java",
            "csharp",
            "go",
            "rust",
        ]

    def generate(
        self,
        prompt: str,
        context: str = "",
        language: Optional[str] = None,
        *,
        context_files: Optional[List[str]] = None,
    ) -> GeneratedCode:
        """Generate code based on stored context.

        Backwards compatible with the older signature:
            generate(prompt, context, language="python")

        Newer API (used by tests):
            set_language(...), add_context(...), generate(prompt, context_files=[...])
        """
        resolved_language = language or self.language or "python"

        used_contexts: List[str] = []
        context_snippets: List[str] = []

        if context_files:
            for name in context_files:
                if name in self.contexts:
                    used_contexts.append(name)
                    context_snippets.append(self.contexts[name])
        elif context:
            # Inline context (legacy usage)
            used_contexts.append(context[:50] + ("..." if len(context) > 50 else ""))
            context_snippets.append(context)

        # Simplified generation - in production, use an LLM.
        context_header = "" if not used_contexts else f"# Context used: {', '.join(used_contexts)}\n"
        code = (
            f"# Generated for: {prompt}\n"
            f"{context_header}"
            f"def generated_function():\n"
            f"    \"\"\"Auto-generated stub.\"\"\"\n"
            f"    pass\n"
        )

        return GeneratedCode(
            language=resolved_language,
            code=code,
            context_used=used_contexts,
            description=prompt,
        )
