#!/usr/bin/env python3
"""Template core - minimal parser-safe implementation."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    import rust_core as rc  # type: ignore
except ImportError:
    rc = None

from .base_core import BaseCore


class TemplateCore(BaseCore):
    """Standard implementation for managing structured templates."""

    def __init__(self) -> None:
        super().__init__()
        self.templates: Dict[str, str] = {
            "python_full": "Python code template: [code]",
            "improvement": "Suggested improvement: [description]",
            "report": "Analysis report for [file]: [content]",
        }

    def register_template(self, name: str, content: str) -> None:
        """Adds a new template to the registry."""
        self.templates[name] = content

    def get_template(self, name: str) -> Optional[str]:
        """Retrieves a template by name."""
        return self.templates.get(name)

    def apply_template(self, name: str, context: Dict[str, Any]) -> str:
        """Applies context variables to a template."""
        if name not in self.templates:
            return ""
        content = self.templates[name]
        if rc and hasattr(rc, "apply_template_rust"):
            str_context = {k: str(v) for k, v in context.items()}
            return rc.apply_template_rust(content, str_context)  # type: ignore
        for key, value in context.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))
            content = content.replace(f"[{key}]", str(value))
        return content

    def list_templates(self) -> List[str]:
        """Returns list of registered template names."""
        return list(self.templates.keys())

