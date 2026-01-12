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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent_changes.py"""




from .EntryTemplate import EntryTemplate

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any, Tuple
import hashlib
import json
import logging
import re

class TemplateManager:
    """Manages entry templates with placeholders.

    Provides template storage and application functionality.

    Attributes:
        templates: Dictionary of templates by name.

    Example:
        >>> manager=TemplateManager()
        >>> manager.add_template("bug_fix", "Fixed {issue} in {component}")
        >>> text=manager.apply_template("bug_fix", {"issue": "#123", "component": "auth"})
    """

    def __init__(self) -> None:
        """Initialize the template manager."""
        self.templates: Dict[str, EntryTemplate] = {}

    def add_template(
        self,
        name: str,
        template_text: str,
        description: str = ""
    ) -> EntryTemplate:
        """Add a new template.

        Args:
            name: Template name.
            template_text: Template with placeholders.
            description: Template description.

        Returns:
            The created EntryTemplate.
        """
        # Extract placeholders
        placeholders = re.findall(r'\{(\w+)\}', template_text)

        template = EntryTemplate(
            name=name,
            template_text=template_text,
            placeholders=placeholders,
            description=description
        )
        self.templates[name] = template
        return template

    def apply_template(self, name: str, values: Dict[str, str]) -> str:
        """Apply a template with values.

        Args:
            name: Template name.
            values: Dictionary of placeholder values.

        Returns:
            Filled - in template text.
        """
        template = self.templates.get(name)
        if not template:
            return ""

        result = template.template_text
        for placeholder, value in values.items():
            result = result.replace(f"{{{placeholder}}}", value)
        return result

    def get_template_placeholders(self, name: str) -> List[str]:
        """Get placeholders for a template.

        Args:
            name: Template name.

        Returns:
            List of placeholder names.
        """
        template = self.templates.get(name)
        return template.placeholders if template else []
