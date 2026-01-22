<<<<<<< HEAD
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
"""
Unified Template Core for PyAgent.
Handles variable substitution, template registration, and versioning.
"""

from __future__ import annotations
<<<<<<< HEAD

from typing import Any, Dict, List
=======
import re
from typing import Any, Dict, Optional, List
from src.core.base.common.base_core import BaseCore
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

try:
    import rust_core as rc
except ImportError:
    rc = None

<<<<<<< HEAD
from .base_core import BaseCore


=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class TemplateCore(BaseCore):
    """
    Standard implementation for manage structured templates.
    Supports variable substitution using {{variable}} or [variable] syntax.
    """
<<<<<<< HEAD

    def __init__(self) -> None:
        """Initialize the template registry."""
        super().__init__()
        self.templates: Dict[str, str] = {
            "python_full": "Python code template: [code]",
            "improvement": "Suggested improvement: [description]",
            "report": "Analysis report for [file]: [content]"
        }
=======
    
    def __init__(self):
        super().__init__()
        self.templates: Dict[str, str] = {}
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

    def register_template(self, name: str, content: str) -> None:
        """Adds a new template to the registry."""
        self.templates[name] = content

<<<<<<< HEAD
    def get_template(self, name: str) -> str | None:
        """Retrieves a template by name."""
        return self.templates.get(name)

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    def apply_template(self, name: str, context: Dict[str, Any]) -> str:
        """Applies context variables to a template."""
        if name not in self.templates:
            return ""
<<<<<<< HEAD

        content = self.templates[name]

=======
        
        content = self.templates[name]
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # Try Rust acceleration for high-performance substitution
        if rc and hasattr(rc, "apply_template_rust"):
            # Convert context to string dict
            str_context = {k: str(v) for k, v in context.items()}
<<<<<<< HEAD
            return rc.apply_template_rust(content, str_context)  # pylint: disable=no-member

=======
            return rc.apply_template_rust(content, str_context)
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # Python fallback
        for key, value in context.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))
            content = content.replace(f"[{key}]", str(value))
        return content

    def list_templates(self) -> List[str]:
        """Returns list of registered template names."""
        return list(self.templates.keys())
