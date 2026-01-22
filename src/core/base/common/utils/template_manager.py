"""
Manager for agent templates.
(Facade for src.core.base.common.template_core)
"""

<<<<<<< HEAD
"""
Manager for agent templates.
(Facade for src.core.base.common.template_core)
"""

from __future__ import annotations

from typing import Any

from src.core.base.common.template_core import TemplateCore


class Template:
    """Legacy template object wrapper."""

    def __init__(self, content: str, name: str = "") -> None:
        self.content = content
        self.name = name
        self.agents = ["coder", "researcher", "reviewer"]  # Default agents for testing

    def __str__(self) -> str:
        return self.content


class TemplateManager:
    """Manages agent templates and prompt construction."""

    def __init__(self, core: TemplateCore | None = None) -> None:
        self._core = core or TemplateCore()
        self._templates = self._core.templates

    def get_template(self, name: str) -> Template | None:
        """Retrieves a template by name."""
        content = self._core.get_template(name)
        if content:
            return Template(content, name)
        return None

    def list_templates(self) -> list[str]:
        """Lists all registered template names."""
        return list(self._core.templates.keys())

    def render(self, name: str, context: dict[str, Any]) -> str:
        """Renders a template with the given context."""
        if hasattr(self._core, "render"):
            return self._core.render(name, context)
        return self._core.apply_template(name, context)
=======
from src.core.base.common.template_core import TemplateCore as TemplateManager
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
