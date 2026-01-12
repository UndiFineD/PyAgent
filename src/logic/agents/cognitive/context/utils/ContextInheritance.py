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


"""Auto-extracted class from agent_context.py"""




from src.logic.agents.cognitive.context.models.InheritanceMode import InheritanceMode
from src.logic.agents.cognitive.context.models.InheritedContext import InheritedContext

from src.core.base.BaseAgent import BaseAgent
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

class ContextInheritance:
    """Manages context inheritance from parent files.

    Provides functionality for child contexts to inherit
    from parent contexts.

    Example:
        >>> inheritance=ContextInheritance()
        >>> inherited=inheritance.inherit_from("parent.description.md", "child.description.md")
    """

    def __init__(self) -> None:
        """Initialize context inheritance manager."""
        self.inheritance_map: Dict[str, InheritedContext] = {}
        self.mode: InheritanceMode = InheritanceMode.MERGE
        self.parent_path: Optional[str] = None

    def set_mode(self, mode: InheritanceMode) -> None:
        """Set inheritance mode."""
        self.mode = mode

    def set_parent(self, parent_path: str) -> None:
        """Set parent context."""
        self.parent_path = parent_path

    def apply(self, child_content: str, parent_content: str) -> str:
        """Apply the currently configured inheritance mode."""
        return self.resolve_inheritance(parent_content, child_content, self.mode)

    def get_hierarchy(self) -> List[str]:
        """Get inheritance hierarchy."""
        return [self.parent_path] if self.parent_path else []

    def inherit_from(
        self,
        parent_path: str,
        child_path: str,
        mode: InheritanceMode = InheritanceMode.MERGE
    ) -> InheritedContext:
        """Set up inheritance relationship.

        Args:
            parent_path: Path to parent context.
            child_path: Path to child context.
            mode: Inheritance mode.

        Returns:
            InheritedContext configuration.
        """
        inherited = InheritedContext(
            parent_path=parent_path,
            mode=mode
        )
        self.inheritance_map[child_path] = inherited
        return inherited

    def resolve_inheritance(
            self,
            parent_content: str,
            child_content: str,
            mode: InheritanceMode) -> str:
        """Resolve inheritance to produce final content.

        Args:
            parent_content: Parent context content.
            child_content: Child context content.
            mode: Inheritance mode.

        Returns:
            Resolved content.
        """
        if mode == InheritanceMode.OVERRIDE:
            return child_content
        elif mode == InheritanceMode.APPEND:
            return parent_content + "\n\n" + child_content
        else:  # MERGE
            # Simple merge: keep child sections, add missing from parent
            child_sections = set(re.findall(r"##\s+(\w+)", child_content))
            parent_sections = re.findall(r"(##\s+\w+.*?)(?=##|\Z)", parent_content, re.DOTALL)

            result = child_content
            for section in parent_sections:
                section_name = re.search(r"##\s+(\w+)", section)
                if section_name and section_name.group(1) not in child_sections:
                    result += "\n" + section.strip()
            return result
