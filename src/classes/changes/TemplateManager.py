#!/usr/bin/env python3

"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations

from .EntryTemplate import EntryTemplate

from base_agent import BaseAgent
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
