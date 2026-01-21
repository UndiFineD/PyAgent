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


"""Auto-extracted class from agent.py"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from src.core.base.common.utils.agent_template import AgentTemplate

__version__ = VERSION


class TemplateManager:
    """Manage agent templates for common use cases.

    Example:
        manager=TemplateManager()
        manager.add_template(AgentTemplate(
            name = "python_cleanup",
            agents = ["coder", "tests"],
            file_patterns = ["*.py"],
        ))

        template=manager.get_template("python_cleanup")
        agent=template_to_agent(template)
    """

    def __init__(self) -> None:
        """Initialize manager."""
        self._templates: dict[str, AgentTemplate] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register default templates."""
        self._templates["python_full"] = AgentTemplate(
            name="python_full",
            description="Full Python code improvement",
            agents=["coder", "tests", "documentation", "errors"],
            file_patterns=["*.py"],
        )

        self._templates["markdown_docs"] = AgentTemplate(
            name="markdown_docs",
            description="Markdown documentation improvement",
            agents=["documentation"],
            file_patterns=["*.md"],
        )

        self._templates["quick_fix"] = AgentTemplate(
            name="quick_fix",
            description="Quick fixes only",
            agents=["coder"],
            config={"max_files": 10},
            file_patterns=["*.py"],
        )

    def add_template(self, template: AgentTemplate) -> None:
        """Add a template.

        Args:
            template: Template to add.
        """
        self._templates[template.name] = template

    def get_template(self, name: str) -> AgentTemplate | None:
        """Get a template by name.

        Args:
            name: Template name.

        Returns:
            Template or None if not found.
        """
        return self._templates.get(name)

    def list_templates(self) -> list[str]:
        """List available template names."""
        return list(self._templates.keys())
