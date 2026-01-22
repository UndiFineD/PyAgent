# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Unified Template Core for PyAgent.
Handles variable substitution, template registration, and versioning.
"""

from __future__ import annotations
import re
from typing import Any, Dict, Optional, List
from src.core.base.common.base_core import BaseCore

try:
    import rust_core as rc
except ImportError:
    rc = None

class TemplateCore(BaseCore):
    """
    Standard implementation for manage structured templates.
    Supports variable substitution using {{variable}} or [variable] syntax.
    """
    
    def __init__(self):
        super().__init__()
        self.templates: Dict[str, str] = {}

    def register_template(self, name: str, content: str) -> None:
        """Adds a new template to the registry."""
        self.templates[name] = content

    def apply_template(self, name: str, context: Dict[str, Any]) -> str:
        """Applies context variables to a template."""
        if name not in self.templates:
            return ""
        
        content = self.templates[name]
        
        # Try Rust acceleration for high-performance substitution
        if rc and hasattr(rc, "apply_template_rust"):
            # Convert context to string dict
            str_context = {k: str(v) for k, v in context.items()}
            return rc.apply_template_rust(content, str_context)
        
        # Python fallback
        for key, value in context.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))
            content = content.replace(f"[{key}]", str(value))
        return content

    def list_templates(self) -> List[str]:
        """Returns list of registered template names."""
        return list(self.templates.keys())
