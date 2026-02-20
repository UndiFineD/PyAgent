from __future__ import annotations
"""
Parser-safe TemplateManager stub.

Provides minimal Template and TemplateManager classes so imports succeed
while template subsystem is being repaired.
"""




from typing import Any, Dict, Optional


class Template:
    def __init__(self, content: str, name: str = "") -> None:
        self.content = content
        self.name = name

    def __str__(self) -> str:
        return self.content


class TemplateManager:
    def __init__(self, core: Optional[Any] = None) -> None:
        self._core = core
        self._templates: Dict[str, str] = {}

    def register_template(self, name: str, content: str) -> None:
        self._templates[name] = content

    def get_template(self, name: str) -> Optional[Template]:
        content = self._templates.get(name)
        if content is None:
            return None
        return Template(content, name)

    def list_templates(self) -> list[str]:
        return list(self._templates.keys())


__all__ = ["Template", "TemplateManager"]
